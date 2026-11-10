"""Redrawn Equality Engine game board (after Figure 1 of the paper)."""
from common import *

W, H = 1040, 760
d = Doc(W, H, "The Equality Engine game board. A hiring system's pipeline runs in a loop from the state of "
               "the world to a sample, a dataset, algorithms, and job applications, and each stage has a card "
               "slot for its bias type: historical, representation, measurement, modeling, and deployment. "
               "The corners hold the Discover Bias and Debias decks, the Take Actions areas (student pool +10, "
               "preventive measure +30), and a leaderboard.")
arrow_marker(d, "arw", STONE, 12)

# board surface
d(f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="26" fill="{BOARD}" stroke="{mix(INK, BOARD, 0.12)}" stroke-width="1.5"/>')

CX, CY, R, NR = 520, 388, 178, 46
STAGE_ANGLES = [-90, -162, -234, -306, -378]

def pt(a, r=R):
    return CX + r * math.cos(math.radians(a)), CY + r * math.sin(math.radians(a))

nodes = [pt(a) for a in STAGE_ANGLES]

# track + flow arrows
d(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{mix(FACE, BOARD, 0.75)}" stroke-width="30"/>')
d(f'<circle cx="{CX}" cy="{CY}" r="{R + 15}" fill="none" stroke="{LINE}" stroke-width="1"/>')
d(f'<circle cx="{CX}" cy="{CY}" r="{R - 15}" fill="none" stroke="{LINE}" stroke-width="1"/>')
GAP = 19
for i, a in enumerate(STAGE_ANGLES):
    b = STAGE_ANGLES[i + 1] if i + 1 < len(STAGE_ANGLES) else -450
    (x1, y1), (x2, y2) = pt(a - GAP), pt(b + GAP)
    d(f'<path d="M{f1(x1)} {f1(y1)}A{R} {R} 0 0 0 {f1(x2)} {f1(y2)}" fill="none" stroke="{STONE}" '
      f'stroke-width="2" stroke-linecap="round" marker-end="url(#arw)"/>')

# centre caption
d.text(CX, CY - 4, "HIRING PIPELINE", 11.5, CLAY, wt=600, anchor="middle", ls=2.2)
d.text(CX, CY + 20, "where bias creeps in", 19, INK_SOFT, fam="serif_it", anchor="middle")

# ---------- stage nodes ----------
for i, (x, y) in enumerate(nodes):
    d.defs.append(f'<clipPath id="n{i}"><circle cx="{f1(x)}" cy="{f1(y)}" r="{NR - 2}"/></clipPath>')
    d(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{NR}" fill="{FACE}" stroke="{INK}" stroke-width="1.8"/>')

# 0 state of the world: a varied crowd
x, y = nodes[0]
d(f'<g clip-path="url(#n0)">')
crowd = [(-19, -17, 6.2, 0), (0, -21, 6.2, 2), (19, -17, 6.2, 4), (-10, -3, 7.6, 1), (10, -3, 7.6, 3)]
for dx, dy, r, t in crowd:
    person(d, x + dx, y + dy, r, TONES[t], ring=FACE)
d("</g>")

# 1 sample: three people drawn from the crowd
x, y = nodes[1]
d(f'<g clip-path="url(#n1)">')
for dx, dy, r, t in [(-13, -13, 7, 2), (13, -13, 7, 4), (0, -5, 8.4, 1)]:
    person(d, x + dx, y + dy, r, TONES[t], ring=FACE)
d("</g>")

# 2 dataset: a database cylinder
x, y = nodes[2]
top, rx, ry = y - 18, 19, 6.5
d(f'<path d="M{f1(x - rx)} {f1(top)}V{f1(top + 36)}A{rx} {ry} 0 0 0 {f1(x + rx)} {f1(top + 36)}V{f1(top)}Z" '
  f'fill="{FACE}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
for k in (1, 2):
    yb = top + 12 * k
    d(f'<path d="M{f1(x - rx)} {f1(yb)}A{rx} {ry} 0 0 0 {f1(x + rx)} {f1(yb)}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
d(f'<ellipse cx="{f1(x)}" cy="{f1(top)}" rx="{rx}" ry="{ry}" fill="{PAPER_DEEP}" stroke="{INK}" stroke-width="1.8"/>')
for k in range(3):
    d(f'<circle cx="{f1(x + 10)}" cy="{f1(top + 12 * k + 10.5)}" r="1.9" fill="{CLAY}"/>')

# 3 algorithms: a small neural network
x, y = nodes[3]
layers = [(-18, [-13, 0, 13]), (0, [-18, -6, 6, 18]), (18, [-7, 7])]
for (xa, ya_list), (xb, yb_list) in zip(layers, layers[1:]):
    for ya in ya_list:
        for yb in yb_list:
            d(f'<line x1="{f1(x + xa)}" y1="{f1(y + ya)}" x2="{f1(x + xb)}" y2="{f1(y + yb)}" stroke="{SAND}" stroke-width="1.2"/>')
for li, (xa, ys) in enumerate(layers):
    for ya in ys:
        d(f'<circle cx="{f1(x + xa)}" cy="{f1(y + ya)}" r="4" fill="{CLAY if li == 2 else INK}"/>')

# 4 job applications: a résumé that gets a decision
x, y = nodes[4]
x0, y0, dw, dh = x - 19, y - 22, 34, 44
d(f'<path d="M{f1(x0)} {f1(y0 + 3)}Q{f1(x0)} {f1(y0)} {f1(x0 + 3)} {f1(y0)}H{f1(x0 + dw - 9)}L{f1(x0 + dw)} {f1(y0 + 9)}'
  f'V{f1(y0 + dh - 3)}Q{f1(x0 + dw)} {f1(y0 + dh)} {f1(x0 + dw - 3)} {f1(y0 + dh)}H{f1(x0 + 3)}Q{f1(x0)} {f1(y0 + dh)} '
  f'{f1(x0)} {f1(y0 + dh - 3)}Z" fill="{FACE}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
d(f'<circle cx="{f1(x0 + 10)}" cy="{f1(y0 + 12)}" r="4.6" fill="{TONES[4]}"/>')
d(f'<rect x="{f1(x0 + 18)}" y="{f1(y0 + 9)}" width="9" height="2.6" rx="1.3" fill="{SAND}"/>')
d(f'<rect x="{f1(x0 + 18)}" y="{f1(y0 + 14)}" width="7" height="2.6" rx="1.3" fill="{SAND}"/>')
for k in range(3):
    d(f'<rect x="{f1(x0 + 6)}" y="{f1(y0 + 23 + 6 * k)}" width="{22 - 5 * (k == 2)}" height="2.6" rx="1.3" fill="{SAND}"/>')
bx, by = x + 15, y + 15
d(f'<circle cx="{f1(bx)}" cy="{f1(by)}" r="10" fill="{CLAY}" stroke="{FACE}" stroke-width="2.5"/>')
d(f'<path d="M{f1(bx - 4.2)} {f1(by + 0.2)}L{f1(bx - 1.2)} {f1(by + 3.2)}L{f1(bx + 4.4)} {f1(by - 3)}" fill="none" '
  f'stroke="{FACE}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')

# ---------- stage labels (inside the ring) ----------
SL = 22
(x, y) = nodes[0]; d.text(x, y + NR + 27, "State of the world", SL, INK, fam="serif", anchor="middle")
(x, y) = nodes[1]; d.text(x + NR + 13, y + 6, "Sample", SL, INK, fam="serif")
(x, y) = nodes[2]; d.text(x, y - NR - 13, "Dataset", SL, INK, fam="serif", anchor="middle")
(x, y) = nodes[3]; d.text(x, y - NR - 13, "Algorithms", SL, INK, fam="serif", anchor="middle")
(x, y) = nodes[4]
d.text(x - NR - 13, y - 5, "Job", SL, INK, fam="serif", anchor="end")
d.text(x - NR - 13, y + 17, "applications", SL, INK, fam="serif", anchor="end")

# ---------- bias trays (outside the ring) ----------
SW_, SH_, SG = 36, 50, 8
LBL = 16

def tray(cat, cx, top):
    d.text(cx, top + 15, f"{cat['name']} bias", LBL, cat["dark"], wt=600, anchor="middle")
    x = cx - (3 * SW_ + 2 * SG) / 2
    for k in range(3):
        fill = cat["tint2"] if k == 0 else FACE
        dash = "" if k == 0 else ' stroke-dasharray="4 3.5"'
        d(f'<rect x="{f1(x + k * (SW_ + SG))}" y="{f1(top + 27)}" width="{SW_}" height="{SH_}" rx="5" fill="{fill}" '
          f'stroke="{cat["color"]}" stroke-width="1.6"{dash}/>')
    # a hint of the card already placed in the first slot
    d(f'<rect x="{f1(x + 7)}" y="{f1(top + 27 + 9)}" width="{SW_ - 14}" height="3" rx="1.5" fill="{cat["color"]}" opacity=".55"/>')
    d(f'<rect x="{f1(x + 7)}" y="{f1(top + 27 + 16)}" width="{SW_ - 20}" height="3" rx="1.5" fill="{cat["color"]}" opacity=".35"/>')

def tray_half(cat):
    return max(sw(f"{cat['name']} bias", LBL, 600), 3 * SW_ + 2 * SG) / 2

TRAY_H = 27 + SH_
x, y = nodes[0]; tray(CATS[0], x, y - NR - 20 - TRAY_H)
x, y = nodes[1]; tray(CATS[1], x - NR - 18 - tray_half(CATS[1]), y - TRAY_H / 2 - 2)
x, y = nodes[2]; tray(CATS[2], x - 12, y + NR + 20)
x, y = nodes[3]; tray(CATS[3], x + 12, y + NR + 20)
x, y = nodes[4]; tray(CATS[4], x + NR + 18 + tray_half(CATS[4]), y - TRAY_H / 2 - 2)

# ---------- corner zones ----------
ZW, ZH = 250, 180
def zone(x, y, w, h):
    d(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{FACE}" stroke="{LINE}" stroke-width="1.2"/>')

def header(x, y, w, n, title, pts):
    badge(d, x + 26, y + 30, n)
    d.text(x + 48, y + 35.5, title, 16.5, INK, wt=600)
    pill(d, x + w - 18, y + 19, pts, anchor="end")

def deck(x, y, fill, label, label_fill, size):
    for k, t in ((2, 0.45), (1, 0.72)):
        d(f'<rect x="{x + 4 * k}" y="{y - 4 * k}" width="72" height="98" rx="8" fill="{mix(fill, FACE, t)}"/>')
    d(f'<rect x="{x}" y="{y}" width="72" height="98" rx="8" fill="{fill}"/>')
    d(f'<rect x="{x + 5}" y="{y + 5}" width="62" height="88" rx="5" fill="none" stroke="{label_fill}" stroke-opacity=".35" stroke-width="1"/>')
    d.text(x + 36, y + 56, label, size, label_fill, fam="serif", anchor="middle")

def deposit(x, y):
    d(f'<rect x="{x}" y="{y}" width="72" height="98" rx="8" fill="none" stroke="{STONE}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    d(f'<path d="M{x + 36} {y + 34}v18m-6-6l6 6l6-6" fill="none" stroke="{SAND}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    d.text(x + 36, y + 72, "DEPOSIT", 10, STONE, wt=600, anchor="middle", ls=1.2)

# 1 Discover bias (top left)
zx, zy = 26, 26
zone(zx, zy, ZW, ZH); header(zx, zy, ZW, 1, "Discover bias", "+5")
deck(zx + 52, zy + 66, CLAY, "Bias", FACE, 27); deposit(zx + 140, zy + 66)

# 2 Debias (top right)
zx = W - 26 - ZW
zone(zx, zy, ZW, ZH); header(zx, zy, ZW, 2, "Debias", "+5")
deck(zx + 52, zy + 66, INK, "Debias", SOFT_ACCENT, 22); deposit(zx + 140, zy + 66)

# Leaderboard (bottom left)
ZH2 = 196
zx, zy = 26, H - 26 - ZH2
zone(zx, zy, ZW, ZH2)
cx, cy = zx + 26, zy + 30
d(f'<path d="M{cx - 7} {cy - 7}h14v4a7 7 0 0 1-14 0z" fill="{CLAY}"/>'
  f'<path d="M{cx - 7} {cy - 5}h-3.5a3.5 3.5 0 0 0 3.5 4.5M{cx + 7} {cy - 5}h3.5a3.5 3.5 0 0 1-3.5 4.5" fill="none" stroke="{CLAY}" stroke-width="1.6"/>'
  f'<rect x="{cx - 1.5}" y="{cy + 3}" width="3" height="4" fill="{CLAY}"/><rect x="{cx - 5.5}" y="{cy + 7}" width="11" height="2.6" rx="1.2" fill="{CLAY}"/>')
d.text(zx + 48, zy + 35.5, "Leaderboard", 16.5, INK, wt=600)
for k, wbar in enumerate((150, 122, 96)):
    ry_ = zy + 56 + 27 * k
    d.text(zx + 30, ry_ + 15.5, str(k + 1), 14, STONE, wt=600, anchor="middle")
    d(f'<rect x="{zx + 48}" y="{ry_ + 2}" width="{wbar}" height="18" rx="9" fill="{PAPER_DEEP}"/>')
for k, line in enumerate(wrap("After three rounds, each bias card still on the board costs 5 points.",
                              ZW - 40, lambda s: sw(s, 12.5))):
    d.text(zx + 20, zy + 156 + 17 * k, line, 12.5, INK_SOFT)

# 3 Take actions (bottom right)
zx = W - 26 - ZW
zone(zx, zy, ZW, ZH2); header(zx, zy, ZW, 3, "Take actions", "×2")
def area(y, name, pts, rest):
    d(f'<rect x="{zx + 14}" y="{y}" width="{ZW - 28}" height="62" rx="31" fill="{PAPER}"/>')
    d.text(zx + 64, y + 27, name, 14.5, INK, wt=600)
    d.text(zx + 64, y + 46, "", 12.5, INK_SOFT, spans=[(pts, f'font-weight="600" fill="{CLAY}"'), (rest, "")])
ay = zy + 58
area(ay, "Student pool", "+10", " per student hired")
for (dx, dy, t) in ((-7, -5, 1), (7, -5, 4), (0, 7, 3)):
    d(f'<circle cx="{zx + 40 + dx}" cy="{ay + 31 + dy}" r="7" fill="{TONES[t]}" stroke="{PAPER}" stroke-width="1.5"/>')
ay2 = ay + 70
area(ay2, "Preventive measure", "+30", " for 3 debias cards")
sx, sy = zx + 40, ay2 + 31
d(f'<path d="M{sx} {sy - 13}l11 4v7c0 7-5 11.5-11 14c-6-2.5-11-7-11-14v-7z" fill="{INK}"/>'
  f'<path d="M{sx - 4.5} {sy + 0.5}l3 3l6-6.5" fill="none" stroke="{FACE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

print(d.render(OUT + "equality-engine-board.svg"))
