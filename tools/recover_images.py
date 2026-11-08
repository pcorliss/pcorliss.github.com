#!/usr/bin/env python3
"""Repair images referenced by old posts.

Most post images hot-link files hosted on blogspot.com. Fifteen of them are
long gone (Blogger killed the old thumbnail service), and the surviving ones are
still linked over http, which trips mixed-content warnings on an https site.

What this does, in one pass, and safely to re-run:

* collects every external image reference in _posts, both <img src> and the
  <a href> "click for full size" wrappers around them;
* groups references that are the same image served at different Blogger sizes
  (/s200/, /s1600/, ...), so a thumbnail and its full-size link stay together;
* pulls each one out of the Wayback Machine (`id_` snapshots, i.e. original
  bytes with no Wayback chrome) into images/recovered/;
* rewrites the post to use the local files, naming the largest copy *-full;
* upgrades references that are still alive to https, but only after checking
  that the https URL actually responds.

Usage:
  python3 tools/recover_images.py --dry-run   # audit only, changes nothing
  python3 tools/recover_images.py             # download and rewrite posts

A JSON summary of every decision lands in /tmp/image-map.json.
"""
import concurrent.futures as cf
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "_posts")
OUTDIR = os.path.join(ROOT, "images", "recovered")
MANIFEST = "/tmp/image-map.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}

SRC_RE = re.compile(r"""(<img[^>]*?\bsrc\s*=\s*)(["'])(.*?)\2""", re.I | re.S)
HREF_RE = re.compile(r"""\bhref\s*=\s*(["'])(http[^"']+?)\1""", re.I | re.S)
IMAGE_EXT = re.compile(r"\.(png|jpe?g|gif|bmp|webp)([?#]|$)", re.I)

# Blogger/Google Photos put the resize in the path, e.g. /s200/chart.png. Same
# image, different size, so the size is stripped to group references together.
SIZE_RE = re.compile(r"/(s\d{2,4}|w\d{3,4}[a-z-]*)(?=/[^/]+$)")
SIZES = ["s1600", "s1600-h", "s0", "w640-h", "s640", "s512", "s400", "s320", "s200"]

