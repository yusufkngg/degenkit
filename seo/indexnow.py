#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Naver, Seznam, Yep…) with every URL in sitemap.xml.
Run AFTER deploying:  python3 seo/indexnow.py"""
import re, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY = "f779a30091a5bce060453e5996fd53dc"
urls = re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": "degenkit.app", "key": KEY, "keyLocation": f"https://degenkit.app/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
print(urls and f"Submitting {len(urls)} URLs…"); print("HTTP", urllib.request.urlopen(req, timeout=30).status)
