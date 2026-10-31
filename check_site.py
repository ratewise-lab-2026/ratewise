"""Static checks for the generated site.

- resolves every internal link the way a browser would (relative to the page)
- flags broken links, missing redirect stubs, orphans
- checks title / description / single h1 / canonical on content pages
- validates every JSON-LD block

Run: python check_site.py
"""
import json
import pathlib
import posixpath
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
# served by _redirects (not real files)
REDIRECTS = {"/etsy-fee-calculator.html", "/etsy-fee-calculator", "/fee-calculator.html"}
GO = re.compile(r"^/go/")

pages = [p for p in ROOT.rglob("*.html")
         if not p.name.startswith("_") and "go" not in p.relative_to(ROOT).parts]
pages_rel = {p.relative_to(ROOT).as_posix() for p in pages}

errors, warnings = [], []
inbound = {rel: set() for rel in pages_rel}

HREF = re.compile(r'href="([^"]+)"')


def resolve(page_rel: str, href: str) -> str | None:
    """Return the site-root path for an internal href, or None if external."""
    if href.startswith(("http", "mailto:", "tel:", "javascript:", "#")):
        return None
    target = href.split("#")[0].split("?")[0]
    if not target:
        return None
    if target.startswith("/"):
        return "/" + posixpath.normpath(target.lstrip("/"))
    base = posixpath.dirname(page_rel)
    return "/" + posixpath.normpath(posixpath.join(base, target))


for p in pages:
    rel = p.relative_to(ROOT).as_posix()
    text = p.read_text(encoding="utf-8")

    title = re.search(r"<title>(.*?)</title>", text, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', text)
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", text, re.S)
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', text)

    if not title:
        errors.append(f"{rel}: missing <title>")
    if not desc:
        errors.append(f"{rel}: missing meta description")
    elif not (50 <= len(desc.group(1)) <= 170):
        warnings.append(f"{rel}: meta description length {len(desc.group(1))} (aim 50-170)")
    if len(h1s) != 1:
        errors.append(f"{rel}: expected exactly 1 <h1>, found {len(h1s)}")
    if not canonical:
        errors.append(f"{rel}: missing canonical")

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: invalid JSON-LD ({e.msg})")

    for href in HREF.findall(text):
        site_path = resolve(rel, href)
        if site_path is None:
            continue
        if site_path in REDIRECTS:
            continue
        if GO.match(site_path):
            if not (ROOT / (site_path.lstrip("/") + ".html")).exists():
                warnings.append(f"{rel}: redirect stub missing -> {href}")
            continue
        clean = site_path.lstrip("/")
        if clean in ("", "index.html"):
            inbound["index.html"].add(rel)
            continue
        if (ROOT / clean).exists():
            if clean in inbound:
                inbound[clean].add(rel)
        else:
            errors.append(f"{rel}: broken link -> {href}")

for page, sources in inbound.items():
    if page != "index.html" and page != "404.html" and not sources:
        warnings.append(f"{page}: no inbound internal links (orphan)")

titles = {}
for p in pages:
    t = re.search(r"<title>(.*?)</title>", p.read_text(encoding="utf-8"), re.S)
    if t:
        titles.setdefault(t.group(1).strip(), []).append(p.relative_to(ROOT).as_posix())
for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate <title> in {ps}")

print(f"checked {len(pages)} pages")
for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print("\nRESULT:", "PASS" if not errors else f"FAIL ({len(errors)} errors)")
sys.exit(0 if not errors else 1)
