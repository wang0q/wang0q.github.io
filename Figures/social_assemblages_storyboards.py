"""Design-space grid of the 15 storyboards (Social Assemblages, CHI 2026).

Reads the storyboard images from sources/storyboards/L<row>-S<column>.jpg
(made by extract_storyboard_tiles.py) and lays them out with the site's type.
"""
from io import BytesIO
from PIL import Image
from common import *

ROWS = [("L1", "Human", "augmentation"), ("L2", "Social", "replica"), ("L3", "Omniscient", "social beings")]
COLS = ["Data collection", "Profiling", "Social formation", "Social maintenance", "Reflection"]

tiles = [[Image.open(f"{SOURCES}storyboards/L{r + 1}-S{c + 1}.jpg").convert("RGB") for c in range(5)]
         for r in range(3)]

W = 1120
LBL = 176            # row-label column
M = 20
GX, GY = 10, 12
avail = W - M - LBL - M - 4 * GX
# column widths follow the storyboards' own proportions (mean width per column)
colw_src = [sum(tiles[r][c].size[0] for r in range(3)) / 3 for c in range(5)]
rowh_src = sum(t.size[1] for row in tiles for t in row) / 15
k = avail / sum(colw_src)
CWS = [w * k for w in colw_src]
TH = rowh_src * k
TOP = 96
H = int(TOP + 3 * TH + 2 * GY + 30)

d = Doc(W, H, "The 15 storyboards arranged as the study's design space. Columns are the five stages of forming "
              "social interaction: data collection, profiling, social formation, social maintenance, and "
              "reflection. Rows are three levels of AI social capability: human augmentation, social replica, "
              "and omniscient social beings. The storyboard for social formation with an omniscient social AI, "
              "Figure 3 in the paper, is outlined.")

x0 = M + LBL
colx = [x0 + sum(CWS[:c]) + GX * c for c in range(5)]

# axis: stages (a cycle)
d.text(x0, 26, "", 11, CLAY, wt=600, ls=1.8,
       spans=[("STAGES OF FORMING SOCIAL INTERACTION", ""), ("  a cycle", f'dx="6" fill="{STONE}" letter-spacing="0.4" font-weight="400" font-size="12"')])
ay = 40
d(f'<line x1="{x0}" y1="{ay}" x2="{W - M - 22}" y2="{ay}" stroke="{SAND}" stroke-width="1.4"/>')
ex = W - M - 14
d(f'<path d="M{ex - 9} {ay}H{ex}a7 7 0 0 1 0 14" fill="none" stroke="{SAND}" stroke-width="1.4" stroke-linecap="round"/>'
  f'<path d="M{ex - 3} {ay + 10}l3 4l3.5-3.5" fill="none" stroke="{SAND}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')
for c, name in enumerate(COLS):
    cx = colx[c]
    d(f'<circle cx="{f1(cx + 3)}" cy="{ay}" r="3" fill="{CLAY}"/>')
    d.text(cx, 66, f"S{c + 1}", 10.5, STONE, wt=600, ls=1)
    nm = name
    d.text(cx + 22, 66, nm, 14, INK, wt=600)
    assert cx + 22 + sw(nm, 14, 600) <= cx + CWS[c] + GX, nm

# axis: capability
d.text(M, 66, "AI SOCIAL CAPABILITY", 11, CLAY, wt=600, ls=1.8)
lx = M + 6
d(f'<line x1="{lx}" y1="{TOP + 4}" x2="{lx}" y2="{TOP + 3 * TH + 2 * GY - 6}" stroke="{SAND}" stroke-width="1.4"/>'
  f'<path d="M{lx - 4} {TOP + 3 * TH + 2 * GY - 10}l4 5l4-5" fill="none" stroke="{SAND}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')

for r, (lv, a, b) in enumerate(ROWS):
    ty = TOP + r * (TH + GY)
    d(f'<circle cx="{lx}" cy="{f1(ty + TH / 2 - 26)}" r="3" fill="{CLAY}"/>')
    d.text(M + 22, ty + TH / 2 - 22, lv, 10.5, STONE, wt=600, ls=1)
    d.text(M + 22, ty + TH / 2 + 2, a, 21, INK, fam="serif")
    d.text(M + 22, ty + TH / 2 + 24, b, 21, INK, fam="serif")
    for c in range(5):
        x, w = colx[c], CWS[c]
        img = tiles[r][c]
        # keep ~2.2x the drawn size for sharp rendering, then JPEG-encode
        tw = int(round(w * 2.2)); th = int(round(TH * 2.2))
        im2 = img.resize((min(tw, img.size[0]), min(th, img.size[1])), Image.LANCZOS) if tw < img.size[0] else img
        buf = BytesIO(); im2.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        cid = f"t{r}{c}"
        d.defs.append(f'<clipPath id="{cid}"><rect x="{f1(x)}" y="{f1(ty)}" width="{f1(w)}" height="{f1(TH)}" rx="7"/></clipPath>')
        d(f'<image x="{f1(x)}" y="{f1(ty)}" width="{f1(w)}" height="{f1(TH)}" preserveAspectRatio="xMidYMid slice" '
          f'clip-path="url(#{cid})" href="data:image/jpeg;base64,{b64}"/>')
        hl = (r, c) == (2, 2)
        d(f'<rect x="{f1(x)}" y="{f1(ty)}" width="{f1(w)}" height="{f1(TH)}" rx="7" fill="none" '
          f'stroke="{CLAY if hl else LINE}" stroke-width="{3 if hl else 1.2}"/>')
        if hl:
            d.text(x + w / 2, ty + TH + 19, "Figure 3 in the paper", 11.5, CLAY, wt=600, anchor="middle")

print(d.render(OUT + "social-assemblages-storyboards.svg"), W, H)
