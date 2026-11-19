# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/simpson007/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/simpson007/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A program that writes one image summing up the world's news of Thursday 19 November 2026 — the first Trump–Xi–Putin trilateral in Shenzhen, the world court's Myanmar genocide judgment, GTA VI rolling out worldwide, and split markets — to /output/entry.png.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## What's in the picture

A one-page newspaper front page for Thursday 19 November 2026:

- **Lead — Shenzhen:** Trump, Xi and Putin meet for the first time as a trio, on the sidelines of APEC. Nuclear arms top the agenda after New START lapsed in February; the war in Iran is on the table too.
- **The Hague:** The International Court of Justice delivers its judgment on whether Myanmar committed genocide against the Rohingya; a finding of guilt would be a first for the court.
- **Vice City:** Grand Theft Auto VI unlocks at midnight around the world, 13 years after GTA V. Early reviews give it 99 on Metacritic; pre-sales near $1.5bn.
- **Markets:** Dow −1.1%, S&P −0.2% (fifth straight loss), Nasdaq +0.4%, Brent −1.3% to $91.95, gold −2.5% to $3,753; Fed minutes point to more rate rises.
- **Also:** Democrats nominate Hakeem Jeffries for Speaker (251–11), Anthropic prices its IPO at $83 and starts trading as ANT, Cyclone Akvan bears down on India's east coast, the EU proposes a €45bn loan to Ukraine, Nvidia's Huang quits, Iran widens its Gulf attacks, and Voyager 1 reaches a light-day from Earth.

## How it was made

`render.py` draws the front page with Pillow (deterministic: fixed text and geometry, no network, no randomness) and writes `entry.png` (1024×1024, about 140 KiB). `main.ts` (Node 22, standard library only) copies it to `/output/entry.png`, so two runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ngqr1ydj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
