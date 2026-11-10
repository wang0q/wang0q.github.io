"""Concept figure for "Good" XAI Design: AI -> XAI criteria -> user effects.

XAI reflects certain aspects of an AI to its users, guided by recommended
criteria (C1 ... Cn). Those criteria are judged good or important on the
explanation itself, yet the effects they have on users are unknown, and not
necessarily good or important.
"""
from math import cos, sin, radians
from common import *
from common import _T

W, H = 1120, 520
ACCENT = _T.get("accent-line", BLUSH)

ALT = ("Concept of the study. An AI system is a black box to its users. Explainable AI (XAI) "
       "reflects certain aspects of it, guided by criteria C1 to Cn that frameworks recommend. "
       "Those criteria are judged good or important on the explanation itself, but the effects "
       "they have on users are unknown, and not necessarily good or important.")

# ---------- geometry ----------
CX, CY, R = 140, 262, 72                      # AI cube (isometric hexagon)
def hexpt(deg):
    return (CX + R * cos(radians(deg)), CY + R * sin(radians(deg)))
TOP, UR, LR, BOT, LL, UL = (hexpt(a) for a in (-90, -30, 30, 90, 150, 210))

KX, KTOP, KSH, KBOT, KHW = 430, 96, 346, 440, 115   # XAI kite: spine x, apex, shoulders, tip, half width
NR = 17                                             # criterion node radius
NODES = [("1", 158), ("2", 200), ("3", 242), ("4", 284), ("n", 384)]

BX, BY, BS = 642, 196, 148                    # the "Good? Important?" box
BMX, BMY = BX, BY + BS / 2                    # where criteria lines meet the box

def kite_left(s):
    """Point on the kite's left outline; s runs 0 (apex) -> 1 (shoulder) -> 2 (tip)."""
    if s <= 1:
        return (KX - KHW * s, KTOP + (KSH - KTOP) * s)
    u = s - 1
    return (KX - KHW + KHW * u, KSH + (KBOT - KSH) * u)

# one colour per criterion, from the palette's dark tone to its accent
COLS = [mix(ACCENT, DARK, k / (len(NODES) - 1)) for k in range(len(NODES))]

def pt(p):
    return f"{f1(p[0])} {f1(p[1])}"

# ---------- AI -> XAI: each criterion reflects certain aspects ----------
# Lines start inside the cube's right face and are drawn under it, so they leave from its edge.
ORIGINS = [(178, 250), (190, 266), (172, 278), (186, 292), (164, 302), (195, 241)]
REFLECTS = {0: [0, 2, 5], 1: [1, 3], 2: [2, 4], 3: [0, 5], 4: [3, 4]}
# aspects no criterion picks up: these stop at the edge of the XAI
UNSEEN = [(1, 0.55), (4, 0.86), (2, 1.32)]

FX = 975                                      # cloud centre

# Two layouts: the full figure for the project page, and a compact one for the
# research-page card, where the parts sit closer together and the text is larger.
FULL = dict(ai=0, box=0, q=0, fx=0, head=32, label=21, label_x=290, label_y=(146, 170), box_text=23)
CARD = dict(ai=60, box=-45, q=-70, fx=-95, head=40, label=25, label_x=322, label_y=(116, 144), box_text=26)


