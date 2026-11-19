# News in one image: 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Krwanz/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Krwanz/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A broadsheet front page for Thursday, 19 November 2026, drawn entirely
in code — no external images. Built for the
[make.fun bounty](https://make.fun/bounty/news-image-20261119)
`news-image-20261119` (prize $250, top 50).

## The day, in seven stories plus a ticker

1. **Trump, Xi and Putin meet face to face** — the first trilateral
   summit of its kind in Shenzhen: 90 minutes on Ukraine, nuclear
   arms and trade, ending in a joint "peace declaration".
2. **Myanmar guilty of genocide** — the UN's highest court rules
   Myanmar committed state-sponsored genocide against the Rohingya,
   the first ruling of its kind.
3. **Kerch Bridge hit again** — a third strike in a week halts
   traffic; a 227-metre road arch already lies in the strait after
   Kyiv's seven-stage operation.
4. **Tanks push into central Gaza** — a rare ground operation past
   the ceasefire line near Nuseirat.
5. **Violence reaches 28 districts** — four killed as the banned
   Awami League's shutdown turns violent in Bangladesh; Yunus's
   ancestral home is torched in Chattogram.
6. **Van Gogh sells for a record $190.4m** — "Chestnut Trees in
   Flower" (1890) at Sotheby's New York: $165m hammer, $190.4m
   with fees.
7. **Anthropic's $81.3bn IPO is the biggest ever** — priced at $83
   a share, worth about $1.5 trillion; trading on the Nasdaq
   starts today.

Also today: Iran strikes Kuwait and Bahrain after a U.S. attack on
Qeshm Island, Denmark approves its Greenland pact 109-0, COP31
deadlocked on fossil fuels, 589m children in conflict zones.

Every story was checked against reporting published on 19 November
2026 (Reuters, AP, Just Security, The Art Newspaper).

## Reproduce

```sh
python3 build_poster.py   # writes entry.png, 1024x1024, deterministic
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR`
byte-identical on every run. The poster is drawn with Python 3
standard library plus Pillow; no network is used.

## Files

- `build_poster.py` — the poster generator (written fresh, from scratch)
- `entry.png` — the 1024x1024 poster it draws
- `main.py` — the entry program: copies `entry.png` to the output dir
- `LICENSE` — MIT
