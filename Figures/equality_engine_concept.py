"""New concept figure for Equality Engine: problem -> game -> outcome."""
from common import *

W, H = 1120, 520
PW, PY, PH = 340, 14, 492
PX = [20, 390, 760]
IN = 28  # panel inner padding

d = Doc(W, H, "Equality Engine at a glance. The problem: bias creeps into every stage of a hiring algorithm, "
              "from the state of the world (historical bias) to the sample (representation), dataset "
              "(measurement), algorithms (modeling), and job applications (deployment). The game: two players "
              "act as engineers who debug it together over three rounds of Discover Bias, Debias, and Take "
              "Actions. The outcome: students' median self-reported knowledge of ML bias rose from 16.5 to 24 "
              "out of 28 after one session.")
arrow_marker(d, "arw", STONE, 10)
arrow_marker(d, "arc", CLAY, 12)

def panel(i, eyebrow, headline):
    x = PX[i]
    d(f'<rect x="{x}" y="{PY}" width="{PW}" height="{PH}" rx="18" fill="{FACE}" stroke="{LINE}" stroke-width="1.2"/>')
    d.text(x + IN, PY + 40, "", 11.5, CLAY, wt=600, ls=1.8,
           spans=[(f"0{i + 1}", ""), (eyebrow, f'dx="10" fill="{STONE}"')])
    lines = wrap(headline, PW - 2 * IN, lambda s: serif.w(s, 26))
    assert len(lines) <= 2, lines
    for k, line in enumerate(lines):
        d.text(x + IN, PY + 77 + 29 * k, line, 26, INK, fam="serif")
    return x

