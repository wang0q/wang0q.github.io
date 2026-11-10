"""Research-page card image for Explainable AI in Everyday Life, sized for a 16:10 card.

Same drawing as everyday_xai_concept.py in its compact mode (no descriptions, larger
titles), scaled to fill the card.
"""
from common import *
from everyday_xai_concept import draw, ALT, CARD_EXTENT as BOX

W, H = 960, 600
PAD = 24

bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
s = min((W - 2 * PAD) / bw, (H - 2 * PAD) / bh)
tx = (W - bw * s) / 2 - BOX[0] * s
ty = (H - bh * s) / 2 - BOX[1] * s

d = Doc(W, H, ALT)
d(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
d(f'<g transform="translate({f1(tx)} {f1(ty)}) scale({s:.4f})">')
draw(d, card=True)
d("</g>")
print(d.render(OUT + "everyday-xai-card.svg"))