def draw(d, halo=FRAME, captions=True, L=FULL):
    """Draw the diagram into d. halo is the background colour that gaps and cut-outs use."""
    ai, fx = L["ai"], L["fx"]
    cx, top, ur, lr, bot, ul = CX + ai, *[(p[0] + ai, p[1]) for p in (TOP, UR, LR, BOT, UL)]
    ll = (LL[0] + ai, LL[1])
    origins = [(x + ai, y) for x, y in ORIGINS]
    bx = BX + L["box"]
    bmx = bx

    d(f'<path d="M{pt((KX, KTOP))}L{pt(kite_left(1))}L{pt((KX, KBOT))}L{pt((2 * KX - kite_left(1)[0], KSH))}Z" fill="{FACE}"/>')
    for o, s in UNSEEN:
        d(f'<line x1="{origins[o][0]}" y1="{origins[o][1]}" x2="{f1(kite_left(s)[0])}" y2="{f1(kite_left(s)[1])}" '
          f'stroke="{mix(STONE, FACE, 0.42)}" stroke-width="1.2"/>')
    for k, os_ in REFLECTS.items():
        ny = NODES[k][1]
        for o in os_:
            ox, oy = origins[o]
            d(f'<line x1="{ox}" y1="{oy}" x2="{KX - NR}" y2="{ny}" stroke="{COLS[k]}" stroke-width="1.6" '
              f'stroke-opacity=".85" stroke-linecap="round"/>')

    # ---------- XAI -> box ----------
    for k, (_, ny) in enumerate(NODES):
        d(f'<line x1="{KX + NR}" y1="{ny}" x2="{bmx}" y2="{f1(BMY)}" stroke="{STONE}" stroke-width="1.5" stroke-opacity=".5"/>')

    # ---------- the AI: a black box ----------
    d(f'<path d="M{pt(top)}L{pt(ur)}L{pt((cx, CY))}L{pt(ul)}Z" fill="{mix(FACE, INK, 0.16)}"/>')
    d(f'<path d="M{pt(ul)}L{pt((cx, CY))}L{pt(bot)}L{pt(ll)}Z" fill="{INK}"/>')
    d(f'<path d="M{pt((cx, CY))}L{pt(ur)}L{pt(lr)}L{pt(bot)}Z" fill="{mix(FACE, INK, 0.07)}"/>')
    for p in (ul, ur, bot):
        d(f'<line x1="{cx}" y1="{CY}" x2="{f1(p[0])}" y2="{f1(p[1])}" stroke="{halo}" stroke-width="5"/>')
    d.text(cx, top[1] - 24, "AI", L["head"], INK, fam="serif", anchor="middle")

    # label on the AI -> XAI lines, clear of the "AI" heading and the kite's edge
    lx, size = L["label_x"], L["label"]
    for line, ly in zip(("reflects certain", "aspects of the AI"), L["label_y"]):
        d.text(lx, ly, line, size, CLAY, fam="serif_it", anchor="middle")
        half = serif_it.w(line, size) / 2
        assert lx + half < kite_left((ly - KTOP) / (KSH - KTOP))[0] - 8, line
        assert lx - half > cx + serif.w("AI", L["head"]) / 2 + 10, line

    # ---------- the XAI: criteria on a spine ----------
    d(f'<path d="M{pt((KX, KTOP))}L{pt(kite_left(1))}L{pt((KX, KBOT))}L{pt((2 * KX - kite_left(1)[0], KSH))}Z" '
      f'fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    d(f'<line x1="{KX}" y1="{KTOP}" x2="{KX}" y2="{KBOT}" stroke="{INK}" stroke-width="2.6"/>')
    for k, (sub, ny) in enumerate(NODES):
        c = COLS[k]
        d(f'<circle cx="{KX}" cy="{ny}" r="{NR}" fill="{mix(c, FACE, 0.3)}" stroke="{c}" stroke-width="1.6"/>')
        d.text(KX - 1, ny + 5.5, "C" + sub, 19, INK, fam="serif_it", anchor="middle",
               spans=[("C", ""), (sub, 'font-size="13" dy="3"')])
    # a quiet "and so on" between C4 and Cn
    for j in range(3):
        d(f'<circle cx="{KX + 26}" cy="{318 + 14 * j}" r="1.8" fill="{STONE}"/>')
    d.text(KX, KTOP - 22, "XAI", L["head"], INK, fam="serif", anchor="middle")

    # ---------- the judgement: good? important? ----------
    d(f'<rect x="{bx}" y="{BY}" width="{BS}" height="{BS}" rx="22" fill="{INK}"/>')
    bt = L["box_text"]
    for k, line in enumerate(("Good?", "Important?", "…")):
        d.text(bx + BS / 2, BY + BS / 2 + 16 + 28 * bt / 23 * (k - 1), line, bt, FACE, fam="serif_it", anchor="middle")
    assert serif_it.w("Important?", bt) < BS - 28

    # ---------- box -> user effects, through a question mark ----------
    for ex, ey in ((930, 238), (928, 262), (930, 288), (940, 306)):
        d(f'<line x1="{bx + BS}" y1="{f1(BMY)}" x2="{ex + fx}" y2="{ey}" stroke="{STONE}" stroke-width="1.1" stroke-opacity=".35"/>')
    d.text(842 + L["q"], 302, "?", 92, INK, fam="serif", anchor="middle",
           extra=f' stroke="{halo}" stroke-width="12" paint-order="stroke" stroke-linejoin="round"')

    # thought cloud: stroke every lobe at double width, then fill them again on top,
    # which leaves a single outline around the union
    lobes = [("c", 925, 274, 42), ("c", 968, 228, 50), ("c", 1028, 236, 42), ("c", 1058, 280, 34),
             ("r", 890, 252, 198, 64, 32)]
    def lobe(b, attrs):
        if b[0] == "c":
            return f'<circle cx="{b[1] + fx}" cy="{b[2]}" r="{b[3]}" {attrs}/>'
        return f'<rect x="{b[1] + fx}" y="{b[2]}" width="{b[3]}" height="{b[4]}" rx="{b[5]}" {attrs}/>'
    for b in lobes:
        d(lobe(b, f'fill="{INK}" stroke="{INK}" stroke-width="6"'))
    for b in lobes:
        d(lobe(b, f'fill="{FACE}"'))
    effect = mix(STONE, FACE, 0.38)
    for ex, ey in ((952, 244), (1008, 238), (950, 292), (1010, 286)):
        d(f'<circle cx="{ex + fx}" cy="{ey}" r="18" fill="{effect}"/>')
    d.text(FX + fx + 8, 152, "User effects", L["head"], INK, fam="serif", anchor="middle")

    # the users, thinking
    for bx_, by_, br in ((1022, 336, 6.5), (1034, 354, 4.2)):
        d(f'<circle cx="{bx_ + fx}" cy="{by_}" r="{br}" fill="{FACE}" stroke="{INK}" stroke-width="2.4"/>')
    person(d, 1076 + fx, 384, 10.5, FACE, ring=INK)
    person(d, 1050 + fx, 378, 10.5, FACE, ring=INK)

    if captions:
        d.text(KX, KBOT + 30, "XAI criteria", 22, INK_SOFT, fam="serif_it", anchor="middle")
        CAPS = [
            (cx, 250, "A black box to the people who use it"),
            ((bx + BS / 2), 270, "Judged on the explanation itself"),
            (FX + fx + 14, 250, "Real effects on users, not necessarily good or important"),
        ]
        CAP_Y = KBOT + 30
        for ccx, maxw, text in CAPS:
            lines = wrap(text, maxw, lambda s: sw(s, 16.5))
            assert len(lines) <= 2, lines
            for k, line in enumerate(lines):
                d.text(ccx, CAP_Y + 23 * k, line, 16.5, INK_SOFT, anchor="middle")
            assert 8 <= ccx - max(sw(l, 16.5) for l in lines) / 2 and ccx + max(sw(l, 16.5) for l in lines) / 2 <= W - 8, text


if __name__ == "__main__":
    d = Doc(W, H, ALT)
    draw(d)
    print(d.render(OUT + "good-xai-concept.svg"))
