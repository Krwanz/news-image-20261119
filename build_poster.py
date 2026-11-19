#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news poster (1024x1024) with PIL.

Every pixel is drawn in code: flat colour blocks, rules, simple
pictograms and wrapped text. No external images, no network.
Stories are the day's real headlines, checked against several
news round-ups for 19 November 2026.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 26)
NAVY = (18, 32, 62)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
SLATE = (90, 96, 110)
CARD = (255, 255, 255)
LINE = (200, 192, 175)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=6):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def kicker(draw, x, y, text, color=RED, size=21):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=color)
    return y + size + 8


def headline(draw, x, y, text, size, width, fill=INK, fnt_path=SERIF):
    f = font(fnt_path, size)
    return para(draw, x, y, text, f, width, fill=fill, leading=4)


def card(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=LINE, width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)


def scales(draw, cx, cy, s, color):
    """Simple scales-of-justice pictogram centred at (cx, cy)."""
    draw.line([(cx, cy - 34 * s), (cx, cy + 30 * s)], fill=color, width=5)
    draw.line([(cx - 42 * s, cy - 22 * s), (cx + 42 * s, cy - 22 * s)],
              fill=color, width=5)
    draw.ellipse([cx - 6 * s, cy - 42 * s, cx + 6 * s, cy - 30 * s],
                 fill=color)
    for dx in (-42, 42):
        draw.line([(cx + dx * s, cy - 22 * s), (cx + dx * s - 16 * s, cy + 6 * s)],
                  fill=color, width=4)
        draw.line([(cx + dx * s, cy - 22 * s), (cx + dx * s + 16 * s, cy + 6 * s)],
                  fill=color, width=4)
        draw.arc([cx + dx * s - 18 * s, cy - 4 * s, cx + dx * s + 18 * s,
                  cy + 22 * s], 0, 180, fill=color, width=4)
    draw.rectangle([cx - 26 * s, cy + 30 * s, cx + 26 * s, cy + 36 * s],
                   fill=color)


