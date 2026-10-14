# Rohit Sharma FanClub — Hitman 45

An independent fan-made cricket website. All site work is kept in `nitishratre45/rohitsharmafanclub`; the Tilak Varma FanClub repository is separate and is not modified.

## Production

- Cloudflare Pages: https://rohitsharmafanclub.pages.dev
- Production branch: `main`
- Build command: none (static HTML/CSS/JS)
- Build output directory: repository root

## Features

- Responsive homepage and shared mobile navigation
- Career batting snapshot, source-linked bowling snapshot and Stats Explorer
- Recent innings archive with opponent/format/search filters
- Records and milestone references linked to ICC/BCCI sources
- Photo gallery with attribution and original publisher links
- Newsroom with curated official links and scheduled RSS headline refresh
- Official video-source hub
- Site-wide search across stats, bowling, records, matches, news, photos and videos
- Fan Zone local poll (stored on the visitor's device only)
- 1080 × 1350 wallpaper creator with PNG export
- Read-only Admin Studio health checks for public JSON endpoints and the latest public GitHub Actions run

## Automation and validation

`Rohit FanClub Site Check` runs on pushes, pull requests, manual dispatch and every 12 hours. It checks required files, JavaScript syntax, Python syntax, JSON schemas and local HTML references.

`Refresh Rohit News` runs every 6 hours and can be started manually. It reads the public ESPNcricinfo RSS feed and caches Rohit-related articles in `data/news.json`. If the feed is unreachable or has no matching items, the last successful article cache is preserved.

## Data quality

- Batting stats use a dated ICC profile snapshot.
- Bowling stats use a dated BCCI profile snapshot and may differ in update date or match totals.
- Recent innings are a dated snapshot from the ICC player profile, not live scores. Some links open the player profile or series report rather than a ball-by-ball scorecard.
- Photo and video sections link to original publishers instead of copying their galleries or hosting copyrighted streams.
- The Fan Zone poll is local to the visitor's browser; it is not a shared public tally.
- The wallpaper creator produces typography and shapes and does not include official player photography.

## Disclaimer

Independent fan-made project; not affiliated with Rohit Sharma, BCCI, ICC, IPL or any team.
