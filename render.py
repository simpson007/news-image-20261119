#!/usr/bin/env python3
"""Paint the world-news front page for Thursday 19 November 2026.

Running `python3 render.py` produces entry.png in this same folder.
The picture is fully reproducible: the wording never changes, the layout
never moves, and nothing depends on the clock, on chance, or on the
network. Rendering needs only the standard library and Pillow; the
entry program (main.ts) just copies the finished PNG into place.

What the page reports — every item was first carried on Wednesday
18 November or Thursday 19 November 2026 and cross-checked against
several news outlets:
- Shenzhen hosts a first-ever three-way meeting of Trump, Xi and
  Putin on Thursday, alongside APEC. With New START having expired
  in February, nuclear arms lead the agenda, and the Iran war is
  also up for discussion. Trump and Putin are set to meet alone too.
- The Hague: at 10 a.m. on Thursday the International Court of
  Justice rules on whether Myanmar committed genocide against the
  Rohingya in 2017. A guilty ruling would be the first time the
  court has found a state guilty of genocide.
- Vice City: Grand Theft Auto VI goes live at midnight worldwide on
  19 November, thirteen years after GTA V. Reviewers score it 99 on
  Metacritic, pre-orders approach $1.5bn, and Take-Two shares
  climbed more than 8% in early trading.
- Markets at Wednesday's close: the Dow fell 1.1% to 50,198, its
  third loss in a row; the S&P slipped 0.2% to 7,324, a fifth
  straight loss; the Nasdaq rose 0.4% to 24,430. Fed minutes point
  to further rate rises. Brent dropped 1.3% to $91.95, gold 2.5%
  to $3,753.
- Washington: House Democrats pick Hakeem Jeffries as their Speaker
  nominee, 251–11 behind closed doors; a win in the full House on
  3 January would make him the first Black Speaker.
- Anthropic: its IPO is priced at $83 a share, above the $70–78
  range, in a larger 980-million-share sale worth roughly $81bn;
  trading starts on the Nasdaq on Thursday as ANT.
- Cyclone Akvan: a severe storm in the Bay of Bengal heads for
  India's east coast, with landfall expected on Friday between
  Narsapur and Puri; schools are closed and red alerts are in force.
- Brussels: the European Commission puts forward a EUR 45bn loan
  for Ukraine in 2027, to be repaid only once Russia pays
  reparations.
- Also in brief: Nvidia founder Jensen Huang steps down; Iran
  broadens its attacks on Gulf states, striking a US base in
  Kuwait and Bahrain again; NASA's Voyager 1 reaches one
  light-day from Earth.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

SHEET_W, SHEET_H = 1024, 1024

# Ink and paper for the whole page. The names describe each colour's
# role; every entry here is used by at least one scene below.
PALETTE = {
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

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font_for(style, size):
    """Fetch one of the three DejaVu faces at the requested point size."""
    faces = {"serif-bold": "DejaVuSerif-Bold.ttf",
             "sans-bold": "DejaVuSans-Bold.ttf",
             "sans": "DejaVuSans.ttf"}
    return ImageFont.truetype(os.path.join(FONT_DIR, faces[style]), size)


def vertical_gradient(canvas, x, y, w, h, top_rgb, bottom_rgb):
    """Paint a box that blends smoothly from one colour to another."""
    for row in range(h):
        blend = row / max(h - 1, 1)
        shade = tuple(round(top_rgb[k] + (bottom_rgb[k] - top_rgb[k]) * blend)
                      for k in range(3))
        canvas.line([(x, y + row), (x + w, y + row)], fill=shade)


def wrap_line(canvas, text, font, width):
    """Greedy word wrap: fit as many words on each line as `width` allows."""
    lines, current = [], ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if canvas.textlength(candidate, font=font) <= width:
            current = candidate
        elif current:
            lines.append(current)
            current = word
        else:
            current = word
    if current:
        lines.append(current)
    return lines


def typeset(canvas, x, y, text, font, color, width, leading):
    """Draw a wrapped paragraph starting at (x, y); return the y below it."""
    for line in wrap_line(canvas, text, font, width):
        canvas.text((x, y), line, font=font, fill=color)
        y += leading
    return y


def star_shape(canvas, cx, cy, outer_r, inner_r, spikes, color):
    """A spiky star centred on (cx, cy), alternating outer/inner radius."""
    corners = []
    for i in range(spikes * 2):
        radius = outer_r if i % 2 == 0 else inner_r
        angle = math.pi * i / spikes - math.pi / 2
        corners.append((cx + radius * math.cos(angle),
                        cy + radius * math.sin(angle)))
    canvas.polygon(corners, fill=color)


def hline(canvas, x0, x1, y, color=None, thick=2):
    """A horizontal rule running from x0 to x1 at height y."""
    canvas.line([(x0, y), (x1, y)], fill=color or PALETTE["rule"], width=thick)


def pennant(canvas, x, y, w, h, country):
    """A small flag on a pole; (x, y) is the top-left corner of the cloth."""
    canvas.line([(x, y), (x, y + h + 26)], fill=(40, 40, 44), width=3)
    pole = x + 3
    if country == "us":
        for i in range(7):
            canvas.rectangle(
                [pole, y + i * h // 7, pole + w, y + (i + 1) * h // 7],
                fill=PALETTE["white"] if i % 2 else PALETTE["red"])
        canvas.rectangle([pole, y, pole + w * 2 // 5, y + h * 4 // 7],
                         fill=(30, 50, 110))
    elif country == "cn":
        canvas.rectangle([pole, y, pole + w, y + h], fill=(222, 40, 30))
        canvas.ellipse([x + 8, y + 5, x + 16, y + 13], fill=PALETTE["yellow"])
    elif country == "ru":
        canvas.rectangle([pole, y, pole + w, y + h // 3], fill=PALETTE["white"])
        canvas.rectangle([pole, y + h // 3, pole + w, y + 2 * h // 3],
                         fill=(30, 80, 180))
        canvas.rectangle([pole, y + 2 * h // 3, pole + w, y + h],
                         fill=(200, 30, 30))


def summit_scene(canvas, x, y, w, h):
    """Shenzhen at dusk: skyline, low sun, three flags in front."""
    vertical_gradient(canvas, x, y, w, h, (24, 32, 66), (214, 120, 70))
    canvas.ellipse([x + w - 90, y + 12, x + w - 40, y + 62],
                   fill=(245, 196, 60))
    towers = [60, 96, 74, 120, 84, 104, 68, 92, 56, 110, 78, 88]
    slot = w // len(towers)
    for i, tower_h in enumerate(towers):
        left = x + i * slot
        canvas.rectangle([left + 2, y + h - tower_h, left + slot - 2, y + h],
                         fill=(28, 26, 48))
        for wy in range(y + h - tower_h + 8, y + h - 8, 12):
            for wx in range(left + 7, left + slot - 8, 12):
                if (wx * 7 + wy * 3) % 26 < 12:
                    canvas.rectangle([wx, wy, wx + 3, wy + 4],
                                     fill=(250, 210, 90))
    canvas.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 20, 34))
    pennant(canvas, x + 60, y + h - 92, 52, 34, "us")
    pennant(canvas, x + w // 2 - 26, y + h - 92, 52, 34, "cn")
    pennant(canvas, x + w - 112, y + h - 92, 52, 34, "ru")
    canvas.text((x + 12, y + 10), "SHENZHEN  —  APEC SUMMIT",
                font=font_for("sans-bold", 17), fill=PALETTE["white"])


def court_scene(canvas, x, y, w, h):
    """A classical court house: pediment, columns, steps."""
    vertical_gradient(canvas, x, y, w, h, (200, 214, 226), (168, 186, 200))
    canvas.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 128, 136))
    left, right = x + 60, x + w - 60
    canvas.rectangle([left, y + 34, right, y + h - 22], fill=(226, 220, 204))
    canvas.polygon([(left - 12, y + 36), (right + 12, y + 36),
                    ((left + right) // 2, y + 8)], fill=(206, 198, 178))
    canvas.ellipse([(left + right) // 2 - 10, y + 18,
                    (left + right) // 2 + 10, y + 34], fill=(150, 130, 90))
    centres = [left + 30 + i * (right - left - 60) // 4 for i in range(5)]
    for cx in centres:
        canvas.rectangle([cx - 9, y + 40, cx + 9, y + h - 30],
                         fill=(246, 242, 228))
        canvas.rectangle([cx - 13, y + 36, cx + 13, y + 42],
                         fill=(236, 230, 212))
        canvas.rectangle([cx - 13, y + h - 34, cx + 13, y + h - 28],
                         fill=(236, 230, 212))
    canvas.rectangle([left + 60, y + h - 28, right - 60, y + h - 22],
                     fill=(90, 70, 50))
    for i in range(3):
        canvas.rectangle([x + 24 + i * 8, y + h - 22, x + w - 24 - i * 8,
                          y + h - 18 + i * 4], fill=(150, 148, 140))


def vice_scene(canvas, x, y, w, h):
    """Vice City at night: neon skyline, pink sun, palms."""
    vertical_gradient(canvas, x, y, w, h, (28, 8, 52), (150, 40, 110))
    canvas.ellipse([x + w // 2 - 26, y + 6, x + w // 2 + 26, y + 58],
                   fill=(255, 110, 170))
    blocks = [30, 48, 38, 58, 44, 52, 34, 46]
    slot = w // len(blocks)
    for i, block_h in enumerate(blocks):
        left = x + i * slot
        canvas.rectangle([left + 2, y + h - block_h, left + slot - 2, y + h],
                         fill=(16, 10, 30))
        for wy in range(y + h - block_h + 6, y + h - 6, 11):
            for wx in range(left + 6, left + slot - 8, 11):
                if (wx + wy) % 20 < 9:
                    canvas.rectangle(
                        [wx, wy, wx + 3, wy + 4],
                        fill=(80, 230, 220) if (wx // 12) % 2
                        else (255, 90, 180))
    for px, lean in [(x + 26, -1), (x + w - 34, 1)]:
        canvas.line([(px, y + h), (px + lean * 10, y + h - 34)],
                    fill=(10, 8, 20), width=5)
        for k in range(5):
            a = math.pi * (0.15 + k * 0.17)
            canvas.arc([px + lean * 10 - 16, y + h - 52,
                        px + lean * 10 + 16, y + h - 20],
                       180 + k * 36, 180 + k * 36 + 40,
                       fill=(10, 8, 20), width=3)


def trend_line(canvas, x, y, w, h):
    """A market line that falls, then rises, ending in an upward arrow."""
    pts = []
    for i in range(10):
        px = x + i * w / 9
        if i <= 5:
            py = y + h * (0.12 + 0.68 * i / 5)
        else:
            py = y + h * (0.80 - 0.62 * (i - 5) / 4)
        pts.append((px, py))
    canvas.line(pts, fill=PALETTE["gold_lt"], width=4, joint="curve")
    tip = pts[-1]
    canvas.polygon([(tip[0], tip[1]), (tip[0] - 16, tip[1] - 2),
                    (tip[0] - 2, tip[1] + 12)], fill=PALETTE["up"])


def header_banner(canvas):
    """Navy masthead with the paper's name, date and a gold rule."""
    canvas.rectangle([0, 0, SHEET_W, 118], fill=PALETTE["navy"])
    canvas.text((SHEET_W // 2, 10), "THE WORLD IN ONE DAY",
                font=font_for("serif-bold", 54), fill=PALETTE["white"],
                anchor="ma")
    canvas.text((SHEET_W // 2, 74), "THURSDAY  ·  19 NOVEMBER 2026",
                font=font_for("sans-bold", 28), fill=PALETTE["gold_lt"],
                anchor="ma")
    hline(canvas, 0, SHEET_W, 118, PALETTE["gold"], 4)


def lead_article(canvas):
    """The Shenzhen summit: big headline, dusk scene, three paragraphs."""
    canvas.text((40, 134), "SHENZHEN  —  THE FIRST TRILATERAL",
                font=font_for("sans-bold", 21), fill=PALETTE["red"])
    canvas.text((40, 160), "TRUMP, XI AND PUTIN",
                font=font_for("sans-bold", 40), fill=PALETTE["ink"])
    canvas.text((40, 202), "MEET IN SHENZHEN",
                font=font_for("sans-bold", 40), fill=PALETTE["ink"])
    summit_scene(canvas, 40, 248, 560, 216)
    col = 624
    y = typeset(canvas, col, 252,
                "The leaders of the US, China and Russia sit down "
                "together for the first time today in Shenzhen, on "
                "the sidelines of APEC.",
                font_for("sans", 19), PALETTE["ink"], 360, 24)
    y = typeset(canvas, col, y + 8,
                "Nuclear arms top the agenda after New START lapsed "
                "in February; the war in Iran is on the table too.",
                font_for("sans", 19), PALETTE["ink"], 360, 24)
    typeset(canvas, col, y + 8,
            "Trump and Putin are also due a one-to-one.",
            font_for("sans", 19), PALETTE["ink"], 360, 24)
    hline(canvas, 40, 984, 480)


def middle_band(canvas):
    """Two stories side by side: The Hague ruling and the GTA VI launch."""
    court_scene(canvas, 40, 494, 452, 74)
    canvas.text((40, 578), "THE HAGUE", font=font_for("sans-bold", 20),
                fill=PALETTE["red"])
    canvas.text((40, 602), "WORLD COURT RULES",
                font=font_for("sans-bold", 26), fill=PALETTE["ink"])
    canvas.text((40, 632), "ON MYANMAR TODAY",
                font=font_for("sans-bold", 26), fill=PALETTE["ink"])
    typeset(canvas, 40, 666,
            "The court rules at 10 a.m. on whether Myanmar committed "
            "genocide against the Rohingya. A guilty verdict would "
            "be a first.",
            font_for("sans", 18), PALETTE["body"], 452, 22)
    vice_scene(canvas, 532, 494, 452, 74)
    canvas.text((532, 578), "VICE CITY  —  GTA VI",
                font=font_for("sans-bold", 20), fill=PALETTE["red"])
    canvas.text((532, 602), "GAMERS ENTER",
                font=font_for("sans-bold", 26), fill=PALETTE["ink"])
    canvas.text((532, 632), "VICE CITY",
                font=font_for("sans-bold", 26), fill=PALETTE["ink"])
    typeset(canvas, 532, 666,
            "Grand Theft Auto VI unlocks at midnight around the "
            "world, 13 years after GTA V. Early reviews give it 99 "
            "on Metacritic; pre-sales near $1.5bn.", font_for("sans", 18),
            PALETTE["body"], 452, 22)
    hline(canvas, 40, 984, 732)


def markets_band(canvas):
    """The navy markets strip: split indices, the trend line, the numbers."""
    canvas.rectangle([0, 742, SHEET_W, 832], fill=PALETTE["navy"])
    canvas.text((40, 754), "MARKETS SPLIT",
                font=font_for("sans-bold", 26), fill=PALETTE["gold_lt"])
    trend_line(canvas, 330, 752, 180, 66)
    canvas.text((530, 754),
                "Dow −1.1% · S&P −0.2% · Nasdaq +0.4%",
                font=font_for("sans-bold", 20), fill=PALETTE["white"])
    canvas.text((530, 788),
                "Brent −1.3% to $91.95  ·  Gold −2.5% to $3,753",
                font=font_for("sans", 19), fill=PALETTE["pale"])
    canvas.text((40, 782), "Fed minutes point to more hikes",
                font=font_for("sans", 19), fill=PALETTE["pale"])


def briefs_band(canvas):
    """Four short news briefs in a row, each with a coloured kicker bar."""
    items = [
        ("WASHINGTON", PALETTE["red"],
         "Democrats nominate Jeffries for Speaker, 251–11"),
        ("ANTHROPIC IPO", (14, 90, 60),
         "Prices its shares at $83; $81bn raise, trades today"),
        ("CYCLONE AKVAN", (90, 60, 120),
         "Severe storm nears India's east coast; landfall Friday"),
        ("BRUSSELS", (120, 70, 20),
         "EU offers Kyiv €45bn, repaid once Russia pays up"),
    ]
    cx = 40
    for kicker, accent, headline in items:
        canvas.rectangle([cx, 844, cx + 226, 850], fill=accent)
        canvas.text((cx, 860), kicker, font=font_for("sans-bold", 17),
                    fill=accent)
        typeset(canvas, cx, 884, headline, font_for("sans-bold", 20),
                PALETTE["ink"], 226, 25)
        cx += 238
    hline(canvas, 40, 984, 972)


def foot_line(canvas):
    """One centred line of further headlines along the bottom edge."""
    canvas.text((SHEET_W // 2, 984),
                "ALSO: Nvidia's Huang quits  ·  Iran widens attacks on Gulf "
                "states  ·  Voyager 1 reaches a light-day from Earth",
                font=font_for("sans", 16), fill=PALETTE["gray"], anchor="ma")


def render_page():
    """Compose every band onto the sheet and save the finished PNG."""
    img = Image.new("RGB", (SHEET_W, SHEET_H), PALETTE["paper"])
    canvas = ImageDraw.Draw(img)
    header_banner(canvas)
    lead_article(canvas)
    middle_band(canvas)
    markets_band(canvas)
    briefs_band(canvas)
    foot_line(canvas)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render_page()
