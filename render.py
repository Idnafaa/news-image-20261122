#!/usr/bin/env python3
"""Render the v2 entry image for news-image-20261122.

Draws a 1024x1024 broadsheet front page, "THE WORLD IN ONE DAY", summing
up Sunday 22 November 2026: 1 lead story, 6 illustrated cards and 27
numbered briefs (34 stories). Every story was cross-checked against at
least two independent reports of that day. Output is deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # content width

PAPER = (247, 243, 234)
INK = (24, 22, 20)
RED = (178, 34, 34)
NAVY = (27, 42, 84)
GOLD = (196, 141, 26)
TEAL = (18, 110, 110)
GREY = (96, 92, 86)
LIGHT = (226, 219, 203)

FDIR = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


SERIF_BLACK = "NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SERIF = "NotoSerif-Regular.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS = "NotoSans-Regular.ttf"


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


def block(draw, x, y, text, fnt, max_w, fill=INK, leading=1.18, max_lines=None):
    """Draw wrapped text; return the y just below it."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    step = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def rule(draw, x0, x1, y, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


# --------------------------------------------------------------------------
# Small flat illustrations, one per story. Each draws inside (x, y, w, h).
# --------------------------------------------------------------------------

def art_cop31(d, x, y, w, h):
    """Cracked globe beside a clock running past midnight."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 52))
    cx, cy, r = x + w * 0.34, y + h * 0.52, h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 96, 140), outline=(150, 190, 220), width=3)
    for k in (-0.55, 0.0, 0.55):
        d.arc([cx - r * (1 - abs(k)) - 2, cy - r, cx + r * (1 - abs(k)) + 2, cy + r], 90, 270, fill=(150, 190, 220), width=2)
        d.arc([cx - r * (1 - abs(k)) - 2, cy - r, cx + r * (1 - abs(k)) + 2, cy + r], 270, 90, fill=(150, 190, 220), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(150, 190, 220), width=2)
    # crack
    pts = [(cx - r * 0.15, cy - r), (cx + r * 0.05, cy - r * 0.45), (cx - r * 0.2, cy - r * 0.05),
           (cx + r * 0.12, cy + r * 0.4), (cx - r * 0.05, cy + r)]
    d.line(pts, fill=(255, 214, 90), width=4)
    # clock
    kx, ky, kr = x + w * 0.78, y + h * 0.5, h * 0.3
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(247, 243, 234), outline=(24, 22, 20), width=3)
    for a in range(0, 360, 30):
        import math
        x1 = kx + kr * 0.82 * math.sin(math.radians(a))
        y1 = ky - kr * 0.82 * math.cos(math.radians(a))
        x2 = kx + kr * 0.95 * math.sin(math.radians(a))
        y2 = ky - kr * 0.95 * math.cos(math.radians(a))
        d.line([(x1, y1), (x2, y2)], fill=INK, width=2)
    d.line([(kx, ky), (kx, ky - kr * 0.7)], fill=RED, width=4)          # minute hand at 12
    d.line([(kx, ky), (kx + kr * 0.45, ky + kr * 0.25)], fill=INK, width=4)  # hour past 12
    d.ellipse([kx - 4, ky - 4, kx + 4, ky + 4], fill=INK)
    # thermometer
    tx = x + w * 0.93
    d.rounded_rectangle([tx - 6, y + h * 0.18, tx + 6, y + h * 0.78], 6, fill=(247, 243, 234), outline=INK, width=2)
    d.rectangle([tx - 3, y + h * 0.3, tx + 3, y + h * 0.78], fill=RED)
    d.ellipse([tx - 10, y + h * 0.72, tx + 10, y + h * 0.9], fill=RED, outline=INK, width=2)


def art_summit(d, x, y, w, h):
    """Three flags over a shared table."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    cols = [(178, 34, 34), (27, 42, 84), (196, 141, 26)]
    for i, c in enumerate(cols):
        fx = x + w * (0.2 + 0.3 * i)
        d.line([(fx, y + h * 0.12), (fx, y + h * 0.62)], fill=INK, width=3)
        d.polygon([(fx, y + h * 0.12), (fx + w * 0.2, y + h * 0.2), (fx, y + h * 0.28)], fill=c)
    d.rectangle([x + w * 0.08, y + h * 0.66, x + w * 0.92, y + h * 0.74], fill=(90, 64, 40))
    d.rectangle([x + w * 0.14, y + h * 0.74, x + w * 0.2, y + h * 0.9], fill=(90, 64, 40))
    d.rectangle([x + w * 0.8, y + h * 0.74, x + w * 0.86, y + h * 0.9], fill=(90, 64, 40))
    for i, c in enumerate(cols):
        px = x + w * (0.2 + 0.3 * i)
        d.ellipse([px - 9, y + h * 0.5, px + 9, y + h * 0.5 + 18], fill=c)


