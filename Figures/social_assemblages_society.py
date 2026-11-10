"""Home-page card image for Social Assemblages: human + AI -> human–AI assemblages -> a mixed society.

Humans and AIs co-shape each other, merge into hybrid forms, and together make up a
society of humans, AIs, and human–AI assemblages.
"""
from common import *

W, H = 960, 680
d = Doc(W, H, "A person and an AI co-shape each other, and combine into human–AI assemblages: a centaur with a human head "
              "on a four-legged AI body, an AI head on a human body, and a figure that is half human, half AI. "
              "Together with people and AIs, they form a mixed society, linked by social ties.")
arrow_marker(d, "arc", CLAY, 15)
SW = 2.4   # outline width on AI parts (in figure units)

# ---------- figures, each drawn around (0, 0) inside a roughly 96 x 96 square ----------
def _ai_head():
    """A wide robot head with ears and a short antenna."""
    return (f'<line x1="0" y1="-36" x2="0" y2="-43" stroke="{INK}" stroke-width="{SW}"/>'
            f'<circle cx="0" cy="-47" r="4.5" fill="{CLAY}"/>'
            f'<circle cx="-37" cy="-16" r="5.5" fill="{BLUSH}" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="37" cy="-16" r="5.5" fill="{BLUSH}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="-33" y="-36" width="66" height="40" rx="14" fill="{BLUSH}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<rect x="-22" y="-27" width="44" height="22" rx="9" fill="{FACE}"/>'
            f'<circle cx="-9" cy="-16" r="3.8" fill="{INK}"/><circle cx="9" cy="-16" r="3.8" fill="{INK}"/>')

BODY = "M-46 46C-46 16 -26 8 0 8C26 8 46 16 46 46Z"       # a wide, low body
HEAD = dict(cx=0, cy=-24, r=23)                            # a person's head, close to the body

def human(tone):
    return f'<circle cx="0" cy="{HEAD["cy"]}" r="{HEAD["r"]}" fill="{tone}"/><path d="{BODY}" fill="{tone}"/>'

def ai():
    return f'<path d="{BODY}" fill="{BLUSH}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>' + _ai_head()

def ai_head_human(tone):
    """An AI head on a human body."""
    return f'<path d="{BODY}" fill="{tone}"/>' + _ai_head()

def half_and_half(tone):
    """Left half human, right half AI, stitched down the middle."""
    cy, r = HEAD["cy"], HEAD["r"]
    s = (f'<path d="M0 {cy - r}A{r} {r} 0 0 0 0 {cy + r}Z" fill="{tone}"/>'
         f'<path d="M0 {cy - r}A{r} {r} 0 0 1 0 {cy + r}Z" fill="{BLUSH}"/>'
         f'<path d="M0 8C-26 8 -46 16 -46 46H0Z" fill="{tone}"/>'
         f'<path d="M0 8C26 8 46 16 46 46H0Z" fill="{BLUSH}"/>'
         f'<rect x="5" y="{cy - 6}" width="9" height="9" rx="2" fill="{INK}"/>'       # a square robot eye
         f'<circle cx="-9.5" cy="{cy - 1.5}" r="3.6" fill="{INK}" opacity=".6"/>'    # a human eye
         f'<line x1="0" y1="{cy - r - 2}" x2="0" y2="46" stroke="{INK}" stroke-width="1.8"/>')
    for y in (cy - 15, cy - 3, cy + 9, 20, 32):
        s += f'<line x1="-4.5" y1="{y}" x2="4.5" y2="{y}" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>'
    return s

def centaur(tone):
    """A centaur: a human head on a compact, four-legged AI body."""
    s = ''
    for x in (-29, -11, 11, 29):
        s += f'<line x1="{x}" y1="30" x2="{x}" y2="44" stroke="{INK}" stroke-width="7.5" stroke-linecap="round"/>'
    s += (f'<rect x="-44" y="-6" width="88" height="38" rx="15" fill="{BLUSH}" stroke="{INK}" stroke-width="{SW}"/>'
          f'<rect x="-24" y="2" width="48" height="22" rx="8" fill="{FACE}"/>'
          f'<circle cx="-9" cy="13" r="3.8" fill="{INK}"/><circle cx="9" cy="13" r="3.8" fill="{INK}"/>'
          f'<line x1="33" y1="-6" x2="36" y2="-15" stroke="{INK}" stroke-width="2"/><circle cx="37" cy="-18" r="4.2" fill="{CLAY}"/>'
          f'<rect x="-8" y="-13" width="16" height="9" rx="3" fill="{tone}"/>'
          f'<circle cx="0" cy="-31" r="21" fill="{tone}"/>')
    return s

def place(svg, x, y, s=1.0):
    d(f'<g transform="translate({f1(x)} {f1(y)}) scale({s})">{svg}</g>')

def arrow(x0, x1, y):
    d(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{CLAY}" stroke-width="2.6" stroke-linecap="round" marker-end="url(#arc)"/>')

# ---------- 1. human + AI, co-shaping ----------
C1 = 120
place(human(TONES[1]), C1, 236, 1.15)
place(ai(), C1, 426, 1.15)
d(f'<path d="M{C1 - 62} 250C{C1 - 108} 300 {C1 - 108} 356 {C1 - 64} 404" fill="none" stroke="{CLAY}" stroke-width="2.4" stroke-linecap="round" marker-end="url(#arc)"/>')
d(f'<path d="M{C1 + 64} 404C{C1 + 108} 356 {C1 + 108} 300 {C1 + 62} 250" fill="none" stroke="{CLAY}" stroke-width="2.4" stroke-linecap="round" marker-end="url(#arc)"/>')

arrow(220, 282, 330)

# ---------- 2. human–AI assemblages ----------
C2 = 392
place(centaur(TONES[4]), C2, 170)
place(ai_head_human(TONES[2]), C2, 336)
place(half_and_half(TONES[0]), C2, 498)

arrow(490, 552, 330)

# ---------- 3. a mixed society ----------
d(f'<ellipse cx="752" cy="330" rx="200" ry="262" fill="{mix(BLUSH, FACE, 0.12)}"/>')
crowd = [
    (632, 156, human(TONES[2])), (742, 128, ai()), (862, 162, half_and_half(TONES[4])),
    (660, 324, centaur(TONES[0])), (790, 300, human(TONES[3])), (888, 338, ai_head_human(TONES[1])),
    (626, 492, ai()), (748, 500, human(TONES[0])), (862, 494, half_and_half(TONES[1])),
]
ties = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4), (4, 5), (3, 6), (4, 7), (5, 8), (6, 7), (7, 8), (3, 7)]
for a, b in ties:
    (xa, ya, _), (xb, yb, _) = crowd[a], crowd[b]
    d(f'<line x1="{xa}" y1="{ya + 4}" x2="{xb}" y2="{yb + 4}" stroke="{mix(CLAY, FACE, 0.35)}" stroke-width="1.6" stroke-dasharray="2 5" stroke-linecap="round"/>')
for x, y, svg in crowd:
    place(svg, x, y, 0.72)

# ---------- labels ----------
for x, label in ((C1, "Human + AI"), (C2, "Human–AI assemblages"), (752, "A mixed society")):
    d.text(x, 640, label, 22, INK, fam="display", wt=600, anchor="middle")
assert C2 + sw("Human–AI assemblages", 22, 600) / 2 < 752 - sw("A mixed society", 22, 600) / 2 - 16

print(d.render(OUT + "social-assemblages-society.svg"))
