# Figures

Scripts that draw the SVG figures in `Images/`. They take the colours from whichever palette `style.css` imports (`Palettes/*.css`), so **run them again after switching palettes**.

| Script | Writes |
|---|---|
| `equality_engine_concept.py` | `Images/equality-engine-concept.svg` |
| `equality_engine_board.py` | `Images/equality-engine-board.svg` |
| `equality_engine_cards.py` | `Images/equality-engine-cards.svg` |
| `social_assemblages_concept.py` | `Images/social-assemblages-concept.svg` |
| `social_assemblages_society.py` | `Images/social-assemblages-society.svg` (research-page card) |
| `social_assemblages_card.py` | `Images/social-assemblages-card.svg` (earlier card version, not used now) |
| `social_assemblages_overview.py` | `Images/social-assemblages-overview.svg` |
| `social_assemblages_storyboards.py` | `Images/social-assemblages-storyboards.svg` |
| `good_xai_concept.py` | `Images/good-xai-concept.svg` |
| `good_xai_card.py` | `Images/good-xai-card.svg` (research-page card; reuses the drawing in `good_xai_concept.py`) |
| `everyday_xai_concept.py` | `Images/everyday-xai-concept.svg` |
| `everyday_xai_card.py` | `Images/everyday-xai-card.svg` (research-page card; reuses the drawing in `everyday_xai_concept.py`) |

## Run

One-time setup:

```bash
pip3 install fonttools brotli pillow numpy
```

Rebuild all figures, from the website folder:

```bash
python3 Figures/build_all.py
```

Or rebuild one figure:

```bash
python3 Figures/equality_engine_board.py
```

## What's in here

- `common.py` holds the shared pieces: it reads the palette, measures text so lines wrap and fit, and embeds a small subset of the serif font in each SVG so headings match the site.
- `fonts/` has Cormorant Garamond (SemiBold and Medium Italic), the site's serif, by the Cormorant Project Authors, under the [SIL Open Font License](https://openfontlicense.org).
- `sources/storyboards/` has the 15 hand-drawn storyboards, cut out of the Figma export of the paper's grid. To refresh them from a new export, run `python3 Figures/extract_storyboard_tiles.py path/to/export.svg`.

## Notes

- Text is measured with Helvetica, so the scripts are meant to be run on macOS. Elsewhere they still run, but use rough text widths, so check that labels still fit.
- The five bias colours in the Equality Engine figures are fixed in `common.py` (`CATS`), not taken from the palette, and were checked for colour-blind contrast. Every one appears next to its text label.
- Text in each figure is real SVG text, so edit wording in the scripts, not in the SVG files.
