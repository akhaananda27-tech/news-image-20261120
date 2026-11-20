#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Friday 20 November 2026.

Every story is a real story reported on that day. Text is rendered with
PIL so no letter is ever garbled. Output: entry.png, 1024x1024.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (24, 64, 128)
GREY = (110, 110, 108)
LIGHT = (232, 230, 222)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    """Greedy word wrap, returns list of lines that fit `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, width, fill=INK, leading=None):
    """Draw wrapped paragraph, return y after last line."""
    lh = leading or int(f.size * 1.32)
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def rule(d, x0, x1, y, w=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(d, x, y, text, size=15):
    f = font(SANS_B, size)
    d.text((x, y), text, font=f, fill=RED)
    return y + size + 8


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 30  # margin
R = W - M

# ---------------------------------------------------------------- masthead
rule(d, M, R, 22, 3)
d.text((W // 2, 34), "THE WORLD TODAY", font=font(SERIF_B, 68),
       fill=INK, anchor="ma")
d.text((W // 2, 112), "FRIDAY 20 NOVEMBER 2026",
       font=font(SANS_B, 27), fill=RED, anchor="ma")
d.text((W // 2, 146), "12 STORIES  ·  5 REGIONS  ·  ONE DAY, ONE PAGE",
       font=font(SANS, 14), fill=GREY, anchor="ma")
rule(d, M, R, 172, 2)
rule(d, M, R, 177, 1)

# ---------------------------------------------------------------- lead story
y = 192
x = M
y = kicker(d, x, y, "UKRAINE  ·  WAR", 16)
head = "KYIV BRIDGES HIT IN RUSSIA'S BIGGEST BARRAGE OF THE YEAR"
y = para(d, x, y, head, font(SERIF_B, 32), 590, leading=39)
y += 4
deck = ("More than 110 missiles and 400 drones rained down overnight. "
        "Three bridges over the Dnipro were damaged, cutting links across "
        "the capital. At least nine people were killed and 28 hurt \u2014 "
        "hours after Putin met Trump and Xi in Shenzhen.")
y = para(d, x, y, deck, font(SERIF, 15), 590, leading=21)

# lead illustration: bridge over the Dnipro, blast above the deck
ix0, iy0, ix1, iy1 = 648, 196, R, 392
d.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=2)
d.rectangle([ix0, iy0, ix1, iy0 + 118], fill=(214, 228, 240))       # sky
d.rectangle([ix0, iy0 + 118, ix1, iy1], fill=(126, 164, 196))       # river
# sun haze
d.ellipse([ix0 + 24, iy0 + 18, ix0 + 66, iy0 + 60], fill=(240, 214, 130))
# bridge towers and deck
for tx in (ix0 + 78, ix0 + 218):
    d.rectangle([tx, iy0 + 46, tx + 12, iy0 + 150], fill=INK)
d.line([(ix0 + 84, iy0 + 52), (ix0 + 224, iy0 + 128)], fill=INK, width=2)
d.line([(ix0 + 224, iy0 + 52), (ix0 + 84, iy0 + 128)], fill=INK, width=2)
d.rectangle([ix0 + 8, iy0 + 128, ix1 - 8, iy0 + 140], fill=INK)      # deck
d.rectangle([ix0 + 8, iy0 + 140, ix1 - 8, iy0 + 146], fill=(90, 90, 90))
# blast starburst above the deck
cx, cy = ix0 + 250, iy0 + 84
for ang in range(0, 360, 30):
    import math
    a = math.radians(ang)
    d.line([(cx, cy), (cx + 46 * math.cos(a), cy + 46 * math.sin(a))],
           fill=(214, 90, 20), width=5)
d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(230, 120, 30))
d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(250, 200, 60))
# smoke
d.ellipse([cx - 66, cy - 58, cx - 26, cy - 18], fill=(120, 120, 120))
d.ellipse([cx - 52, cy - 72, cx - 18, cy - 38], fill=(150, 150, 150))
# caption
d.text((ix0, iy1 + 8), "Three Dnipro bridges damaged; traffic halted.",
       font=font(SANS, 12), fill=GREY)

rule(d, M, R, 434, 2)

# ---------------------------------------------------------------- row 2: two columns
def story2(x0, x1, y0, kick, head, body, icon):
    y = y0
    y = kicker(d, x0, y, kick, 14)
    y = para(d, x0, y, head, font(SERIF_B, 23), x1 - x0 - 78, leading=28)
    y += 3
    y = para(d, x0, y, body, font(SERIF, 14), x1 - x0, leading=19)
    icon(x1 - 66, y0 + 26)
    return y


def icon_cyclone(cx, cy):
    # spiral storm with rain
    import math
    for i in range(5):
        r = 7 + i * 5
        d.arc([cx - r, cy - r, cx + r, cy + r], 20 + i * 45, 230 + i * 45,
              fill=BLUE if i % 2 == 0 else (60, 120, 170), width=4)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=BLUE)
    for dx in (-26, 0, 26):
        d.line([(cx + dx, cy + 32), (cx + dx - 4, cy + 44)], fill=BLUE, width=3)


def icon_flags(cx, cy):
    # US / Russia / China mini flags side by side
    fw, fh = 20, 14
    # US: stripes + canton
    for i in range(7):
        d.rectangle([cx - 34, cy - 18 + i * 2, cx - 14, cy - 16 + i * 2],
                    fill=RED if i % 2 == 0 else PAPER)
    d.rectangle([cx - 34, cy - 18, cx - 24, cy - 8], fill=BLUE)
    # Russia: white-blue-red
    for i, c in enumerate((PAPER, BLUE, RED)):
        d.rectangle([cx - 8, cy - 18 + i * 5, cx + 12, cy - 13 + i * 5], fill=c)
    d.rectangle([cx - 8, cy - 18, cx + 12, cy - 3], outline=INK, width=1)
    # China: red + stars
    d.rectangle([cx + 18, cy - 18, cx + 38, cy - 3], fill=RED)
    d.text((cx + 20, cy - 17), "\u2605", font=font(SANS_B, 9), fill=(250, 220, 60))


y2 = story2(M, 497, 450, "INDIA  ·  WEATHER",
             "CYCLONE AKVAN MAKES LANDFALL",
             "The storm crossed the Odisha coast near Gopalpur with winds "
             "of 70\u201380 km/h \u2014 India's third cyclone in under a "
             "month. Heavy rain followed; no deaths reported so far.",
             icon_cyclone)
y2b = story2(527, R, 450, "CHINA  ·  DIPLOMACY",
              "TRUMP, PUTIN AND XI MEET IN SHENZHEN",
              "The first three-way summit of the US, Russian and Chinese "
              "leaders ends with a four-point peace declaration \u2014 but "
              "no breakthrough on Ukraine. Trump calls Putin \u201cmy friend\u201d.",
              icon_flags)
rule(d, M, R, 622, 2)

# ---------------------------------------------------------------- row 3: three columns
def story3(x0, x1, y0, kick, head, body, icon):
    y = y0
    y = kicker(d, x0, y, kick, 13)
    y = para(d, x0, y, head, font(SERIF_B, 20), x1 - x0, leading=24)
    y += 3
    y = para(d, x0, y, body, font(SERIF, 13.5), x1 - x0, leading=18)
    icon(x1 - 40, y0 + 22)
    return y


def icon_chart(cx, cy):
    pts = [(cx - 34, cy - 22), (cx - 18, cy - 26), (cx - 6, cy - 12),
           (cx + 8, cy - 16), (cx + 20, cy + 2), (cx + 34, cy + 16)]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.line([(cx + 26, cy + 16), (cx + 34, cy + 16)], fill=RED, width=4)
    d.line([(cx + 34, cy + 8), (cx + 34, cy + 16)], fill=RED, width=4)


def icon_eu_uk(cx, cy):
    # EU circle of stars + UK cross, simplified
    d.ellipse([cx - 34, cy - 18, cx - 2, cy + 14], fill=BLUE)
    for i in range(8):
        import math
        a = math.radians(i * 45)
        sx, sy = cx - 18 + 11 * math.cos(a), cy - 2 + 11 * math.sin(a)
        d.text((sx - 3, sy - 5), "\u2605", font=font(SANS_B, 7), fill=(250, 220, 60))
    d.rectangle([cx + 6, cy - 16, cx + 34, cy + 12], fill=(30, 60, 140))
    d.line([(cx + 6, cy - 16), (cx + 34, cy + 12)], fill=PAPER, width=3)
    d.line([(cx + 34, cy - 16), (cx + 6, cy + 12)], fill=PAPER, width=3)
    d.line([(cx + 20, cy - 16), (cx + 20, cy + 12)], fill=RED, width=4)
    d.line([(cx + 6, cy - 2), (cx + 34, cy - 2)], fill=RED, width=4)


def icon_thermo(cx, cy):
    d.rounded_rectangle([cx - 6, cy - 22, cx + 6, cy + 8], radius=6,
                        outline=INK, width=2, fill=PAPER)
    d.rectangle([cx - 3, cy - 8, cx + 3, cy + 6], fill=RED)
    d.ellipse([cx - 10, cy + 2, cx + 10, cy + 22], fill=RED, outline=INK, width=2)


c3 = (R - M - 2 * 24) // 3
x3a, x3b, x3c = M, M + c3 + 24, M + 2 * (c3 + 24)
story3(x3a, x3a + c3, 638, "MARKETS",
       "ASIA'S AI SELL-OFF DEEPENS",
       "Nikkei falls 5%, Taiwan heads for its worst week since 1990 and "
       "the Kospi drops 5.7% as doubts grow over AI spending. Anthropic's "
       "record $81bn IPO cannot stop the slide.",
       icon_chart)
story3(x3b, x3b + c3, 638, "EUROPE",
       "UK AND EU STRIKE POST-BREXIT DEAL",
       "At a Brussels summit the two sides agree to ease food trade, let "
       "100,000 young people a year live and work across the Channel, and "
       "link their carbon markets from 2028.",
       icon_eu_uk)
story3(x3c, x3c + c3, 638, "CLIMATE  ·  COP31",
       "COP31 ENDS IN DEADLOCK",
       "On the final day in Antalya, the draft deal drops every mention of "
       "fossil fuels \u2014 and the $120bn adaptation figure. Nearly 200 "
       "countries face talks running into the weekend.",
       icon_thermo)
rule(d, M, R, 830, 2)

# ---------------------------------------------------------------- also today
y = 846
d.text((M, y), "ALSO TODAY", font=font(SANS_B, 16), fill=INK)
y += 28
briefs = [
    ("POLAND", "A Russian missile crosses into NATO airspace; jets "
     "scrambled. Warsaw calls it a provocation."),
    ("THE HAGUE", "Myanmar rejects the world court's ruling that it "
     "committed genocide against the Rohingya."),
    ("RIYADH", "A Houthi missile damages the Saudi wealth fund's tower, "
     "the capital's tallest building."),
    ("GAZA", "Israel ends its largest tank raid since the October 2025 "
     "ceasefire."),
    ("NEW YORK", "The S&P 500 falls for a sixth straight day; gold and "
     "silver hit one-year lows."),
    ("LVIV", "Strikes hit Ukraine's west too: two killed, a railway "
     "station left cratered."),
]
col_w = (R - M - 24) // 2
by = y
for i, (tag, txt) in enumerate(briefs):
    bx = M if i % 2 == 0 else M + col_w + 24
    brow = i // 2
    yy = by + brow * 42
    d.rectangle([bx, yy + 2, bx + 8, yy + 10], fill=RED)
    d.text((bx + 14, yy), tag + " \u2014 ",
           font=font(SANS_B, 13), fill=INK)
    tw = d.textlength(tag + " \u2014  ", font=font(SANS_B, 13))
    para(d, bx + 14 + tw, yy, txt, font(SERIF, 13),
         col_w - 14 - tw, leading=17)

# ---------------------------------------------------------------- footer
rule(d, M, R, 998, 1, fill=GREY)
d.text((W // 2, 1004),
       "THE WORLD TODAY  ·  FRIDAY 20 NOVEMBER 2026  ·  EVERY STORY AS REPORTED ON THE DAY",
       font=font(SANS, 11), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
