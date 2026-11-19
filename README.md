# The World in One Day — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/simpson007/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/simpson007/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One newspaper front page that sums up the world's news of Thursday,
19 November 2026, in a single 1024×1024 PNG image. It is drawn as a
broadsheet: a big headline story on top, the day's other major stories
below it, market numbers in a strip, and a footer of smaller items —
everything a reader needs to catch up on the day at a glance.

## How it is made

`render.py` draws the whole front page with Pillow — masthead, columns,
rules and captions, all placed by code, no stock photos. Running it twice
produces the exact same bytes, so the picture is fully reproducible.
`entry.png` in this repository is the finished picture that `render.py`
produces. `main.ts` is the entrypoint: it only copies `entry.png` into
the output directory the harness provides, nothing else.

## Files

- `entry.png` — the finished 1024×1024 front page
- `render.py` — the Pillow program that draws the front page
- `main.ts` — the Node 22 entrypoint, copies `entry.png` to the output
- `package.json` — package metadata
- `LICENSE` — MIT

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That writes the front page to `out/entry.png`. With no
`MAKEFUN_OUTPUT_DIR` set, the program writes to `/output/entry.png`
instead. To redraw the picture from scratch, run `python3 render.py`
first — it regenerates `entry.png` byte for byte.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ngqr1ydj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