# connectors between panels
for gx in (PX[0] + PW + 15, PX[1] + PW + 15):
    cy = PY + PH / 2
    d(f'<circle cx="{gx}" cy="{cy}" r="16" fill="{FRAME}" stroke="{LINE}" stroke-width="1.2"/>')
    d(f'<path d="M{gx - 6} {cy}H{gx + 5}M{gx + 1} {cy - 4.5}L{gx + 5.5} {cy}L{gx + 1} {cy + 4.5}" fill="none" stroke="{CLAY}" '
      f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

# ---------- 01 The problem ----------
x = panel(0, "THE PROBLEM", "Bias creeps into every stage of a hiring algorithm")
STAGE_SIZE = 13.5
pw = max(sw(c["stage"], STAGE_SIZE, 600) for c in CATS) + 24
top = PY + 146
d.text(x + IN, top, "PIPELINE STAGE", 10, STONE, wt=600, ls=1.3)
d.text(x + IN + pw + 12, top, "BIAS IT INVITES", 10, STONE, wt=600, ls=1.3)
ROW, RH = 58, 36
for k, c in enumerate(CATS):
    ry = top + 14 + k * ROW
    d(f'<rect x="{x + IN}" y="{ry}" width="{f1(pw)}" height="{RH}" rx="{RH / 2}" fill="{PAPER}" stroke="{LINE}" stroke-width="1"/>')
    d.text(x + IN + pw / 2, ry + 22.5, c["stage"], STAGE_SIZE, INK, wt=600, anchor="middle")
    if k < len(CATS) - 1:
        ax = x + IN + pw / 2
        d(f'<line x1="{f1(ax)}" y1="{ry + RH + 4}" x2="{f1(ax)}" y2="{ry + ROW - 5}" stroke="{STONE}" stroke-width="1.6" marker-end="url(#arw)"/>')
    tx = x + IN + pw + 12
    d(f'<rect x="{f1(tx)}" y="{ry + 6}" width="18" height="24" rx="3.5" fill="{c["tint2"]}" stroke="{c["color"]}" stroke-width="1.6"/>')
    d(f'<rect x="{f1(tx + 4)}" y="{ry + 12}" width="10" height="2.4" rx="1.2" fill="{c["color"]}" opacity=".7"/>')
    label = c["name"]
    assert tx + 26 + sw(label, 14.5, 600) <= x + PW - 14, label
    d.text(tx + 26, ry + 23.5, label, 14.5, c["dark"], wt=600)
for k, line in enumerate(wrap("Five sources of bias, adapted from Suresh and Guttag’s ML life-cycle framework",
                              PW - 2 * IN, lambda s: sw(s, 12))):
    d.text(x + IN, PY + PH - 34 + 16 * k, line, 12, STONE)

# ---------- 02 The game ----------
x = panel(1, "THE GAME", "Players act as engineers who debug it together")
# speech bubbles
def bubble(bx, by, text, tail_x, tail_dir, fill, color):
    bw = sw(text, 14.5) + 28
    if tail_dir == "right":
        bx -= bw
    d(f'<rect x="{f1(bx)}" y="{by}" width="{f1(bw)}" height="36" rx="18" fill="{fill}"/>')
    tx = tail_x
    d(f'<path d="M{f1(tx - 7)} {by + 34}L{f1(tx + (-6 if tail_dir == "left" else 6))} {by + 47}L{f1(tx + 7)} {by + 34}Z" fill="{fill}"/>')
    d.text(bx + bw / 2, by + 23, text, 14.5, color, anchor="middle")
b1 = PY + 128
bubble(x + IN, b1, "Same résumés, different names…", x + 66, "left", PAPER, INK)
bubble(x + PW - IN, b1 + 46, "Historical bias?", x + PW - 66, "right", BLUSH_TINT, CLAY_DEEP)
# players at a table
py_ = PY + 250
person(d, x + 70, py_, 15, TONES[1], ring=FACE)
person(d, x + PW - 70, py_, 15, TONES[2], ring=FACE)
tbl = py_ + 36
d(f'<rect x="{x + IN}" y="{tbl}" width="{PW - 2 * IN}" height="10" rx="5" fill="{PAPER_DEEP}"/>')
d(f'<rect x="{x + 20}" y="{tbl + 10}" width="{PW - 40}" height="16" fill="{FACE}"/>')  # trim shoulders under the table
cx_ = x + PW / 2
d(f'<g transform="rotate(-7 {cx_} {tbl - 22})">'
  f'<rect x="{cx_ - 17}" y="{tbl - 46}" width="34" height="46" rx="5" fill="{CLAY}"/>'
  f'<rect x="{cx_ - 13}" y="{tbl - 42}" width="26" height="38" rx="3" fill="none" stroke="{FACE}" stroke-opacity=".4"/></g>')
d.text(cx_ - 2.5, tbl - 16, "?", 22, FACE, fam="serif", anchor="middle", extra=f' transform="rotate(-7 {cx_} {tbl - 22})"')
# the three phases
phases = [("Discover bias", "+5", "Name the bias type on a card"),
          ("Debias", "+5", "Debate how to fix it"),
          ("Take actions", "×2", "Get students hired, prevent bias")]
p0 = PY + 322
for k, (name, pts, desc) in enumerate(phases):
    ry = p0 + k * 41
    if k < 2:
        d(f'<line x1="{x + IN + 13}" y1="{ry + 14 + 14}" x2="{x + IN + 13}" y2="{ry + 41}" stroke="{LINE}" stroke-width="1.5"/>')
    badge(d, x + IN + 13, ry + 14, k + 1)
    d.text(x + IN + 36, ry + 13, name, 15, INK, wt=600)
    pill(d, x + PW - IN, ry - 2, pts, anchor="end", h=21, size=12)
    d.text(x + IN + 36, ry + 31, desc, 12.5, INK_SOFT)
# loop note
ly = PY + PH - 24
lx = x + IN + 13
d(f'<path d="M{lx + 6} {ly - 9}A7.5 7.5 0 1 0 {lx + 7.5} {ly - 2}" fill="none" stroke="{CLAY}" stroke-width="1.8" stroke-linecap="round"/>'
  f'<path d="M{lx + 2.5} {ly - 10.5}L{lx + 6.5} {ly - 9.5}L{lx + 6.5} {ly - 13.5}" fill="none" stroke="{CLAY}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
note = "Three rounds per session, one team score"
assert x + IN + 36 + sw(note, 12) <= x + PW - IN, note
d.text(x + IN + 36, ly, note, 12, STONE)

# ---------- 03 The outcome ----------
x = panel(2, "THE OUTCOME", "Students’ knowledge of ML bias rose")
lab_y, num_y = PY + 148, PY + 202
d.text(x + IN, lab_y, "BEFORE", 10, STONE, wt=600, ls=1.3)
d.text(x + IN, num_y, "16.5", 60, STONE, fam="serif")
nw = serif.w("16.5", 60)
ax0, ax1 = x + IN + nw + 16, x + IN + nw + 58
d(f'<line x1="{f1(ax0)}" y1="{num_y - 18}" x2="{f1(ax1)}" y2="{num_y - 18}" stroke="{CLAY}" stroke-width="2" stroke-linecap="round" marker-end="url(#arc)"/>')
d.text(ax1 + 18, lab_y, "AFTER", 10, CLAY, wt=600, ls=1.3)
d.text(ax1 + 16, num_y, "24", 60, CLAY, fam="serif")
d.text(ax1 + 18 + serif.w("24", 60), num_y, "/ 28", 18, STONE, fam="serif", extra=' dx="2"')
for k, line in enumerate(wrap("Median self-reported knowledge of ML bias, before and after one session",
                              PW - 2 * IN, lambda s: sw(s, 12.5))):
    d.text(x + IN, PY + 230 + 17 * k, line, 12.5, INK_SOFT)
# scale 0–28
by = PY + 288
x0, x1 = x + IN + 4, x + PW - IN - 4
def sx(v): return x0 + (x1 - x0) * v / 28
d(f'<rect x="{f1(x0)}" y="{by - 3}" width="{f1(x1 - x0)}" height="6" rx="3" fill="{PAPER_DEEP}"/>')
d(f'<rect x="{f1(sx(16.5))}" y="{by - 3}" width="{f1(sx(24) - sx(16.5))}" height="6" fill="{BLUSH}"/>')
d(f'<circle cx="{f1(sx(16.5))}" cy="{by}" r="7" fill="{FACE}" stroke="{STONE}" stroke-width="2.5"/>')
d(f'<circle cx="{f1(sx(24))}" cy="{by}" r="8" fill="{CLAY}" stroke="{FACE}" stroke-width="2"/>')
for v in (0, 7, 14, 21, 28):
    d.text(sx(v), by + 24, str(v), 11, STONE, anchor="middle")
d.text(x + IN, PY + 342, "12 students · Wilcoxon signed-rank test, p = .002", 12, INK_SOFT)
d(f'<line x1="{x + IN}" y1="{PY + 362}" x2="{x + PW - IN}" y2="{PY + 362}" stroke="{LINE}" stroke-width="1"/>')

def takeaway(ty, icon, text):
    cx, cy = x + IN + 14, ty + 6
    d(f'<circle cx="{cx}" cy="{cy}" r="14" fill="{BLUSH_TINT}"/>')
    d(icon(cx, cy))
    for k, line in enumerate(wrap(text, PW - 2 * IN - 40, lambda s: sw(s, 14))):
        d.text(x + IN + 40, ty + 12 * 0 + 19 * k + 5, line, 14, INK)

talk = lambda cx, cy: (f'<path d="M{cx - 7} {cy - 5}h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-8l-4 3.5v-3.5h-2a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z" '
                       f'fill="none" stroke="{CLAY_DEEP}" stroke-width="1.6" stroke-linejoin="round"/>')
miss = lambda cx, cy: (f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{CLAY_DEEP}" stroke-width="1.6"/>'
                       f'<circle cx="{cx}" cy="{cy}" r="2.6" fill="{CLAY_DEEP}"/>')
takeaway(PY + 390, talk, "Debias discussions were the most compelling part")
takeaway(PY + 440, miss, "Representation bias drew 40% of all wrong guesses")

print(d.render(OUT + "equality-engine-concept.svg"))
