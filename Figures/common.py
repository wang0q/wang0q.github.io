"""Shared helpers for the site's figures: palette, text measuring, and a small SVG builder.

See README.md in this folder for how to run the scripts.
"""
import base64, html, io, logging, math, os
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

logging.getLogger("fontTools").setLevel(logging.ERROR)  # quiet harmless font-table warnings

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                  # the website folder
OUT = os.path.join(ROOT, "Images") + "/"
SOURCES = os.path.join(HERE, "sources") + "/"
FONTS = os.path.join(HERE, "fonts") + "/"
SERIF_FILE = FONTS + "cormorant-garamond-latin-600-normal.woff2"
SERIF_IT_FILE = FONTS + "cormorant-garamond-latin-500-italic.woff2"

# Site colours come from the palette file that style.css imports (Palettes/*.css),
# so re-running the scripts after a palette switch keeps the figures in step.
import re as _re

def _load_palette():
    css = open(ROOT + "/style.css").read()
    m = _re.search(r'@import url\("?(Palettes/[^")]+)"?\)', css)
    src = open(ROOT + "/" + m.group(1)).read() if m else css
    toks = dict(_re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6})", src))
    return (m.group(1) if m else "style.css"), toks

PALETTE_FILE, _T = _load_palette()
INK = _T["ink"]; INK_SOFT = _T["ink-soft"]; STONE = _T["stone"]; SAND = _T["sand"]
PAPER = _T["paper"]; PAPER_DEEP = _T["paper-deep"]; BLUSH = _T["blush"]; CLAY = _T["clay"]
CLAY_DEEP = _T["clay-deep"]; DARK = _T.get("dark", INK)
FRAME = _T.get("card", "#fbfaf7")          # figure-frame background
FACE = "#ffffff" if PAPER.lower() == "#ffffff" else "#fffefb"
LINE = None; BOARD = None; BLUSH_TINT = None  # set below (need mix)

SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
DISPLAY = "Manrope, Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"  # site headings
SERIF = "'EE Serif', 'Cormorant Garamond', Georgia, 'Times New Roman', serif"
SERIF_IT = "'EE Serif Italic', 'Cormorant Garamond', Georgia, 'Times New Roman', serif"


def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb2hex(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in c)

def mix(a, b, t):
    """t parts of a, (1-t) parts of b."""
    A, B = hex2rgb(a), hex2rgb(b); return rgb2hex([A[i] * t + B[i] * (1 - t) for i in range(3)])

def _lum(h):
    def ch(v):
        v /= 255; return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = hex2rgb(h); return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)


LINE = mix(INK, FRAME, 0.13)
BOARD = mix(PAPER_DEEP, FRAME, 0.85)
BLUSH_TINT = mix(BLUSH, FACE, 0.26)
SOFT_ACCENT = mix(BLUSH, FACE, 0.7)      # light accent text on dark fills

# Five bias categories, in pipeline order. Hues validated with the dataviz
# palette checker (all-pairs CVD 6.5 = floor band, so every swatch carries a text label).
CATS = [
    dict(key="historical", name="Historical", color="#2f8a5f", stage="State of the world"),
    dict(key="representation", name="Representation", color="#3f8fc4", stage="Sample"),
    dict(key="measurement", name="Measurement", color="#44509c", stage="Dataset"),
    dict(key="modeling", name="Modeling", color="#ad3a33", stage="Algorithms"),
    dict(key="deployment", name="Deployment", color="#bf7f1a", stage="Job applications"),
]
for c in CATS:
    c["tint"] = mix(c["color"], FACE, 0.12)
    c["tint2"] = mix(c["color"], FACE, 0.26)
    d, t = c["color"], 1.0
    while min(contrast(d, c["tint"]), contrast(d, BOARD)) < 4.8:
        t -= 0.03; d = mix(c["color"], "#1e1916", t)
    c["dark"] = d


class Measure:
    def __init__(self, path, idx=None, factor=1.0):
        f = TTFont(path, fontNumber=idx) if idx is not None else TTFont(path)
        self.cmap = f.getBestCmap(); self.hm = f["hmtx"].metrics; self.upm = f["head"].unitsPerEm
        self.fb = self.cmap.get(ord("n")); self.factor = factor

    def w(self, s, size, ls=0):
        tot = sum(self.hm[self.cmap.get(ord(ch), self.fb)][0] for ch in s)
        return (tot / self.upm * size + ls * max(len(s) - 1, 0)) * self.factor


class _Rough:
    """Fallback when Helvetica is missing (not macOS): an average-width estimate."""
    def __init__(self, em):
        self.em = em

    def w(self, s, size, ls=0):
        return len(s) * size * self.em + ls * max(len(s) - 1, 0)


HELV = "/System/Library/Fonts/Helvetica.ttc"
# Sans text is measured with Helvetica to wrap lines and check fits. Inter (the
# site's sans) runs a little wider, so widths are padded by 5%.
if os.path.exists(HELV):
    sans_r = Measure(HELV, 0, 1.05)
    sans_b = Measure(HELV, 1, 1.05)
else:
    sans_r, sans_b = _Rough(0.56), _Rough(0.6)
serif = Measure(SERIF_FILE)
serif_it = Measure(SERIF_IT_FILE)

def sw(s, size, wt=400, ls=0):
    return (sans_b if wt >= 600 else sans_r).w(s, size, ls)

