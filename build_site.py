"""Static site generator - shared page factory.

Every internal link is written RELATIVE to the page that contains it, so the
exact same generated files work:
  * at a domain root        (Cloudflare Pages / Netlify / custom domain)
  * in a sub-folder         (GitHub Pages: username.github.io/repo/)
  * even opened from a local disk (file://)

SITE is used only for canonical / og:url / sitemap and must be set to the real
public URL before you submit the sitemap to Google.
"""
import html
import json
import pathlib

import settings

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://ratewise-lab-2026.github.io/ratewise"   # real public URL (GitHub Pages, project site)
SITE_NAME = "RateWise"
TAGLINE = "Free calculators for freelancers, sellers and side-hustlers"

# Internal "site paths" (always written root-relative here); rel() converts them.
NAV = """
<header class="site">
  <div class="wrap">
    <a class="logo" href="/"><span>Rate</span>Wise</a>
    <nav class="top">
      <a href="/">All tools</a>
      <a href="/tools/marketplace-fee-calculator.html">Seller fees</a>
      <a href="/etsy-fees-2026.html">Etsy fees 2026</a>
      <a href="/etsy-vs-shopify-fees.html">Etsy vs Shopify</a>
    </nav>
  </div>
</header>"""

FOOTER = """
<footer class="site">
  <div class="wrap">
    <div>&copy; 2026 RateWise &mdash; estimates only, not financial advice.</div>
    <div>
      <a href="/about.html">About</a> &middot;
      <a href="/privacy.html">Privacy</a> &middot;
      <a href="/disclosure.html">Affiliate disclosure</a>
    </div>
  </div>
</footer>"""


def _head_extras() -> str:
    """Search-engine verification meta tags and optional analytics snippet."""
    parts = []
    if settings.GOOGLE_VERIFICATION:
        parts.append(f'<meta name="google-site-verification" content="{settings.GOOGLE_VERIFICATION}">')
    if settings.BING_VERIFICATION:
        parts.append(f'<meta name="msvalidate.01" content="{settings.BING_VERIFICATION}">')
    if settings.BAIDU_VERIFICATION:
        parts.append(f'<meta name="baidu-site-verification" content="{settings.BAIDU_VERIFICATION}">')
    if settings.ANALYTICS_SNIPPET:
        parts.append(settings.ANALYTICS_SNIPPET)
    return "\n".join(parts)



def esc(s: str) -> str:
    return html.escape(str(s), quote=False)


def _page_path(slug: str) -> str:
    """Where this page file lives, relative to the site root."""
    return f"tools/{slug}.html"


def _rel_from(page_file: str, target: str) -> str:
    """Relative href from the page file to a target site path.

    page_file: e.g. 'tools/marketplace-fee-calculator.html'
    target:    e.g. '/' or '/about.html'
    """
    depth = page_file.count("/")
    if target == "/":
        return "../" * depth if depth else "./"
    clean = target.lstrip("/")
    return "../" * depth + clean


def rel_from(page_file: str, html_text: str) -> str:
    """Rewrite every root-relative href/src in html_text into a relative one."""
    import re

    def sub(m):
        attr, val = m.group(1), m.group(2)
        if val.startswith(("/", "http", "mailto:", "#")):
            if val.startswith("/"):
                return f'{attr}="{_rel_from(page_file, val)}"'
        return m.group(0)

    return re.sub(r'(href|src)="([^"]+)"', sub, html_text)


def page(
    *,
    slug: str,
    title: str,
    description: str,
    h1: str,
    lede: str,
    tool_html: str = "",
    js: str = "",
    sections: list | None = None,
    faqs: list | None = None,
) -> str:
    """sections: list of (heading, raw_html). faqs: list of (q, a)."""
    page_file = _page_path(slug)
    canonical = f"{SITE}/{page_file}"
    sections = sections or []
    faqs = faqs or []

    body = "\n".join(f'<section class="prose"><h2>{esc(h)}</h2>\n{c}</section>' for h, c in sections)

    faq_html = ""
    faq_ld = ""
    if faqs:
        items = "\n".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
        faq_html = f'<section class="prose"><h2>FAQ</h2><div class="faq">\n{items}\n</div></section>'
        faq_ld = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faqs
                ],
            }
        )
        faq_ld = f'<script type="application/ld+json">{faq_ld}</script>'

    webapp_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": h1,
            "url": canonical,
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Any",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        }
    )

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{webapp_ld}</script>
{faq_ld}
{_head_extras()}
</head>
<body>
{NAV}
<main>
  <p class="small muted"><a href="/">Home</a> &rsaquo; {esc(h1)}</p>
  <h1>{esc(h1)}</h1>
  <p class="lede">{esc(lede)}</p>
  {tool_html}
  {body}
  {faq_html}
</main>
{FOOTER}
{('<script>' + js + '</script>') if js else ''}
</body>
</html>
"""
    return rel_from(page_file, doc)


def simple_page(*, path: str, title: str, description: str, h1: str, body_html: str) -> str:
    clean = path[1:] if path.startswith("/") else path
    clean = "" if clean in ("index.html", "") else clean
    canonical = f"{SITE}/{clean}" if clean else f"{SITE}/"
    page_file = clean or "index.html"
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{_head_extras()}
</head>
<body>
{NAV}
<main>
  <p class="small muted"><a href="/">Home</a> &rsaquo; {esc(h1)}</p>
  <h1>{esc(h1)}</h1>
  {body_html}
</main>
{FOOTER}
</body>
</html>
"""
    return rel_from(page_file, doc)


def not_found_page() -> str:
    """404 page: GitHub Pages serves this automatically for unknown URLs."""
    body = """
<p class="lede">That page moved or never existed. Try one of these:</p>
<div class="cards">
  <a class="card" href="/tools/marketplace-fee-calculator.html">
    <h3>Fee &amp; profit calculator</h3>
    <p>The main tool: real profit per sale on Etsy, eBay, TikTok Shop and Shopify.</p>
  </a>
  <a class="card" href="/etsy-fees-2026.html">
    <h3>Etsy fees 2026</h3>
    <p>Every fee, with a worked example.</p>
  </a>
  <a class="card" href="/">
    <h3>All tools</h3>
    <p>Back to the homepage.</p>
  </a>
</div>
"""
    return simple_page(
        path="404.html",
        title="Page not found — RateWise",
        description="The page you asked for does not exist. Use the fee calculator or go back to the homepage.",
        h1="Page not found",
        body_html=body,
    )


def write(rel_path: str, content: str) -> None:
    p = ROOT / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("wrote", p.relative_to(ROOT))