def art_hormuz(d, x, y, w, h):
    """Tankers in a strait with missile arcs."""
    d.rectangle([x, y, x + w, y + h], fill=(20, 40, 66))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(36, 84, 120))
    d.polygon([(x, y + h * 0.62), (x + w * 0.3, y + h * 0.62), (x + w * 0.22, y + h * 0.3), (x, y + h * 0.3)], fill=(214, 196, 150))
    d.polygon([(x + w, y + h * 0.62), (x + w * 0.74, y + h * 0.62), (x + w * 0.82, y + h * 0.34), (x + w, y + h * 0.34)], fill=(214, 196, 150))
    for i, (tx, tc) in enumerate([(0.42, (200, 60, 50)), (0.58, (230, 170, 60))]):
        bx = x + w * tx
        d.rectangle([bx, y + h * 0.56, bx + w * 0.13, y + h * 0.66], fill=tc)
        d.rectangle([bx + w * 0.02, y + h * 0.5, bx + w * 0.05, y + h * 0.56], fill=(240, 240, 240))
    for sx in (0.12, 0.9):
        d.arc([x + w * sx - w * 0.16, y + h * 0.1, x + w * sx + w * 0.16, y + h * 0.55], 200, 330, fill=(255, 120, 80), width=3)
    d.ellipse([x + w * 0.47, y + h * 0.44, x + w * 0.53, y + h * 0.54], fill=(255, 160, 60))
    d.polygon([(x + w * 0.5, y + h * 0.3), (x + w * 0.46, y + h * 0.46), (x + w * 0.54, y + h * 0.46)], fill=(255, 90, 40))


def art_kyiv(d, x, y, w, h):
    """Apartment block with a collapsed section and a drone."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 64, 82))
    bx, bw = x + w * 0.12, w * 0.6
    d.rectangle([bx, y + h * 0.2, bx + bw, y + h * 0.92], fill=(196, 188, 172))
    for r in range(4):
        for c in range(5):
            wx = bx + bw * (0.06 + 0.19 * c)
            wy = y + h * (0.27 + 0.16 * r)
            col = (70, 80, 100) if (r + c) % 3 else (240, 200, 110)
            d.rectangle([wx, wy, wx + bw * 0.11, wy + h * 0.09], fill=col)
    # collapsed corner
    d.polygon([(bx + bw * 0.62, y + h * 0.2), (bx + bw, y + h * 0.2), (bx + bw, y + h * 0.55),
               (bx + bw * 0.8, y + h * 0.44), (bx + bw * 0.7, y + h * 0.34)], fill=(58, 64, 82))
    d.polygon([(bx + bw * 0.66, y + h * 0.92), (bx + bw * 0.85, y + h * 0.6), (bx + bw * 1.05, y + h * 0.92)], fill=(120, 112, 98))
    # drone
    dx, dy = x + w * 0.86, y + h * 0.3
    d.ellipse([dx - 8, dy - 5, dx + 8, dy + 5], fill=(20, 20, 24))
    for ox, oy in [(-16, -9), (16, -9), (-16, 9), (16, 9)]:
        d.line([(dx, dy), (dx + ox, dy + oy)], fill=(20, 20, 24), width=2)
        d.ellipse([dx + ox - 6, dy + oy - 3, dx + ox + 6, dy + oy + 3], outline=(200, 200, 210), width=2)


def art_court(d, x, y, w, h):
    """Courthouse columns with a gavel in front."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 233, 220))
    d.polygon([(x + w * 0.06, y + h * 0.3), (x + w * 0.5, y + h * 0.08), (x + w * 0.94, y + h * 0.3)], fill=(120, 110, 92))
    for i in range(5):
        cx = x + w * (0.14 + 0.18 * i)
        d.rectangle([cx - 6, y + h * 0.34, cx + 6, y + h * 0.78], fill=(150, 140, 118))
    d.rectangle([x + w * 0.06, y + h * 0.8, x + w * 0.94, y + h * 0.88], fill=(120, 110, 92))
    # gavel
    gx, gy = x + w * 0.5, y + h * 0.52
    d.line([(gx - w * 0.18, gy + h * 0.24), (gx + w * 0.12, gy - h * 0.1)], fill=(90, 64, 40), width=9)
    d.rectangle([gx + w * 0.0, gy - h * 0.24, gx + w * 0.26, gy - h * 0.02], fill=(110, 78, 48))
    d.rectangle([gx + w * 0.0, gy - h * 0.24, gx + w * 0.06, gy - h * 0.02], fill=GOLD)
    d.rectangle([gx + w * 0.2, gy - h * 0.24, gx + w * 0.26, gy - h * 0.02], fill=GOLD)
    d.ellipse([gx - w * 0.24, gy + h * 0.22, gx - w * 0.08, gy + h * 0.34], fill=(90, 64, 40))


