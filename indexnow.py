"""
Ping IndexNow so Bing / Yandex crawl new or changed pages within hours.

Usage (after you upload new pages to GitHub Pages):
    python indexnow.py

The key below must also exist on your site as a text file at /<key>.txt
containing exactly the key. build_all.py creates that file for you.
"""
import json
import pathlib
import urllib.request

KEY = "b9fabfff464d90a8c380cce03ef6ac64"
HOST = "ratewise-lab-2026.github.io"
BASE = f"https://{HOST}/ratewise/"
ROOT = pathlib.Path(__file__).resolve().parent


def all_urls() -> list[str]:
    urls = [BASE]
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(("_", "go/")) or rel == "404.html":
            continue
        if rel == "index.html":
            continue
        urls.append(BASE + rel)
    return urls


def main() -> None:
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"{BASE}{KEY}.txt",
        "urlList": all_urls(),
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow responded: HTTP {resp.status}")
            print("200/202 means accepted; 4xx means check the key file and host.")
    except urllib.error.HTTPError as e:
        print(f"IndexNow rejected: HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", "replace")[:400])
    except Exception as e:  # noqa: BLE001
        print(f"Could not reach IndexNow: {e}")
    print(f"submitted {len(payload['urlList'])} urls")


if __name__ == "__main__":
    main()
