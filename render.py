#!/usr/bin/env python3
"""Render 'The World in One Day — 22 November 2026' as a 1024x1024 broadsheet.

Fresh renderer written for the news-image-20261122 edition. Draws a cream-paper
front page with PIL primitives: masthead, figure strip, one lead story, two
secondary leads, six illustrated cards, numbered briefs and a sources footer.
Deterministic: no clock, no randomness, no network.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 233)
INK = (26, 26, 26)
NAVY = (27, 42, 74)
RED = (178, 34, 34)
TEAL = (18, 110, 110)
GOLD = (176, 132, 32)
GREY = (90, 90, 90)
RULE = (60, 60, 60)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def scene_raid(d, x, y, w, h):
    """Night raid in Sinaloa: dark sky, helicopter, burning truck, escort."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 30, 58))
    for i in range(14):  # stars
        sx = x + 12 + (i * 53) % (w - 24)
        sy = y + 8 + (i * 29) % 34
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 225, 240))
    gy = y + h - 26
    d.rectangle([x, gy, x + w, y + h], fill=(52, 44, 34))
    # helicopter
    hx, hy = x + w - 150, y + 26
    d.ellipse([hx, hy, hx + 62, hy + 22], fill=(12, 12, 16))
    d.rectangle([hx - 26, hy + 8, hx + 4, hy + 13], fill=(12, 12, 16))
    d.line([hx + 6, hy - 6, hx + 56, hy - 6], fill=(200, 200, 210), width=3)
    d.line([hx + 31, hy - 6, hx + 31, hy], fill=(200, 200, 210), width=3)
    d.polygon([(hx + 24, hy + 22), (hx + 38, hy + 22), (hx + 62, gy)], fill=(240, 230, 170))
    # burning truck
    tx, ty = x + 26, gy - 30
    d.rectangle([tx, ty, tx + 78, ty + 24], fill=(30, 30, 30))
    d.rectangle([tx + 78, ty + 6, tx + 100, ty + 24], fill=(40, 40, 40))
    for wx in (tx + 12, tx + 58, tx + 84):
        d.ellipse([wx, ty + 20, wx + 13, ty + 33], fill=(10, 10, 10))
    for i, (fx, fh, fc) in enumerate([(6, 26, (230, 90, 20)), (26, 36, (240, 140, 30)),
                                      (46, 30, (250, 190, 60)), (62, 22, (230, 90, 20))]):
        d.polygon([(tx + fx, ty), (tx + fx + 7, ty - fh), (tx + fx + 14, ty)], fill=fc)
    # escorted figure between two soldiers
    cx = x + w // 2 + 20
    for i, col in enumerate([(70, 80, 60), (120, 110, 90), (70, 80, 60)]):
        px = cx + i * 26
        d.ellipse([px, gy - 34, px + 11, gy - 23], fill=(214, 180, 150))
        d.rectangle([px + 1, gy - 23, px + 10, gy - 4], fill=col)
        d.line([px + 3, gy - 4, px + 1, gy], fill=col, width=3)
        d.line([px + 8, gy - 4, px + 10, gy], fill=col, width=3)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def scene_cop(d, x, y, w, h):
    """Climate talks in overtime: long table, flags, big clock past deadline."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 238, 244))
    ty = y + h - 44
    d.rectangle([x + 18, ty, x + w - 18, ty + 16], fill=(120, 84, 48))
    for i in range(7):  # delegate silhouettes
        px = x + 34 + i * ((w - 90) // 6)
        d.ellipse([px, ty - 20, px + 13, ty - 7], fill=(60, 60, 70))
        d.rectangle([px + 1, ty - 7, px + 12, ty], fill=(60, 60, 70))
    for i, fc in enumerate([(200, 40, 40), (40, 80, 180), (40, 150, 70), (230, 180, 40)]):
        fx = x + 26 + i * 30
        d.line([fx, y + 10, fx, y + 40], fill=INK, width=2)
        d.rectangle([fx, y + 10, fx + 20, y + 24], fill=fc)
    cx, cy, r = x + w - 52, y + 42, 30  # clock, hands past twelve
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK, width=3)
    d.line([cx, cy, cx, cy - r + 6], fill=INK, width=3)
    d.line([cx, cy, cx + 14, cy + 10], fill=RED, width=3)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def scene_tankers(d, x, y, w, h):
    """Tanker convoy facing a naval blockade line in a strait."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 220, 232))
    wy = y + h - 52
    d.rectangle([x, wy, x + w, y + h], fill=(52, 104, 150))
    d.polygon([(x, wy), (x + 70, wy - 34), (x + 120, wy)], fill=(150, 120, 84))
    d.polygon([(x + w - 120, wy), (x + w - 70, wy - 34), (x + w, wy)], fill=(150, 120, 84))
    for i in range(3):  # tankers in line
        tx = x + 24 + i * 78
        d.polygon([(tx, wy - 6), (tx + 66, wy - 6), (tx + 57, wy + 8), (tx + 9, wy + 8)], fill=(44, 48, 56))
        d.rectangle([tx + 7, wy - 20, tx + 52, wy - 6], fill=(178, 60, 44))
        d.rectangle([tx + 52, wy - 28, tx + 62, wy - 6], fill=(230, 230, 230))
    bx = x + w - 64  # warship beyond the line
    d.polygon([(bx, wy - 4), (bx + 56, wy - 4), (bx + 48, wy + 8), (bx + 8, wy + 8)], fill=(90, 98, 110))
    d.rectangle([bx + 20, wy - 22, bx + 36, wy - 4], fill=(110, 118, 130))
    for i in range(6):  # dashed blockade line
        ly = y + 16 + i * 16
        d.line([x + w - 74, ly, x + w - 74, ly + 8], fill=RED, width=3)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def card_bridges(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 36, 64))
    ry = y + h - 30
    d.rectangle([x, ry, x + w, y + h], fill=(40, 70, 120))
    by = ry - 22
    d.line([x + 8, by, x + w - 8, by], fill=(200, 200, 205), width=5)
    for px in (x + 40, x + w // 2, x + w - 52):
        d.line([px, by, px, ry], fill=(200, 200, 205), width=4)
    for i in range(3):  # missile arcs
        sx = x + 20 + i * 60
        d.arc([sx, y + 6, sx + 90, y + 78], start=200, end=340, fill=(250, 170, 60), width=3)
        d.ellipse([sx + 84, y + 44, sx + 92, y + 52], fill=(250, 120, 40))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def card_servers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 230, 236))
    for r in range(3):
        for c in range(3):
            rx = x + 16 + c * ((w - 32) // 3)
            ry = y + 12 + r * ((h - 24) // 3)
            d.rectangle([rx, ry, rx + 34, ry + 20], fill=(52, 62, 80))
            for i in range(3):
                d.ellipse([rx + 4 + i * 9, ry + 13, rx + 9 + i * 9, ry + 18],
                          fill=(250, 90, 60) if (r + c + i) % 3 == 0 else (120, 220, 140))
    wx, wy = x + w - 44, y + 16
    d.polygon([(wx, wy + 30), (wx + 16, wy), (wx + 32, wy + 30)], fill=(250, 190, 40), outline=INK)
    d.text((wx + 13, wy + 12), "!", font=F(SANS_BOLD, 18), fill=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def card_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 224, 234))
    wy = y + h - 22
    d.rectangle([x, wy, x + w, y + h], fill=(60, 110, 155))
    sx = x + 30
    d.polygon([(sx, wy - 6), (sx + w - 60, wy - 6), (sx + w - 76, wy + 8), (sx + 14, wy + 8)], fill=(56, 60, 68))
    for i, cc in enumerate([(200, 70, 50), (60, 120, 180), (230, 170, 50)]):
        d.rectangle([sx + 16 + i * 44, wy - 24, sx + 56 + i * 44, wy - 6], fill=cc)
    for i, (fx, fh) in enumerate([(24, 14), (70, 18), (116, 12)]):
        d.polygon([(sx + fx, wy - 24), (sx + fx + 10, wy - 24 - fh), (sx + fx + 20, wy - 24)],
                  fill=(240, 120, 30) if i % 2 else (250, 180, 50))
    d.ellipse([sx + 64, wy - 52, sx + 92, wy - 38], fill=(90, 90, 95))
    d.ellipse([sx + 84, wy - 58, sx + 118, wy - 42], fill=(110, 110, 115))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def card_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    base = y + h - 26
    d.polygon([(x + 6, base), (x + 70, y + 30), (x + 140, base)], fill=(140, 120, 96))
    d.polygon([(x + 90, base), (x + 170, y + 18), (x + w - 8, base)], fill=(120, 102, 80))
    d.polygon([(x + 152, y + 34), (x + 170, y + 18), (x + 188, y + 34)], fill=(250, 250, 250))
    pts = []
    for i in range(9):  # seismograph trace
        px = x + 14 + i * ((w - 28) // 8)
        amp = [2, 3, 14, 26, 10, 20, 6, 3, 2][i]
        pts.append((px, y + h - 12 - amp))
    d.line(pts, fill=RED, width=3)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


LEAD = ("'EL CHAPO ISIDRO' TAKEN IN SINALOA",
        "Mexican special forces, acting on US intelligence, captured Fausto Isidro Meza Flores — one of "
        "the FBI's 10 most wanted — in Guasave, Sinaloa. The overnight firefight killed 11 people, four "
        "soldiers and seven cartel gunmen, and set off burning roadblocks across the state before he was "
        "flown to Mexico City. (AP, Reuters)")

CARDS = [
    ("CLIMATE TALKS RUN PAST THE DEADLINE",
     "COP31 in Antalya went deep into overtime, nearly 200 countries deadlocked over fossil fuels and "
     "finance; the draft dropped the phase-out language and a $120bn adaptation target. (Reuters)",
     scene_cop),
    ("IRAN MASSES TANKERS TO RUN THE BLOCKADE",
     "14+ Iranian tankers are assembling at Kharg Island to challenge the US naval blockade; two "
     "tankers were hit by projectiles near Hormuz. (UKMTO)", scene_tankers),
    ("KYIV'S BRIDGES POUNDED AFTER KERCH STRIKES",
     "Russia answered Ukraine's Crimean Bridge attacks with 400+ drones and 110+ missiles, hitting all "
     "three Dnipro bridges in Kyiv; eight people were killed. (Reuters)", card_bridges),
    ("HACKERS INSIDE THE FBI AND USDA",
     "The FBI is probing an intrusion into its NCIC crime database while a USDA farm-payment system was "
     "also breached; the US cyber chief was fired Thursday. (NBC, CNN)", card_servers),
    ("RUSSIAN CARGO SHIP BURNS IN THE BALTIC",
     "A Russian merchant ship caught fire in the Gulf of Finland after a reported drone strike; Finland "
     "tightened security. (Yle)", card_ship),
    ("6.8 QUAKE SHAKES PERU'S ANDES",
     "A magnitude 6.7–6.8 earthquake near Junín sent Lima residents into the streets; no casualties or "
     "major damage reported. (AP, USGS)", card_quake),
]

BRIEFS = [
    "Houthis report 70+ Saudi airstrikes across eight Yemeni areas; Saudi forces down three missiles and a drone.",
    "Tech selloff deepens: Anthropic shares slide after its record IPO; Trump demands Nvidia reinstate Jensen Huang.",
    "Israel: opposition leader Eisenkot invites Netanyahu's Likud to coalition talks.",
    "Denmark accuses Russia of plotting to assassinate a US-Ukrainian rapper; urges EU visa limits.",
    "Estonia to close road border crossings with Russia for six months.",
    "France: sixth Saturday of cost-of-living protests draws a smaller crowd of 82,500.",
    "Iraq: fire at a Basra power plant kills at least four, injures more than thirty.",
    "Nigeria: boat carrying mourners to a funeral sinks, 24 dead.",
    "Man convicted of starting the Palisades fire in Los Angeles.",
    "A lock of George Washington's hair sells for $4,000 at auction.",
    "Phumzile Mlambo-Ngcuka, South Africa's first female vice-president, dies aged 71.",
    "States agree to elaborate rules for AI 'killer robots' by 2028.",
    "Sudan: Tasis Alliance seizes the Bau region of Blue Nile; RSF accused of killing civilians.",
    "Modi at the SCO summit: civilizational links are the strongest guarantee of peace.",
    "Haiti signs a deal with El Salvador to build new prisons.",
    "Japanese forces to use Indian facilities for live-fire training for the first time.",
    "Crude oil futures fall more than 3% amid the Hormuz standoff.",
    "India: eleven die after drinking adulterated alcohol in Manipur.",
    "Melting Swiss ice reveals a 4,000-year-old bronze neck ring on an Alpine pass.",
    "FEMA's Washington office infested with bed bugs; 1,000+ staff told to work from home.",
    "Cyclone Akvan: fourteen flights cancelled at Ranchi airport.",
    "Gaza: seven Palestinians killed in Israeli attacks despite the ceasefire.",
    "England thrash the All Blacks in rugby; Arsenal held 2–2 at Newcastle.",
    "PSG beat Nice 3–2 but lose Doué to a serious injury.",
]

FIGURES = [("11", "dead in the Sinaloa raid"), ("6.8", "Peru quake magnitude"),
           ("400+", "drones in Russia's barrage"), ("14+", "tankers massed at Kharg"),
           ("$120bn", "adaptation target dropped"), ("82,500", "protesters in France")]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28

    # Masthead
    d.text((M, 12), "THE WORLD IN ONE DAY", font=F(SERIF_BLACK, 50), fill=INK)
    d.text((M, 70), "SUNDAY, 22 NOVEMBER 2026 · THE DAY'S WORLD NEWS ON ONE PAGE",
           font=F(SANS_BOLD, 15), fill=NAVY)
    d.text((M, 92), "A cartel kingpin falls, climate talks stall past their deadline, and tankers mass "
                    "against a blockade.", font=F(SERIF_REG, 16), fill=GREY)
    d.line([M, 116, W - M, 116], fill=RULE, width=3)
    d.line([M, 121, W - M, 121], fill=RULE, width=1)

    # Figure strip
    fy = 130
    fw = (W - 2 * M) // 6
    for i, (num, lab) in enumerate(FIGURES):
        fx = M + i * fw
        d.text((fx + 4, fy), num, font=F(SERIF_BLACK, 24), fill=RED if i in (0, 2) else NAVY)
        para(d, fx + 4, fy + 29, lab, F(SANS_REG, 10), fw - 10, 12, fill=GREY, max_lines=2)
    d.line([M, fy + 56, W - M, fy + 56], fill=RULE, width=1)

    # Lead story
    ly = fy + 66
    scene_w, scene_h = 430, 126
    scene_raid(d, M, ly, scene_w, scene_h)
    tx = M + scene_w + 16
    d.text((tx, ly), LEAD[0], font=F(SERIF_BLACK, 24), fill=INK)
    para(d, tx, ly + 32, LEAD[1], F(SANS_REG, 13), W - M - tx, 17, max_lines=6)
    d.line([M, ly + scene_h + 10, W - M, ly + scene_h + 10], fill=RULE, width=1)

    # Six cards, 3 x 2
    cy = ly + scene_h + 20
    cw = (W - 2 * M - 24) // 3
    for i, (head, body, scene) in enumerate(CARDS):
        cx = M + (i % 3) * (cw + 12)
        cyy = cy + (i // 3) * 164
        scene(d, cx, cyy, cw, 66)
        hy2 = para(d, cx, cyy + 70, head, F(SERIF_BOLD, 13), cw, 15, max_lines=2)
        para(d, cx, hy2 + 2, body, F(SANS_REG, 11), cw, 13, max_lines=4)
    by = cy + 2 * 164 + 4
    d.line([M, by, W - M, by], fill=RULE, width=1)

    # Briefs, 3 columns
    by += 8
    d.text((M, by), "THE DAY IN BRIEF", font=F(SANS_BOLD, 14), fill=NAVY)
    by += 20
    colw = (W - 2 * M - 24) // 3
    per = (len(BRIEFS) + 2) // 3
    for c in range(3):
        yy = by
        for j in range(per):
            idx = c * per + j
            if idx >= len(BRIEFS):
                break
            d.text((M + c * (colw + 12), yy), f"{idx + 1}.", font=F(SANS_BOLD, 10), fill=RED)
            yy = para(d, M + c * (colw + 12) + 18, yy, BRIEFS[idx], F(SANS_REG, 10), colw - 18, 12,
                      max_lines=2)
            yy += 2

    # Footer
    fy2 = H - 46
    d.line([M, fy2, W - M, fy2], fill=RULE, width=1)
    d.text((M, fy2 + 7), "DATE CHECK: every story above was reported on 22 November 2026 (in at least one "
                         "time zone). Older events are not shown as today's news.",
           font=F(SANS_BOLD, 10), fill=NAVY)
    d.text((M, fy2 + 23), "Sources: AP · Reuters · NBC · CNN · UKMTO · USGS · Yle · TankerTrackers",
           font=F(SANS_REG, 10), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