def fetch(url, method="GET", timeout=90):
    req = urllib.request.Request(url, method=method, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as err:
        return err.code, b"", err.headers
    except Exception:
        return 0, b"", {}

def status_of(url):
    code = fetch(url, "HEAD")[0]
    return code if code else fetch(url)[0]

def size_variants(url):
    if not SIZE_RE.search(url):
        return [url]
    out, seen = [], set()
    for size in SIZES + [""]:
        cand = SIZE_RE.sub("/" + size if size else "", url)
        if cand not in seen:
            seen.add(cand)
            out.append(cand)
    return out

def identity(url):
    """Group key: the url with its resize segment blanked out."""
    return SIZE_RE.sub("/SIZE/", url)

def cdx_timestamp(url, tries=3):
    q = urllib.parse.urlencode({"url": url, "output": "json", "filter": "statuscode:200", "limit": -3})
    for attempt in range(tries):
        code, body, _ = fetch("http://web.archive.org/cdx/search/cdx?" + q)
        if code == 200:
            try:
                rows = json.loads(body)
            except ValueError:
                rows = []
            return rows[-1][1] if len(rows) > 1 else None
        time.sleep(8 * (attempt + 1))   # Wayback rate limits a lot
    return None

def closest_timestamp(url):
    code, body, _ = fetch("http://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe=""))
    if code != 200:
        return None
    try:
        snap = (json.loads(body).get("archived_snapshots") or {}).get("closest") or {}
    except ValueError:
        return None
    return snap["timestamp"] if snap.get("available") else None

def wayback_image(url):
    """(bytes, source url, snapshot timestamp) for the best archived copy."""
    for attempt in range(2):
        for cand in [url] + size_variants(url):
            ts = cdx_timestamp(cand) or closest_timestamp(cand)
            time.sleep(1)  # be gentle with the index
            if not ts:
                continue
            code, data, headers = fetch(f"http://web.archive.org/web/{ts}id_/{cand}")
            if code == 200 and data and headers.get("Content-Type", "").startswith("image"):
                return data, cand, ts
        time.sleep(5)
    return None, None, None

def base_name(url):
    """Blogger's own filename, tidied up. Old screenshots came out named like
    "Pembroke_Welsh_Corgi_600.jpg (600×470) - Google Chrome_005.png", so the
    browser chrome, the pixel note and the screenshot counter come off."""
    raw = os.path.basename(urllib.parse.urlparse(url).path)
    stem, ext = os.path.splitext(urllib.parse.unquote(raw.replace("+", " ")))
    stem = re.sub(r"_\d{2,4}$", "", stem)
    stem = re.sub(r"\s*-\s*(Google Chrome|Mozilla Firefox|Safari)\s*$", "", stem, flags=re.I)
    stem = re.sub(r"\(\d+\s*[×x]\s*\d+\)", "", stem)
    stem = re.sub(r"[\s_]+", "-", stem)
    stem = re.sub(r"[^A-Za-z0-9.-]", "", re.sub(r"-{2,}", "-", stem)).strip("-.")
    return (stem or "image")[:55], (ext.lower() or ".png")

def unique_name(stem, ext, suffix, taken):
    name = f"{stem}{suffix}{ext}"
    n = 2
    while name in taken or os.path.exists(os.path.join(OUTDIR, name)):
        name = f"{stem}{suffix}-{n}{ext}"
        n += 1
    taken.add(name)
    return name

def image_refs(text):
    """External image urls: <img src> plus <a href> full-size wrappers."""
    refs = [m.group(3) for m in SRC_RE.finditer(text)]
    refs += [m.group(2) for m in HREF_RE.finditer(text) if IMAGE_EXT.search(m.group(2))]
    return [r for r in refs if r.startswith("http")]

def set_alt(text, local, alt):
    """Old Blogger screenshots mostly had alt="" or no alt at all; the filename
    is the only caption the author left, so use it."""
    alt = alt.replace('"', "&quot;")

    def one(match):
        tag = match.group(0)
        if re.search(r"\balt\s*=", tag, re.I):
            return re.sub("""\\balt\\s*=\\s*("[^"]*"|'[^']*')""", f'alt="{alt}"', tag, count=1)
        return tag.replace(f'src="{local}"', f'src="{local}" alt="{alt}"', 1)

    return re.sub(r'<img[^>]*?src="' + re.escape(local) + r'"[^>]*?>', one, text)

def main():
    dry = "--dry-run" in sys.argv
    paths = sorted(os.path.join(POSTS, f) for f in os.listdir(POSTS) if not f.startswith("."))
    refs = {p: image_refs(open(p, encoding="utf-8", errors="replace").read()) for p in paths}
    urls = sorted({u for v in refs.values() for u in v})
    print(f"external image references: {len(urls)}")

    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        status = dict(zip(urls, pool.map(status_of, urls)))
    dead = [u for u in urls if status[u] and status[u] >= 400]
    alive = [u for u in urls if status[u] and status[u] < 400]
    print(f"alive: {len(alive)}   dead: {len(dead)}")

    # Group dead references so a thumbnail and its full-size link share a name.
    groups = {}
    for url in dead:
        groups.setdefault(identity(url), []).append(url)

    os.makedirs(OUTDIR, exist_ok=True)
    taken = set(os.listdir(OUTDIR))
    mapping, unrecovered, recovered = {}, [], 0
    for members in groups.values():
        copies = {}  # archived source url -> (bytes, source, timestamp)
        for url in members:
            for cand in [url] + size_variants(url):
                if cand in copies:
                    break
                data, source, ts = wayback_image(cand)
                if data:
                    copies[source] = (data, source, ts)
                    break
        if not copies:
            unrecovered.extend(members)
            continue
        recovered += 1
        biggest = max(copies.values(), key=lambda c: len(c[0]))[1]
        stem, ext = base_name(copies[biggest][1])
        alt = re.sub(r"\s{2,}", " ", re.sub(r"-full$", "", stem)).replace("-", " ").strip()
        alt = re.sub(r"\.(jpe?g|png|gif|bmp|webp)$", "", alt, flags=re.I)
        for source, (data, _, ts) in copies.items():
            is_full = source == biggest and len(copies) > 1
            name = unique_name(stem, ext, "-full" if is_full else "", taken)
            if not dry:
                with open(os.path.join(OUTDIR, name), "wb") as fh:
                    fh.write(data)
            local = "/images/recovered/" + name
            print(f"  {'OK  ' if not dry else 'DRY '}{len(data) // 1024:>5}KB  {name}")
            mapping[source] = {"local": local, "bytes": len(data), "alt": alt,
                               "snapshot": f"https://web.archive.org/web/{ts}/{source}"}
            # every other Blogger size of the same image points at the same file
            for alias in size_variants(source):
                mapping.setdefault(alias, {"local": local, "bytes": len(data), "alt": alt,
                                           "snapshot": mapping[source]["snapshot"], "alias": True})

    upgrades = {}
    http_urls = [u for u in alive if u.startswith("http://")]
    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        codes = dict(zip(http_urls, pool.map(lambda u: status_of("https://" + u[7:]), http_urls)))
    for url, code in codes.items():
        if code == 200:
            upgrades[url] = "https://" + url[7:]
    print(f"recovered groups: {recovered}   unrecovered: {len(unrecovered)}   https upgrades: {len(upgrades)}/{len(http_urls)}")

    if not dry:
        touched = 0
        for path in paths:
            orig = text = open(path, encoding="utf-8").read()
            for source, info in mapping.items():
                if f'"{source}"' in text or f"'{source}'" in text:
                    text = text.replace(f'"{source}"', f'"{info["local"]}"').replace(f"'{source}'", f"'{info['local']}'")
                    text = set_alt(text, info["local"], info["alt"])
            for url, secure in upgrades.items():
                text = text.replace(f'"{url}"', f'"{secure}"').replace(f"'{url}'", f"'{secure}'")
            if text != orig:
                open(path, "w", encoding="utf-8").write(text)
                touched += 1
        print(f"posts rewritten: {touched}")

    json.dump({"local": mapping, "unrecovered": unrecovered, "https": upgrades}, open(MANIFEST, "w"), indent=2)
    print("manifest:", MANIFEST)

if __name__ == "__main__":
    main()
