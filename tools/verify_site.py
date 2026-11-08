#!/usr/bin/env python3
"""Verify the generated site: internal links, #fragment anchors, mixed-content refs.

Run `jekyll serve` first, then:  python3 tools/verify_site.py [base-url]
"""
import os, re, sys, urllib.parse, urllib.request, urllib.error

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_site')
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:4000'

href_src = re.compile(r'(?:href|src|poster)="([^"]*)"')
id_re = re.compile(r'\bid="([^"]+)"')

pages = ['/' + os.path.relpath(os.path.join(root, f), SITE).replace(os.sep, '/')
         for root, _, files in os.walk(SITE) for f in files if f.endswith('.html')]

ids, refs = {}, []
for web in pages:
    path = os.path.join(SITE, web.lstrip('/'))
    html = open(path, encoding='utf-8', errors='replace').read()
    ids[web] = set(id_re.findall(html))
    refs += [(web, m.group(1)) for m in href_src.finditer(html)]


def web_path(src_page, ref):
    """Where a relative ref points, expressed as a site path."""
    target = urllib.parse.urldefrag(ref)[0]
    if not target:
        return src_page
    if target.startswith('/'):
        return urllib.parse.unquote(target)
    base = os.path.dirname(src_page)
    return urllib.parse.unquote(os.path.normpath(os.path.join(base, target)).replace(os.sep, '/'))


def status(path):
    path, _, query = path.partition('?')          # keep the cache-buster out of the URL path
    url = BASE + urllib.parse.quote(path) + ('?' + query if query else '')
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


status_cache, broken, bad_anchor, pages_seen = {}, set(), set(), set()
for src_page, ref in refs:
    if ref.startswith(('mailto:', 'tel:', 'javascript:')) or ref.startswith('//'):
        continue
    scheme = urllib.parse.urlparse(ref).scheme
    if scheme.startswith('http'):
        continue
    if not ref or ref.startswith('#'):
        target, frag = src_page, urllib.parse.urldefrag(ref)[1]
    else:
        target, frag = web_path(src_page, ref), urllib.parse.urldefrag(ref)[1]
    if not target:
        continue
    pages_seen.add(target)
    if target not in status_cache:
        status_cache[target] = status(target)
    if status_cache[target] != 200:
        broken.add((status_cache[target], target, src_page))
    if frag:
        target_ids = ids.get(target)
        if target_ids is None:          # non-html target: anchor can't be checked
            continue
        if frag not in target_ids and urllib.parse.unquote(frag) not in target_ids:
            bad_anchor.add((src_page, ref))

mixed = sorted({r for _, r in refs if r.startswith('http://')})
hosts = sorted({urllib.parse.urlparse(r).netloc for _, r in refs
                if urllib.parse.urlparse(r).scheme.startswith('http')})

print(f'pages: {len(pages)}   distinct internal targets: {len(pages_seen)}')
print(f'broken internal links: {len(broken)}')
for code, target, src in sorted(broken):
    print(f'   {code}  {target}   (linked from {src})')
print(f'unresolvable #anchors: {len(bad_anchor)}')
for src, ref in sorted(bad_anchor)[:30]:
    print(f'   {src} -> {ref}')
print(f'http:// (mixed content) refs: {len(mixed)}')
for r in mixed:
    print('   ', r)
print('external hosts:', ', '.join(hosts))
