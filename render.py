"""Draw the news-image-20261117 entry: a one-page broadsheet of the world
news of Tuesday, 17 November 2026.

Renders at 3x and downscales with LANCZOS (pil_image_craft). Pure Pillow
vector drawing: no photos, no raster assets. Deterministic: no time, no
unseeded random. Writes news.png next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

S = 3  # supersample factor
W, H = 1024, 1024
G = 12  # gutter between panels
HERE = os.path.dirname(os.path.abspath(__file__))

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (246, 241, 227)
NAVY = (22, 35, 63)
NAVY_DK = (15, 25, 46)
INK = (27, 27, 27)
RED = (179, 39, 30)
GOLD = (217, 164, 65)
CREAM = (255, 251, 238)
GREY = (120, 118, 110)
SUB = (214, 220, 232)


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def sc(v):
    return int(round(v * S))


def xy(x, y):
    return (sc(x), sc(y))


def rect(d, box, fill=None, outline=None, width=1):
    d.rectangle([sc(box[0]), sc(box[1]), sc(box[2]), sc(box[3])],
                fill=fill, outline=outline, width=sc(width))


def ellipse(d, box, fill=None, outline=None, width=1):
    d.ellipse([sc(box[0]), sc(box[1]), sc(box[2]), sc(box[3])],
              fill=fill, outline=outline, width=sc(width))


def poly(d, points, fill=None, outline=None):
    d.polygon([(sc(x), sc(y)) for x, y in points], fill=fill, outline=outline)


def line(d, points, fill, width=1):
    d.line([(sc(x), sc(y)) for x, y in points], fill=fill, width=sc(width))


def wrap(d, text, fnt, max_w):
    """Greedy word wrap to max_w (final px)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= sc(max_w):
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(d, path, size, text, max_w, min_size=18):
    """Largest font size <= size that fits text on one line, else min."""
    s = size
    while s > min_size:
        f = font(path, s)
        if d.textlength(text, font=f) <= sc(max_w):
            return f
        s -= 1
    return font(path, min_size)


def text(d, pos, s, fnt, fill):
    d.text(xy(*pos), s, font=fnt, fill=fill)


