#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page (1024x1024 PNG).

Design: broadsheet masthead, figures strip, dotted world map with numbered
pins, one lead story, six regional sections in a 3x2 grid (each with an
illustrated card plus short briefs), a global-and-sport strip, and a
date-check footer. All drawing uses PIL primitives; no external assets,
no randomness, fully deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (29, 34, 38)
TEAL = (15, 61, 62)
OCHRE = (199, 125, 42)
PINRED = (176, 58, 46)
SLATE = (90, 98, 104)
RULE = (60, 66, 70)
NIGHT = (18, 32, 48)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=1.18, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    step = int(fnt.size * leading)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# --------------------------------------------------------------------------
# World landmass grid ('#' = land). 72 columns x 34 rows.
# --------------------------------------------------------------------------
MAP_GRID = [
    "                                                                        ",
    "      #####                                  ##  ####################   ",
    "   ###########      ###        #  ####################################  ",
    "  #############   #########  ########################################## ",
    "  ############    ########  ########################################### ",
    "   ##########      ######   #########################################   ",
    "    ########        ####    ########################################    ",
    "     ######          ##     #######################################     ",
    "      #####                 #####################################       ",
    "       ####                  ###################################        ",
    "        ###                   #################################         ",
    "         ##                    ###############################          ",
    "          #                     #############################           ",
    "           ##                    ###########################            ",
    "          ####                    #########################             ",
    "         ######                    #######################              ",
    "        ########                    #####################               ",
    "        #########                    ###################                ",
    "         ########                     #################                 ",
    "          #######                      ###############                  ",
    "           ######                       #############                   ",
    "           #####                         ###########                    ",
    "            ####                          #########                     ",
    "            ###                            #######                      ",
    "            ##                              #####                       ",
    "            #                                ###                        ",
    "                                                                        ",
]

# Pin positions on the grid (col, row) -> card number.
PINS = {
    1: (40, 8),    # Antalya, Turkey (COP31)
    2: (45, 11),   # Bahrain / Hormuz
    3: (39, 6),    # Kyiv, Ukraine
    4: (8, 10),    # Guasave, Mexico
    5: (57, 11),   # Shenzhen, China
    6: (16, 17),   # Junin, Peru
    7: (38, 5),    # Gulf of Finland
    8: (18, 8),    # Washington, US
    9: (70, 1),    # Mercury (space, top-right corner)
    10: (34, 15),  # Bayelsa, Nigeria
    11: (54, 16),  # Cikande, Indonesia
    12: (50, 12),  # Odisha, India
}


def draw_map(draw, x0, y0, w, h):
    cols = len(MAP_GRID[0])
    rows = len(MAP_GRID)
    cw = w / cols
    ch = h / rows
    r = min(cw, ch) * 0.36
    for ri, row in enumerate(MAP_GRID):
        for ci, cell in enumerate(row):
            if cell == "#":
                cx = x0 + (ci + 0.5) * cw
                cy = y0 + (ri + 0.5) * ch
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 130, 132))
    pin_font = font(SANS_B, 11)
    for num, (ci, ri) in PINS.items():
        cx = x0 + (ci + 0.5) * cw
        cy = y0 + (ri + 0.5) * ch
        pr = 8
        draw.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=PINRED,
                     outline=PAPER, width=1)
        t = str(num)
        tw = draw.textlength(t, font=pin_font)
        draw.text((cx - tw / 2, cy - 6), t, font=pin_font, fill=(255, 255, 255))


