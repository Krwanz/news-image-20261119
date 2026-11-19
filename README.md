[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Krwanz/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Krwanz/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# News in one image: 19 November 2026

A newspaper-style poster summing up Thursday 19 November 2026 in one
1024×1024 image, drawn entirely in code with Python + PIL
(`build_poster.py`, no external images, no network).

Entry for the [make.fun bounty news-image-20261119](https://make.fun/bounty/news-image-20261119).

## The stories

- **The lead — Shenzhen:** Trump, Xi and Putin meet face to face for the
  first trilateral summit of its kind — 90 minutes on Ukraine, nuclear
  arms and trade, ending in a joint “peace declaration”.
- **The Hague:** the International Court of Justice rules Myanmar
  committed genocide against the Rohingya — the first state-genocide
  ruling of its kind by the UN's highest court.
- **Kerch Strait:** the Crimean Bridge is hit a third time in a week; a
  road span falls and car traffic halts.
- **Gaza:** Israeli tanks push into central Gaza past the ceasefire line
  in a rare ground operation.
- **Bangladesh:** Muhammad Yunus's ancestral home is torched as violence
  reaches 28 districts.
- **Art & climate:** Van Gogh's “Chestnuts in Flower” sells for a record
  $190.4m, while COP31 ministers race to unblock talks in Antalya.

## Run

```sh
python3 build_poster.py   # redraw entry.png from scratch
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`; running
it twice produces byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
