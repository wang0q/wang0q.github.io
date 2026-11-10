"""Concept figure for Social Assemblages: a human–AI assemblage, its tensions, and the design shift."""
from common import *

W, H = 1120, 600
MID = 560
d = Doc(W, H, "Concept of the study. A user and their social AI form a human–AI assemblage in which they "
              "co-shape each other. The AI polishes what the user sends out and filters what comes in from "
              "other people, some of whom are drawn in without knowing. Tensions arise for the individual "
              "(blurred agency and identity; quantified sociality) and between people (short-term ease, "
              "long-term erosion; AI as a social third party). The paper calls for a shift from user-centered "
              "to relational and provocative design.")
arrow_marker(d, "arc", CLAY, 12)
arrow_marker(d, "ars", STONE, 11)

# column heads
for x, eb, head in ((40, "THE INDIVIDUAL", "Inside the human–AI assemblage"),
                    (MID + 30, "THE INTERPERSONAL", "Between the assemblage and others")):
    d.text(x, 38, eb, 11.5, CLAY, wt=600, ls=1.8)
    d.text(x, 70, head, 25, INK, fam="serif")
d(f'<line x1="{MID}" y1="22" x2="{MID}" y2="462" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="4 5"/>')

# ---------- the assemblage ----------
ACX, ACY = 300, 214
d(f'<ellipse cx="{ACX}" cy="{ACY}" rx="214" ry="104" fill="{mix(BLUSH, FACE, 0.16)}" stroke="{BLUSH}" stroke-width="1.6" stroke-dasharray="6 5"/>')
d.text(ACX, ACY - 76, "HUMAN–AI ASSEMBLAGE", 10.5, CLAY_DEEP, wt=600, anchor="middle", ls=1.6)

# the user
ux, uy = 196, 190
person(d, ux, uy, 19, TONES[1], ring=None)
d.text(ux, uy + 84, "User", 13, INK_SOFT, wt=600, anchor="middle")

# the social AI (a friendly robot, after the storyboards)
rx_, ry_ = 382, 196
d(f'<line x1="{rx_}" y1="{ry_ - 30}" x2="{rx_}" y2="{ry_ - 40}" stroke="{INK}" stroke-width="2"/>'
  f'<circle cx="{rx_}" cy="{ry_ - 43}" r="4" fill="{CLAY}"/>'
  f'<rect x="{rx_ - 26}" y="{ry_ - 30}" width="52" height="44" rx="13" fill="{BLUSH}" stroke="{INK}" stroke-width="2"/>'
  f'<rect x="{rx_ - 17}" y="{ry_ - 19}" width="34" height="20" rx="8" fill="{FACE}"/>'
  f'<circle cx="{rx_ - 7}" cy="{ry_ - 9}" r="3" fill="{INK}"/><circle cx="{rx_ + 7}" cy="{ry_ - 9}" r="3" fill="{INK}"/>'
  f'<rect x="{rx_ - 19}" y="{ry_ + 19}" width="38" height="30" rx="9" fill="{BLUSH}" stroke="{INK}" stroke-width="2"/>'
  f'<circle cx="{rx_ - 30}" cy="{ry_ + 0}" r="4.5" fill="{BLUSH}" stroke="{INK}" stroke-width="1.6"/>'
  f'<circle cx="{rx_ + 30}" cy="{ry_ + 0}" r="4.5" fill="{BLUSH}" stroke="{INK}" stroke-width="1.6"/>')
d.text(rx_, uy + 84, "Social AI", 13, INK_SOFT, wt=600, anchor="middle")

# co-shaping arrows
d(f'<path d="M{ux + 40} {uy - 18}Q{(ux + rx_) / 2} {uy - 54} {rx_ - 42} {uy - 18}" fill="none" stroke="{CLAY}" stroke-width="1.8" marker-end="url(#arc)"/>')
d(f'<path d="M{rx_ - 42} {uy + 44}Q{(ux + rx_) / 2} {uy + 80} {ux + 40} {uy + 44}" fill="none" stroke="{CLAY}" stroke-width="1.8" marker-end="url(#arc)"/>')
d.text((ux + rx_) / 2, uy + 16, "co-shape", 18, CLAY_DEEP, fam="serif_it", anchor="middle")
d.text((ux + rx_) / 2, uy + 36, "each other", 18, CLAY_DEEP, fam="serif_it", anchor="middle")