def spaced_text(d, pos, s, fnt, fill, tracking=6):
    """Draw text with extra tracking (final px between glyphs)."""
    x, y = pos
    for ch in s:
        d.text(xy(x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) / S + tracking


# ---------------------------------------------------------------- art
def draw_kerch(d, box):
    """Kerch Bridge hero art. Local coords: 992 x 292; the navy caption band
    covers local y 192..292, so the visible scene is y 0..192."""
    import math
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (sc(w), sc(h)))
    td = ImageDraw.Draw(tmp)
    # dusk sky
    for i in range(sc(150)):
        t = i / max(1, sc(150) - 1)
        c = tuple(int((38, 52, 90)[k] + ((226, 138, 62)[k] - (38, 52, 90)[k]) * t)
                  for k in range(3))
        td.line([(0, i), (sc(w), i)], fill=c)
    # small low sun, upper right
    td.ellipse([sc(845), sc(28), sc(905), sc(88)], fill=(244, 196, 120))
    td.ellipse([sc(860), sc(43), sc(890), sc(73)], fill=(252, 222, 160))
    # sea
    td.rectangle([0, sc(146), sc(w), sc(h)], fill=(24, 58, 84))
    for wy in (158, 172, 184):
        td.line([(sc(20), sc(wy)), (sc(w - 20), sc(wy))],
                fill=(70, 118, 148), width=sc(2))
    # smoke rising from the gap
    for cx, cy, r in ((478, 58, 24), (508, 38, 28), (542, 62, 20), (520, 18, 16)):
        td.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                   fill=(150, 145, 140))
    # explosion glow at the gap
    for r, col in ((36, (255, 130, 30)), (24, (255, 180, 60)), (13, (255, 225, 140))):
        td.ellipse([sc(500 - r), sc(128 - r), sc(500 + r), sc(128 + r)], fill=col)
    td.polygon([(sc(492), sc(96)), (sc(500), sc(70)), (sc(508), sc(96))],
               fill=(255, 180, 60))
    # bridge deck: two spans with a gap in the middle
    deck_y = 128
    td.rectangle([sc(20), sc(deck_y), sc(428), sc(deck_y + 18)],
                 fill=(112, 119, 132))
    td.rectangle([sc(572), sc(deck_y), sc(w - 20), sc(deck_y + 18)],
                 fill=(112, 119, 132))
    for dx in range(40, 420, 34):
        td.rectangle([sc(dx), sc(deck_y + 7), sc(dx + 18), sc(deck_y + 10)],
                     fill=(240, 240, 230))
    for dx in range(592, 950, 34):
        td.rectangle([sc(dx), sc(deck_y + 7), sc(dx + 18), sc(deck_y + 10)],
                     fill=(240, 240, 230))
    # support pillars down into the water
    for px in (110, 320, 680, 900):
        td.rectangle([sc(px), sc(deck_y + 18), sc(px + 16), sc(192)],
                     fill=(86, 92, 104))
    # intact steel arch over the left span
    td.arc([sc(150), sc(10), sc(430), sc(246)], start=180, end=360,
           fill=(158, 166, 180), width=sc(12))
    # fallen arch: same curve, rotated 25 degrees, plunging into the water
    cx, cy, rx, ry = 525, 170, 85, 55
    pts = []
    for deg in range(200, 341, 6):
        a = math.radians(deg)
        x = cx + rx * math.cos(a)
        y = cy + ry * math.sin(a)
        ang = math.radians(25)
        xr = cx + (x - cx) * math.cos(ang) - (y - cy) * math.sin(ang)
        yr = cy + (x - cx) * math.sin(ang) + (y - cy) * math.cos(ang)
        pts.append((sc(xr), sc(yr)))
    td.line(pts, fill=(158, 166, 180), width=sc(12), joint="curve")
    # tilted deck fragment in the gap + splash
    td.polygon([(sc(452), sc(140)), (sc(516), sc(130)), (sc(538), sc(148)),
                (sc(476), sc(158))], fill=(96, 102, 114))
    td.ellipse([sc(462), sc(168), sc(566), sc(192)], fill=(150, 190, 215))
    td.ellipse([sc(486), sc(176), sc(542), sc(192)], fill=(200, 225, 240))
    d._image.paste(tmp, (sc(x0), sc(y0)))