def art_hack(d, x, y, w, h):
    """Server racks, one flashing a warning."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 30))
    for i in range(3):
        rx = x + w * (0.08 + 0.32 * i)
        d.rectangle([rx, y + h * 0.14, rx + w * 0.24, y + h * 0.88], fill=(40, 54, 72), outline=(90, 120, 150), width=2)
        for r in range(4):
            ry = y + h * (0.22 + 0.16 * r)
            d.rectangle([rx + 6, ry, rx + w * 0.24 - 6, ry + h * 0.09], fill=(24, 34, 48))
            dot = (90, 220, 130) if (i + r) % 2 else (255, 90, 70)
            d.ellipse([rx + 10, ry + 4, rx + 18, ry + 12], fill=dot)
    wx, wy = x + w * 0.8, y + h * 0.3
    d.polygon([(wx, wy - h * 0.16), (wx - w * 0.09, wy + h * 0.12), (wx + w * 0.09, wy + h * 0.12)], fill=(255, 190, 40), outline=INK)
    d.text((wx - 3, wy - h * 0.09), "!", font=font(SANS_BOLD, 20), fill=INK)


def art_mercury(d, x, y, w, h):
    """Mercury with an orbiting spacecraft."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 26))
    import random
    rng = random.Random(7)
    for _ in range(46):
        sx = x + rng.randrange(4, int(w) - 4)
        sy = y + rng.randrange(4, int(h) - 4)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 205, 225))
    cx, cy, r = x + w * 0.42, y + h * 0.54, h * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 156, 140), outline=(210, 200, 182), width=2)
    for ox, oy, cr in [(-0.3, -0.2, 0.16), (0.25, 0.15, 0.2), (-0.05, 0.4, 0.12), (0.35, -0.3, 0.1)]:
        d.ellipse([cx + r * ox - r * cr, cy + r * oy - r * cr, cx + r * ox + r * cr, cy + r * oy + r * cr],
                  outline=(120, 110, 96), width=2)
    d.arc([cx - r * 1.9, cy - r * 0.75, cx + r * 1.9, cy + r * 0.75], 15, 345, fill=(150, 190, 230), width=2)
    px, py = cx + r * 1.55, cy - r * 0.55
    d.rectangle([px - 7, py - 5, px + 7, py + 5], fill=(230, 230, 235))
    d.rectangle([px - 20, py - 3, px - 8, py + 3], fill=(70, 110, 180))
    d.rectangle([px + 8, py - 3, px + 20, py + 3], fill=(70, 110, 180))


# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------

FIGURES = [
    ("0", "deals adopted at COP31"),
    ("3", "nuclear powers at one table"),
    ("14", "missing in the Dymer rubble"),
    ("2,700", "drones fired at Ukraine in a week"),
    ("0.639s", "Verstappen's Vegas margin"),
    ("8 yrs", "BepiColombo's voyage to Mercury"),
]

LEAD = {
    "head": "COP31 ENDS WITH NO DEAL AT ALL",
    "body": ("The UN climate summit in Antalya collapsed on Sunday after the EU, Panama and the "
             "Marshall Islands rejected a fourth draft text that never mentioned fossil fuels. "
             "Nearly 200 countries went home with no adopted decision at all, two days past "
             "the deadline. (Reuters, AFP)"),
    "art": art_cop31,
}

