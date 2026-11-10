"""Redrawn three-phase study overview (after Figure 1 of the CHI 2026 paper)."""
from common import *

W, H = 1120, 384
CW, CH, CY = 320, 290, 22
XS = [20, 400, 780]

d = Doc(W, H, "Overview of the three-phase study. Phase 1, Ideation, with 12 participants, produced a design "
              "space with two dimensions. Phase 2, Design, by the research team, produced 15 storyboards. "
              "Phase 3, Elicitation, with 18 participants, six of them returning from Phase 1, was analyzed "
              "into 4 themes. 24 people took part in total.")
arrow_marker(d, "arc", CLAY, 12)

PHASES = [
    ("Ideation", "12 participants", "2", "design dimensions",
     "Co-design interviews on forming social connections online"),
    ("Design", "Research team", "15", "storyboards",
     "One storyboard for each stage × capability pairing"),
    ("Elicitation", "18 participants", "4", "themes",
     "Think-aloud interviews in reaction to the storyboards"),
]

def icon_space(cx, cy):
    gw, gh, s, g = 5, 3, 9, 3
    x0 = cx - (gw * s + (gw - 1) * g) / 2 + 3
    y0 = cy - (gh * s + (gh - 1) * g) / 2 - 3
    for r in range(gh):
        for c in range(gw):
            fill = mix(BLUSH, FACE, [0.45, 0.72, 1.0][r])
            d(f'<rect x="{f1(x0 + c * (s + g))}" y="{f1(y0 + r * (s + g))}" width="{s}" height="{s}" rx="2" fill="{fill}"/>')
    ax, ay = x0 - 6, y0 + gh * s + (gh - 1) * g + 6
    d(f'<path d="M{f1(ax)} {f1(y0 - 2)}V{f1(ay)}H{f1(x0 + gw * (s + g) + 4)}" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    d(f'<path d="M{f1(x0 + gw * (s + g) + 1)} {f1(ay - 3.5)}l3.5 3.5l-3.5 3.5" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')

def icon_boards(cx, cy):
    for k, (dx, dy) in enumerate(((10, -10), (5, -5), (0, 0))):
        x, y = cx - 24 + dx, cy - 14 + dy
        d(f'<rect x="{f1(x)}" y="{f1(y)}" width="40" height="28" rx="3" fill="{FACE if k == 2 else mix(BLUSH, FACE, 0.3 + 0.2 * k)}" stroke="{INK}" stroke-width="1.6"/>')
    x, y = cx - 24, cy - 14
    d(f'<circle cx="{f1(x + 11)}" cy="{f1(y + 13)}" r="4" fill="{TONES[1]}"/>'
      f'<path d="M{f1(x + 4.5)} {f1(y + 28)}q6.5-9 13 0" fill="{TONES[1]}"/>'
      f'<rect x="{f1(x + 20)}" y="{f1(y + 5)}" width="15" height="9" rx="4.5" fill="{BLUSH}"/>')

def icon_talk(cx, cy):
    d(f'<path d="M{cx - 4} {cy - 20}h22a6 6 0 0 1 6 6v10a6 6 0 0 1-6 6h-3l-5 5v-5h-14a6 6 0 0 1-6-6v-10a6 6 0 0 1 6-6z" fill="{BLUSH}"/>')
    d(f'<path d="M{cx - 22} {cy - 10}h24a6 6 0 0 1 6 6v11a6 6 0 0 1-6 6h-15l-6 6v-6h-3a6 6 0 0 1-6-6v-11a6 6 0 0 1 6-6z" fill="{FACE}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')
    for k in range(3):
        d(f'<circle cx="{cx - 15 + 7 * k}" cy="{cy + 2.5}" r="1.9" fill="{INK}"/>')

ICONS = [icon_space, icon_boards, icon_talk]

for i, (title, who, num, unit, desc) in enumerate(PHASES):
    x = XS[i]
    d(f'<rect x="{x}" y="{CY}" width="{CW}" height="{CH}" rx="18" fill="{FACE}" stroke="{LINE}" stroke-width="1.2"/>')
    d.text(x + 28, CY + 40, f"PHASE {i + 1}", 11.5, CLAY, wt=600, ls=1.8)
    d.text(x + 28, CY + 77, title, 30, INK, fam="serif")
    person(d, x + 33, CY + 98, 4.2, STONE)
    d.text(x + 46, CY + 109, who, 14, INK_SOFT)
    # icon + output
    icx, icy = x + 76, CY + 178
    d(f'<circle cx="{icx}" cy="{icy}" r="46" fill="{BLUSH_TINT}"/>')
    ICONS[i](icx, icy)
    ox = x + 146
    d.text(ox, CY + 148, "OUTPUT", 10, STONE, wt=600, ls=1.3)
    d.text(ox, CY + 199, num, 54, CLAY, fam="serif")
    d.text(ox, CY + 222, unit, 14.5, INK, wt=600)
    d(f'<line x1="{x + 28}" y1="{CY + 244}" x2="{x + CW - 28}" y2="{CY + 244}" stroke="{LINE}" stroke-width="1"/>')
    lines = wrap(desc, CW - 56, lambda s: sw(s, 13))
    assert len(lines) <= 2, lines
    for k, line in enumerate(lines):
        d.text(x + 28, CY + 266 + 17 * k, line, 13, INK_SOFT)

# arrows between phases
for gx in (XS[0] + CW, XS[1] + CW):
    yy = CY + CH / 2
    d(f'<line x1="{gx + 12}" y1="{yy}" x2="{gx + 46}" y2="{yy}" stroke="{CLAY}" stroke-width="2" stroke-linecap="round" marker-end="url(#arc)"/>')

# returning participants
x1, x3 = XS[0] + CW / 2, XS[2] + CW / 2
y0 = CY + CH + 4
d(f'<path d="M{x1} {y0}C{x1} {y0 + 52} {x3} {y0 + 52} {x3} {y0 + 6}" fill="none" stroke="{STONE}" stroke-width="1.5" '
  f'stroke-dasharray="5 5" marker-end="url(#arc)"/>')
label = "6 Phase 1 participants return · 24 people in total"
lw = sw(label, 12.5, 600) + 28
d(f'<rect x="{f1(W / 2 - lw / 2)}" y="{y0 + 28}" width="{f1(lw)}" height="26" rx="13" fill="{FRAME}" stroke="{LINE}" stroke-width="1"/>')
d.text(W / 2, y0 + 45.5, label, 12.5, INK_SOFT, wt=600, anchor="middle")

print(d.render(OUT + "social-assemblages-overview.svg"))