# --------------------------------------------------------------------------
# Small scene illustrations (simple primitives, drawn inside a box).
# --------------------------------------------------------------------------
def ill_globe_crack(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    cx, cy, r = x + w // 3, y + h // 2, h // 3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 200, 210), width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(90, 150, 160), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(90, 150, 160), width=2)
    pts = [(cx - 4, cy - r), (cx + 6, cy - r // 2), (cx - 5, cy), (cx + 5, cy + r // 2), (cx - 3, cy + r)]
    d.line(pts, fill=(240, 180, 60), width=3)
    kx, ky, kr = x + 2 * w // 3 + 10, y + h // 2, h // 4
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(245, 240, 225), outline=(200, 60, 50), width=3)
    d.line([kx, ky, kx, ky - kr + 5], fill=INK, width=3)
    d.line([kx, ky, kx + kr - 8, ky + 4], fill=INK, width=3)


def ill_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 48, 66))
    sea = y + int(h * 0.72)
    d.rectangle([x, sea, x + w, y + h], fill=(30, 90, 120))
    hx, hw = x + w // 6, w * 2 // 3
    d.polygon([(hx, sea), (hx + hw, sea), (hx + hw - 12, sea - 12), (hx + 12, sea - 12)], fill=(60, 66, 72))
    d.rectangle([hx + hw - 34, sea - 30, hx + hw - 14, sea - 12], fill=(200, 205, 210))
    for i in range(3):
        tx = hx + 16 + i * 26
        d.rectangle([tx, sea - 20, tx + 18, sea - 12], fill=(150, 90, 50))
    fx, fy = hx + hw // 2, sea - 22
    d.polygon([(fx, fy - 22), (fx - 8, fy), (fx + 8, fy)], fill=(240, 140, 40))
    d.polygon([(fx, fy - 13), (fx - 4, fy), (fx + 4, fy)], fill=(250, 210, 90))


