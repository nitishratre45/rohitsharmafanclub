# Rohit Sharma FanClub — Hitman 45

An independent fan-made cricket website. This repository is separate from `nitishratre45/tilakvarmafanclub`; the Tilak repository is not modified by this project.

## Site

- Cloudflare Pages project: `rohitsharmafanclub`
- Production URL: https://rohitsharmafanclub.pages.dev
- Production branch: `main`
- Build command: none (static HTML/CSS/JS)
- Build output directory: repository root

## Project structure

- `index.html`, `home/` — responsive homepage, shared styles and navigation
- `stats/` — career snapshot, Batting, Bowling and Stats Explorer modules
- `photos/` — JSON-backed gallery and attributed publisher links
- `matches/` — JSON-backed searchable archive with format filter
- `records/` — JSON-backed milestones with source links
- `news/` — filterable source links; no fake breaking headlines
- `videos/` — official video-source hub; no rehosted streams
- `data/` — profile, stats, photo albums, matches, records, news and video source data
- `.github/workflows/site-check.yml` — push/PR checks and scheduled validation

## Verification and data quality

The GitHub Actions workflow checks required files, parses JSON, validates JavaScript syntax, checks local HTML references and ensures the site code does not reference the Tilak repository. It runs on pushes, pull requests, manual dispatch and every 12 hours.

Career figures are a dated snapshot with a source URL; they are **not a live feed**. Always follow the linked ICC profile for the latest numbers. Bowling figures and match scorecards must not be fabricated. The match archive remains empty until verified scorecard data is added.

Photo assets must be accessible, attributed and used consistently with the publisher's terms. The gallery links to the original sources instead of copying third-party galleries.

## Disclaimer

Independent fan-made project; not affiliated with Rohit Sharma, BCCI, ICC, IPL or any team.
