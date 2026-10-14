#!/usr/bin/env python3
"""Refresh Rohit Sharma headlines from public cricket publisher pages."""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "news.json"
ESPN_FEED = "https://www.espncricinfo.com/rss/content/story/feeds/0.xml"
ICC_PLAYER_NEWS = "https://www.icc-cricket.com/news/category/player-3852?appview=true"
HEADERS = {"User-Agent": "RohitSharmaFanClubNewsRefresh/1.2 (+https://github.com/nitishratre45/rohitsharmafanclub)"}

def plain(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", unescape(value)).strip()

def request(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=25) as response:
        return response.read()

def clean_icc_title(value):
    """Separate the publication date from ICC archive titles and remove UI labels."""
    title = plain(value)
    date_match = re.search(r"\s+(\d{1,2}\s+[A-Za-z]+,?\s+\d{4})$", title)
    date_label = plain(date_match.group(1)) if date_match else "ICC news archive"
    if date_match:
        title = title[:date_match.start()].strip()
    for prefix in ("News ", "The ICC Review ", "ICC Men's Cricket WC ", "Men’s Rankings "):
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
            break
    return title or plain(value), date_label

class ArticleLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.articles = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        if href.startswith("/news/") and "/news/category/" not in href:
            url = "https://www.icc-cricket.com" + href
        elif href.startswith("https://www.icc-cricket.com/news/") and "/news/category/" not in href:
            url = href
        else:
            return
        self.current = {"url": url, "parts": []}
    def handle_data(self, data):
        if self.current is not None:
            self.current["parts"].append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            raw_title = plain(" ".join(self.current["parts"]))
            title, date_label = clean_icc_title(raw_title)
            url = self.current["url"].split("#", 1)[0].rstrip("/")
            if len(title) > 12 and url not in {a["url"] for a in self.articles}:
                self.articles.append({"title": title, "publisher": "ICC", "dateLabel": date_label, "summary": "Article listed in the ICC Rohit Sharma news archive.", "url": url, "category": "ICC player news"})
            self.current = None

def read_espn():
    root = ET.fromstring(request(ESPN_FEED))
    articles = []
    for item in root.findall(".//item"):
        title = plain(item.findtext("title"))
        description = plain(item.findtext("description"))
        link = (item.findtext("link") or "").strip()
        pub_date = plain(item.findtext("pubDate"))
        if not link.startswith("https://") or not ("rohit sharma" in (title + " " + description).lower()):
            continue
        articles.append({"title": title, "publisher": "ESPNcricinfo", "dateLabel": pub_date or "RSS article", "summary": description[:500], "url": link, "category": "Latest article"})
        if len(articles) >= 20:
            break
    return articles

def read_icc():
    parser = ArticleLinks()
    parser.feed(request(ICC_PLAYER_NEWS).decode("utf-8", errors="replace"))
    return parser.articles[:20]

def main():
    candidates = []
    failures = []
    for name, reader in (("ESPNcricinfo RSS", read_espn), ("ICC player news archive", read_icc)):
        try:
            candidates.extend(reader())
        except Exception as exc:
            failures.append(name + ": " + str(exc))
    unique = []
    seen = set()
    for item in candidates:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)
    if not unique:
        print("No matching headlines found; retaining the last successful cache. " + " | ".join(failures))
        if len(failures) == 2:
            raise RuntimeError("Both news sources failed: " + " | ".join(failures))
        return
    current = json.loads(DATA.read_text(encoding="utf-8"))
    if unique == current.get("articles", []):
        print("No new matching articles; data file unchanged.")
        return
    current["articles"] = unique[:30]
    current["lastUpdated"] = datetime.now(timezone.utc).date().isoformat()
    current["source"] = {"name": "ESPNcricinfo RSS + ICC player news archive", "feedUrl": ESPN_FEED, "iccArchiveUrl": ICC_PLAYER_NEWS}
    DATA.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated " + str(len(current["articles"])) + " source-linked Rohit-related articles.")

if __name__ == "__main__":
    main()
