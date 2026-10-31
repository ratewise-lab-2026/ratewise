"""Final integrity pass: HTML well-formedness, relative asset resolution,
JSON-LD, and sitemap consistency. Run after build_all.py.

python verify_site.py
"""
import html.parser
import json
import pathlib
import posixpath
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Checker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}>")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"unclosed <{self.stack.pop()}> before </{tag}>")
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f"stray </{tag}>")


errors = []
pages = [p for p in ROOT.rglob("*.html")
         if not p.name.startswith("_")
         and "go" not in p.relative_to(ROOT).parts
         and p.name != "404.html"]

for p in pages:
    rel = p.relative_to(ROOT).as_posix()
    text = p.read_text(encoding="utf-8")
    c = Checker()
    c.feed(text)
    c.close()
    if c.stack:
        c.errors.append("unclosed at EOF: " + ", ".join(c.stack))
    for e in c.errors:
        errors.append(f"{rel}: {e}")

    # every local asset reference must resolve relative to the page itself
    for attr, href in re.findall(r'(href|src)="([^"]+)"', text):
        if href.startswith(("http", "mailto:", "tel:", "javascript:", "#", "data:")):
            continue
        if href.startswith("/"):
            errors.append(f"{rel}: absolute path left in output -> {href}")
            continue
        target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), href.split("#")[0]))
        if target.startswith("go/"):
            continue  # affiliate redirect stubs: served by _redirects on Cloudflare, plain file elsewhere
        if not (ROOT / target).exists():
            errors.append(f"{rel}: unresolved asset link -> {href}")

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: invalid JSON-LD ({e.msg})")

if not (ROOT / "assets" / "style.css").exists():
    errors.append("assets/style.css missing")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
if len(locs) != len(pages):
    errors.append(f"sitemap has {len(locs)} urls but {len(pages)} indexable pages exist")
if any("/ratewise.pages.dev" in u for u in locs):
    print("NOTE  sitemap still uses the placeholder domain — set SITE in build_site.py before submitting it")

print(f"pages: {len(pages)} | sitemap urls: {len(locs)}")
for e in errors:
    print("ERROR", e)
print("\nRESULT:", "PASS" if not errors else f"FAIL ({len(errors)})")
sys.exit(0 if not errors else 1)
