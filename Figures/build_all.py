"""Regenerate every figure in Images/ that these scripts draw.

Usage (from the website folder):
    python3 Figures/build_all.py
"""
import os, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = [
    "equality_engine_concept.py",
    "equality_engine_board.py",
    "equality_engine_cards.py",
    "social_assemblages_concept.py",
    "social_assemblages_society.py",
    "social_assemblages_card.py",
    "social_assemblages_overview.py",
    "social_assemblages_storyboards.py",
    "good_xai_concept.py",
    "good_xai_card.py",
    "everyday_xai_concept.py",
    "everyday_xai_card.py",
]

sys.path.insert(0, HERE)
from common import PALETTE_FILE  # noqa: E402

print(f"Palette: {PALETTE_FILE}")
for name in SCRIPTS:
    runpy.run_path(os.path.join(HERE, name), run_name="__main__")