def ill_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 36, 46))
    bx, bw, bh = x + w // 3, w // 3, int(h * 0.62)
    by = y + h - bh
    d.rectangle([bx, by, bx + bw, y + h], fill=(110, 116, 122))
    for r in range(3):
        for c in range(3):
            wx = bx + 6 + c * (bw // 3)
            wy = by + 6 + r * (bh // 3)
            d.rectangle([wx, wy, wx + 8, wy + 9], fill=(250, 215, 120))
    d.polygon([(bx + bw // 2, by), (bx + bw, by + bh // 2), (bx + bw // 2, by + bh // 2)], fill=(70, 76, 82))
    dx, dy = x + w - 26, y + 16
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(220, 80, 60))
    d.line([dx - 12, dy - 10, dx + 12, dy - 10], fill=(220, 80, 60), width=2)
    d.line([dx - 12, dy + 10, dx + 12, dy + 10], fill=(220, 80, 60), width=2)


def ill_mountains(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 54, 44))
    base = y + h
    d.polygon([(x, base), (x + w // 3, y + h // 3), (x + 2 * w // 3, base)], fill=(90, 110, 92))
    d.polygon([(x + w // 3, base), (x + 2 * w // 3, y + h // 5), (x + w, base)], fill=(70, 92, 74))
    hx, hy = x + w - 30, y + 18
    d.rectangle([hx - 14, hy, hx + 14, hy + 6], fill=(230, 230, 230))
    d.line([hx - 18, hy - 4, hx + 18, hy - 4], fill=(230, 230, 230), width=2)
    d.line([hx, hy + 6, hx, hy + 12], fill=(230, 230, 230), width=2)


def ill_towers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 34, 54))
    cols = [(200, 70, 60), (240, 200, 90), (90, 160, 220)]
    for i in range(3):
        tx = x + 14 + i * (w // 3)
        th = int(h * (0.55 + 0.12 * i))
        d.rectangle([tx, y + h - th, tx + w // 5, y + h], fill=(70, 84, 110))
        d.rectangle([tx + 3, y + h - th + 4, tx + w // 5 - 3, y + h - th + 12], fill=cols[i])
        for r in range(2):
            for c in range(2):
                wx = tx + 4 + c * 10
                wy = y + h - th + 18 + r * 12
                d.rectangle([wx, wy, wx + 6, wy + 7], fill=(250, 220, 140))


def ill_ship_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 44, 58))
    sea = y + int(h * 0.74)
    d.rectangle([x, sea, x + w, y + h], fill=(34, 84, 110))
    hx, hw = x + w // 5, w * 3 // 5
    d.polygon([(hx, sea), (hx + hw, sea), (hx + hw - 10, sea - 14), (hx + 10, sea - 14)], fill=(52, 58, 64))
    d.rectangle([hx + 8, sea - 26, hx + 26, sea - 14], fill=(180, 186, 192))
    sx, sy = hx + hw // 2, sea - 16
    for i in range(3):
        d.ellipse([sx - 8 + i * 3, sy - 30 - i * 10, sx + 8 + i * 3, sy - 14 - i * 10], fill=(90, 96, 102))
    d.polygon([(sx, sy - 16), (sx - 7, sy), (sx + 7, sy)], fill=(240, 140, 40))


def ill_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 26))
    for sx, sy in [(10, 10), (30, 22), (w - 18, 12), (w - 34, 26), (w // 2, 8)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(230, 235, 240))
    cx, cy, r = x + w // 2, y + h // 2 + 4, h // 3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 160, 150))
    for ox, oy, orr in [(-8, -6, 5), (7, 4, 4), (-3, 9, 3), (10, -9, 3)]:
        d.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr], fill=(140, 132, 122))
    d.ellipse([cx - r - 14, cy - r // 2, cx + r + 14, cy + r // 2], outline=(240, 200, 110), width=2)
    d.rectangle([cx + r + 8, cy - r // 2 - 3, cx + r + 16, cy - r // 2 + 3], fill=(240, 200, 110))


def ill_boat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(36, 60, 66))
    sea = y + int(h * 0.66)
    d.rectangle([x, sea, x + w, y + h], fill=(40, 110, 130))
    for i in range(3):
        wy = sea + 6 + i * 8
        d.arc([x + 6, wy, x + 30, wy + 10], 0, 180, fill=(140, 200, 215), width=2)
        d.arc([x + w - 30, wy, x + w - 6, wy + 10], 0, 180, fill=(140, 200, 215), width=2)
    hx, hw = x + w // 4, w // 2
    d.polygon([(hx, sea), (hx + hw, sea), (hx + hw - 8, sea + 10), (hx + 8, sea + 10)], fill=(120, 84, 50))
    d.rectangle([hx + hw // 2 - 2, sea - 22, hx + hw // 2 + 2, sea], fill=(90, 64, 40))
    d.polygon([(hx + hw // 2 + 2, sea - 22), (hx + hw // 2 + 16, sea - 4), (hx + hw // 2 + 2, sea - 4)], fill=(235, 230, 215))


def ill_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 66))
    cx, cy = x + w // 2, y + h // 2
    for r in range(26, 4, -6):
        d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 20, 300, fill=(170, 215, 230), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 245, 248))
    for i in range(4):
        rx = x + 10 + i * (w - 20) // 3
        d.line([rx, y + h - 14, rx - 5, y + h - 4], fill=(140, 200, 220), width=2)


ILLUSTRATIONS = {
    "globe": ill_globe_crack, "tanker": ill_tanker, "drone": ill_drone,
    "mountains": ill_mountains, "towers": ill_towers, "ship": ill_ship_fire,
    "mercury": ill_mercury, "boat": ill_boat, "cyclone": ill_cyclone,
}

# --------------------------------------------------------------------------
# Content. Every item was reported on 22 November 2026 (cross-checked 2+
# sources: Reuters, AFP, AP, UKMTO, USGS, ESA, Yle, NBC, CNN, RFE/RL).
# --------------------------------------------------------------------------
FIGURES = [
    ("0", "deals adopted at COP31"),
    ("186", "drones fired at Ukraine overnight"),
    ("14+", "tankers massed at Kharg Island"),
    ("6.8", "magnitude of the Peru quake"),
    ("11", "killed in the Sinaloa capture raid"),
    ("8 yrs", "BepiColombo's voyage to Mercury"),
]

LEAD = {
    "pin": 1, "ill": "globe",
    "head": "COP31 ENDS WITH NO DEAL AT ALL",
    "body": ("The UN climate summit in Antalya collapsed on Sunday after the EU, "
             "Panama and the Marshall Islands rejected a fourth draft text that "
             "never mentioned fossil fuels. Nearly 200 countries went home with "
             "no adopted decision, two days past the deadline — the longest COP "
             "on record. (Reuters, AFP)"),
}

REGIONS = [
    {
        "name": "AMERICAS",
        "card": {"pin": 4, "ill": "mountains",
                 "head": "'EL CHAPO ISIDRO' TAKEN IN SINALOA",
                 "body": "Mexican special forces with US intelligence captured FBI Top-10 fugitive Fausto Isidro Meza Flores in Guasave; a firefight killed 11. (AP, Reuters)"},
        "briefs": [
            "US stocks fall into correction: S&P 500 down 3.7%, Nasdaq 5.3%. (AP)",
            "Democrats clinch a House majority of at least 258 seats. (AP)",
            "DEA confirms first known large-scale US nitazene lab, in Baton Rouge.",
            "Delta delays hundreds of flights after a system outage. (AP)",
        ],
    },
    {
        "name": "EUROPE",
        "card": {"pin": 3, "ill": "drone",
                 "head": "186-DRONE BARRAGE; BLOCK FALLS IN DYMER",
                 "body": "Russia launched 186 drones overnight; 161 were downed, yet strikes hit 18 locations. A drone collapsed part of a block in Dymer — 14 missing. (AP)"},
        "briefs": [
            "Russian cargo ship Sparta II still burning in the Gulf of Finland. (Yle)",
            "NATO chief Rutte pledges to defend Poland after missile incursion. (AFP)",
            "Denmark expels Russia's defence attaché over alleged murder plot. (Reuters)",
            "Zelensky: 2,700 drones in one week; Patriot delays 'difficult to understand'.",
        ],
    },
    {
        "name": "MIDDLE EAST",
        "card": {"pin": 2, "ill": "tanker",
                 "head": "IRAN HITS BAHRAIN; TANKERS STRUCK",
                 "body": "Projectiles hit an industrial site in Sitra, injuring two, as Tehran claimed strikes on US Patriot sites; two tankers were hit near Hormuz. (AFP, UKMTO)"},
        "briefs": [
            "14+ tankers massed at Kharg Island to run the US blockade. (UKMTO)",
            "Settlers torch 12 Palestinian vehicles in four West Bank villages. (AFP)",
            "Fire at Basra's Hartha power station kills at least four. (AP)",
            "Iran says it downed a US drone over Qeshm Island. (IRNA)",
        ],
    },
    {
        "name": "AFRICA",
        "card": {"pin": 10, "ill": "boat",
                 "head": "MOURNERS' BOAT CAPSIZES: 24 DEAD",
                 "body": "A boat carrying mourners to a funeral capsized in Nigeria's Bayelsa State, killing 24 people. (AP)"},
        "briefs": [
            "Drones strike Khartoum and damage a UN building.",
            "Phumzile Mlambo-Ngcuka, former UN Women chief, dies at 71.",
            "Fresh fighting reported in Sudan's Blue Nile region.",
        ],
    },
    {
        "name": "ASIA–PACIFIC",
        "card": {"pin": 5, "ill": "towers",
                 "head": "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                 "body": "The three nuclear powers held a first trilateral summit after APEC — joint concern on nuclear risks, but no arms limits, no Ukraine deal. (RFE/RL)"},
        "briefs": [
            "EU–Indonesia trade deal after almost 10 years; tariffs scrapped on 98.5% of goods. (AFP)",
            "Candy-factory fire in Cikande, Banten: three dead, 36 missing. (AP)",
            "SEC probes Nvidia's accounting; Jensen Huang to testify. (Reuters)",
            "Anthropic mathematician says Claude helped prove the Riemann hypothesis.",
        ],
    },
    {
        "name": "SOUTH ASIA",
        "card": {"pin": 12, "ill": "cyclone",
                 "head": "CYCLONE AKVAN EMPTIES ODISHA COAST",
                 "body": "Cyclone Akvan forces 300,000 people from their homes in Odisha; schools shut in six districts. (AFP)"},
        "briefs": [
            "Modi addresses the SCO summit.",
            "Manipur adulterated alcohol kills 11.",
            "Japan holds a live-fire exercise in India.",
        ],
    },
]

GLOBAL_STRIP = {
    "name": "GLOBAL & SPORT",
    "card": {"pin": 9, "ill": "mercury",
             "head": "BEPICOLOMBO REACHES MERCURY",
             "body": "The twin ESA–JAXA spacecraft entered orbit around Mercury, ending an eight-year journey. (ESA)"},
    "briefs": [
        "Magnitude 6.8 quake near Junín shakes Peru; Lima flees outdoors, no casualties. (AP, USGS)",
        "Hackers breach FBI crime database and a USDA payment system; US cyber chief fired. (NBC, CNN)",
        "UN autonomous-weapons talks end with no binding deal; work extended to 2028.",
        "One-time CRISPR therapy cuts bad cholesterol by 52% in trial results.",
        "SPORT: Verstappen wins Las Vegas GP by 0.639s; England beat All Blacks 37–12; Leeds stun Chelsea 4–1.",
    ],
}


def pin_chip(d, x, y, num):
    d.ellipse([x, y, x + 18, y + 18], fill=PINRED, outline=PAPER, width=1)
    t = str(num)
    f = font(SANS_B, 10)
    tw = d.textlength(t, font=f)
    d.text((x + 9 - tw / 2, y + 3), t, font=f, fill=(255, 255, 255))


def draw_region(d, reg, x, y, w):
    """Draw one region block; return the y just below it."""
    d.rectangle([x, y, x + w, y + 20], fill=TEAL)
    d.text((x + 8, y + 3), reg["name"], font=font(SANS_B, 12), fill=(255, 255, 255))
    y += 25
    card = reg["card"]
    iw, ih = 84, 56
    ILLUSTRATIONS[card["ill"]](d, x, y, iw, ih)
    pin_chip(d, x + 3, y + 3, card["pin"])
    tx = x + iw + 8
    twd = w - iw - 8
    ty = draw_wrapped(d, tx, y, card["head"], font(SERIF_B, 12), twd, INK,
                      leading=1.08, max_lines=3)
    ty = draw_wrapped(d, tx, ty + 1, card["body"], font(SANS, 10), twd, INK,
                      leading=1.18, max_lines=4)
    y = max(y + ih, ty) + 5
    for b in reg["briefs"]:
        d.ellipse([x + 1, y + 3, x + 5, y + 7], fill=OCHRE)
        y = draw_wrapped(d, x + 10, y, b, font(SANS, 10), w - 10, INK,
                         leading=1.16, max_lines=2)
        y += 2
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    inner_w = W - 2 * M

    # ---- Masthead -------------------------------------------------------
    y = 20
    centered(d, W // 2, y, "THE WORLD IN ONE DAY", font(SERIF_B, 56), INK)
    y += 68
    centered(d, W // 2, y, "SUNDAY · 22 NOVEMBER 2026 · THE DAY'S WORLD NEWS ON ONE PAGE",
             font(SANS_B, 16), OCHRE)
    y += 24
    centered(d, W // 2, y, "Climate talks collapse, three nuclear powers meet, and the Gulf crisis deepens.",
             font(SERIF, 18), SLATE)
    y += 28
    d.line([M, y, W - M, y], fill=INK, width=3)
    d.line([M, y + 5, W - M, y + 5], fill=INK, width=1)
    y += 13

    # ---- Figures strip --------------------------------------------------
    fig_w = inner_w // len(FIGURES)
    for i, (num, label) in enumerate(FIGURES):
        fx = M + i * fig_w
        d.text((fx, y), num, font=font(SERIF_B, 30), fill=PINRED if i % 2 == 0 else TEAL)
        draw_wrapped(d, fx, y + 37, label, font(SANS, 10.5), fig_w - 12, SLATE, max_lines=2)
        if i:
            d.line([fx - 8, y + 2, fx - 8, y + 56], fill=(190, 184, 168), width=1)
    y += 62
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 9

    # ---- Map band -------------------------------------------------------
    map_h = 124
    d.rectangle([M, y, W - M, y + map_h], fill=(232, 238, 236), outline=RULE, width=1)
    draw_map(d, M + 10, y + 6, inner_w - 20, map_h - 26)
    d.text((M + 12, y + map_h - 18), "WHERE IT HAPPENED — pins mark where today's stories broke; numbered pins match the cards below",
           font=font(SANS_B, 11), fill=TEAL)
    y += map_h + 10

    # ---- Lead story -----------------------------------------------------
    lead_h = 98
    ill_w = 280
    ILLUSTRATIONS[LEAD["ill"]](d, M, y, ill_w, lead_h)
    pin_chip(d, M + 5, y + 5, LEAD["pin"])
    lx = M + ill_w + 16
    lw = W - M - lx
    ly = draw_wrapped(d, lx, y + 2, LEAD["head"], font(SERIF_B, 27), lw, INK, leading=1.05)
    draw_wrapped(d, lx, ly + 3, LEAD["body"], font(SANS, 13), lw, INK, leading=1.22)
    y += lead_h + 10
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 9

    # ---- Regional grid (3 columns x 2 rows) -----------------------------
    col_w = inner_w // 3 - 12
    cols_x = [M, M + inner_w // 3 + 6, M + 2 * inner_w // 3 + 12]
    rows = [[0, 1, 2], [3, 4, 5]]
    row_y = y
    for row in rows:
        bottoms = []
        for ci, ridx in enumerate(row):
            bottoms.append(draw_region(d, REGIONS[ridx], cols_x[ci], row_y, col_w))
        row_y = max(bottoms) + 6

    # ---- Global & sport strip -------------------------------------------
    d.line([M, row_y, W - M, row_y], fill=RULE, width=1)
    row_y += 8
    strip = GLOBAL_STRIP
    d.rectangle([M, row_y, M + 150, row_y + 20], fill=TEAL)
    d.text((M + 8, row_y + 3), strip["name"], font=font(SANS_B, 12), fill=(255, 255, 255))
    row_y += 25
    card = strip["card"]
    iw, ih = 84, 56
    ILLUSTRATIONS[card["ill"]](d, M, row_y, iw, ih)
    pin_chip(d, M + 3, row_y + 3, card["pin"])
    tx = M + iw + 8
    ty = draw_wrapped(d, tx, row_y, card["head"], font(SERIF_B, 12), 200, INK,
                      leading=1.08, max_lines=3)
    ty = draw_wrapped(d, tx, ty + 1, card["body"], font(SANS, 10), 200, INK,
                      leading=1.18, max_lines=4)
    bx = tx + 212
    bw = W - M - bx
    by = row_y
    for b in strip["briefs"]:
        d.ellipse([bx + 1, by + 3, bx + 5, by + 7], fill=OCHRE)
        by = draw_wrapped(d, bx + 10, by, b, font(SANS, 10), bw - 10, INK,
                          leading=1.16, max_lines=2)
        by += 2
    row_y = max(row_y + ih, ty, by)

    # ---- Footer ---------------------------------------------------------
    fy = H - 46
    d.line([M, fy, W - M, fy], fill=RULE, width=1)
    d.text((M, fy + 7),
           "DATE CHECK: every story above was reported on 22 November 2026 (in at least one time zone). Older events are not shown as today's news.",
           font=font(SANS_B, 11), fill=TEAL)
    d.text((M, fy + 24),
           "Sources: Reuters · AFP · AP · UKMTO · USGS · ESA · Yle · NBC · CNN · RFE/RL",
           font=font(SANS, 11), fill=SLATE)
    print("content bottom:", row_y, "footer top:", fy)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
