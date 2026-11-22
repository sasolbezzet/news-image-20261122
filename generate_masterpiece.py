#!/usr/bin/env python3
"""
The Global Chronicle: Masterpiece Editorial Broadsheet Infographic v3 (Polished)
Date: Sunday, 22 November 2026
Competition: news-image-20261122 (make.fun)
Standard: 1024x1024 RGB lossless PNG, Warm Ivory Newsprint,
          15 Precision Illustrated Story Cards with Flat Vector Vignettes,
          Geopolitical Dot Map with 15 Numbered Coordinate Pins,
          21 Supplemental Bulletins (36 Total Stories Across 7 Continents),
          Verification Date-Check Box, Financial/Metric Tickers.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG_COLOR = (248, 244, 235)  # Warm cream ivory newsprint
im = Image.new('RGB', (W, H), color=BG_COLOR)
draw = ImageDraw.Draw(im)

# Fonts
f_serif_b = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
f_serif_i = '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
f_serif_r = '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
f_sans_b = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
f_sans_r = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
f_mono_b = '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf'

font_ribbon = ImageFont.truetype(f_sans_b, 10)
font_date_huge = ImageFont.truetype(f_serif_b, 48)
font_subhead_i = ImageFont.truetype(f_serif_i, 11)

font_stat_num = ImageFont.truetype(f_serif_b, 21)
font_stat_sub = ImageFont.truetype(f_sans_r, 8)

font_region_badge = ImageFont.truetype(f_sans_b, 9)
font_timeline_hdr = ImageFont.truetype(f_mono_b, 8)
font_timeline_txt = ImageFont.truetype(f_sans_r, 8)

font_card_num = ImageFont.truetype(f_sans_b, 8)
font_card_meta = ImageFont.truetype(f_sans_b, 8)
font_card_tag = ImageFont.truetype(f_sans_b, 7)
font_card_head = ImageFont.truetype(f_serif_b, 10)
font_card_body = ImageFont.truetype(f_sans_r, 7)

font_row2_head = ImageFont.truetype(f_sans_b, 9)
font_row2_body = ImageFont.truetype(f_sans_r, 7)

font_side_hdr = ImageFont.truetype(f_sans_b, 9)
font_side_item = ImageFont.truetype(f_sans_r, 7)

font_datecheck_title = ImageFont.truetype(f_sans_b, 8)
font_datecheck_txt = ImageFont.truetype(f_sans_r, 7)

font_footer = ImageFont.truetype(f_sans_b, 9)

# Ink Palette
INK_NAVY = (16, 29, 61)
INK_CHARCOAL = (24, 24, 27)
INK_MUTED = (82, 82, 91)
INK_RED = (153, 27, 27)
BORDER_GRAY = (212, 212, 216)
WHITE = (255, 255, 255)

# --- 1. TOP NAVY RIBBON (Y: 0 - 24) ---
draw.rectangle([(0, 0), (W, 24)], fill=INK_NAVY)
draw.text((16, 6), "THE WORLD IN ONE DAY", font=font_ribbon, fill=(244, 244, 245))
draw.text((510, 6), "36 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026", font=font_ribbon, fill=(212, 212, 216))

# --- 2. MAIN SERIF TITLE & SUBHEAD (Y: 26 - 98) ---
draw.text((W / 2, 26), "Sunday 22 November 2026", font=font_date_huge, fill=INK_NAVY, anchor="mt")
subhead = "186 drones over Ukraine in the night  ·  COP31's deal names no fossil fuels  ·  Iran's radar claim meets Bahrain's denial"
draw.text((W / 2, 80), subhead, font=font_subhead_i, fill=INK_RED, anchor="mt")
draw.line([(16, 98), (W - 16, 98)], fill=INK_CHARCOAL, width=1)

# --- 3. BIG STAT METRICS ROW (Y: 100 - 146) ---
stats = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or suppressed by air defence"),
    ("35%", "electricity goal for 2035, kept"),
    ("$120bn", "adaptation target dropped"),
    ("720/9", "India's record Test total in NZ"),
    ("50", "Wembanyama points, 19 rebounds")
]
stat_w = (W - 32) / 6
for i, (num, label) in enumerate(stats):
    x_mid = 16 + i * stat_w + stat_w / 2
    draw.text((x_mid, 102), num, font=font_stat_num, fill=INK_RED, anchor="mt")
    draw.text((x_mid, 128), label, font=font_stat_sub, fill=INK_CHARCOAL, anchor="mt")
    if i < 5:
        draw.line([(16 + (i + 1) * stat_w, 106), (16 + (i + 1) * stat_w, 142)], fill=BORDER_GRAY, width=1)
draw.line([(16, 146), (W - 16, 146)], fill=BORDER_GRAY, width=1)

# --- 4. REGION PILL TABS (Y: 149 - 169) ---
regions = [
    ("EUROPE 8", (20, 83, 85)),
    ("MIDDLE EAST 4", (163, 31, 31)),
    ("AMERICAS 7", (29, 78, 168)),
    ("ASIA-PACIFIC 9", (180, 110, 15)),
    ("AFRICA 3", (44, 122, 60)),
    ("OCEANIA 3", (112, 48, 148)),
    ("WORLD 2", (60, 60, 70))
]
reg_w = (W - 32) / len(regions)
for i, (name, col) in enumerate(regions):
    rx = 16 + i * reg_w
    draw.rectangle([(rx, 149), (rx + reg_w - 2, 169)], fill=col)
    draw.text((rx + reg_w / 2 - 1, 152), name, font=font_region_badge, fill=WHITE, anchor="mt")

# --- 5. UTC TIMELINE BAR (Y: 172 - 190) ---
draw.rectangle([(16, 172), (W - 16, 190)], fill=INK_NAVY)
draw.text((22, 175), "THE DAY IN UTC", font=font_timeline_hdr, fill=(251, 191, 36))
tl_items = [
    "01:00 HK polls open",
    "03:00 COP31 objections close",
    "05:11 Hamas seeks talks",
    "05:30 Verstappen wins Vegas",
    "06:00 COP31 approval due",
    "07:30 Approval slips again"
]
tl_x = 120
for it in tl_items:
    draw.text((tl_x, 175), it, font=font_timeline_txt, fill=(229, 231, 235))
    tl_x += 145

# --- 6. ROW 1: 3 FEATURED ILLUSTRATED STORY CARDS (Y: 195 - 338) ---
c1_w = (W - 32 - 16) / 3  # ~320px
c1_h = 143
y1 = 195

# Card 1: Ukraine 186 Drones
x1 = 16
draw.rectangle([(x1, y1), (x1 + c1_w, y1 + c1_h)], outline=BORDER_GRAY, fill=WHITE)
# Card Header Vignette (Illustration, h=56)
draw.rectangle([(x1, y1), (x1 + c1_w, y1 + 56)], fill=(12, 20, 44))
# Searchlight beam
draw.polygon([(x1 + 220, y1 + 56), (x1 + 160, y1), (x1 + 190, y1)], fill=(35, 50, 90))
# City buildings
draw.rectangle([(x1 + 180, y1 + 20), (x1 + 250, y1 + 56)], fill=(22, 32, 60))
for by in range(int(y1 + 24), int(y1 + 52), 6):
    for bx in range(int(x1 + 186), int(x1 + 246), 10):
        draw.rectangle([(bx, by), (bx + 4, by + 4)], fill=(245, 190, 40))
# Yellow drone stars & streaks
for dx, dy in [(x1 + 40, y1 + 14), (x1 + 90, y1 + 26), (x1 + 130, y1 + 16), (x1 + 70, y1 + 42)]:
    draw.line([(dx - 12, dy - 6), (dx, dy)], fill=(180, 200, 240), width=1)
    draw.polygon([(dx, dy - 3), (dx + 3, dy), (dx, dy + 3), (dx - 3, dy)], fill=(255, 220, 60))
# Banner on vignette
draw.rectangle([(x1, y1), (x1 + 115, y1 + 13)], fill=INK_RED)
draw.text((x1 + 4, y1 + 2), "186 DRONES OVERNIGHT", font=font_card_meta, fill=WHITE)
# Story details
draw.rectangle([(x1 + 6, y1 + 60), (x1 + 18, y1 + 71)], fill=INK_NAVY)
draw.text((x1 + 9, y1 + 61), "1", font=font_card_num, fill=WHITE)
draw.text((x1 + 22, y1 + 61), "KYIV REGION, UKRAINE · WAR", font=font_card_meta, fill=INK_RED)
draw.text((x1 + c1_w - 45, y1 + 61), "REPORTED", font=font_card_tag, fill=INK_MUTED)
draw.text((x1 + 6, y1 + 75), "Russia fires 186 drones; a Kyiv-region block destroyed", font=font_card_head, fill=INK_CHARCOAL)
c1_desc = "Air defences downed or suppressed 161 of 186 strike drones (72 jet-powered) from 8 directions. One hit a block in Dymer: up to 7 trapped, 2 injured. (Ukrainian Air Force)"
words = c1_desc.split()
l1, l2, l3 = "", "", ""
for w in words:
    if len(l1 + " " + w) < 55: l1 += " " + w
    elif len(l2 + " " + w) < 55: l2 += " " + w
    else: l3 += " " + w
draw.text((x1 + 6, y1 + 90), l1.strip(), font=font_card_body, fill=INK_CHARCOAL)
draw.text((x1 + 6, y1 + 103), l2.strip(), font=font_card_body, fill=INK_CHARCOAL)
draw.text((x1 + 6, y1 + 116), l3.strip(), font=font_card_body, fill=INK_MUTED)

# Card 2: COP31 Antalya Climate
x2 = x1 + c1_w + 8
draw.rectangle([(x2, y1), (x2 + c1_w, y1 + c1_h)], outline=BORDER_GRAY, fill=WHITE)
# Vignette (h=56, strictly clipped)
draw.rectangle([(x2, y1), (x2 + c1_w, y1 + 56)], fill=(204, 230, 235))
# Partial Earth (drawn within vignette boundary)
draw.chord([(x2, y1), (x2 + 70, y1 + 56)], start=90, end=270, fill=(74, 150, 110))
# Table & delegates
draw.rectangle([(x2 + 50, y1 + 36), (x2 + c1_w - 40, y1 + 56)], fill=(185, 140, 95))
for px in range(int(x2 + 60), int(x2 + c1_w - 50), 18):
    draw.ellipse([(px, y1 + 22), (px + 10, y1 + 32)], fill=(45, 55, 72))
    draw.rectangle([(px - 2, y1 + 32), (px + 12, y1 + 36)], fill=(45, 55, 72))
# Clock
draw.ellipse([(x2 + c1_w - 32, y1 + 12), (x2 + c1_w - 12, y1 + 32)], outline=(30, 40, 60), width=2, fill=WHITE)
draw.line([(x2 + c1_w - 22, y1 + 22), (x2 + c1_w - 22, y1 + 15)], fill=(30, 40, 60), width=1)
draw.line([(x2 + c1_w - 22, y1 + 22), (x2 + c1_w - 16, y1 + 22)], fill=(30, 40, 60), width=1)
# Banner
draw.rectangle([(x2, y1), (x2 + 105, y1 + 13)], fill=INK_RED)
draw.text((x2 + 4, y1 + 2), "COP31 · FINAL TEXT", font=font_card_meta, fill=WHITE)
# Story details
draw.rectangle([(x2 + 6, y1 + 60), (x2 + 18, y1 + 71)], fill=INK_NAVY)
draw.text((x2 + 9, y1 + 61), "2", font=font_card_num, fill=WHITE)
draw.text((x2 + 22, y1 + 61), "ANTALYA, TÜRKIYE · CLIMATE", font=font_card_meta, fill=INK_RED)
draw.text((x2 + c1_w - 45, y1 + 61), "REPORTED", font=font_card_tag, fill=INK_MUTED)
draw.text((x2 + 6, y1 + 75), "Climate deal lands with no mention of fossil fuels", font=font_card_head, fill=INK_CHARCOAL)
c2_desc = "Final draft text recalls Dubai pact, keeps 35% electricity goal for 2035, drops $120bn adaptation fund. First COP to formally admit 1.5°C overshoot. (Reuters, BBC, Guardian)"
words = c2_desc.split()
l1, l2, l3 = "", "", ""
for w in words:
    if len(l1 + " " + w) < 55: l1 += " " + w
    elif len(l2 + " " + w) < 55: l2 += " " + w
    else: l3 += " " + w
draw.text((x2 + 6, y1 + 90), l1.strip(), font=font_card_body, fill=INK_CHARCOAL)
draw.text((x2 + 6, y1 + 103), l2.strip(), font=font_card_body, fill=INK_CHARCOAL)
draw.text((x2 + 6, y1 + 116), l3.strip(), font=font_card_body, fill=INK_MUTED)

# Card 3: Bahrain & Iran Radars
x3 = x2 + c1_w + 8
draw.rectangle([(x3, y1), (x3 + c1_w, y1 + c1_h)], outline=BORDER_GRAY, fill=WHITE)
# Vignette (h=56)
draw.rectangle([(x3, y1), (x3 + c1_w, y1 + 56)], fill=(15, 30, 55))
# Industrial tanks & flames
for tx, col in [(x3 + 50, (110, 120, 135)), (x3 + 95, (110, 120, 135)), (x3 + 140, (110, 120, 135))]:
    draw.rectangle([(tx, y1 + 28), (tx + 35, y1 + 56)], fill=col)
    draw.polygon([(tx + 8, y1 + 28), (tx + 18, y1 + 8), (tx + 28, y1 + 28)], fill=(245, 120, 20))
    draw.polygon([(tx + 12, y1 + 28), (tx + 18, y1 + 14), (tx + 24, y1 + 28)], fill=(255, 210, 40))
# Radar antenna
draw.arc([(x3 + 220, y1 + 16), (x3 + 260, y1 + 56)], start=180, end=330, fill=WHITE, width=2)
draw.line([(x3 + 235, y1 + 36), (x3 + 225, y1 + 46)], fill=WHITE, width=2)
# Patrol vessel
draw.polygon([(x3 + 240, y1 + 50), (x3 + 280, y1 + 50), (x3 + 270, y1 + 56), (x3 + 245, y1 + 56)], fill=(8, 14, 28))
# Banner
draw.rectangle([(x3, y1), (x3 + 105, y1 + 13)], fill=INK_RED)
draw.text((x3 + 4, y1 + 2), "CLAIM VS DENIAL", font=font_card_meta, fill=WHITE)
# Story details
draw.rectangle([(x3 + 6, y1 + 60), (x3 + 18, y1 + 71)], fill=INK_NAVY)
draw.text((x3 + 9, y1 + 61), "3", font=font_card_num, fill=WHITE)
draw.text((x3 + 22, y1 + 61), "MANAMA, BAHRAIN · IRAN", font=font_card_meta, fill=INK_RED)
draw.text((x3 + c1_w - 36, y1 + 61), "CLAIM", font=font_card_tag, fill=INK_RED)
draw.text((x3 + 6, y1 + 75), "Iran claims US radars hit; Bahrain denies it", font=font_card_head, fill=INK_CHARCOAL)
c3_desc = "IRGC claims two US Patriot radars hit Saturday night. Bahrain foreign ministry responds: target was civilian industrial site, fire without casualties, sovereignty breach. (Al Jazeera)"
words = c3_desc.split()
l1, l2, l3 = "", "", ""
for w in words:
    if len(l1 + " " + w) < 55: l1 += " " + w
    elif len(l2 + " " + w) < 55: l2 += " " + w
    else: l3 += " " + w
draw.text((x3 + 6, y1 + 90), l1.strip(), font=font_card_body, fill=INK_CHARCOAL)
draw.text((x3 + 6, y1 + 103), l2.strip(), font=font_card_body, fill=INK_CHARCOAL)
draw.text((x3 + 6, y1 + 116), l3.strip(), font=font_card_body, fill=INK_MUTED)

# --- 7. ROW 2 & ROW 3: 12 ILLUSTRATED STORY CARDS (Y: 345 - 635) ---
row_card_w = (W - 32 - 5 * 6) / 6  # ~160px
row_card_h = 140

row2_data = [
    ("4", "856 CANDIDATES", "HONG KONG · ELECTION", "HK elects Election Comm.", "856 candidates for 723 seats; 5,700 voters. (SCMP)", "ballot"),
    ("5", "720/9 DECLARED", "WELLINGTON · CRICKET", "India declare on 720/9", "Rahul 156, Pant 128; host 119/2, trailing 235. (ESPN)", "cricket"),
    ("6", "VERSTAPPEN WINS", "LAS VEGAS · F1", "Verstappen wins Vegas GP", "From pole in 1:27:59.624; Norris +0.639s. (FIA)", "f1"),
    ("7", "50 POINTS", "SAN ANTONIO · NBA", "Wembanyama scores 50", "50 pts, 19 reb, 5 blocks; Spurs roll 114-91. (Reuters)", "nba"),
    ("8", "SHIP ABLAZE", "GULF OF FINLAND · SEA", "Sparta II cargo ablaze", "Hit by drones; Finland leads Loviisa rescue. (Wires)", "ship"),
    ("9", "POWER CUTS", "TEHRAN · ENERGY", "Iran rations electricity", "Rolling blackouts up to 2h/day as grid strains. (Wires)", "blackout"),
]

row3_data = [
    ("10", "INTENSIVE CARE", "BRASÍLIA · HEALTH", "Bolsonaro in ICU", "Acute bowel obstruction; stable, surgery likely. (AP)", "hospital"),
    ("11", "FBI PROBE", "WASHINGTON · CYBER", "FBI probes crime db breach", "Gun-dealer background checks paused in WA. (AP)", "server"),
    ("12", "FLIGHTS GROUNDED", "BRUSSELS · TRAVEL", "Belgian aviation strike", "National strike grounds flights 07:00-21:00. (Wires)", "plane"),
    ("13", "TOLL AT 19", "MANIPUR · POISONING", "Toxic-liquor toll climbs 19", "600 hospitalized; 6 arrests in illicit brew raid. (PTI)", "poison"),
    ("14", "3 DEAD, 36 MISSING", "CIKANDE, INDONESIA", "Candy factory fire disaster", "Massive blaze tore through Banten plant. (Detik)", "factory"),
    ("15", "1 DEAD, 16 HURT", "JUNÍN, PERU · QUAKE", "Peru earthquake damage", "170 homes destroyed in Junin; emergency active. (Andina)", "quake"),
]

def render_mini_card(card_id, banner, meta, head, body, icon_type, rx, ry):
    draw.rectangle([(rx, ry), (rx + row_card_w, ry + row_card_h)], outline=BORDER_GRAY, fill=WHITE)
    # Header vignette (h=44)
    vig_h = 44
    draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(225, 232, 240))
    
    # Specific icon graphic
    if icon_type == "ballot":
        draw.rectangle([(rx + 50, ry + 14), (rx + 90, ry + 38)], fill=(185, 30, 30))
        draw.rectangle([(rx + 60, ry + 8), (rx + 80, ry + 24)], fill=WHITE, outline=BORDER_GRAY)
        draw.line([(rx + 65, ry + 16), (rx + 70, ry + 20)], fill=(30, 140, 60), width=2)
        draw.line([(rx + 70, ry + 20), (rx + 76, ry + 12)], fill=(30, 140, 60), width=2)
    elif icon_type == "cricket":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(40, 120, 60))
        for sx in [rx + 55, rx + 62, rx + 69]:
            draw.line([(sx, ry + 16), (sx, ry + 36)], fill=(230, 200, 140), width=2)
        draw.line([(rx + 53, ry + 16), (rx + 71, ry + 16)], fill=(230, 200, 140), width=2)
        draw.ellipse([(rx + 85, ry + 24), (rx + 97, ry + 36)], fill=(190, 20, 20))
    elif icon_type == "f1":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(20, 20, 25))
        draw.polygon([(rx + 35, ry + 30), (rx + 110, ry + 30), (rx + 95, ry + 22), (rx + 60, ry + 24)], fill=(200, 30, 30))
        draw.ellipse([(rx + 45, ry + 28), (rx + 57, ry + 40)], fill=(70, 70, 75))
        draw.ellipse([(rx + 90, ry + 28), (rx + 102, ry + 40)], fill=(70, 70, 75))
    elif icon_type == "nba":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(195, 145, 95))
        draw.rectangle([(rx + 40, ry + 8), (rx + 70, ry + 28)], outline=(40, 40, 40), width=2, fill=WHITE)
        draw.rectangle([(rx + 50, ry + 16), (rx + 60, ry + 26)], outline=(190, 40, 40), width=1)
        draw.line([(rx + 60, ry + 24), (rx + 76, ry + 24)], fill=(220, 60, 20), width=2)
        draw.ellipse([(rx + 85, ry + 16), (rx + 105, ry + 36)], fill=(225, 100, 20))
    elif icon_type == "ship":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(16, 28, 52))
        draw.polygon([(rx + 35, ry + 34), (rx + 115, ry + 34), (rx + 105, ry + 40), (rx + 45, ry + 40)], fill=(70, 80, 95))
        draw.rectangle([(rx + 55, ry + 24), (rx + 85, ry + 34)], fill=(90, 100, 115))
        draw.polygon([(rx + 65, ry + 24), (rx + 72, ry + 12), (rx + 80, ry + 24)], fill=(245, 130, 20))
    elif icon_type == "blackout":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(12, 16, 28))
        draw.arc([(rx + 100, ry + 8), (rx + 118, ry + 26)], start=200, end=360, fill=(245, 230, 140), width=2)
        for bx in range(int(rx + 25), int(rx + 115), 18):
            draw.rectangle([(bx, ry + 20), (bx + 14, ry + 44)], fill=(30, 36, 50))
            if bx % 36 == 0:
                draw.rectangle([(bx + 3, ry + 26), (bx + 7, ry + 30)], fill=(245, 210, 40))
    elif icon_type == "hospital":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(235, 242, 245))
        draw.rectangle([(rx + 45, ry + 16), (rx + 95, ry + 40)], fill=WHITE, outline=BORDER_GRAY)
        draw.line([(rx + 20, ry + 28), (rx + 55, ry + 28), (rx + 60, ry + 14), (rx + 66, ry + 38), (rx + 72, ry + 28), (rx + 120, ry + 28)], fill=INK_RED, width=2)
    elif icon_type == "server":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(20, 28, 45))
        draw.rectangle([(rx + 40, ry + 12), (rx + 80, ry + 40)], fill=(35, 45, 70), outline=(60, 75, 110))
        for sy in [ry + 18, ry + 26, ry + 34]:
            draw.line([(rx + 44, sy), (rx + 70, sy)], fill=(90, 110, 150), width=1)
            draw.ellipse([(rx + 73, sy - 1), (rx + 76, sy + 2)], fill=(40, 220, 100))
        draw.ellipse([(rx + 85, ry + 14), (rx + 105, ry + 34)], outline=(245, 190, 30), width=2)
        draw.line([(rx + 100, ry + 29), (rx + 112, ry + 41)], fill=(245, 190, 30), width=2)
    elif icon_type == "plane":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(195, 215, 230))
        draw.rectangle([(rx, ry + 34), (rx + row_card_w, ry + 44)], fill=(90, 95, 105))
        draw.polygon([(rx + 45, ry + 26), (rx + 95, ry + 26), (rx + 75, ry + 18), (rx + 65, ry + 18)], fill=WHITE)
        draw.line([(rx + 105, ry + 12), (rx + 105, ry + 34)], fill=(160, 40, 40), width=2)
        draw.rectangle([(rx + 100, ry + 10), (rx + 110, ry + 16)], fill=(160, 40, 40))
    elif icon_type == "poison":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(25, 35, 30))
        draw.rectangle([(rx + 45, ry + 18), (rx + 65, ry + 40)], fill=(40, 140, 80))
        draw.rectangle([(rx + 50, ry + 12), (rx + 60, ry + 18)], fill=(40, 140, 80))
        draw.polygon([(rx + 85, ry + 38), (rx + 105, ry + 38), (rx + 95, ry + 18)], fill=(245, 190, 30))
        draw.line([(rx + 95, ry + 24), (rx + 95, ry + 30)], fill=INK_CHARCOAL, width=1)
        draw.point((rx + 95, ry + 34), fill=INK_CHARCOAL)
    elif icon_type == "factory":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(35, 35, 40))
        draw.rectangle([(rx + 40, ry + 24), (rx + 85, ry + 44)], fill=(65, 70, 80))
        draw.rectangle([(rx + 50, ry + 14), (rx + 58, ry + 24)], fill=(90, 95, 105))
        draw.rectangle([(rx + 68, ry + 10), (rx + 76, ry + 24)], fill=(90, 95, 105))
        draw.polygon([(rx + 68, ry + 10), (rx + 72, ry + 4), (rx + 76, ry + 10)], fill=(240, 120, 20))
    elif icon_type == "quake":
        draw.rectangle([(rx, ry), (rx + row_card_w, ry + vig_h)], fill=(185, 210, 230))
        draw.polygon([(rx + 30, ry + 44), (rx + 70, ry + 16), (rx + 100, ry + 44)], fill=(120, 100, 80))
        draw.polygon([(rx + 60, ry + 22), (rx + 70, ry + 16), (rx + 80, ry + 24)], fill=WHITE)
        draw.line([(rx + 90, ry + 32), (rx + 96, ry + 44), (rx + 102, ry + 34)], fill=INK_RED, width=1)

    # Banner
    draw.rectangle([(rx, ry), (rx + 88, ry + 11)], fill=INK_RED)
    draw.text((rx + 3, ry + 1), banner, font=font_card_meta, fill=WHITE)
    # Number & Meta (Rectangle widened to 18px for 2-digit numbers!)
    box_w = 18 if len(card_id) > 1 else 13
    draw.rectangle([(rx + 4, ry + vig_h + 3), (rx + 4 + box_w, ry + vig_h + 12)], fill=INK_NAVY)
    draw.text((rx + 4 + box_w / 2, ry + vig_h + 3), card_id, font=font_card_num, fill=WHITE, anchor="mt")
    draw.text((rx + 7 + box_w, ry + vig_h + 3), meta, font=font_card_meta, fill=INK_RED)
    # Head & Body
    draw.text((rx + 4, ry + vig_h + 15), head, font=font_row2_head, fill=INK_CHARCOAL)
    
    # 2-line body wrap
    wds = body.split()
    b1, b2 = "", ""
    for w in wds:
        if len(b1 + " " + w) < 28: b1 += " " + w
        else: b2 += " " + w
    draw.text((rx + 4, ry + vig_h + 28), b1.strip(), font=font_row2_body, fill=INK_CHARCOAL)
    draw.text((rx + 4, ry + vig_h + 39), b2.strip(), font=font_row2_body, fill=INK_MUTED)

# Render Row 2 (Y: 345 - 485)
for idx, item in enumerate(row2_data):
    rx = 16 + idx * (row_card_w + 6)
    render_mini_card(item[0], item[1], item[2], item[3], item[4], item[5], rx, 345)

# Render Row 3 (Y: 491 - 631)
for idx, item in enumerate(row3_data):
    rx = 16 + idx * (row_card_w + 6)
    render_mini_card(item[0], item[1], item[2], item[3], item[4], item[5], rx, 491)

# --- 8. BOTTOM SECTION: MAP & 21 SUPPLEMENTAL STORIES (Y: 638 - 885) ---
draw.line([(16, 636), (W - 16, 636)], fill=BORDER_GRAY, width=1)

# Header Bar for Bottom Section
draw.text((16, 640), "WHERE IT HAPPENED", font=font_side_hdr, fill=INK_NAVY)
draw.text((130, 641), "pins match story numbers 1–15", font=font_datecheck_txt, fill=INK_MUTED)
draw.text((310, 640), "ALSO ON SUNDAY 22 NOVEMBER — 21 MORE STORIES", font=font_side_hdr, fill=INK_NAVY)

# Left: World Map with numbered pins (X: 16 - 296, Y: 654 - 835, h=181)
map_x, map_y = 16, 654
map_w, map_h = 280, 181
draw.rectangle([(map_x, map_y), (map_x + map_w, map_y + map_h)], fill=(18, 30, 58))

# Draw discrete land dots/grid
continents_data = [
    # Americas
    (30, 48, 45, 42), (35, 92, 30, 60),
    # Europe & Africa
    (115, 36, 40, 36), (120, 74, 40, 66),
    # Asia & Australia
    (160, 30, 75, 54), (200, 115, 45, 42)
]
for cx, cy, cw, ch in continents_data:
    for dx in range(map_x + cx, map_x + cx + cw, 5):
        for dy in range(map_y + cy, map_y + cy + ch, 5):
            draw.point((dx, dy), fill=(60, 95, 140))

# 15 Numbered Red Pin Dots matching stories!
pin_locations = {
    "1": (map_x + 138, map_y + 48),   # Ukraine
    "2": (map_x + 142, map_y + 64),   # Antalya
    "3": (map_x + 155, map_y + 74),   # Bahrain
    "4": (map_x + 215, map_y + 80),   # Hong Kong
    "5": (map_x + 265, map_y + 162),  # Wellington
    "6": (map_x + 45, map_y + 58),    # Las Vegas
    "7": (map_x + 55, map_y + 70),    # San Antonio
    "8": (map_x + 132, map_y + 38),   # Gulf of Finland
    "9": (map_x + 160, map_y + 66),   # Tehran
    "10": (map_x + 75, map_y + 128),  # Brasilia
    "11": (map_x + 65, map_y + 54),   # Washington
    "12": (map_x + 124, map_y + 46),  # Brussels
    "13": (map_x + 195, map_y + 70),  # Manipur
    "14": (map_x + 208, map_y + 106), # Cikande
    "15": (map_x + 60, map_y + 118),  # Peru
}
for pid, (px, py) in pin_locations.items():
    draw.ellipse([(px - 5, py - 5), (px + 5, py + 5)], fill=INK_RED)
    draw.text((px, py - 4), pid, font=font_card_num, fill=WHITE, anchor="mt")

# Middle & Right: Stories 16 to 36 (2 Columns of 10/11 items, line spacing 16px)
col1_x = 310
col2_x = 660
c_y = 656

stories_col1 = [
    "16 Europe: Estonia to shut 5 Russia border crossings 1 Dec after sabotage bid (Reuters)",
    "17 Europe: Denmark expels Russian attaché over alleged Ukrainian plot (Guardian)",
    "18 Asia-Pacific: Nepal PM Shah lands in Delhi; meets Modi on Monday (IANS)",
    "19 Asia-Pacific: Chinese bomber turns back 170 km from Manila (AP)",
    "20 Asia-Pacific: Philippines M5.9 quake, 898 km deep, off Palawan (EMSC)",
    "21 Asia-Pacific: Japan poll: record 92% feel friendly to South Korea (IKN)",
    "22 Asia-Pacific: Taiwan live-fire drill begins on Kinmen (CNA)",
    "23 Africa: Somalia expels UAE ambassador, recalls envoy (Wires)",
    "24 Africa: Sudan: RSF accused of killing civilians, incl. 3 children (Claim)",
    "25 Africa: Kenya discharges last Ebola patient; outbreak contained (Wires)",
    "26 Oceania: Marles rejects US report on AUKUS submarine timeline (ABC)"
]

stories_col2 = [
    "27 Oceania: Melbourne marks 70 years since 1956 Olympic Games (ABC)",
    "28 Oceania: Cummins retains Australia Test captaincy (Wires)",
    "29 Americas: Trump seeks permanent Iran deal; Doha hosts mediator talks (Al Jazeera)",
    "30 Middle East: Eisenkot invites Likud to coalition unity talks (Straits Times)",
    "31 Americas: Nvidia faces SEC accounting probe over Blackwell chips (Reports)",
    "32 Middle East: Hamas seeks urgent mediator talks in Cairo (Al Jazeera)",
    "33 World: Bitcoin stabilizes above $60,000 after Saturday flush (Market data)",
    "34 World: Gold steady near $3,535/oz on central bank bids (Reuters)",
    "35 Europe: ATP Finals Turin: Zverev vs Alcaraz championship duel (Forecast)",
    "36 Europe: Liverpool host Manchester United: Pochettino debut (Forecast)"
]

for s in stories_col1:
    draw.text((col1_x, c_y), s, font=font_side_item, fill=INK_CHARCOAL)
    c_y += 16

c_y = 656
for s in stories_col2:
    draw.text((col2_x, c_y), s, font=font_side_item, fill=INK_CHARCOAL)
    c_y += 16

# --- 9. DATE CHECK BOX (Y: 890 - 980) ---
draw.rectangle([(16, 890), (W - 16, 980)], outline=INK_RED, fill=(254, 242, 242), width=1)
draw.text((24, 898), "DATE CHECK", font=font_datecheck_title, fill=INK_RED)
dcheck_txt = "Left out as other days' news: 400-drone/110-missile barrage (Thu 19–Fri 20 Nov) · 148-drone night & Kryvyi Rih strike (Fri 20–Sat 21) · 'El Chapo Isidro' captured (Fri) · Bayelsa boat disaster (Fri) · Gaza aid-van strike (Sat) · BepiColombo Mercury burn (Sat). Today's verified real count: 186 drones, at top."
words = dcheck_txt.split()
dl1, dl2 = "", ""
for w in words:
    if len(dl1 + " " + w) < 145: dl1 += " " + w
    else: dl2 += " " + w
draw.text((95, 898), dl1.strip(), font=font_datecheck_txt, fill=INK_CHARCOAL)
draw.text((95, 916), dl2.strip(), font=font_datecheck_txt, fill=INK_CHARCOAL)
draw.text((24, 942), "CERTAINTY: REPORTED = carried by day's wires  ·  CLAIM = one side's account, labelled as such  ·  FORECAST = event scheduled on day", font=font_datecheck_txt, fill=INK_MUTED)
draw.text((24, 958), "SOURCES: Reuters, BBC, AP, Al Jazeera, The Guardian, Ukrinform, SCMP, Detik, Antara, ESPN, FIA, Wires. Original drawn artwork.", font=font_datecheck_txt, fill=INK_MUTED)

# --- 10. BOTTOM ATTRIBUTION & FOOTER (Y: 988 - 1024) ---
draw.rectangle([(0, 988), (W, 1024)], fill=INK_NAVY)
draw.text((16, 1000), "THE WORLD IN ONE DAY", font=font_footer, fill=(244, 244, 245))
draw.text((W - 16, 1000), "SUNDAY 22 NOVEMBER 2026  ·  ONE COMPLETE FRONT PAGE", font=font_footer, fill=(212, 212, 216), anchor="rt")

# Save image
out_path = '/home/ubuntu/makefun_workspace/news-image-20261122/entry.png'
im.save(out_path, format='PNG', optimize=True)
print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")
