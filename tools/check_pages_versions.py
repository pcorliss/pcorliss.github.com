#!/usr/bin/env python3
"""Compare the local toolchain with the versions GitHub Pages runs.

GitHub Pages ignores our Gemfile: it builds with its own `github-pages` gem and
publishes the exact versions it uses at https://pages.github.com/versions/.
Since we pin the output-shaping gems to match, this script checks that the pins
have not drifted.

    python3 tools/check_pages_versions.py

Exits non-zero when something we pin is no longer what Pages reports, or when
Pages has started reporting a version for a gem we do not have.
"""
import json
import re
import subprocess
import sys
import urllib.request

VERSIONS_URL = "https://pages.github.com/versions/"

# Only the gems that decide the HTML we ship. Pages ships ~47 gems; the rest are
# plugins this site does not use and cannot affect the output.
WATCHED = [
    "jekyll",
    "kramdown",
    "kramdown-parser-gfm",
    "liquid",
    "rouge",
    "jekyll-sass-converter",
    "safe_yaml",
]


def pages_versions():
    html = urllib.request.urlopen(VERSIONS_URL, timeout=30).read().decode()
    out = {}
    for row in re.findall(r"<tr>(.*?)</tr>", html, re.S):
        cells = [re.sub(r"<[^>]+>", "", c).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        if len(cells) >= 2 and re.match(r"^\d+(\.\d+)*$", cells[1]):
            out[cells[0]] = cells[1]
    return out


def local_versions():
    listing = subprocess.run(
        ["bundle", "list"], capture_output=True, text=True, check=True
    ).stdout
    return dict(re.findall(r"\*\s+(\S+)\s+\((\S+)\)", listing))


def main():
    try:
        pages = pages_versions()
    except Exception as exc:  # noqa: BLE001 - report, do not traceback
        print(f"could not read {VERSIONS_URL}: {exc}")
        return 2
    local = local_versions()

    bad = 0
    for gem in WATCHED:
        want, have = pages.get(gem), local.get(gem)
        if want is None:
            print(f"?  {gem:24s} Pages does not report a version")
            continue
        if have is None:
            print(f"X  {gem:24s} Pages runs {want}, not in the bundle")
            bad += 1
        elif have != want:
            print(f"X  {gem:24s} local {have:10s} != Pages {want}")
            bad += 1
        else:
            print(f"ok {gem:24s} {have}")

    print()
    print(f"github-pages gem on Pages: {pages.get('github-pages', 'unknown')}")
    if bad:
        print(f"\n{bad} gem(s) out of step with Pages.")
        print(f"Bump the pins in Gemfile to match {VERSIONS_URL}")
        print("then `bundle update` and re-diff _site against a known-good build.")
        return 1
    print("Local toolchain matches Pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
