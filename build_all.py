"""Build every page, then regenerate sitemap.xml.

Run:  python build_all.py
"""
import pathlib
import re

import build_pages
import build_pages2
from build_site import SITE, not_found_page, write

ROOT = pathlib.Path(__file__).resolve().parent

# 404 page (GitHub Pages / Cloudflare serve it for unknown URLs)
write("404.html", not_found_page())

# Pages that exist on disk, excluding private/build/redirect files
pages = []
for p in sorted(ROOT.rglob("*.html")):
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith("_") or rel == "404.html" or rel.startswith("go/"):
        continue
    if rel == "index.html":
        pages.insert(0, "")
    else:
        pages.append(rel)

urls = []
for rel in pages:
    loc = f"{SITE}/{rel}" if rel else f"{SITE}/"
    urls.append(
        f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if not rel else '0.8'}</priority></url>"
    )

sitemap = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(urls)
    + "\n</urlset>\n"
)
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
print(f"sitemap.xml written ({len(pages)} urls)")
