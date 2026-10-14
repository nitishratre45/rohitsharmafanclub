# Rohit Sharma FanClub — Hitman 45

An independent fan-made cricket website inspired by the information architecture of the Tilak Varma FanClub project. This repository is separate; no changes are made to `nitishratre45/tilakvarmafanclub`.

## Current structure

- `index.html`, `home/` — responsive home and shared visual system
- `stats/` — career-statistics landing page
- `photos/` — gallery landing page and album data
- `matches/` — match archive landing page and data contract
- `records/` — sourced career milestones
- `news/` — sourced news links
- `videos/` — official video-source hub
- `data/` — player profile and structured data snapshots
- `.github/workflows/site-check.yml` — scheduled repository smoke check

## Deploy to Cloudflare Pages

Use Git integration, production branch `main`, build command empty, and output directory `/`. The site is static HTML/CSS/JS.

## Data quality

Do not label values as live unless a live source is configured. Store source URLs and update timestamps for every imported snapshot. Verify official statistics before publishing. Gallery image URLs should be verified and properly attributed.

## Disclaimer

Independent fan project; not affiliated with Rohit Sharma, BCCI, ICC, IPL or any team.