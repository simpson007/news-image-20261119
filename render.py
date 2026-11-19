#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Run: python3 render.py  -> writes entry.png beside this file.
Deterministic: fixed text, fixed geometry, no time, no randomness, no network.
Only the Python standard library + Pillow are used to render; the entry
program itself (main.ts) only copies the finished entry.png.

Facts, all first reported on Wednesday 18 November 2026 or on Thursday
19 November 2026 and checked against several news sources:
- Shenzhen: Trump, Xi and Putin meet on Thursday 19 November in
  Shenzhen, the first trilateral of the three leaders, on the sidelines
  of APEC. Nuclear arms top the agenda after New START lapsed in
  February; the war in Iran is on the table too. Trump and Putin are
  also due a one-to-one.
- The Hague: the International Court of Justice delivers its judgment
  at 10 a.m. on Thursday on whether Myanmar committed genocide against
  the Rohingya in 2017. A finding of guilt would be the first time the
  court has held a state responsible for genocide.
- Vice City: Grand Theft Auto VI unlocks at midnight around the world
  on 19 November, 13 years after GTA V. Early reviews give it 99 on
  Metacritic; pre-sales are near $1.5bn and Take-Two shares rose over
  8% in early trading.
- Markets (Wednesday close): Dow -1.1% to 50,198, a third straight
  loss; S&P -0.2% to 7,324, a fifth straight loss; Nasdaq +0.4% to
  24,430. Fed minutes point to more rate rises. Brent -1.3% to $91.95
  and gold -2.5% to $3,753.
- Washington: House Democrats nominate Hakeem Jeffries for Speaker,
  251-11 in a closed-door vote; if the full House elects him on
  3 January he will be the first Black Speaker.
- Anthropic: prices its IPO at $83 a share, above its $70-78 range,
  in an enlarged 980-million-share offering worth about $81bn; shares
  start trading on the Nasdaq on Thursday under the ticker ANT.
- Cyclone Akvan: a severe cyclonic storm in the Bay of Bengal bears
  down on India's east coast; landfall is forecast for Friday between
  Narsapur and Puri, with schools shut and red alerts out.
- Brussels: the European Commission proposes a EUR 45bn loan to
  Ukraine for 2027, repaid only once Russia pays reparations.
- Also: Nvidia founder Jensen Huang resigns; Iran widens its attacks
  on Gulf states, hitting a US base in Kuwait and Bahrain again;
  NASA's Voyager 1 reaches a light-day from Earth.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024

C = {
    "paper": (247, 243, 232),
    "ink": (20, 20, 20),
    "navy": (16, 38, 63),
    "red": (179, 38, 30),
    "gold": (201, 162, 39),
    "gold_lt": (232, 196, 90),
    "gray": (88, 88, 88),
    "sky": (223, 232, 238),
    "white": (255, 255, 255),
    "orange": (232, 120, 30),
    "yellow": (245, 196, 60),
    "down": (220, 60, 50),
    "up": (60, 180, 90),
    "rule": (200, 192, 170),
    "body": (60, 60, 60),
    "pale": (200, 210, 220),
}

FONTS = "/usr/share/fonts/truetype/dejavu"


def load_font(kind, size):
    name = {"serif-bold": "DejaVuSerif-Bold.ttf",
            "sans-bold": "DejaVuSans-Bold.ttf",
            "sans": "DejaVuSans.ttf"}[kind]
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def vgrad(d, x, y, w, h, top, bottom):
    for row in range(h):
        t = row / max(h - 1, 1)
        col = tuple(round(top[k] + (bottom[k] - top[k]) * t)
                    for k in range(3))
        d.line([(x, y + row), (x + w, y + row)], fill=col)


def wrap_text(d, text, f, maxw):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        elif cur:
            out.append(cur)
            cur = word
        else:
            cur = word
    if cur:
        out.append(cur)
    return out


