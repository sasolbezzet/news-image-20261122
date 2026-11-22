#!/usr/bin/env python3
"""
generate_broadsheet.py — make.fun competition entry "news-image-20261122".

Renders THE WORLD CHRONICLE, a 1024x1024 RGB front page for Sunday
22 November 2026: one global lead (COP31), a world situation map, a metric
strip and six panels carrying 36 dispatches across six continents.

The layout is measured (no character-count guessing), so long words cannot
spill out of a column. Output: ./entry.png, optimized, under 1 MiB.

    python3 generate_broadsheet.py
"""

from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# --- palette ---------------------------------------------------------------
PAPER = (247, 243, 233)
PANEL = (252, 249, 242)
INK = (26, 24, 22)
MUTED = (94, 88, 77)
FAINT = (140, 132, 118)
RULE = (176, 167, 151)
HAIR = (208, 199, 184)
RED = (169, 32, 42)
SEA = (238, 232, 219)
LAND = (221, 210, 188)

FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/Library/Fonts",
]


def font_path(bold: bool, serif: bool) -> str:
    names = []
    if serif:
        names += [
            "LiberationSerif-Bold.ttf" if bold else "LiberationSerif-Regular.ttf",
            "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf",
        ]
    else:
        names += [
            "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf",
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        ]
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    raise SystemExit("No usable serif/sans TrueType font found.")


_cache: dict[tuple[bool, bool, int], ImageFont.FreeTypeFont] = {}