def wrap(text, maxw, measure):
    """Greedy wrap; breaks at spaces and after hyphens inside words."""
    import re
    toks = []  # (piece, joiner-before)
    for i, word in enumerate(text.split(" ")):
        parts = re.findall(r"[^-]+-?|-", word)
        for j, p in enumerate(parts):
            toks.append((p, " " if (j == 0 and i > 0) else ""))
    lines, cur = [], ""
    for p, j in toks:
        t = cur + j + p if cur else p
        if not cur or measure(t) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = p
    if cur:
        lines.append(cur)
    return lines

def esc(s):
    return html.escape(s, quote=False)

def f1(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def _fontface(family, path, chars, weight, style):
    f = TTFont(path)
    o = Options(); o.flavor = "woff2"; o.layout_features = ["kern", "liga", "lnum"]; o.name_IDs = []
    o.notdef_outline = True; o.hinting = False
    sub = Subsetter(o); sub.populate(text="".join(sorted(chars)) + " "); sub.subset(f)
    f.flavor = "woff2"; buf = io.BytesIO(); f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")


class Doc:
    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.body, self.defs = [], []
        self.serif_chars, self.serif_it_chars = set(), set()

    def __call__(self, s):
        self.body.append(s)

    def text(self, x, y, t, size, fill=INK, fam="sans", wt=400, anchor="start", ls=0, extra="", spans=None):
        cls = {"sans": "s", "display": "dp", "serif": "f", "serif_it": "fi"}[fam]
        if fam == "serif":
            self.serif_chars.update(t if spans is None else "".join(p[0] for p in spans)); wt = 600
        if fam == "serif_it":
            self.serif_it_chars.update(t); wt = 500
        attrs = f' class="{cls}" x="{f1(x)}" y="{f1(y)}" font-size="{size}"'
        if wt != 400: attrs += f' font-weight="{wt}"'
        if anchor != "start": attrs += f' text-anchor="{anchor}"'
        if ls: attrs += f' letter-spacing="{ls}"'
        attrs += f' fill="{fill}"{extra}'
        if spans:
            inner = "".join(
                f'<tspan{"" if not a else " " + a}>{esc(p)}</tspan>' for p, a in spans)
        else:
            inner = esc(t)
        self.body.append(f"<text{attrs}>{inner}</text>")

    def render(self, path):
        css = []
        if self.serif_chars:
            css.append(_fontface("EE Serif", SERIF_FILE, self.serif_chars, 600, "normal"))
        if self.serif_it_chars:
            css.append(_fontface("EE Serif Italic", SERIF_IT_FILE, self.serif_it_chars, 500, "italic"))
        css.append(f".dp{{font-family:{DISPLAY}}}.s{{font-family:{SANS}}}.f{{font-family:{SERIF};font-variant-numeric:lining-nums}}.fi{{font-family:{SERIF_IT};font-style:italic}}")
        lab = html.escape(self.label)
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'width="{self.w}" height="{self.h}" role="img" aria-label="{lab}">',
               f"<title>{lab}</title>", "<defs>", "<style>" + "\n".join(css) + "</style>",
               *self.defs, "</defs>", *self.body, "</svg>", ""]
        with open(path, "w") as fh:
            fh.write("\n".join(out))
        return path


# ---------- shared drawings ----------
TONES = ["#d9aa82", "#8a5a3c", "#e8c7a3", "#5d3c2a", "#b8825a"]

def person(d, x, y, r, fill, ring=None):
    st = f' stroke="{ring}" stroke-width="{f1(r * 0.32)}"' if ring else ""
    d(f'<path d="M{f1(x - 1.8 * r)} {f1(y + 3.3 * r)}C{f1(x - 1.8 * r)} {f1(y + 1.6 * r)} {f1(x - 1 * r)} {f1(y + 1.28 * r)} '
      f'{f1(x)} {f1(y + 1.28 * r)}C{f1(x + 1 * r)} {f1(y + 1.28 * r)} {f1(x + 1.8 * r)} {f1(y + 1.6 * r)} {f1(x + 1.8 * r)} '
      f'{f1(y + 3.3 * r)}Z" fill="{fill}"{st}/>')
    d(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{fill}"{st}/>')

def pill(d, x, y, label, size=12.5, fill=BLUSH_TINT, color=CLAY_DEEP, anchor="start", h=22, pad=9):
    w = sw(label, size, 600) + 2 * pad
    if anchor == "end": x -= w
    if anchor == "middle": x -= w / 2
    d(f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{h}" rx="{h / 2}" fill="{fill}"/>')
    d.text(x + w / 2, y + h / 2 + size * 0.36, label, size, color, wt=600, anchor="middle")
    return w

def badge(d, cx, cy, n, r=13):
    d(f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{r}" fill="{BLUSH_TINT}"/>')
    d.text(cx, cy + 4.6, str(n), 13, CLAY_DEEP, wt=600, anchor="middle")

def arrow_marker(d, mid, color, size=11):
    d.defs.append(
        f'<marker id="{mid}" viewBox="0 0 10 10" refX="7.5" refY="5" markerUnits="userSpaceOnUse" '
        f'markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse">'
        f'<path d="M1.5 1.5L8 5L1.5 8.5" fill="none" stroke="{color}" stroke-width="1.7" '
        f'stroke-linecap="round" stroke-linejoin="round"/></marker>')