def draw_para(d, x, y, text, f, fill, maxw, leading):
    for line in wrap_text(d, text, f, maxw):
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def starburst(d, cx, cy, outer, inner, points, fill):
    verts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / points - math.pi / 2
        verts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(verts, fill=fill)


def rule(d, x0, x1, y, fill=None, width=2):
    d.line([(x0, y), (x1, y)], fill=fill or C["rule"], width=width)


def flag(d, x, y, w, h, kind):
    """A small waving flag on a pole at (x, y): top-left corner, w x h."""
    d.line([(x, y), (x, y + h + 26)], fill=(40, 40, 44), width=3)
    if kind == "us":
        for i in range(7):
            d.rectangle([x + 3, y + i * h // 7, x + 3 + w, y + (i + 1) * h // 7],
                        fill=C["white"] if i % 2 else C["red"])
        d.rectangle([x + 3, y, x + 3 + w * 2 // 5, y + h * 4 // 7],
                    fill=(30, 50, 110))
    elif kind == "cn":
        d.rectangle([x + 3, y, x + 3 + w, y + h], fill=(222, 40, 30))
        d.ellipse([x + 8, y + 5, x + 16, y + 13], fill=C["yellow"])
    elif kind == "ru":
        d.rectangle([x + 3, y, x + 3 + w, y + h // 3], fill=C["white"])
        d.rectangle([x + 3, y + h // 3, x + 3 + w, y + 2 * h // 3],
                    fill=(30, 80, 180))
        d.rectangle([x + 3, y + 2 * h // 3, x + 3 + w, y + h],
                    fill=(200, 30, 30))


def shenzhen_summit(d, x, y, w, h):
    """Shenzhen at dusk: skyline, low sun, three flags in front."""
    vgrad(d, x, y, w, h, (24, 32, 66), (214, 120, 70))
    d.ellipse([x + w - 90, y + 12, x + w - 40, y + 62],
              fill=(245, 196, 60))
    heights = [60, 96, 74, 120, 84, 104, 68, 92, 56, 110, 78, 88]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 2, y + h - bh, bx + bw - 2, y + h],
                    fill=(28, 26, 48))
        wy = y + h - bh + 8
        while wy < y + h - 8:
            wx = bx + 7
            while wx < bx + bw - 8:
                if (wx * 7 + wy * 3) % 26 < 12:
                    d.rectangle([wx, wy, wx + 3, wy + 4],
                                fill=(250, 210, 90))
                wx += 12
            wy += 12
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 20, 34))
    flag(d, x + 60, y + h - 92, 52, 34, "us")
    flag(d, x + w // 2 - 26, y + h - 92, 52, 34, "cn")
    flag(d, x + w - 112, y + h - 92, 52, 34, "ru")
    d.text((x + 12, y + 10), "SHENZHEN  —  APEC SUMMIT",
           font=load_font("sans-bold", 17), fill=C["white"])


def hague_court(d, x, y, w, h):
    """A classical court house: pediment, columns, steps."""
    vgrad(d, x, y, w, h, (200, 214, 226), (168, 186, 200))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 128, 136))
    bx0, bx1 = x + 60, x + w - 60
    d.rectangle([bx0, y + 34, bx1, y + h - 22], fill=(226, 220, 204))
    d.polygon([(bx0 - 12, y + 36), (bx1 + 12, y + 36),
               ((bx0 + bx1) // 2, y + 8)], fill=(206, 198, 178))
    d.ellipse([(bx0 + bx1) // 2 - 10, y + 18, (bx0 + bx1) // 2 + 10,
               y + 34], fill=(150, 130, 90))
    for i in range(5):
        cx = bx0 + 30 + i * (bx1 - bx0 - 60) // 4
        d.rectangle([cx - 9, y + 40, cx + 9, y + h - 30], fill=(246, 242, 228))
        d.rectangle([cx - 13, y + 36, cx + 13, y + 42], fill=(236, 230, 212))
        d.rectangle([cx - 13, y + h - 34, cx + 13, y + h - 28],
                    fill=(236, 230, 212))
    d.rectangle([bx0 + 60, y + h - 28, bx1 - 60, y + h - 22],
                fill=(90, 70, 50))
    for i in range(3):
        d.rectangle([x + 24 + i * 8, y + h - 22, x + w - 24 - i * 8,
                     y + h - 18 + i * 4], fill=(150, 148, 140))


def vice_city(d, x, y, w, h):
    """Vice City at night: neon skyline, pink sun, palms."""
    vgrad(d, x, y, w, h, (28, 8, 52), (150, 40, 110))
    d.ellipse([x + w // 2 - 26, y + 6, x + w // 2 + 26, y + 58],
              fill=(255, 110, 170))
    heights = [30, 48, 38, 58, 44, 52, 34, 46]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 2, y + h - bh, bx + bw - 2, y + h],
                    fill=(16, 10, 30))
        wy = y + h - bh + 6
        while wy < y + h - 6:
            wx = bx + 6
            while wx < bx + bw - 8:
                if (wx + wy) % 20 < 9:
                    d.rectangle([wx, wy, wx + 3, wy + 4],
                                fill=(80, 230, 220) if (wx // 12) % 2
                                else (255, 90, 180))
                wx += 11
            wy += 11
    for px, lean in [(x + 26, -1), (x + w - 34, 1)]:
        d.line([(px, y + h), (px + lean * 10, y + h - 34)],
               fill=(10, 8, 20), width=5)
        for k in range(5):
            a = math.pi * (0.15 + k * 0.17)
            d.arc([px + lean * 10 - 16, y + h - 52, px + lean * 10 + 16,
                   y + h - 20], 180 + k * 36, 180 + k * 36 + 40,
                  fill=(10, 8, 20), width=3)


def split_line(d, x, y, w, h):
    """A market line that falls, then rises."""
    pts = []
    for i in range(10):
        px = x + i * w / 9
        if i <= 5:
            py = y + h * (0.12 + 0.68 * i / 5)
        else:
            py = y + h * (0.80 - 0.62 * (i - 5) / 4)
        pts.append((px, py))
    d.line(pts, fill=C["gold_lt"], width=4, joint="curve")
    tip = pts[-1]
    d.polygon([(tip[0], tip[1]), (tip[0] - 16, tip[1] - 2),
               (tip[0] - 2, tip[1] + 12)], fill=C["up"])


def masthead(d):
    d.rectangle([0, 0, PAGE_W, 118], fill=C["navy"])
    d.text((PAGE_W // 2, 10), "THE WORLD IN ONE DAY",
           font=load_font("serif-bold", 54), fill=C["white"], anchor="ma")
    d.text((PAGE_W // 2, 74), "THURSDAY  ·  19 NOVEMBER 2026",
           font=load_font("sans-bold", 28), fill=C["gold_lt"], anchor="ma")
    rule(d, 0, PAGE_W, 118, fill=C["gold"], width=4)


def lead_story(d):
    d.text((40, 134), "SHENZHEN  —  THE FIRST TRILATERAL",
           font=load_font("sans-bold", 21), fill=C["red"])
    d.text((40, 160), "TRUMP, XI AND PUTIN",
           font=load_font("sans-bold", 40), fill=C["ink"])
    d.text((40, 202), "MEET IN SHENZHEN",
           font=load_font("sans-bold", 40), fill=C["ink"])
    shenzhen_summit(d, 40, 248, 560, 216)
    lx = 624
    y = draw_para(d, lx, 252,
                  "The leaders of the US, China and Russia sit down "
                  "together for the first time today in Shenzhen, on "
                  "the sidelines of APEC.",
                  load_font("sans", 19), C["ink"], 360, 24)
    y = draw_para(d, lx, y + 8,
                  "Nuclear arms top the agenda after New START lapsed "
                  "in February; the war in Iran is on the table too.",
                  load_font("sans", 19), C["ink"], 360, 24)
    draw_para(d, lx, y + 8,
              "Trump and Putin are also due a one-to-one.",
              load_font("sans", 19), C["ink"], 360, 24)
    rule(d, 40, 984, 480)


def middle_row(d):
    hague_court(d, 40, 494, 452, 74)
    d.text((40, 578), "THE HAGUE", font=load_font("sans-bold", 20),
           fill=C["red"])
    d.text((40, 602), "WORLD COURT RULES",
           font=load_font("sans-bold", 26), fill=C["ink"])
    d.text((40, 632), "ON MYANMAR TODAY",
           font=load_font("sans-bold", 26), fill=C["ink"])
    draw_para(d, 40, 666,
              "The court rules at 10 a.m. on whether Myanmar committed "
              "genocide against the Rohingya. A guilty verdict would "
              "be a first.",
              load_font("sans", 18), C["body"], 452, 22)
    vice_city(d, 532, 494, 452, 74)
    d.text((532, 578), "VICE CITY  —  GTA VI",
           font=load_font("sans-bold", 20), fill=C["red"])
    d.text((532, 602), "GAMERS ENTER",
           font=load_font("sans-bold", 26), fill=C["ink"])
    d.text((532, 632), "VICE CITY",
           font=load_font("sans-bold", 26), fill=C["ink"])
    draw_para(d, 532, 666,
              "Grand Theft Auto VI unlocks at midnight around the "
              "world, 13 years after GTA V. Early reviews give it 99 "
              "on Metacritic; pre-sales near $1.5bn.", load_font("sans", 18),
              C["body"], 452, 22)
    rule(d, 40, 984, 732)


def markets_strip(d):
    d.rectangle([0, 742, PAGE_W, 832], fill=C["navy"])
    d.text((40, 754), "MARKETS SPLIT",
           font=load_font("sans-bold", 26), fill=C["gold_lt"])
    split_line(d, 330, 752, 180, 66)
    d.text((530, 754),
           "Dow −1.1% · S&P −0.2% · Nasdaq +0.4%",
           font=load_font("sans-bold", 20), fill=C["white"])
    d.text((530, 788),
           "Brent −1.3% to $91.95  ·  Gold −2.5% to $3,753",
           font=load_font("sans", 19), fill=C["pale"])
    d.text((40, 782), "Fed minutes point to more hikes",
           font=load_font("sans", 19), fill=C["pale"])


def bottom_row(d):
    cards = [
        ("WASHINGTON", C["red"],
         "Democrats nominate Jeffries for Speaker, 251–11"),
        ("ANTHROPIC IPO", (14, 90, 60),
         "Prices its shares at $83; $81bn raise, trades today"),
        ("CYCLONE AKVAN", (90, 60, 120),
         "Severe storm nears India's east coast; landfall Friday"),
        ("BRUSSELS", (120, 70, 20),
         "EU offers Kyiv €45bn, repaid once Russia pays up"),
    ]
    cx = 40
    for kicker, color, head in cards:
        d.rectangle([cx, 844, cx + 226, 850], fill=color)
        d.text((cx, 860), kicker, font=load_font("sans-bold", 17), fill=color)
        draw_para(d, cx, 884, head, load_font("sans-bold", 20), C["ink"],
                  226, 25)
        cx += 238
    rule(d, 40, 984, 972)


def footer(d):
    d.text((PAGE_W // 2, 984),
           "ALSO: Nvidia's Huang quits  ·  Iran widens attacks on Gulf "
           "states  ·  Voyager 1 reaches a light-day from Earth",
           font=load_font("sans", 16), fill=C["gray"], anchor="ma")


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), C["paper"])
    d = ImageDraw.Draw(img)
    masthead(d)
    lead_story(d)
    middle_row(d)
    markets_strip(d)
    bottom_row(d)
    footer(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