# ---------- other people ----------
others = [(760, 150, 2, False), (900, 178, 4, False), (842, 270, 0, True)]
for (px, py, t, unaware) in others:
    if unaware:
        d(f'<circle cx="{px}" cy="{py + 18}" r="40" fill="none" stroke="{STONE}" stroke-width="1.3" stroke-dasharray="3 4"/>')
    person(d, px, py, 13.5, TONES[t] if not unaware else mix(TONES[t], FACE, 0.55))
d.text(842 + 50, 300, "drawn in", 15.5, INK_SOFT, fam="serif_it")
d.text(842 + 50, 318, "without knowing", 15.5, INK_SOFT, fam="serif_it")
d.text(830, 112, "OTHER PEOPLE", 10.5, STONE, wt=600, anchor="middle", ls=1.6)

# signal arrows through the AI
ax0, ax1 = 452, 708
d(f'<line x1="{ax0}" y1="186" x2="{ax1}" y2="186" stroke="{INK}" stroke-width="1.8" marker-end="url(#ars)"/>')
d.text((ax0 + ax1) / 2 + 30, 176, "polishes what goes out", 13, INK, anchor="middle")
d(f'<line x1="{ax1}" y1="236" x2="{ax0}" y2="236" stroke="{INK}" stroke-width="1.8" marker-end="url(#ars)"/>')
d.text((ax0 + ax1) / 2 + 30, 258, "filters what comes in", 13, INK, anchor="middle")

# ---------- tensions ----------
CARDS = [
    (40, "Blurred agency and identity", "Convenience now, but social skills and a sense of self at risk"),
    (300, "Quantified sociality", "Social metrics offer insight, and stir up anxiety"),
    (MID + 30, "Short-term ease, long-term erosion", "Filtered, polished exchanges feel easier but less authentic"),
    (MID + 290, "AI as a social third party", "A non-judgmental advisor for the user; privacy and consent harms for others"),
]
ty0, tw, th = 352, 240, 112
d.text(40, ty0 - 14, "TENSIONS", 10.5, STONE, wt=600, ls=1.6)
d.text(MID + 30, ty0 - 14, "TENSIONS", 10.5, STONE, wt=600, ls=1.6)
for x, title, desc in CARDS:
    d(f'<rect x="{x}" y="{ty0}" width="{tw}" height="{th}" rx="14" fill="{FACE}" stroke="{LINE}" stroke-width="1.2"/>')
    d(f'<rect x="{x}" y="{ty0 + 18}" width="3" height="24" rx="1.5" fill="{BLUSH}"/>')
    tl = wrap(title, tw - 40, lambda s: sw(s, 15, 600))
    for k, line in enumerate(tl):
        d.text(x + 20, ty0 + 35 + 19 * k, line, 15, INK, wt=600)
    dl = wrap(desc, tw - 40, lambda s: sw(s, 13.5))
    y = ty0 + 35 + 19 * (len(tl) - 1) + 24
    assert y + 19 * (len(dl) - 1) <= ty0 + th - 12, (title, dl)
    for k, line in enumerate(dl):
        d.text(x + 20, y + 19 * k, line, 13.5, INK_SOFT)

# ---------- the design shift ----------
by = 492
d(f'<rect x="20" y="{by}" width="{W - 40}" height="88" rx="16" fill="{mix(BLUSH, FACE, 0.14)}"/>')
d.text(44, by + 50, "THE CALL", 10.5, CLAY, wt=600, ls=1.6)
bx1 = 172
d.text(bx1, by + 40, "From user-centered design", 22, STONE, fam="serif")
d.text(bx1, by + 64, "optimizing one user’s immediate experience", 13.5, INK_SOFT)
ax = bx1 + 330
d(f'<line x1="{ax}" y1="{by + 44}" x2="{ax + 52}" y2="{by + 44}" stroke="{CLAY}" stroke-width="2.2" stroke-linecap="round" marker-end="url(#arc)"/>')
bx2 = ax + 80
d.text(bx2, by + 40, "To relational and provocative design", 22, CLAY, fam="serif")
d.text(bx2, by + 64, "designing for relationships, with purposeful friction", 13.5, INK)
assert bx2 + serif.w("To relational and provocative design", 22) <= W - 40
assert bx2 + sw("designing for relationships, with purposeful friction", 13.5) <= W - 40

print(d.render(OUT + "social-assemblages-concept.svg"))
