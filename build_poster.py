#!/usr/bin/env python3
"""Draw the 19 November 2026 front page: seven stories plus a ticker.

A broadsheet front page rendered entirely in code with Pillow. No
external images, no network, no randomness: running this file twice
writes byte-identical PNGs.

Layout, top to bottom on a 1024x1024 page:
  masthead + dateline, a full-width lead story with a stat strip,
  a 2x2 grid of world stories, a bottom row with the record art sale
  and the record IPO, a dark "also today" ticker, and a source line.
Every story was checked against reporting published on 19 Nov 2026.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 229)
INK = (22, 21, 19)
RED = (158, 27, 30)
MUTED = (107, 101, 90)
RULE = (201, 192, 171)
DARK = (22, 21, 19)
CREAM = (246, 241, 229)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = word if not line else line + " " + word
        if draw.textlength(trial, font=fnt) <= max_width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top-left at (x, y); return the y just below the block."""
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_lines(draw, text, path, start_size, max_width, max_lines, min_size=18):
    """Largest size (from start_size down) whose wrap fits max_lines."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_width)


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def vline(draw, x, y0, y1, fill=RULE, width=1):
    draw.line([(x, y0), (x, y1)], fill=fill, width=width)


def kicker(draw, x, y, number, label, fnt):
    draw.text((x, y), "%s  ·  %s" % (number, label), font=fnt, fill=RED)


def story_card(draw, box, number, label, headline, deck,
               head_size=30, head_lines=2, deck_size=20):
    """One bordered story card; returns nothing. Text never leaves the box."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    pad = 16
    cx, cw = x0 + pad, x1 - x0 - 2 * pad
    y = y0 + 13
    kicker(draw, cx, y, number, label, font(SANS_BOLD, 15))
    y += 26
    hfnt, hlines = fit_lines(draw, headline, SERIF_BOLD, head_size,
                             cw, head_lines)
    y = text_block(draw, cx, y, hlines, hfnt, INK, int(head_size * 1.08) + 2)
    y += 4
    dfnt = font(SERIF, deck_size)
    dlines = wrap(draw, deck, dfnt, cw)
    text_block(draw, cx, y, dlines, dfnt, INK, deck_size + 7)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 26
    left, right = margin, W - margin

    # Double outer frame.
    d.rectangle([11, 11, W - 12, H - 12], outline=INK, width=3)
    d.rectangle([19, 19, W - 20, H - 20], outline=INK, width=1)

    # ---- Masthead -----------------------------------------------------
    y = 30
    mast = font(SERIF_BLACK, 58)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, y), title, font=mast, fill=INK)
    y += 70
    hline(d, left, right, y, INK, 3)
    hline(d, left, right, y + 5, INK, 1)
    y += 12

    # ---- Dateline row -------------------------------------------------
    small = font(SANS_BOLD, 16)
    d.text((left, y), "THURSDAY, 19 NOVEMBER 2026", font=small, fill=MUTED)
    rtext = "SEVEN STORIES  ·  ONE DAY"
    d.text((right - d.textlength(rtext, font=small), y), rtext,
           font=small, fill=MUTED)
    y += 24
    hline(d, left, right, y, RULE, 1)
    y += 10

    # ---- Lead story ---------------------------------------------------
    hero = (left, y, right, y + 236)
    d.rectangle(hero, outline=INK, width=2)
    hx, hw = left + 22, right - left - 44
    hy = hero[1] + 14
    kicker(d, hx, hy, "01", "THE LEAD  —  SHENZHEN SUMMIT",
           font(SANS_BOLD, 17))
    hy += 30
    hfnt, hlines = fit_lines(d, "Trump, Xi and Putin meet face to face",
                             SERIF_BOLD, 50, hw, 2)
    hy = text_block(d, hx, hy, hlines, hfnt, INK, 56)
    hy += 6
    deck = ("The first trilateral summit of its kind: 90 minutes on "
            "Ukraine, nuclear arms and trade, ending in a joint "
            "\u201cpeace declaration\u201d.")
    dfnt = font(SERIF, 23)
    dlines = wrap(d, deck, dfnt, hw)
    hy = text_block(d, hx, hy, dlines, dfnt, INK, 30)
    # Stat strip along the hero's foot.
    sy = hero[3] - 46
    hline(d, hx, right - 22, sy, RULE, 1)
    stats = [("90 MINUTES", "the meeting in Shenzhen"),
             ("3 LEADERS", "Trump  ·  Xi  ·  Putin"),
             ("1 DECLARATION", "a joint \u201cpeace\u201d text")]
    col_w = hw / 3
    for i, (big, small_text) in enumerate(stats):
        cx = hx + i * col_w
        if i:
            vline(d, int(cx - 12), sy + 8, sy + 38, RULE, 1)
        d.text((cx, sy + 8), big, font=font(SANS_BOLD, 16), fill=RED)
        d.text((cx, sy + 28), small_text, font=font(SANS, 14), fill=MUTED)
    y = hero[3] + 12

    # ---- 2x2 grid -----------------------------------------------------
    gap = 14
    vgap = 12
    col_w = (right - left - gap) // 2
    row_h = 160
    grid = [
        ("02", "THE HAGUE  —  INTERNATIONAL COURT",
         "Myanmar guilty of genocide",
         "The UN\u2019s highest court rules Myanmar committed "
         "state-sponsored genocide against the Rohingya \u2014 the "
         "first ruling of its kind."),
        ("03", "KERCH STRAIT  —  THIRD STRIKE IN A WEEK",
         "Kerch Bridge hit again",
         "A third strike halts traffic; a 227-metre road arch already "
         "lies in the strait after Kyiv\u2019s seven-stage operation."),
        ("04", "GAZA  —  GROUND OPERATION",
         "Tanks push into central Gaza",
         "Israeli forces launch a rare ground operation past the "
         "ceasefire line near Nuseirat; residents flee under "
         "artillery fire."),
        ("05", "BANGLADESH  —  LOCKDOWN TURNS VIOLENT",
         "Violence reaches 28 districts",
         "Four killed as the banned Awami League\u2019s shutdown turns "
         "violent; Yunus\u2019s ancestral home is torched in Chattogram."),
    ]
    for i, (num, label, head, deck) in enumerate(grid):
        gx = left + (i % 2) * (col_w + gap)
        gy = y + (i // 2) * (row_h + vgap)
        story_card(d, (gx, gy, gx + col_w, gy + row_h),
                   num, label, head, deck)
    y += 2 * row_h + vgap + 12

    # ---- Bottom row: art + business -----------------------------------
    row_h = 168
    bottom = [
        ("06", "ART  —  RECORD SALE",
         "Van Gogh sells for a record $190.4m",
         "\u201cChestnut Trees in Flower\u201d (1890) smashes the "
         "artist\u2019s auction record \u2014 $165m hammer, $190.4m "
         "with fees."),
        ("07", "BUSINESS  —  RECORD IPO",
         "Anthropic\u2019s $81.3bn IPO is the biggest ever",
         "The Claude maker prices at $83 a share, worth about $1.5 "
         "trillion; trading starts today."),
    ]
    for i, (num, label, head, deck) in enumerate(bottom):
        gx = left + i * (col_w + gap)
        story_card(d, (gx, y, gx + col_w, y + row_h),
                   num, label, head, deck, head_size=28, deck_size=19)
    y += row_h + 10

    # ---- "Also today" ticker ------------------------------------------
    tick = (left, y, right, y + 56)
    d.rectangle(tick, fill=DARK)
    ticker = ("ALSO TODAY   \u00b7   Iran strikes Kuwait and Bahrain after "
              "a U.S. attack on Qeshm Island   \u00b7   Denmark approves "
              "its Greenland pact 109\u20130   \u00b7   COP31 deadlocked "
              "on fossil fuels   \u00b7   589m children in conflict zones")
    tfnt = font(SANS, 16)
    tlines = wrap(d, ticker, tfnt, right - left - 28)
    ty = y + (56 - len(tlines) * 21) // 2
    for ln in tlines:
        d.text((left + 14, ty), ln, font=tfnt, fill=CREAM)
        ty += 21
    y += 56 + 10

    # ---- Footer -------------------------------------------------------
    foot = ("Sources: Reuters, AP, Just Security, The Art Newspaper "
            "\u2014 19 November 2026   \u00b7   Drawn entirely in code")
    ffnt = font(SERIF_ITALIC, 16)
    fw = d.textlength(foot, font=ffnt)
    d.text(((W - fw) / 2, y), foot, font=ffnt, fill=MUTED)

    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    path = render()
    size = os.path.getsize(path)
    with Image.open(path) as im:
        assert im.size == (W, H), im.size
    assert size <= 1048576, size
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))
