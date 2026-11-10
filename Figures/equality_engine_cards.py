"""Redrawn example bias cards (after Figure 2 of the paper)."""
from common import *

CARDS = [
    ("Name Discrimination",
     "Same résumés with “white” names, such as Brendan Baker, got more callbacks than “Black” ones, "
     "such as Lakisha Washington."),
    ("Geographic Diversity",
     "Research indicates that ML models trained on a face image dataset mostly from North America and "
     "Western Europe sometimes perform significantly worse on images from other areas."),
    ("Labeling Bias",
     "MIT pulled offline a huge dataset that had been labeled by humans, because some of the labels "
     "contained derogatory language directed towards Black and Asian individuals."),
    ("Machines Stick to It",
     "With gender-non-specific data, Amazon’s AI model still exhibited bias against women. For example, "
     "it relied on phrases like “women’s chess club” as a proxy for gender."),
    ("Irrelevant Assessment",
     "Some popular work-related AI tools use a person’s speech patterns or facial expressions to infer "
     "work performance."),
]

W = 1120
CW, GAP, M, TOP = 206, 12.5, 20, 14
PAD = 16
TW = CW - 2 * PAD
HEAD = 44
T_SIZE, T_LH = 25, 27
B_SIZE, B_LH = 15.5, 22

layout = []
for (title, body), cat in zip(CARDS, CATS):
    tl = wrap(title, TW, lambda s: serif.w(s, T_SIZE))
    bl = wrap(body, TW, lambda s: sw(s, B_SIZE))
    t0 = HEAD + 38
    rule = t0 + (len(tl) - 1) * T_LH + 15
    b0 = rule + 29
    end = b0 + (len(bl) - 1) * B_LH
    layout.append((cat, tl, bl, t0, rule, b0, end))

CH = max(l[-1] for l in layout) + 22 + 44
ROT = [-1.6, 1.1, -0.7, 1.3, -1.2]
DY = [8, 0, 5, -1, 9]
H = TOP + CH + max(DY) + 18

d = Doc(W, H, "Five example bias cards, one per category. Historical bias: Name Discrimination. "
              "Representation bias: Geographic Diversity. Measurement bias: Labeling Bias. "
              "Modeling bias: Machines Stick to It. Deployment bias: Irrelevant Assessment. "
              "Each card pairs a short title with a real case of bias in hiring or machine learning.")
d.defs.append('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
              f'<feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="{INK}" flood-opacity=".13"/></filter>')

for i, (cat, tl, bl, t0, rule, b0, end) in enumerate(layout):
    x = M + i * (CW + GAP)
    y = TOP + DY[i]
    cx, cy = x + CW / 2, y + CH / 2
    d(f'<g transform="rotate({ROT[i]} {f1(cx)} {f1(cy)})">')
    d(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="16" fill="{FACE}" stroke="{LINE}" stroke-width="1" filter="url(#sh)"/>')
    d(f'<path d="M{x} {y + HEAD}V{y + 16}Q{x} {y} {x + 16} {y}H{x + CW - 16}Q{x + CW} {y} {x + CW} {y + 16}V{y + HEAD}Z" fill="{cat["tint"]}"/>')
    d(f'<rect x="{x}" y="{y + HEAD - 2}" width="{CW}" height="2" fill="{cat["color"]}" opacity=".55"/>')
    d.text(x + PAD, y + 27.5, f"{cat['name']} bias".upper(), 11.5, cat["dark"], wt=600, ls=1.3)
    for k, line in enumerate(tl):
        d.text(x + PAD, y + t0 + k * T_LH, line, T_SIZE, INK, fam="serif")
    d(f'<rect x="{x + PAD}" y="{y + rule}" width="28" height="2.5" rx="1.25" fill="{cat["color"]}"/>')
    for k, line in enumerate(bl):
        d.text(x + PAD, y + b0 + k * B_LH, line, B_SIZE, INK_SOFT)
    fy = y + CH - 44
    d(f'<line x1="{x + PAD}" y1="{fy}" x2="{x + CW - PAD}" y2="{fy}" stroke="{LINE}" stroke-width="1"/>')
    d.text(x + PAD, fy + 26, "", 12, INK_SOFT,
           spans=[("STAGE", f'font-size="10" font-weight="600" letter-spacing="1.2" fill="{STONE}"'),
                  (cat["stage"], 'dx="7"')])
    d("</g>")

print(d.render(OUT + "equality-engine-cards.svg"), W, H)