def bridge(draw, x, y, w, h, color):
    """A suspension bridge with its middle span dropped."""
    deck = y + h - 18
    draw.line([(x, deck), (x + w, deck)], fill=color, width=6)
    for tx in (x + 8, x + w - 8):
        draw.line([(tx, y + 6), (tx, deck)], fill=color, width=6)
    # left cables + deck segment
    draw.line([(x + 8, y + 6), (x + w // 2 - 26, deck)], fill=color, width=3)
    draw.line([(x + w - 8, y + 6), (x + w // 2 + 26, deck)], fill=color, width=3)
    # the fallen middle span, tilted into the water below
    draw.line([(x + w // 2 - 26, deck), (x + w // 2 + 10, deck + 16)],
              fill=RED, width=6)
    draw.line([(x + w // 2 + 26, deck), (x + w // 2 + 40, deck + 10)],
              fill=RED, width=6)


def flame(draw, cx, cy, s, color):
    pts = [(cx, cy - 34 * s), (cx + 16 * s, cy - 6 * s),
           (cx + 8 * s, cy + 4 * s), (cx + 20 * s, cy + 22 * s),
           (cx, cy + 30 * s), (cx - 20 * s, cy + 22 * s),
           (cx - 8 * s, cy + 4 * s), (cx - 16 * s, cy - 6 * s)]
    draw.polygon(pts, fill=color)


def tank(draw, x, y, w, color):
    draw.rounded_rectangle([x, y + 18, x + w, y + 44], radius=8, fill=color)
    draw.rectangle([x + w // 2 - 8, y, x + w // 2 + 8, y + 20], fill=color)
    draw.line([(x + w // 2 + 8, y + 6), (x + w + 26, y + 2)],
              fill=color, width=7)
    for wx in (x + 14, x + w - 26):
        draw.ellipse([wx, y + 46, wx + 12, y + 58], fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 156], fill=GOLD)
    d.text((36, 26), "THE WORLD  •  IN ONE IMAGE",
           font=font(SANS_B, 26), fill=GOLD)
    d.text((36, 62), "19 NOVEMBER 2026",
           font=font(SERIF, 58), fill=(255, 255, 255))
    d.text((36, 122), "THURSDAY  —  SHENZHEN  •  THE HAGUE  •  KERCH  •  GAZA  •  DHAKA",
           font=font(SANS, 19), fill=(190, 198, 214))

    # ---- lead story: Shenzhen summit ------------------------------
    lx, ly, lw, lh = 28, 176, 968, 268
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=12,
                        fill=CARD, outline=LINE, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 8], fill=RED)
    tx = lx + 28
    y = ly + 24
    y = kicker(d, tx, y, "THE LEAD  —  SHENZHEN, CHINA")
    y = headline(d, tx, y, "Trump, Xi and Putin meet face to face",
                 40, 560)
    y = para(d, tx, y + 4,
             "The first trilateral summit of its kind: 90 minutes on "
             "Ukraine, nuclear arms and trade — ending in a joint "
             "“peace declaration”.",
             font(SANS, 21), 560, fill=(60, 60, 70), leading=7)
    # skyline panel on the right of the lead card
    px, py, pw, ph = lx + 620, ly + 24, 320, 200
    d.rectangle([px, py, px + pw, py + ph], fill=(232, 226, 208))
    d.rectangle([px, py + ph - 58, px + pw, py + ph], fill=NAVY)
    towers = [(0, 96), (34, 62), (72, 110), (108, 48), (150, 88),
              (188, 58), (224, 100), (258, 70)]
    for ox, th in towers:
        d.rectangle([px + ox, py + ph - 58 - th, px + ox + 28,
                     py + ph - 58], fill=(70, 78, 96))
    d.ellipse([px + pw - 62, py + 14, px + pw - 18, py + 58], fill=GOLD)
    # three flag discs for the three leaders
    flags = [((178, 34, 34), "US"), ((222, 41, 16), "CN"),
             ((0, 57, 166), "RU")]
    for i, (col, lab) in enumerate(flags):
        cx = px + 52 + i * 108
        d.ellipse([cx - 30, py + ph - 56, cx + 30, py + ph + 4],
                  fill=col, outline=(255, 255, 255), width=3)
        d.text((cx - 12, py + ph - 36), lab, font=font(SANS_B, 20),
               fill=(255, 255, 255))

    # ---- middle row: two cards ------------------------------------
    my, mh = 464, 268
    # ICJ / Myanmar
    card(d, 28, my, 474, mh, NAVY)
    cx = 28 + 474 // 2
    scales(d, cx, my + 72, 1.0, NAVY)
    y = kicker(d, 52, my + 118, "THE HAGUE  —  WORLD COURT", size=19)
    y = headline(d, 52, y, "ICJ: Myanmar committed genocide",
                 26, 426)
    para(d, 52, y + 2,
         "The UN's highest court rules against Myanmar over the "
         "Rohingya — a first of its kind.",
         font(SANS, 17), 426, fill=(60, 60, 70), leading=5)
    # Kerch bridge
    card(d, 522, my, 474, mh, TEAL)
    bridge(d, 522 + 474 // 2 - 150, my + 18, 300, 92, TEAL)
    y = kicker(d, 546, my + 118, "KERCH STRAIT  —  UKRAINE WAR", size=19)
    y = headline(d, 546, y, "Crimean Bridge hit a third time",
                 26, 426)
    para(d, 546, y + 2,
         "A road span falls and car traffic halts after the week's "
         "third strike on the bridge.",
         font(SANS, 17), 426, fill=(60, 60, 70), leading=5)

    # ---- bottom row: three cards ----------------------------------
    by, bh, bw, gap = 748, 208, 310, 19
    xs = [28, 28 + bw + gap, 28 + 2 * (bw + gap)]
    # Gaza
    card(d, xs[0], by, bw, bh, RED)
    tank(d, xs[0] + bw // 2 - 45, by + 14, 90, (70, 78, 96))
    y = kicker(d, xs[0] + 22, by + 84, "GAZA", size=19)
    y = headline(d, xs[0] + 22, y, "Israeli tanks push past the ceasefire line",
                 20, bw - 44)
    para(d, xs[0] + 22, y + 2,
         "A rare ground operation in central Gaza draws a Hamas "
         "protest.", font(SANS, 15), bw - 44, fill=(60, 60, 70),
         leading=4)
    # Bangladesh
    card(d, xs[1], by, bw, bh, (222, 120, 20))
    flame(d, xs[1] + bw // 2, by + 50, 0.9, (222, 120, 20))
    y = kicker(d, xs[1] + 22, by + 84, "BANGLADESH", size=19)
    y = headline(d, xs[1] + 22, y, "Yunus home torched as unrest spreads",
                 20, bw - 44)
    para(d, xs[1] + 22, y + 2,
         "Violence in 28 districts as the ousted party is outlawed.", font(SANS, 15), bw - 44,
         fill=(60, 60, 70), leading=4)
    # Culture & climate
    card(d, xs[2], by, bw, bh, GOLD)
    d.ellipse([xs[2] + bw // 2 - 32, by + 16, xs[2] + bw // 2 + 32,
               by + 80], outline=GOLD, width=5)
    d.text((xs[2] + bw // 2 - 19, by + 34), "$190m",
           font=font(SANS_B, 19), fill=(150, 110, 10))
    y = kicker(d, xs[2] + 22, by + 84, "ART & CLIMATE", size=19)
    y = headline(d, xs[2] + 22, y, "Van Gogh sells for a record $190.4m",
                 20, bw - 44)
    para(d, xs[2] + 22, y + 2,
         "“Chestnuts in Flower” sets a record; COP31 talks race on.",
         font(SANS, 15), bw - 44, fill=(60, 60, 70), leading=4)

    # ---- footer ----------------------------------------------------
    d.rectangle([0, 972, W, H], fill=NAVY)
    d.text((36, 988), "Six stories, one day  •  19 November 2026  •  Drawn from the day's reporting",
           font=font(SANS, 18), fill=(190, 198, 214))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
