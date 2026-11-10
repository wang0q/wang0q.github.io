"""Home-page card image for Social Assemblages: the human–AI assemblage and the people it reaches.

A pared-down version of social_assemblages_concept.py (one combined scene, few words),
laid out to fill the roughly 4:3 image box of the home page's featured card.
"""
from common import *

W, H = 760, 520
d = Doc(W, H, "A user and their social AI sit together inside a human–AI assemblage and co-shape each other. "
              "The AI polishes what the user sends to other people and filters what comes back, and one of "
              "those people is unaware the AI is involved.")
arrow_marker(d, "arc", CLAY, 14)
arrow_marker(d, "ars", STONE, 13)

# ---------- the assemblage ----------
ACX, ACY = 245, 262
d(f'<ellipse cx="{ACX}" cy="{ACY}" rx="215" ry="172" fill="{mix(BLUSH, FACE, 0.16)}" stroke="{BLUSH}" stroke-width="2" stroke-dasharray="7 6"/>')
d.text(ACX, ACY - 118, "HUMAN–AI ASSEMBLAGE", 13.5, CLAY_DEEP, wt=600, anchor="middle", ls=1.8)

# the user
ux, uy = 145, 228
person(d, ux, uy, 27, TONES[1])
d.text(ux, uy + 126, "User", 18, INK_SOFT, wt=600, anchor="middle")

# the social AI (a friendly robot, after the storyboards), drawn around (0, 0) and scaled
rx_, ry_ = 345, 240
d(f'<g transform="translate({rx_} {ry_}) scale(1.32)">'
  f'<line x1="0" y1="-30" x2="0" y2="-40" stroke="{INK}" stroke-width="2"/>'
  f'<circle cx="0" cy="-43" r="4" fill="{CLAY}"/>'
  f'<rect x="-26" y="-30" width="52" height="44" rx="13" fill="{BLUSH}" stroke="{INK}" stroke-width="2"/>'
  f'<rect x="-17" y="-19" width="34" height="20" rx="8" fill="{FACE}"/>'
  f'<circle cx="-7" cy="-9" r="3" fill="{INK}"/><circle cx="7" cy="-9" r="3" fill="{INK}"/>'
  f'<rect x="-19" y="19" width="38" height="30" rx="9" fill="{BLUSH}" stroke="{INK}" stroke-width="2"/>'
  f'<circle cx="-30" cy="0" r="4.5" fill="{BLUSH}" stroke="{INK}" stroke-width="1.6"/>'
  f'<circle cx="30" cy="0" r="4.5" fill="{BLUSH}" stroke="{INK}" stroke-width="1.6"/></g>')
d.text(rx_, uy + 126, "Social AI", 18, INK_SOFT, wt=600, anchor="middle")

# co-shaping arrows
mx = (ux + rx_) / 2
d(f'<path d="M{ux + 48} {uy - 22}Q{mx} {uy - 68} {rx_ - 54} {uy - 22}" fill="none" stroke="{CLAY}" stroke-width="2.2" marker-end="url(#arc)"/>')
d(f'<path d="M{rx_ - 54} {uy + 64}Q{mx} {uy + 104} {ux + 54} {uy + 64}" fill="none" stroke="{CLAY}" stroke-width="2.2" marker-end="url(#arc)"/>')
d.text(mx, uy + 30, "co-shape", 27, CLAY_DEEP, fam="serif_it", anchor="middle")

# ---------- other people ----------
d.text(668, 118, "OTHERS", 13.5, STONE, wt=600, anchor="middle", ls=1.8)
for (px, py, t) in ((625, 168, 2), (712, 196, 4)):
    person(d, px, py, 18, TONES[t])
ox, oy = 668, 318
d(f'<circle cx="{ox}" cy="{oy + 23}" r="52" fill="none" stroke="{STONE}" stroke-width="1.5" stroke-dasharray="4 5"/>')
person(d, ox, oy, 18, mix(TONES[0], FACE, 0.55))
d.text(ox, oy + 106, "unaware", 24, INK_SOFT, fam="serif_it", anchor="middle")

# signal arrows through the AI
ax0, ax1 = 474, 592
d(f'<line x1="{ax0}" y1="232" x2="{ax1}" y2="232" stroke="{INK}" stroke-width="2.2" marker-end="url(#ars)"/>')
d.text((ax0 + ax1) / 2, 216, "polishes", 18, INK, anchor="middle")
d(f'<line x1="{ax1}" y1="290" x2="{ax0}" y2="290" stroke="{INK}" stroke-width="2.2" marker-end="url(#ars)"/>')
d.text((ax0 + ax1) / 2, 318, "filters", 18, INK, anchor="middle")

print(d.render(OUT + "social-assemblages-card.svg"))