def draw_hormuz(d, box):
    """Burning tanker in the Strait of Hormuz. Local coords: 490 x 100."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (sc(w), sc(h)))
    td = ImageDraw.Draw(tmp)
    for i in range(sc(h)):
        t = i / max(1, sc(h) - 1)
        c = tuple(int((232, 154, 74)[k] + ((138, 58, 34)[k] - (232, 154, 74)[k]) * t)
                  for k in range(3))
        td.line([(0, i), (sc(w), i)], fill=c)
    # sea, lighter so the dark hull reads
    td.rectangle([0, sc(60), sc(w), sc(h)], fill=(30, 74, 94))
    for wy in (72, 84, 94):
        td.line([(sc(10), sc(wy)), (sc(w - 10), sc(wy))],
                fill=(90, 150, 175), width=sc(2))
    # tanker: big hull sitting in the water, bow to the right
    td.polygon([(sc(28), sc(62)), (sc(28), sc(86)), (sc(330), sc(86)),
                (sc(362), sc(62)), (sc(28), sc(62))], fill=(38, 44, 52))
    td.rectangle([sc(28), sc(62), sc(362), sc(68)], fill=(150, 52, 40))
    # superstructure + funnel
    td.rectangle([sc(268), sc(30), sc(332), sc(62)], fill=(48, 54, 62))
    for wx in range(276, 326, 14):
        td.rectangle([sc(wx), sc(38), sc(wx + 8), sc(44)], fill=(190, 205, 215))
    td.rectangle([sc(96), sc(40), sc(118), sc(62)], fill=(150, 52, 40))
    # fire on the deck amidships, flames rising from the hull
    for cx, cy, r, col in ((190, 56, 26, (255, 120, 30)), (212, 48, 20, (255, 180, 60)),
                           (168, 50, 15, (255, 200, 90)), (228, 56, 12, (255, 90, 20))):
        td.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)], fill=col)
    td.polygon([(sc(182), sc(58)), (sc(196), sc(22)), (sc(210), sc(58))],
               fill=(255, 200, 90))
    # smoke above the fire
    for cx, cy, r in ((196, 14, 16), (216, 6, 12), (172, 10, 11)):
        td.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)], fill=(52, 50, 52))
    # naval mine, big and spiky, in the foreground water
    import math
    mx, my = 428, 80
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        td.line([(sc(mx + 13 * math.cos(a)), sc(my + 13 * math.sin(a))),
                 (sc(mx + 23 * math.cos(a)), sc(my + 23 * math.sin(a)))],
                fill=(200, 200, 200), width=sc(3))
    td.ellipse([sc(mx - 14), sc(my - 14), sc(mx + 14), sc(my + 14)],
               fill=(16, 16, 18), outline=(120, 120, 120), width=sc(2))
    d._image.paste(tmp, (sc(x0), sc(y0)))


def draw_manila(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (sc(w), sc(h)))
    td = ImageDraw.Draw(tmp)
    for i in range(sc(h)):
        t = i / max(1, sc(h) - 1)
        c = tuple(int((127, 178, 224)[k] + ((226, 238, 246)[k] - (127, 178, 224)[k]) * t)
                  for k in range(3))
        td.line([(0, i), (sc(w), i)], fill=c)
    # clouds
    for cx, cy, r in ((90, 18, 22), (130, 24, 16), (380, 14, 18), (410, 20, 13)):
        td.ellipse([sc(cx - r), sc(cy - r // 2), sc(cx + r), sc(cy + r // 2)],
                   fill=(255, 255, 255))
    # skyline
    for bx, bw, bh in ((0, 46, 30), (52, 34, 44), (92, 52, 26), (300, 40, 36),
                       (346, 30, 48), (382, 56, 28), (444, 46, 40)):
        td.rectangle([sc(bx), sc(h - bh), sc(bx + bw), sc(h)], fill=(90, 107, 132))
    # plane
    td.ellipse([sc(150), sc(38), sc(330), sc(62)], fill=(250, 250, 248))
    td.polygon([(sc(300), sc(40)), (sc(350), sc(28)), (sc(360), sc(34)),
                (sc(315), sc(50))], fill=(220, 226, 232))
    td.polygon([(sc(210), sc(58)), (sc(250), sc(78)), (sc(265), sc(74)),
                (sc(235), sc(58))], fill=(220, 226, 232))
    td.polygon([(sc(160), sc(44)), (sc(150), sc(22)), (sc(168), sc(20)),
                (sc(180), sc(42))], fill=(200, 208, 216))
    for wx in range(180, 320, 22):
        td.rectangle([sc(wx), sc(46), sc(wx + 10), sc(50)], fill=(90, 120, 160))
    # three flag poles with simple flags
    for fx, cols in ((60, [(179, 39, 30), (255, 255, 255), (179, 39, 30)]),
                     (100, [(0, 56, 168), (255, 255, 255), (206, 17, 38)]),
                     (140, [(255, 205, 0), (0, 56, 168), (206, 17, 38)])):
        td.line([(sc(fx), sc(58)), (sc(fx), sc(h - 6))], fill=(60, 60, 60), width=sc(2))
        for j, col in enumerate(cols):
            td.rectangle([sc(fx + 2), sc(58 + j * 7), sc(fx + 26), sc(58 + (j + 1) * 7)],
                         fill=col)
    d._image.paste(tmp, (sc(x0), sc(y0)))


def draw_nvidia(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (sc(w), sc(h)))
    td = ImageDraw.Draw(tmp)
    td.rectangle([0, 0, sc(w), sc(h)], fill=(8, 26, 18))
    # circuit traces
    import random
    rng = random.Random(17112026)
    for _ in range(26):
        x = rng.randint(0, w)
        y = rng.randint(0, h)
        ln = rng.randint(18, 60)
        td.line([(sc(x), sc(y)), (sc(x + ln), sc(y))], fill=(34, 120, 70), width=sc(2))
        td.ellipse([sc(x + ln - 3), sc(y - 3), sc(x + ln + 3), sc(y + 3)],
                   fill=(60, 190, 110))
    # glow behind chip
    td.ellipse([sc(150), sc(-10), sc(340), sc(110)], fill=(20, 90, 55))
    # chip
    cx0, cy0, cx1, cy1 = 185, 18, 305, 82
    for px in range(cx0, cx1, 16):
        td.rectangle([sc(px), sc(cy0 - 8), sc(px + 7), sc(cy0)], fill=(217, 164, 65))
        td.rectangle([sc(px), sc(cy1), sc(px + 7), sc(cy1 + 8)], fill=(217, 164, 65))
    for py in range(cy0, cy1, 16):
        td.rectangle([sc(cx0 - 8), sc(py), sc(cx0), sc(py + 7)], fill=(217, 164, 65))
        td.rectangle([sc(cx1), sc(py), sc(cx1 + 8), sc(py + 7)], fill=(217, 164, 65))
    td.rounded_rectangle([sc(cx0), sc(cy0), sc(cx1), sc(cy1)], radius=sc(8),
                         fill=(28, 92, 58), outline=(120, 220, 160), width=sc(2))
    td.rounded_rectangle([sc(cx0 + 14), sc(cy0 + 12), sc(cx1 - 14), sc(cy1 - 12)],
                         radius=sc(5), fill=(16, 60, 38))
    f = ImageFont.truetype(SANS_B, sc(20))
    lbl = "NVDA"
    tw = td.textlength(lbl, font=f)
    td.text((sc((cx0 + cx1) / 2) - tw / 2, sc(38)), lbl, font=f, fill=(255, 255, 255))
    d._image.paste(tmp, (sc(x0), sc(y0)))


def draw_ebola(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (sc(w), sc(h)))
    td = ImageDraw.Draw(tmp)
    for i in range(sc(h)):
        t = i / max(1, sc(h) - 1)
        c = tuple(int((94, 20, 32)[k] + ((42, 10, 18)[k] - (94, 20, 32)[k]) * t)
                  for k in range(3))
        td.line([(0, i), (sc(w), i)], fill=c)
    # virus particles: spiked circles
    import math
    for cx, cy, r in ((70, 34, 20), (150, 22, 13), (210, 40, 16), (330, 26, 12),
                      (400, 44, 18), (455, 24, 11)):
        for ang in range(0, 360, 30):
            a = math.radians(ang)
            td.line([(sc(cx + r * 0.8 * math.cos(a)), sc(cy + r * 0.8 * math.sin(a))),
                     (sc(cx + r * 1.35 * math.cos(a)), sc(cy + r * 1.35 * math.sin(a)))],
                    fill=(216, 90, 80), width=sc(2))
        td.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                   fill=(192, 57, 43), outline=(230, 120, 105), width=sc(2))
    # medical cross in a white ring, right side
    cx, cy = 405, 50
    td.ellipse([sc(cx - 34), sc(cy - 34), sc(cx + 34), sc(cy + 34)],
               fill=(246, 241, 227))
    td.rectangle([sc(cx - 7), sc(cy - 20), sc(cx + 7), sc(cy + 20)], fill=(179, 39, 30))
    td.rectangle([sc(cx - 20), sc(cy - 7), sc(cx + 20), sc(cy + 7)], fill=(179, 39, 30))
    # dotted spread trail
    for i, (dx, dy) in enumerate(((250, 70), (280, 78), (312, 72), (344, 80), (372, 74))):
        td.ellipse([sc(dx - 4), sc(dy - 4), sc(dx + 4), sc(dy + 4)], fill=(230, 120, 105))
    d._image.paste(tmp, (sc(x0), sc(y0)))


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (sc(W), sc(H)), PAPER)
    d = ImageDraw.Draw(img)
    # expose the canvas to art helpers via d._image (Pillow Draw keeps .im, not
    # the Image; attach it so paste() works)
    d._image = img

    # masthead
    rect(d, (0, 0, W, 146), fill=NAVY)
    rect(d, (0, 140, W, 146), fill=RED)
    kicker = "THE WORLD IN ONE DAY"
    kf = font(SANS_B, 23)
    kw = sum(d.textlength(ch, font=kf) / S + 6 for ch in kicker) - 6
    spaced_text(d, ((W - kw) / 2, 16), kicker, kf, (168, 180, 200), tracking=6)
    df = fit_font(d, SERIF_B, 58, "TUESDAY, 17 NOVEMBER 2026", W - 32, min_size=40)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dw = d.textlength(date, font=df) / S
    text(d, ((W - dw) / 2, 52), date, df, (255, 255, 255))

    # hero
    hero = (16, 158, 1008, 450)
    draw_kerch(d, hero)
    rect(d, (hero[0], 350, hero[2], hero[3]), fill=NAVY)
    hf = font(SANS_B, 37)
    head = "UKRAINE CUTS THE KERCH BRIDGE"
    text(d, (30, 360), head, hf, (255, 255, 255))
    sf = font(SANS, 20)
    sub = ("The road arch falls into the strait on a second night of strikes; "
           "the rail span is damaged too. Russia hits Kyiv's bridges in reply.")
    lines = wrap(d, sub, sf, 948)
    y = 404
    for ln in lines[:2]:
        text(d, (30, y), ln, sf, SUB)
        y += 24

    # grid 2 x 2
    panels = [
        ("TANKERS ABLAZE IN HORMUZ",
         "Iran says a fourth tanker hit a mine in 24 hours; UK maritime "
         "agency confirms attacks.", draw_hormuz),
        ("TRUMP LANDS IN MANILA",
         "ASEAN and Quad open his Asia tour; a Xi-Trump-Putin meeting is set "
         "for Thursday in Shenzhen.", draw_manila),
        ("NVIDIA BEATS THE STREET",
         "$115.8bn revenue in first results since Huang's exit; new "
         "national-security committee.", draw_nvidia),
        ("EBOLA 'STILL NOT UNDER CONTROL'",
         "DR Congo toll passes 5,500 dead and 11,200 cases, Africa CDC warns.",
         draw_ebola),
    ]
    gx, gy = 16, 462
    pw, ph = 490, 186
    for i, (head, sub, art) in enumerate(panels):
        px = gx + (i % 2) * (pw + G)
        py = gy + (i // 2) * (ph + G)
        art(d, (px, py, px + pw, py + 100))
        rect(d, (px, py + 100, px + pw, py + ph), fill=NAVY)
        hf2 = fit_font(d, SANS_B, 25, head, pw - 28)
        text(d, (px + 14, py + 108), head, hf2, (255, 255, 255))
        sf2 = font(SANS, 16.5)
        lines = wrap(d, sub, sf2, pw - 28)
        y = py + 140
        for ln in lines[:2]:
            text(d, (px + 14, y), ln, sf2, SUB)
            y += 20

    # ticker strip
    ty = 858
    rect(d, (16, ty, 1008, ty + 88), fill=CREAM, outline=NAVY, width=2)
    rect(d, (16, ty, 22, ty + 88), fill=RED)
    tf = font(SANS_B, 20)
    text(d, (36, ty + 12), "ALSO TODAY", tf, RED)
    tick = [
        "BAHRAIN \u2014 Iran drones target a U.S. radar base; U.S. says all "
        "intercepted, no damage.",
        "JPMORGAN \u2014 A software bug slows U.S. banking and Zelle; the "
        "bank says no cyberattack.",
    ]
    y = ty + 36
    for item in tick:
        f = fit_font(d, SANS, 18, item, 956, min_size=15)
        text(d, (36, y), item, f, INK)
        y += 24

    # footer
    ff = font(SANS, 15)
    foot = ("Every story above is an event of Tuesday, 17 November 2026, "
            "as reported that day.")
    fw = d.textlength(foot, font=ff) / S
    text(d, ((W - fw) / 2, 966), foot, ff, GREY)

    out = img.resize((W, H), Image.LANCZOS)
    out.save(os.path.join(HERE, "news.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    build()
    print("wrote", os.path.join(HERE, "news.png"))