def F(size: int, bold: bool = False, serif: bool = False):
    key = (bold, serif, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(font_path(bold, serif), size)
    return _cache[key]


# --- text helpers ----------------------------------------------------------
def tw(draw: ImageDraw.ImageDraw, text: str, font) -> float:
    return draw.textlength(text, font=font)


def wrap(draw, text: str, font, width: float) -> list[str]:
    """Greedy word wrap; hard-splits any single word wider than the column."""
    lines: list[str] = []
    cur = ""
    for word in text.split():
        while tw(draw, word, font) > width:  # pathological long token
            cut = len(word)
            while cut > 1 and tw(draw, word[:cut], font) > width:
                cut -= 1
            if cur:
                lines.append(cur)
                cur = ""
            lines.append(word[:cut])
            word = word[cut:]
        trial = f"{cur} {word}".strip()
        if tw(draw, trial, font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def ellipsize(draw, text: str, font, width: float) -> str:
    if tw(draw, text, font) <= width:
        return text
    cut = text
    while cut and tw(draw, cut + "\u2026", font) > width:
        cut = cut[:-1]
    return cut.rstrip(" ,.;:") + "\u2026"


def fit_lines(draw, text: str, font, width: float, max_lines: int) -> list[str]:
    lines = wrap(draw, text, font, width)
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    tail = " ".join(lines[max_lines - 1:]).strip()
    kept[-1] = ellipsize(draw, tail, font, width)
    return kept


def tracked(draw, xy, text: str, font, fill, tracking: float = 0.9):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += tw(draw, ch, font) + tracking
    return x


def tracked_width(draw, text: str, font, tracking: float = 0.9) -> float:
    return sum(tw(draw, c, font) + tracking for c in text) - tracking


def headline(draw, text: str, x: float, y: float, width: float, max_size: int,
             min_size: int, fill=INK, leading: float = 1.0) -> int:
    """Largest serif-bold size whose wrapped lines fit `width`; returns bottom y."""
    size = max_size
    while size > min_size:
        f = F(size, bold=True, serif=True)
        lines = wrap(draw, text, f, width)
        if max(tw(draw, ln, f) for ln in lines) <= width and len(lines) <= 3:
            break
        size -= 1
    f = F(size, bold=True, serif=True)
    lines = wrap(draw, text, f, width)
    cy = y
    for ln in lines:
        draw.text((x, cy), ln, font=f, fill=fill)
        cy += int(size * 1.06 * leading)
    return cy


# --- document --------------------------------------------------------------
im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)

d.rectangle([(0, 0), (W, H)], fill=PAPER)


def hairline(y: float, color=RULE, weight: int = 1):
    d.line([(24, y), (W - 24, y)], fill=color, width=weight)


# ===========================================================================
# 1. MASTHEAD
# ===========================================================================
hairline(16, INK, 2)

mast = F(43, bold=True, serif=True)
mast_text = "THE WORLD CHRONICLE"
mx = (W - tw(d, mast_text, mast)) / 2
d.text((mx, 22), mast_text, font=mast, fill=INK)

meta = F(7, bold=True)
d.text((26, 30), "VOL. XXVI  ·  NO. 326", font=meta, fill=MUTED)
d.text((26, 42), "MORNING EDITION", font=meta, fill=MUTED)
right_block = ["SUNDAY, 22 NOVEMBER 2026", "36 DISPATCHES · 6 CONTINENTS"]
for i, line in enumerate(right_block):
    d.text((W - 26 - tw(d, line, meta), 30 + i * 12), line, font=meta, fill=MUTED)

hairline(70, INK, 2)
d.text((26, 76), "GLOBAL CONSENSUS ROUND-UP  ·  ALL TIMES UTC", font=meta, fill=RED)
tag_r = "ONE WORLD, ONE FRONT PAGE"
d.text((W - 26 - tw(d, tag_r, meta), 76), tag_r, font=meta, fill=MUTED)
hairline(88, RULE, 1)

# ===========================================================================
# 2. GLOBAL LEAD + WORLD MAP
# ===========================================================================
LEAD_X, LEAD_Y, LEAD_W = 26, 96, 578

d.rectangle([(LEAD_X, LEAD_Y + 2), (LEAD_X + 54, LEAD_Y + 16)], fill=RED)
d.text((LEAD_X + 5, LEAD_Y + 4), "GLOBAL LEAD", font=F(7, bold=True), fill=PAPER)
d.text((LEAD_X + 62, LEAD_Y + 4),
       "ANTALYA, TÜRKİYE  ·  UNFCCC COP31", font=F(7, bold=True), fill=MUTED)

lead_y = headline(
    d,
    "COP31 Collapses in Historic Overtime Deadlock",
    LEAD_X, LEAD_Y + 22, LEAD_W, 31, 20,
)
deck = ("EU, Germany and Ireland refuse a final text that omits fossil-fuel "
        "phase-down, leaving the UN climate process without an agreed outcome.")
deck_f = F(9, serif=True)
deck_y = lead_y + 4
for ln in fit_lines(d, deck, deck_f, LEAD_W, 2):
    d.text((LEAD_X, deck_y), ln, font=deck_f, fill=MUTED)
    deck_y += 11

body_y = deck_y + 7
d.line([(LEAD_X, body_y), (LEAD_X + LEAD_W, body_y)], fill=HAIR, width=1)
body_y += 7

lead_body = (
    "The UN climate summit in Antalya ran far past its Friday deadline and "
    "closed without a plenary agreement, the first COP in the conference's "
    "history to end in open deadlock. The presidency's compromise draft "
    "dropped language on phasing down coal, oil and gas, prompting the "
    "European Union, Germany and Ireland to withhold support in the closing "
    "session while developing economies protested unfulfilled adaptation "
    "finance. Negotiators will reconvene in a technical working group, with "
    "loss-and-damage disbursement now the most contested file."
)
body_f = F(9, serif=True)
col_w = (LEAD_W - 18) / 2
lines = wrap(d, lead_body, body_f, col_w)
half = (len(lines) + 1) // 2
for ci, chunk in enumerate((lines[:half], lines[half:])):
    for li, ln in enumerate(chunk):
        d.text((LEAD_X + ci * (col_w + 18), body_y + li * 11), ln,
               font=body_f, fill=INK)
body_bottom = body_y + max(half, len(lines) - half) * 11
assert body_bottom < 302, f"lead overflow: {body_bottom}"

# --- world map -------------------------------------------------------------
MAP_X, MAP_Y, MAP_W, MAP_H = 622, 110, 378, 150
LAT_TOP, LAT_BOT = 82.0, -56.0

d.text((MAP_X, 96), "WORLD SITUATION MAP", font=F(7, bold=True), fill=INK)
d.text((MAP_X + MAP_W - tw(d, "22 NOV · 24:00 UTC", F(6, bold=True)), 97),
       "22 NOV · 24:00 UTC", font=F(6, bold=True), fill=FAINT)

d.rectangle([(MAP_X, MAP_Y), (MAP_X + MAP_W, MAP_Y + MAP_H)], fill=SEA,
            outline=HAIR, width=1)


def project(lon: float, lat: float) -> tuple[float, float]:
    x = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    y = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return (x, y)


LAND_SHAPES: list[list[tuple[float, float]]] = [
    # North America
    [(-168, 66), (-160, 71), (-140, 70), (-120, 70), (-100, 69), (-88, 70),
     (-80, 73), (-64, 60), (-55, 52), (-62, 47), (-70, 44), (-74, 40),
     (-76, 35), (-81, 26), (-83, 29), (-88, 30), (-94, 29), (-97, 26),
     (-99, 20), (-105, 20), (-112, 30), (-117, 33), (-122, 38), (-124, 44),
     (-130, 52), (-138, 58), (-150, 59), (-165, 60)],
    # Central America
    [(-92, 17), (-86, 16), (-83, 9), (-77, 8), (-79, 9), (-84, 12), (-90, 14)],
    # South America
    [(-77, 8), (-72, 11), (-62, 10), (-52, 5), (-44, -2), (-35, -6),
     (-38, -13), (-41, -22), (-48, -26), (-54, -34), (-58, -38), (-62, -41),
     (-65, -50), (-68, -54), (-74, -52), (-73, -45), (-73, -37), (-71, -30),
     (-70, -20), (-76, -14), (-81, -6), (-80, 0), (-78, 4)],
    # Africa
    [(-17, 15), (-16, 21), (-10, 27), (0, 32), (10, 33), (11, 37), (20, 32),
     (25, 32), (34, 31), (35, 28), (43, 12), (51, 12), (43, 1), (41, -10),
     (40, -16), (35, -24), (31, -30), (27, -34), (20, -35), (16, -29),
     (12, -18), (9, -1), (5, 5), (-8, 4), (-13, 9)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (1, 51), (6, 53), (9, 57), (11, 59),
     (6, 62), (15, 69), (28, 70), (40, 68), (60, 70), (75, 73), (100, 76),
     (120, 74), (140, 72), (160, 69), (170, 66), (180, 65), (180, 60),
     (160, 59), (145, 53), (140, 45), (130, 42), (126, 35), (122, 30),
     (118, 24), (110, 20), (105, 10), (100, 4), (98, 8), (96, 16), (90, 22),
     (80, 15), (77, 8), (72, 20), (60, 25), (57, 25), (48, 30), (43, 12),
     (35, 28), (32, 31), (28, 41), (20, 40), (14, 38), (12, 45), (3, 43)],
    # Greenland
    [(-45, 60), (-58, 60), (-55, 68), (-45, 76), (-30, 82), (-22, 70), (-40, 60)],
    # British Isles
    [(-5, 50), (1, 51), (1, 55), (-2, 58), (-5, 58), (-6, 54)],
    # Japan
    [(130, 32), (136, 35), (141, 40), (145, 44), (142, 45), (138, 37), (132, 34)],
    # Indonesia
    [(95, 5), (105, -6), (115, -8), (120, -9), (130, -8), (141, -8),
     (140, -2), (131, -1), (125, 2), (115, 4), (105, 0), (96, 3)],
    # Australia
    [(114, -22), (113, -27), (116, -35), (129, -32), (138, -35), (146, -39),
     (150, -35), (153, -28), (145, -15), (137, -12), (130, -11), (125, -14),
     (114, -18)],
    # New Zealand
    [(173, -35), (178, -38), (174, -41), (171, -44), (167, -46), (169, -42),
     (172, -38)],
]

for shape in LAND_SHAPES:
    pts = [project(lon, lat) for lon, lat in shape]
    d.polygon(pts, fill=LAND, outline=(96, 88, 76))

# equator
eq_y = project(0, 0)[1]
for gx in range(int(MAP_X) + 6, int(MAP_X + MAP_W) - 6, 7):
    d.line([(gx, eq_y), (gx + 3, eq_y)], fill=(150, 140, 122), width=1)

PINNED = [
    ("1", 30.7, 36.9, "ANTALYA·COP31"),
    ("2", 23.9, 59.9, "BALTIC·SPARTA II"),
    ("3", 30.5, 50.4, "KYIV"),
    ("4", 56.6, 26.3, "HORMUZ"),
    ("5", 106.1, -6.1, "BANTEN"),
    ("6", 77.2, 28.6, "NEW DELHI"),
]
for num, lon, lat, _ in PINNED:
    px, py = project(lon, lat)
    d.ellipse([(px - 4.6, py - 4.6), (px + 4.6, py + 4.6)], fill=RED,
              outline=PAPER, width=1)
    nf = F(6, bold=True)
    nx = px - tw(d, num, nf) / 2
    d.text((nx, py - 4.2), num, font=nf, fill=PAPER)

legend_f = F(6, bold=True)
for i, (num, _, _, label) in enumerate(PINNED):
    col, row = i % 3, i // 3
    lx = MAP_X + col * (MAP_W / 3)
    ly = MAP_Y + MAP_H + 5 + row * 9
    d.text((lx, ly), num, font=legend_f, fill=RED)
    d.text((lx + 7, ly), ellipsize(d, label, legend_f, MAP_W / 3 - 10),
           font=legend_f, fill=MUTED)

d.text((MAP_X, MAP_Y + MAP_H + 24), "Colour: conflict / climate / commerce",
       font=F(6, serif=True), fill=FAINT)

# ===========================================================================
# 3. METRIC STRIP
# ===========================================================================
STRIP_Y = 310
hairline(STRIP_Y, INK, 2)
metrics = [
    ("196", "delegations in Antalya did not adopt a text"),
    ("2,700", "drones launched at Ukraine this week"),
    ("36", "daily Panama Canal transit slots restored"),
    ("1.5m", "years of ice archived at Little Dome C"),
]
mw = (W - 52) / 4
for i, (val, lab) in enumerate(metrics):
    x = 26 + i * mw
    vf = F(21, bold=True, serif=True)
    d.text((x, STRIP_Y + 6), val, font=vf, fill=INK)
    lf = F(7, bold=True)
    for j, ln in enumerate(fit_lines(d, lab, lf, mw - 16, 2)):
        d.text((x, STRIP_Y + 31 + j * 9), ln, font=lf, fill=MUTED)
    if i:
        d.line([(x - 12, STRIP_Y + 7), (x - 12, STRIP_Y + 44)], fill=HAIR, width=1)
hairline(STRIP_Y + 47, INK, 1)

# ===========================================================================
# 4. SIX PANELS  ·  36 DISPATCHES
# ===========================================================================
PANELS = [
    ("EUROPE & THE BALTIC", [
        ("Sparta II Burns off Finland",
         "A Russian cargo ship is ablaze near Hanko after a drone strike; Helsinki calls it a grave Baltic escalation."),
        ("Drone Wave Hits Kyiv Outskirts",
         "Residential blocks struck in Dymer as air defences repel one of the war's heaviest overnight barrages."),
        ("Youth Protests on Living Costs",
         "Tens of thousands march in Berlin, Rome and London against rents, austerity and rising defence budgets."),
        ("EU Studies Frozen-Asset Loan",
         "Brussels negotiates a reparations-backed credit for Kyiv as member states argue over legal exposure."),
        ("Berlin's Budget Coalition Test",
         "The ruling parties trade spending demands as the 2027 draft heads for a Bundestag vote this week."),
        ("Corridor X Rail Deal Signed",
         "Balkan states finalise a modernised freight line linking Central Europe to the port of Thessaloniki."),
    ]),
    ("MIDDLE EAST & AFRICA", [
        ("US and Israel Plan on Iran",
         "Officials confirm joint operational planning on nuclear sites while Washington pushes a new pact."),
        ("Gaza's Rubble and Rescue Gap",
         "Civil defence crews lack heavy machinery as debris from the war is estimated above 50 million tonnes."),
        ("Tanker Alerts Near Hormuz",
         "Commercial ships report radio warnings in the Gulf; insurers raise war-risk premiums on transits."),
        ("Sudan Aid Convoy Reaches Darfur",
         "A UN convoy enters El Fasher after weeks of blockade, the first relief delivery since the truce."),
        ("Sahel Bloc Debates Joint Force",
         "AES ministers meet in Niamey on a shared border command as insurgencies push toward coastal states."),
        ("Lagos Coastal Barrier Funded",
         "Nigeria secures multilateral financing for flood defences protecting four million residents."),
    ]),
    ("ASIA-PACIFIC & SOUTH ASIA", [
        ("Candy Factory Fire Kills Dozens",
         "A blaze at a Serang, Banten confectionery plant traps night-shift workers; a safety inquiry opens."),
        ("Jaishankar Meets Nepal's Shah",
         "New Delhi talks cover cross-border power trade, rail links and stability after Kathmandu's transition."),
        ("Tokyo Backs 2nm Semiconductor Line",
         "METI approves a fresh subsidy package for advanced fabrication and chip packaging capacity."),
        ("Patrols Continue in South China Sea",
         "Coast guards shadow survey vessels near the Spratlys as Manila protests water-cannon use."),
        ("Bangladesh Garment Wage Talks",
         "Factory owners and unions resume negotiations after strikes halt output at export hubs."),
        ("Pacific Islands Seek Relocation Fund",
         "Forum leaders press donors for dedicated climate-migration financing as sea-level rise accelerates."),
    ]),
    ("THE AMERICAS", [
        ("Transition Team Drafts Orders",
         "Incoming US officials prepare day-one executive actions on energy permits, tariffs and immigration."),
        ("Border Sensor Grid Expands",
         "Autonomous towers and ground radar go live across southern sectors under a new surveillance contract."),
        ("Panama Canal Adds Transit Slots",
         "The authority lifts daily bookings to 36 vessels as Gatun Lake recovers from a wet season."),
        ("Brazil Cerrado Fund Cleared",
         "A $350m conservation facility ties soy traceability to cheaper rural credit for growers."),
        ("California Snowpack Above Median",
         "Surveys report 112% of average water content, easing drought restrictions into the spring."),
        ("Haiti Mission Mandate Debated",
         "Regional bloc weighs extending the multinational police mission as gang violence displaces thousands."),
    ]),
    ("OCEANIA & THE POLAR REGIONS", [
        ("Sydney Battery Park Goes Live",
         "Australia's largest grid battery begins commercial dispatch, firming 1.4GW of solar capacity."),
        ("New Zealand Alpine Road Reopens",
         "Engineers finish slope repairs on the South Island highway cut by spring landslides."),
        ("PNG Launches Measles Campaign",
         "Health teams reach highland provinces with a catch-up vaccination drive after outbreak reports."),
        ("Antarctic Sea Ice at a New Low",
         "Satellite records show November extent far below the long-term mean for a fifth straight year."),
        ("Ice Core Reaches 1.5 Million Years",
         "Drillers extract a continuous climate archive at Little Dome C, targeting ancient air bubbles."),
        ("Krill Catch Quotas Cut",
         "Commission members reduce limits near the Antarctic Peninsula after survey declines."),
    ]),
    ("SCIENCE, SPACE & TECHNOLOGY", [
        ("DeepSeek-V4 Reasoning Breakthrough",
         "The open-weight model posts frontier scores in maths and code while cutting inference cost."),
        ("BepiColombo Returns Mercury Data",
         "The ESA-JAXA orbiter sends magnetic-field telemetry from its closest flyby of the planet yet."),
        ("5,000-Qubit Routing Demonstrated",
         "A commercial annealing system solves logistics routing at scales once reserved for supercomputers."),
        ("Fusion Magnet Holds 20 Tesla",
         "A compact tokamak sustains steady-state confinement, a milestone for net-energy designs."),
        ("Mars Sample Return Rescoped",
         "Agencies converge on a leaner architecture to bring cached tubes home in the 2030s."),
        ("Oral Obesity Drug Matches Jabs",
         "Late-stage trial results show a GLP-1 pill delivering injection-level weight loss over 68 weeks."),
    ]),
]

PANEL_W, PANEL_H = 472, 202
GAP_X, GAP_Y = 28, 12
GRID_TOP = 366

for idx, (region, stories) in enumerate(PANELS):
    col, row = idx % 2, idx // 2
    px = 26 + col * (PANEL_W + GAP_X)
    py = GRID_TOP + row * (PANEL_H + GAP_Y)

    d.rectangle([(px, py), (px + PANEL_W, py + PANEL_H)], fill=PANEL,
                outline=HAIR, width=1)
    d.rectangle([(px, py), (px + PANEL_W, py + 17)], fill=INK)
    d.text((px + 7, py + 4), region, font=F(8, bold=True), fill=PAPER)
    count_lbl = "6 DISPATCHES"
    d.text((px + PANEL_W - 7 - tw(d, count_lbl, F(6, bold=True)), py + 5),
           count_lbl, font=F(6, bold=True), fill=(196, 186, 170))

    inner_x = px + 9
    inner_w = PANEL_W - 18
    sub_w = (inner_w - 14) / 2
    body_top = py + 24
    cell_h = (PANEL_H - 30) / 3

    for si, (title, text) in enumerate(stories):
        sc, sr = si % 2, si // 2
        sx = inner_x + sc * (sub_w + 14)
        sy = body_top + sr * cell_h

        d.line([(sx, sy), (sx + sub_w, sy)], fill=HAIR, width=1)
        tf = F(9, bold=True)
        title_lines = fit_lines(d, title, tf, sub_w, 2)
        ty = sy + 4
        for ln in title_lines:
            d.text((sx, ty), ln, font=tf, fill=RED if si == 0 else INK)
            ty += 10
        bf = F(8, serif=True)
        by = ty + 1
        for ln in fit_lines(d, text, bf, sub_w, 2 if len(title_lines) > 1 else 3):
            d.text((sx, by), ln, font=bf, fill=(58, 54, 48))
            by += 9
        assert by <= py + PANEL_H, f"panel {region} overflow at story {si}"

# ===========================================================================
# 5. FOOTER
# ===========================================================================
FY = 994
hairline(FY, INK, 2)
foot_f = F(6, bold=True)
d.text((26, FY + 8), "THE WORLD CHRONICLE  ·  22 NOVEMBER 2026  ·  36 DISPATCHES ACROSS SIX CONTINENTS",
       font=foot_f, fill=MUTED)
d.text((26, FY + 18), "Compiled from wire-service consensus reporting at 24:00 UTC. No advertising.",
       font=F(6, serif=True), fill=FAINT)
right = "MAKE.FUN COMPETITION ENTRY"
d.text((W - 26 - tw(d, right, foot_f), FY + 8), right, font=foot_f, fill=RED)
right2 = "NEWS-IMAGE-20261122"
d.text((W - 26 - tw(d, right2, foot_f), FY + 18), right2, font=foot_f, fill=FAINT)

# ===========================================================================
# 6. SAVE + SELF-CHECK
# ===========================================================================
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
im.save(out, format="PNG", optimize=True)

size = os.path.getsize(out)
with Image.open(out) as chk:
    assert chk.size == (1024, 1024), chk.size
    assert chk.mode == "RGB", chk.mode
assert size <= 1024 * 1024, size

print(f"entry.png  {im.size[0]}x{im.size[1]} {im.mode}  {size/1024:.1f} KiB  "
      f"({size} bytes)  budget 1024 KiB")
sys.exit(0)
