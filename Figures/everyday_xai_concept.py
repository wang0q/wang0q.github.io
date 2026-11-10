"""Concept figure for Explainable AI in Everyday Life (DIS 2025): the paper's two central questions.

Question 1: do everyday users want AI to explain itself? An everyday app offers
"Why am I seeing this?". "Not now" leads to the answer "not necessarily" (non-use
and concerns). Question 2: if so, how? "Explain" leads to the three ideal designs
people envision.
"""
from math import cos, sin, radians
from common import *

W, H = 1120, 604
ALT = ("The paper's two central questions. Question 1: do everyday users want AI to explain itself? "
       "A daily app's AI pick offers 'Why am I seeing this?' with two choices. 'Not now' leads to the "
       "answer: not necessarily. XAI is not naturally accepted in daily life, and many people turn "
       "explanations down. Question 2: if so, how? 'Explain' leads to three ideal designs: "
       "contextualized understanding, adoption and adaptation, and multistakeholder values.")

HEAD, EYE = 30, 11.5
RX = 640                                      # right column (question 2)
CARD_EXTENT = (40, 30, 980, 556)              # what draw(card=True) covers: x0, y0, x1, y1


def draw(d, card=False):
    """Draw the figure into d. card=True is the compact research-page version:
    no descriptions or phone caption, shorter boxes, larger titles."""
    rx = 600 if card else RX
    arrow_marker(d, "arc", CLAY, 12)
    arrow_marker(d, "ars", STONE, 12)

    # ---------- column heads ----------
    d.text(40, 44, "QUESTION 1", EYE, CLAY, wt=600, ls=1.8)
    d.text(40, 84, "Do everyday users want AI to explain itself?", HEAD, INK, fam="serif")
    assert 40 + serif.w("Do everyday users want AI to explain itself?", HEAD) < rx - 40
    d.text(rx, 44, "QUESTION 2", EYE, CLAY, wt=600, ls=1.8)
    d.text(rx, 84, "If so, how?", HEAD, INK, fam="serif")

    # ---------- an everyday app ----------
    PX, PY, PW, PH = 40, 124, 160, 316
    d(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="26" fill="{FACE}" stroke="{INK}" stroke-width="2.4"/>')
    d(f'<rect x="{PX + PW / 2 - 22}" y="{PY + 14}" width="44" height="6" rx="3" fill="{LINE}"/>')
    ROW_X, ROW_W, ROW_H = PX + 14, PW - 28, 56
    ROWS = [PY + 40, PY + 116, PY + 192]
    HL = 1                                        # the highlighted row: an AI pick
    ICON_INK = INK_SOFT

    def music(x, y, c):
        d(f'<ellipse cx="{x + 16}" cy="{y + 27}" rx="5.5" ry="4.4" fill="{c}"/>'
          f'<path d="M{x + 21} {y + 27}V{y + 11}C{x + 23} {y + 15} {x + 28} {y + 15} {x + 28} {y + 20}" fill="none" '
          f'stroke="{c}" stroke-width="2" stroke-linecap="round"/>')

    def bag(x, y, c):
        d(f'<rect x="{x + 11}" y="{y + 16}" width="18" height="15" rx="3" fill="none" stroke="{c}" stroke-width="2"/>'
          f'<path d="M{x + 15.5} {y + 16}V{y + 13.5}A4.5 4.5 0 0 1 {x + 24.5} {y + 13.5}V{y + 16}" fill="none" stroke="{c}" stroke-width="2"/>')

    def news(x, y, c):
        d(f'<rect x="{x + 10}" y="{y + 11}" width="20" height="18" rx="2.5" fill="none" stroke="{c}" stroke-width="2"/>'
          f'<path d="M{x + 14} {y + 17}H{x + 26}M{x + 14} {y + 21}H{x + 26}M{x + 14} {y + 25}H{x + 21}" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>')

    def sparkle(cx, cy, r, c):
        d(f'<path d="M{f1(cx)} {f1(cy - r)}Q{f1(cx)} {f1(cy)} {f1(cx + r)} {f1(cy)}Q{f1(cx)} {f1(cy)} {f1(cx)} {f1(cy + r)}'
          f'Q{f1(cx)} {f1(cy)} {f1(cx - r)} {f1(cy)}Q{f1(cx)} {f1(cy)} {f1(cx)} {f1(cy - r)}Z" fill="{c}"/>')

    for k, (ry, icon) in enumerate(zip(ROWS, (music, bag, news))):
        hl = k == HL
        fill = BLUSH_TINT if hl else mix(STONE, FACE, 0.1)
        d(f'<rect x="{ROW_X}" y="{ry}" width="{ROW_W}" height="{ROW_H}" rx="12" fill="{fill}"'
          + (f' stroke="{CLAY}" stroke-width="1.4"' if hl else "") + "/>")
        d(f'<rect x="{ROW_X + 8}" y="{ry + 8}" width="40" height="40" rx="10" fill="{FACE}"/>')
        icon(ROW_X + 8, ry + 8, CLAY_DEEP if hl else ICON_INK)
        bar = CLAY if hl else mix(STONE, FACE, 0.45)
        d(f'<rect x="{ROW_X + 58}" y="{ry + 18}" width="{44 if k != 2 else 50}" height="7" rx="3.5" fill="{bar}"/>')
        d(f'<rect x="{ROW_X + 58}" y="{ry + 32}" width="{30 if k != 1 else 36}" height="6" rx="3" fill="{mix(STONE, FACE, 0.3)}"/>')
        if hl:
            sparkle(ROW_X + ROW_W - 14, ry + 19, 6.5, CLAY)
            sparkle(ROW_X + ROW_W - 25, ry + 10, 3.4, CLAY)
    for j in range(3):
        d(f'<circle cx="{PX + PW / 2 - 12 + 12 * j}" cy="{PY + PH - 34}" r="2.6" fill="{mix(STONE, FACE, 0.45)}"/>')
    for k, line in enumerate(() if card else ("What we listen to,", "buy, and read")):
        d.text(PX + PW / 2, PY + PH + 30 + 19 * k, line, 14.5, INK_SOFT, anchor="middle")

    # ---------- the prompt: Why am I seeing this? ----------
    QX, QW, QH = 236, 316, 124
    QY = ROWS[HL] + ROW_H / 2 - QH / 2
    hy = ROWS[HL] + ROW_H / 2
    d(f'<line x1="{ROW_X + ROW_W + 2}" y1="{hy}" x2="{QX}" y2="{hy}" stroke="{CLAY}" stroke-width="1.6" stroke-dasharray="2 4" stroke-linecap="round"/>')
    d(f'<circle cx="{ROW_X + ROW_W}" cy="{hy}" r="3.5" fill="{CLAY}"/>')
    d(f'<rect x="{QX}" y="{f1(QY + 4)}" width="{QW}" height="{QH}" rx="16" fill="{mix(INK, FRAME, 0.06)}"/>')   # soft shadow
    d(f'<rect x="{QX}" y="{f1(QY)}" width="{QW}" height="{QH}" rx="16" fill="{FACE}" stroke="{LINE}" stroke-width="1.3"/>')
    d(f'<circle cx="{QX + 32}" cy="{f1(QY + 38)}" r="11" fill="{CLAY}"/>')
    d.text(QX + 32, QY + 43, "i", 15, FACE, fam="serif", anchor="middle")
    d.text(QX + 52, QY + 44, "Why am I seeing this?", 17, INK, wt=600)
    assert QX + 52 + sw("Why am I seeing this?", 17, 600) < QX + QW - 16
    BH, BW = 38, 128
    by = QY + QH - BH - 22
    nx, ex = QX + 22, QX + QW - 22 - BW            # "Not now" left, "Explain" right
    d(f'<rect x="{nx}" y="{f1(by)}" width="{BW}" height="{BH}" rx="{BH / 2}" fill="{FACE}" stroke="{STONE}" stroke-width="1.4"/>')
    d.text(nx + BW / 2, by + BH / 2 + 5.4, "Not now", 15, INK_SOFT, wt=600, anchor="middle")
    d(f'<rect x="{ex}" y="{f1(by)}" width="{BW}" height="{BH}" rx="{BH / 2}" fill="{DARK}"/>')
    d.text(ex + BW / 2, by + BH / 2 + 5.4, "Explain", 15, FACE, wt=600, anchor="middle")

    # ---------- Not now -> not necessarily ----------
    NX, NY, NW, NH = QX, 452, QW + 24, (100 if card else 140)
    ax = nx + BW / 2
    d(f'<line x1="{ax}" y1="{f1(QY + QH + 10)}" x2="{ax}" y2="{NY - 8}" stroke="{STONE}" stroke-width="1.8" marker-end="url(#ars)"/>')
    d(f'<rect x="{NX}" y="{NY}" width="{NW}" height="{NH}" rx="16" fill="none" stroke="{STONE}" stroke-width="1.4" stroke-dasharray="5 5"/>')
    d.text(NX + 26, NY + 34, "NON-USE AND CONCERNS", 10.5, STONE, wt=600, ls=1.6)
    d.text(NX + 26, NY + 68 + (4 if card else 0), "Not necessarily", 31 if card else 26, INK, fam="serif")
    for k, line in enumerate(() if card else wrap("XAI is not naturally accepted in daily life, and many people turn explanations down",
                                  NW - 52, lambda s: sw(s, 15))):
        assert k < 2, line
        d.text(NX + 26, NY + 96 + 21 * k, line, 15, INK_SOFT)

    # ---------- Explain -> if so, how? ----------
    CW, CH, GAP = (380 if card else W - 20 - rx), (128 if card else 140), (20 if card else 18)
    CY0 = 112
    cards = [CY0 + k * (CH + GAP) for k in range(3)]
    BRX = rx - 26                                  # the bracket that fans out to the three cards
    jy = by + BH / 2
    d(f'<line x1="{QX + QW + 8}" y1="{f1(jy)}" x2="{BRX}" y2="{f1(jy)}" stroke="{CLAY}" stroke-width="1.8"/>')
    c0, c2 = cards[0] + CH / 2, cards[2] + CH / 2
    d(f'<path d="M{BRX} {f1(c0 + 12)}V{f1(c2 - 12)}" fill="none" stroke="{CLAY}" stroke-width="1.8"/>')
    for cy_top in cards:
        cy = cy_top + CH / 2
        if cy == c0:
            d(f'<path d="M{BRX} {f1(cy + 12)}Q{BRX} {f1(cy)} {BRX + 12} {f1(cy)}H{rx - 7}" fill="none" stroke="{CLAY}" stroke-width="1.8" marker-end="url(#arc)"/>')
        elif cy == c2:
            d(f'<path d="M{BRX} {f1(cy - 12)}Q{BRX} {f1(cy)} {BRX + 12} {f1(cy)}H{rx - 7}" fill="none" stroke="{CLAY}" stroke-width="1.8" marker-end="url(#arc)"/>')
        else:
            d(f'<line x1="{BRX}" y1="{f1(cy)}" x2="{rx - 7}" y2="{f1(cy)}" stroke="{CLAY}" stroke-width="1.8" marker-end="url(#arc)"/>')
    assert c0 < jy < c2

    def pin(x, y, c):
        d(f'<path d="M{x} {y + 14}C{x - 4} {y + 8} {x - 10} {y + 2} {x - 10} {y - 4}A10 10 0 0 1 {x + 10} {y - 4}'
          f'C{x + 10} {y + 2} {x + 4} {y + 8} {x} {y + 14}Z" fill="{c}"/>'
          f'<circle cx="{x}" cy="{y - 4}" r="3.6" fill="{BLUSH_TINT}"/>'
          f'<ellipse cx="{x}" cy="{y + 16}" rx="9" ry="2.6" fill="none" stroke="{c}" stroke-width="1.5"/>')

    def cycle(x, y, c):
        r = 11
        for a0, a1 in ((200, 340), (20, 160)):
            p0 = (x + r * cos(radians(a0)), y + r * sin(radians(a0)))
            p1 = (x + r * cos(radians(a1)), y + r * sin(radians(a1)))
            d(f'<path d="M{f1(p0[0])} {f1(p0[1])}A{r} {r} 0 0 1 {f1(p1[0])} {f1(p1[1])}" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>')
            # arrowhead at p1, pointing along the circle (clockwise in screen space)
            t = radians(a1 + 90)
            tx_, ty_ = cos(t), sin(t)
            nx_, ny_ = -ty_, tx_
            tip = (p1[0] + tx_ * 4.5, p1[1] + ty_ * 4.5)
            b1 = (p1[0] + nx_ * 4.2, p1[1] + ny_ * 4.2)
            b2 = (p1[0] - nx_ * 4.2, p1[1] - ny_ * 4.2)
            d(f'<path d="M{f1(tip[0])} {f1(tip[1])}L{f1(b1[0])} {f1(b1[1])}L{f1(b2[0])} {f1(b2[1])}Z" fill="{c}"/>')

    def group(x, y, c):
        person(d, x - 10, y - 4, 4.6, mix(c, FACE, 0.55))
        person(d, x + 10, y - 4, 4.6, mix(c, FACE, 0.55))
        person(d, x, y - 1, 5.4, c, ring=BLUSH_TINT)

    IDEALS = [
        ("Contextualized understanding", "Make sense of the AI within the person’s own situation, not in the abstract", pin),
        ("Adoption and adaptation", "Help people decide to adopt AI systems, and adapt to them over time", cycle),
        ("Multistakeholder values", "Weigh the values of everyone affected, beyond the person holding the phone", group),
    ]
    for top, (title, desc, icon) in zip(cards, IDEALS):
        d(f'<rect x="{rx}" y="{top}" width="{CW}" height="{CH}" rx="16" fill="{FACE}" stroke="{LINE}" stroke-width="1.2"/>')
        icx, icy = rx + 56, top + CH / 2
        d(f'<circle cx="{icx}" cy="{icy}" r="32" fill="{BLUSH_TINT}"/>')
        icon(icx, icy, CLAY_DEEP)
        tx = rx + 108
        if card:
            tl = wrap(title, CW - 108 - 18, lambda s: sw(s, 22, 600))
            assert len(tl) <= 2, tl
            for k, line in enumerate(tl):
                d.text(tx, top + CH / 2 + 8 - 13.5 * (len(tl) - 1) + 27 * k, line, 22, INK, wt=600)
            continue
        d.text(tx, top + 50, title, 18, INK, wt=600)
        assert tx + sw(title, 18, 600) < rx + CW - 20, title
        lines = wrap(desc, CW - 108 - 26, lambda s: sw(s, 15))
        assert len(lines) <= 3, lines
        for k, line in enumerate(lines):
            d.text(tx, top + 78 + 21 * k, line, 15, INK_SOFT)


if __name__ == "__main__":
    d = Doc(W, H, ALT)
    draw(d)
    print(d.render(OUT + "everyday-xai-concept.svg"))