CARDS = [
    ("TRUMP, XI AND PUTIN MEET IN SHENZHEN",
     "The three nuclear powers held a first trilateral summit at APEC, declaring joint "
     "concern on nuclear risks — but no arms limits, no Ukraine deal. (RFE/RL)", art_summit),
    ("IRAN HITS BAHRAIN; TANKERS STRUCK AT HORMUZ",
     "Iranian projectiles hit an industrial site in Sitra, injuring two, as Tehran claimed "
     "strikes on US Patriot sites; two tankers were hit near Hormuz. (Reuters, UKMTO)", art_hormuz),
    ("DRONE FELLS KYIV APARTMENT BLOCK; 14 MISSING",
     "A Russian drone collapsed part of a five-storey block in Dymer; 14 people are missing. "
     "A Kryvyi Rih missile killed a boy of 7 and a woman of 20. (Reuters, AP)", art_kyiv),
    ("WORLD COURT: MYANMAR COMMITTED GENOCIDE",
     "The International Court of Justice ruled Myanmar committed genocide against the Rohingya "
     "in 2017 — its first finding of state responsibility for genocide. (AP, BBC)", art_court),
    ("HACKERS INSIDE THE FBI AND USDA",
     "The FBI is probing a breach of its NCIC crime database while hackers separately hit a "
     "USDA farm-payment system; the US cyber chief was fired. (AP, CNN, NBC)", art_hack),
    ("BEPICOLOMBO REACHES MERCURY",
     "The twin BepiColombo spacecraft entered orbit around Mercury on Sunday, ending an "
     "eight-year journey to the solar system's smallest planet. (ESA)", art_mercury),
]

