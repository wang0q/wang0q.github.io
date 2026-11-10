"""Cut the 15 storyboards out of a Figma export of the storyboard grid.

Usage:
    python3 extract_storyboard_tiles.py path/to/export.svg   (or a .png of the grid)

The export is the paper's grid: five columns (stages S1–S5) and three rows
(capability levels L1–L3), each storyboard inside a coloured frame. Each row's
frame colour is found automatically, and the inner area of every frame is saved to
sources/storyboards/L<row>-S<column>.jpg, which social_assemblages_storyboards.py reads.
Only needed again if the storyboards change.
"""
import base64, os, re, sys
from io import BytesIO

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "sources", "storyboards")
INSET = 4  # px trimmed inside each frame so no border colour bleeds in


def load(path):
    if path.lower().endswith(".svg"):
        s = open(path).read()
        m = re.search(r"data:image/(?:png|jpeg);base64,([A-Za-z0-9+/=]+)", s)
        if not m:
            sys.exit("No embedded raster image found in the SVG.")
        im = Image.open(BytesIO(base64.b64decode(m.group(1))))
    else:
        im = Image.open(path)
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB")


def runs(idx):
    out, start, prev = [], None, None
    for i in idx:
        if start is None:
            start = prev = i
        elif i == prev + 1:
            prev = i
        else:
            out.append((start, prev)); start = prev = i
    if start is not None:
        out.append((start, prev))
    return out


def frame_colours(a):
    """The saturated colour of each row's frames, read down the first frames' left edge."""
    h, w, _ = a.shape
    sat = a.max(axis=2) - a.min(axis=2)
    for x in range(w // 20, w // 2):          # first column where a strong colour runs a long way down
        col = sat[:, x] > 80
        if col.sum() > h * 0.5:
            break
    colours = []
    for y0, y1 in runs(np.where(sat[:, x] > 80)[0]):
        if y1 - y0 > h * 0.1:
            colours.append(tuple(int(v) for v in np.median(a[y0:y1, x], axis=0)))
    return colours


def main(path):
    img = load(path)
    a = np.array(img).astype(int)
    h, w, _ = a.shape
    colours = frame_colours(a)
    if len(colours) != 3:
        sys.exit(f"Expected 3 frame colours (one per row), found {len(colours)}: {colours}")
    os.makedirs(OUT_DIR, exist_ok=True)
    for r, c in enumerate(colours):
        m = np.abs(a - np.array(c)).sum(axis=2) < 60
        hl = runs(np.where(m.sum(axis=1) > w * 0.25)[0])
        y0, y1 = hl[0][1] + 1 + INSET, hl[-1][0] - INSET
        vl = runs(np.where(m[hl[0][0]:hl[-1][1] + 1].sum(axis=0) > (hl[-1][1] - hl[0][0]) * 0.8)[0])
        if len(vl) != 10:
            sys.exit(f"Row L{r + 1}: expected 10 vertical frame edges, found {len(vl)}")
        for s in range(5):
            x0, x1 = vl[2 * s][1] + 1 + INSET, vl[2 * s + 1][0] - INSET
            out = os.path.join(OUT_DIR, f"L{r + 1}-S{s + 1}.jpg")
            img.crop((x0, y0, x1, y1)).save(out, "JPEG", quality=92, optimize=True)
    print(f"Saved 15 storyboards to {OUT_DIR}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
