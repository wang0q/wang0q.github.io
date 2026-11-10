"""Research-page card image for "Good" XAI Design: the concept diagram, sized for a 16:10 card.

Same drawing as good_xai_concept.py in its compact layout (parts closer together, larger
text, no captions), scaled to fill the card.
"""
from common import *
from good_xai_concept import draw, ALT, CARD

W, H = 960, 600
BOX = (132, 44, 1004, 446)         # extent of the compact layout: x0, y0, x1, y1
PAD = 26

bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
s = min((W - 2 * PAD) / bw, (H - 2 * PAD) / bh)
tx = (W - bw * s) / 2 - BOX[0] * s
ty = (H - bh * s) / 2 - BOX[1] * s

d = Doc(W, H, ALT)
d(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
d(f'<g transform="translate({f1(tx)} {f1(ty)}) scale({s:.4f})">')
draw(d, halo=PAPER, captions=False, L=CARD)
d("</g>")
print(d.render(OUT + "good-xai-card.svg"))
