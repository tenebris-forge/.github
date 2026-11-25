#!/usr/bin/env python3
"""Outline the name "Tenebris Forge" in Geist (SIL Open Font Licence, the typeface of Forja's
app) at weight 800, so the lockups carry paths instead of live text.

    uv run --with 'fonttools[woff]' python3 scripts/wordmark.py

Writes brand/wordmark.json: one SVG path per word on a 1000-unit em, baseline at y=0, and
the advance widths. scripts/logo.py reads it; it does not need fontTools itself.
"""

import json
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "brand" / "fonts" / "geist-latin-wght-normal.woff2"
WEIGHT = 800
TRACKING = 10  # units of the 1000 em between letters


def outline(font, text):
    glyphs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    scale = 1000 / font["head"].unitsPerEm
    pen, x = SVGPathPen(glyphs), 0.0
    for ch in text:
        name = cmap[ord(ch)]
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, 0)))
        x += hmtx[name][0] * scale + TRACKING
    return pen.getCommands(), x - TRACKING


if __name__ == "__main__":
    font = instantiateVariableFont(TTFont(FONT), {"wght": WEIGHT})
    words = {}
    for word in ("Tenebris", "Forge"):
        d, width = outline(font, word)
        words[word] = {"d": d, "width": round(width, 1)}
    space = font["hmtx"][font.getBestCmap()[ord(" ")]][0] * 1000 / font["head"].unitsPerEm
    out = {"font": "Geist", "weight": WEIGHT, "em": 1000, "cap_height": 700, "space": round(space, 1), "words": words}
    (ROOT / "brand" / "wordmark.json").write_text(json.dumps(out, indent=1) + "\n")
    print({w: v["width"] for w, v in words.items()}, "space", round(space, 1))
