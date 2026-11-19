#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a 1024x1024 newspaper poster.

One page of world news for Thursday 19 November 2026, drawn entirely in
code with Pillow: no external images, no network, fully deterministic
(running it twice produces a byte-identical PNG).

Layout, top to bottom: masthead, lead story (Shenzhen trilateral summit),
two rows of two stories (The Hague, Kerch Bridge / Gaza, Bangladesh),
a closing art-and-climate band, and a footer line.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 30
PAPER = (248, 244, 233)
CARD = (255, 253, 245)
INK = (26, 26, 26)
MUTED = (90, 84, 70)
ACCENT = (155, 28, 28)
RULE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_height(draw, lines, fnt, leading):
    if not lines:
        return 0
    ascent, descent = fnt.getmetrics()
    return len(lines) * (ascent + descent + leading) - leading


def draw_wrapped(draw, x, y, lines, fnt, fill, leading=4):
    ascent, descent = fnt.getmetrics()
    step = ascent + descent + leading
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def fit_body(draw, text, fnt_sizes, max_width, max_height, leading=4):
    """Pick the largest body size whose wrapped text fits max_height.

    Returns (font, lines). Raises if even the smallest size overflows,
    so an overflowing poster fails loudly instead of clipping text.
    """
    for size in fnt_sizes:
        fnt = font(SANS, size)
        lines = wrap(draw, text, fnt, max_width)
        if text_height(draw, lines, fnt, leading) <= max_height:
            return fnt, lines
    raise ValueError("body text does not fit: %r" % text[:60])


def draw_card(draw, box, kicker, headline, body, head_size, body_sizes,
              head_lines_max=2):
    """Draw one story card; returns nothing, raises on overflow."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=2)
    pad = 18
    inner_w = (x1 - x0) - 2 * pad
    y = y0 + 14

    kick_font = font(SANS_BOLD, 15)
    draw.text((x0 + pad, y), kicker, font=kick_font, fill=ACCENT)
    y += 24

    head_font = font(SERIF_BOLD, head_size)
    head_lines = wrap(draw, headline, head_font, inner_w)
    if len(head_lines) > head_lines_max:
        raise ValueError("headline too long: %r" % headline)
    y = draw_wrapped(draw, x0 + pad, y, head_lines, head_font, INK, leading=2)

    body_top = y + 8
    body_bottom = y1 - 14
    body_font, body_lines = fit_body(
        draw, body, body_sizes, inner_w, body_bottom - body_top)
    draw_wrapped(draw, x0 + pad, body_top, body_lines, body_font, INK)


def draw_masthead(draw):
    """Title, dateline and rules across the top of the page."""
    cx = SIZE // 2
    title_font = font(SERIF_BOLD, 56)
    title = "THE WORLD IN ONE PAGE"
    tw = draw.textlength(title, font=title_font)
    draw.text((cx - tw / 2, 34), title, font=title_font, fill=INK)

    date_font = font(SANS, 22)
    dateline = "Thursday, 19 November 2026"
    dw = draw.textlength(dateline, font=date_font)
    draw.text((cx - dw / 2, 108), dateline, font=date_font, fill=MUTED)

    draw.line([(MARGIN, 142), (SIZE - MARGIN, 142)], fill=RULE, width=3)
    draw.line([(MARGIN, 148), (SIZE - MARGIN, 148)], fill=RULE, width=1)


def draw_footer(draw):
    foot_font = font(SANS, 15)
    line = "Drawn entirely in code  |  Python + PIL  |  No external images"
    fw = draw.textlength(line, font=foot_font)
    draw.text(((SIZE - fw) / 2, 956), line, font=foot_font, fill=MUTED)


def build():
    for path in (SERIF_BOLD, SANS, SANS_BOLD):
        if not os.path.exists(path):
            raise SystemExit("missing font: %s" % path)

    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle([14, 14, SIZE - 15, SIZE - 15], outline=INK, width=2)

    draw_masthead(draw)

    left = MARGIN
    right = SIZE - MARGIN
    mid_gap = 16
    col_w = (right - left - mid_gap) // 2

    # Lead story, full width.
    draw_card(
        draw, (left, 164, right, 344),
        "THE LEAD  ·  SHENZHEN SUMMIT",
        "Trump, Xi and Putin meet face to face",
        "The first trilateral summit of its kind: 90 minutes on Ukraine, "
        "nuclear arms and trade, ending in a joint \u201cpeace "
        "declaration\u201d.",
        head_size=38, body_sizes=(21, 20, 19))

    # Second row: The Hague and the Kerch Strait.
    draw_card(
        draw, (left, 360, left + col_w, 556),
        "THE HAGUE  ·  INTERNATIONAL COURT",
        "Myanmar guilty of genocide",
        "The court rules Myanmar committed genocide against the Rohingya, "
        "the first such ruling by the UN\u2019s highest court.",
        head_size=27, body_sizes=(19, 18, 17))
    draw_card(
        draw, (right - col_w, 360, right, 556),
        "KERCH STRAIT  ·  THIRD STRIKE IN A WEEK",
        "Kerch Bridge hit again",
        "The Crimean Bridge is hit a third time in a week; a road span "
        "falls and car traffic halts.",
        head_size=27, body_sizes=(19, 18, 17))

    # Third row: Gaza and Bangladesh.
    draw_card(
        draw, (left, 572, left + col_w, 768),
        "GAZA  ·  GROUND OPERATION",
        "Tanks push into central Gaza",
        "Israeli tanks push into central Gaza past the ceasefire line in a "
        "rare ground operation.",
        head_size=27, body_sizes=(19, 18, 17))
    draw_card(
        draw, (right - col_w, 572, right, 768),
        "BANGLADESH  ·  UNREST SPREADS",
        "Violence reaches 28 districts",
        "Muhammad Yunus\u2019s ancestral home is torched as violence "
        "reaches 28 districts.",
        head_size=27, body_sizes=(19, 18, 17))

    # Closing band: art and climate.
    draw_card(
        draw, (left, 784, right, 940),
        "ART & CLIMATE  ·  RECORD SALE AND COP31",
        "Van Gogh sells for a record $190.4m",
        "Van Gogh\u2019s \u201cChestnuts in Flower\u201d sells for a record "
        "$190.4m, while COP31 ministers race to unblock talks in Antalya.",
        head_size=30, body_sizes=(20, 19, 18))

    draw_footer(draw)
    return image


def main():
    image = build()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    image.save(out, format="PNG")
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