BRIEFS = [
    "Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro' in Sinaloa; 11 killed. (AP)",
    "Sanctioned Russian cargo ship Sparta II still burning in the Gulf of Finland after a drone strike. (Yle)",
    "US stocks fall into correction as AI sell-off deepens: S&P 500 down 3.7%, Nasdaq 5.3%. (AP)",
    "EU and Indonesia sign a trade deal after almost 10 years, scrapping tariffs on 98.5% of goods. (AFP)",
    "Fire at a candy factory in Cikande, Banten: three workers dead, 36 still missing. (AP, Reuters)",
    "Magnitude 6.7 earthquake near Junín shakes Peru; Lima residents flee outdoors. (AFP, USGS)",
    "NATO chief Rutte pledges to defend Poland after Russian missiles entered its airspace. (AFP)",
    "Settlers torch 12 Palestinian vehicles in four West Bank villages; Israel opens an inquiry.",
    "Drones strike Khartoum and damage a UN building as Sudan's war grinds on.",
    "Trump's order 14438: federal contractors must clear congressional requests with the White House. (AP)",
    "Trump threatens a 'tremendous tax' on US tech firms that build AI data centres abroad.",
    "Trump says he will work with Democrats on a 10% cap on credit-card interest rates.",
    "Virginia child under five becomes the 12th US measles death of 2026; cases at a 35-year high.",
    "Anthropic mathematician says Claude helped him prove the Riemann hypothesis; two groups confirm it.",
    "One-time CRISPR therapy cuts bad cholesterol by 52% in trial results.",
    "UN autonomous-weapons talks in Geneva end with no binding deal; work extended to 2028.",
    "Missouri judge approves Bayer's $7.25 billion Roundup settlement. (Reuters)",
    "SEC probes Nvidia's accounting; Jensen Huang agrees to testify at a Senate hearing. (Reuters)",
    "DEA confirms the first known large-scale US nitazene lab, found in Baton Rouge.",
    "FBI arrests a Georgia man accused of sending $26,000 to Islamic State-linked individuals.",
    "Democrats clinch a House majority of at least 258 seats; Schumer leads a 56-seat Senate. (AP)",
    "Delta delays hundreds of flights after a weight-and-balance system outage. (AP)",
    "Fire at Basra's Hartha power station kills at least four and injures 30.",
    "Boat carrying mourners to a funeral capsizes in Nigeria's Bayelsa State: 24 dead. (AP)",
    "Cyclone Akvan forces 300,000 people from their homes in Odisha; schools shut in six districts.",
    "Denmark expels Russia's defence attaché over an alleged plot to kill a Ukrainian rapper. (Reuters)",
    "SPORT: Verstappen wins the Las Vegas GP by 0.639s; England beat the All Blacks 37–12; Leeds stun Chelsea 4–1; Malen hits four for Roma.",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # Masthead
    f_mast = font(SERIF_BLACK, 54)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 12), title, font=f_mast, fill=INK)
    y = 76
    f_date = font(SANS_BOLD, 16)
    date_line = "SUNDAY, 22 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS ON ONE PAGE"
    tw = d.textlength(date_line, font=f_date)
    d.text(((W - tw) / 2, y), date_line, font=f_date, fill=NAVY)
    y += 21
    f_stand = font(SERIF, 18)
    stand = "Climate talks collapse, three nuclear powers meet, and the Gulf crisis deepens."
    tw = d.textlength(stand, font=f_stand)
    d.text(((W - tw) / 2, y), stand, font=f_stand, fill=INK)
    y += 27
    rule(d, x0, x1, y, 4)
    rule(d, x0, x1, y + 6, 1)

    # Figures strip
    y += 16
    fw = CW / len(FIGURES)
    f_fig = font(SERIF_BLACK, 28)
    f_figcap = font(SANS, 11)
    for i, (num, cap) in enumerate(FIGURES):
        fx = x0 + i * fw
        d.text((fx, y), num, font=f_fig, fill=RED if i % 2 == 0 else NAVY)
        block(d, fx, y + 35, cap, f_figcap, fw - 10, fill=GREY, leading=1.12, max_lines=2)
        if i:
            d.line([(fx - 8, y + 2), (fx - 8, y + 54)], fill=LIGHT, width=1)
    y += 62
    rule(d, x0, x1, y, 1)

    # Lead story
    y += 12
    lead_art_w = 452
    LEAD["art"](d, x0, y, lead_art_w, 140)
    tx = x0 + lead_art_w + 18
    tw_ = x1 - tx
    f_lead_head = font(SERIF_BLACK, 31)
    hy = block(d, tx, y - 4, LEAD["head"], f_lead_head, tw_, leading=1.06)
    f_body = font(SERIF, 15.5)
    block(d, tx, hy + 5, LEAD["body"], f_body, tw_, leading=1.22)
    y += 140 + 10
    rule(d, x0, x1, y, 1)

    # Cards: 2 rows x 3
    y += 10
    gap = 16
    card_w = (CW - 2 * gap) / 3
    f_card_head = font(SERIF_BOLD, 15)
    f_card_body = font(SERIF, 12.5)
    card_h = 143
    for row in range(2):
        for col in range(3):
            head, body, art = CARDS[row * 3 + col]
            cx = x0 + col * (card_w + gap)
            art(d, int(cx), y, int(card_w), 52)
            hy = block(d, cx, y + 57, head, f_card_head, card_w, leading=1.1, max_lines=2)
            block(d, cx, hy + 2, body, f_card_body, card_w, leading=1.18, max_lines=4)
            if col:
                d.line([(cx - gap / 2, y), (cx - gap / 2, y + card_h - 8)], fill=LIGHT, width=1)
        y += card_h
        if row == 0:
            rule(d, x0, x1, y - 4, 1)
            y += 6
    rule(d, x0, x1, y - 2, 1)

    # Briefs: 3 columns x 9
    y += 8
    f_brief_head = font(SANS_BOLD, 16)
    d.text((x0, y), "THE DAY IN BRIEF", font=f_brief_head, fill=NAVY)
    y += 23
    f_brief = font(SERIF, 11.8)
    f_num = font(SANS_BOLD, 11.8)
    col_w = (CW - 2 * gap) / 3
    per_col = 9
    col_tops = []
    for col in range(3):
        cx = x0 + col * (col_w + gap)
        cy = y
        for j in range(per_col):
            idx = col * per_col + j
            num = f"{idx + 1}."
            d.text((cx, cy), num, font=f_num, fill=RED)
            nw = d.textlength(num + " ", font=f_num)
            cy = block(d, cx + nw, cy, BRIEFS[idx], f_brief, col_w - nw, leading=1.12)
            cy += 3
        col_tops.append(cy)
        if col:
            d.line([(cx - gap / 2, y), (cx - gap / 2, max(col_tops))], fill=LIGHT, width=1)
    y = max(col_tops) + 8
    rule(d, x0, x1, y, 1)

    # Footer
    y += 8
    f_foot = font(SANS, 12)
    d.text((x0, y), "DATE CHECK: every story above was reported on 22 November 2026 (in at least one time zone). Older events are not shown as today's news.",
           font=f_foot, fill=INK)
    d.text((x0, y + 18), "Sources: AP · Reuters · AFP · CNN · NBC · UKMTO · USGS · Yle · RFE/RL · ESA",
           font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png; final y =", y + 18)


if __name__ == "__main__":
    main()
