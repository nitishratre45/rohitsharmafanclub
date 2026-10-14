#!/usr/bin/env python3
"""Refresh Rohit-related headlines from the public ESPNcricinfo RSS feed."""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "news.json"
FEED = "https://www.espncricinfo.com/rss/content/story/feeds/0.xml"
HEADERS = {"User-Agent": "RohitSharmaFanClubNewsRefresh/1.0 (+https://github.com/nitishratre45/rohitsharmafanclub)"}

def plain(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", unescape(value)).strip()

def main():
    with urllib.request.urlopen(urllib.request.Request(FEED, headers=HEADERS), timeout=25) as response:
        payload = response.read()
    root = ET.fromstring(payload)
    articles = []
    for item in root.findall(".//item"):
        title = plain(item.findtext("title"))
        description = plain(item.findtext("description"))
        link = (item.findtext("link") or "").strip()
        pub_date = plain(item.findtext("pubDate"))
        text = (title + " " + description).lower()
        if not link.startswith("https://") or not ("rohit sharma" in text or "rohit" in title.lower()):
            continue
        articles.append({"title": title, "publisher": "ESPNcricinfo", "dateLabel": pub_date or "RSS article", "summary": description[:500], "url": link, "category": "Latest article"})
        if len(articles) >= 20:
            break
    if not articles:
        print("RSS reachable but no matching Rohit headlines found; retaining last successful cache.")
        return
    current = json.loads(DATA.read_text(encoding="utf-8"))
    if articles == current.get("articles", []):
        print("No new matching articles; data file unchanged.")
        return
    current["articles"] = articles
    current["lastUpdated"] = datetime.now(timezone.utc).date().isoformat()
    current["source"] = {"name": "ESPNcricinfo RSS + official source pages", "feedUrl": FEED}
    DATA.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated " + str(len(articles)) + " Rohit-related articles.")

if __name__ == "__main__":
    main()
