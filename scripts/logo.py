#!/usr/bin/env python3
"""Build every file of the Tenebris Forge logo, "the watching ember": an eye in the Forja
hexagon whose pupil is a flame burning past the upper lid, with three sparks.

    python3 scripts/logo.py

Writes, in brand/:
  mark.svg            full colour on transparent
  mark-small.svg      cut for 16-48 px: no sparks, core or bevel, heavier lines
  mark-black.svg, mark-white.svg, mark-mono.svg (one colour, magenta)
  avatar.svg          square, dark background (GitHub, social)
  app-icon.svg        square with safe padding for maskable app icons
  lockup-horizontal.svg, lockup-stacked.svg
PNGs are rendered from these with resvg (see brand/README.md). Geometry on a 256 grid; no clip paths
in the colour master. The name is outlined Geist 800 (scripts/wordmark.py writes brand/wordmark.json).
"""

import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "brand"
INK, VOID = "#1b1e24", "#120a1a"
RING, BEVEL = "#7a2fd6", "#a155b9"
EMBER_HI, EMBER, EMBER_LO, LID = "#ffc66e", "#fb8e31", "#e95904", "#e95904"
FLAME, CORE = "#e84fc0", "#ffc2ee"
SPARK_Y, SPARK_O, SPARK_M = "#ffd28a", "#fb8e31", "#e84fc0"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"


def hexagon(r, cx=128, cy=128):
    return [(cx + r * math.cos(math.radians(a - 90)), cy + r * math.sin(math.radians(a - 90))) for a in range(0, 360, 60)]


def sub(points):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points) + " Z"


def almond(x0, x1, cy, h):
    k = (x1 - x0) * 0.25
    return f"M{x0} {cy} C{x0 + k} {cy - h} {x1 - k} {cy - h} {x1} {cy} C{x1 - k} {cy + h} {x0 + k} {cy + h} {x0} {cy} Z"


def lid(x0, x1, cy, h):
    k = (x1 - x0) * 0.25
    return (f"M{x0} {cy} C{x0 + k} {cy - h} {x1 - k} {cy - h} {x1} {cy} "
            f"C{x1 - k} {cy - h * .35} {x0 + k} {cy - h * .35} {x0} {cy} Z")


def flame(cx, top, bottom, w):
    h = bottom - top
    return (f"M{cx} {top} C{cx + w * .55} {top + h * .25} {cx + w} {top + h * .45} {cx + w * .95} {top + h * .7} "
            f"C{cx + w * .9} {top + h * .9} {cx + w * .45} {bottom} {cx} {bottom} "
            f"C{cx - w * .45} {bottom} {cx - w * .9} {top + h * .9} {cx - w * .95} {top + h * .7} "
            f"C{cx - w} {top + h * .5} {cx - w * .55} {top + h * .38} {cx - w * .2} {top + h * .25} "
            f"C{cx - w * .05} {top + h * .42} {cx + w * .1} {top + h * .45} {cx + w * .2} {top + h * .42} "
            f"C{cx + w * .25} {top + h * .28} {cx + w * .1} {top + h * .12} {cx} {top} Z")


def diamond(x, y, r):
    return f"M{x} {y - r} L{x + r} {y} L{x} {y + r} L{x - r} {y} Z"


def circle(cx, cy, r):
    return f"M{cx - r} {cy} A{r} {r} 0 1 0 {cx + r} {cy} A{r} {r} 0 1 0 {cx - r} {cy} Z"


def ink(w):
    return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" paint-order="stroke"'


EYE = almond(60, 196, 128, 44)
LID_SHAPE = lid(60, 196, 128, 44)
IRIS = circle(128, 130, 30)
TIP = flame(128, 66, 152, 22)
CORE_SHAPE = flame(128, 104, 148, 11)
SPARKS = [(diamond(146, 70, 5), SPARK_Y, 5), (diamond(161, 81, 8), SPARK_O, 6), (diamond(178, 91, 5), SPARK_M, 5)]
RING_SHAPE = f"{sub(hexagon(116))} {sub(hexagon(94))}"
BEVEL_SHAPE = f"{sub(hexagon(102))} {sub(hexagon(94))}"
GRADIENT = ('<linearGradient id="tf-ember" gradientUnits="userSpaceOnUse" x1="0" y1="92" x2="0" y2="166">'
            f'<stop offset="0" stop-color="{EMBER_HI}"/><stop offset=".55" stop-color="{EMBER}"/>'
            f'<stop offset="1" stop-color="{EMBER_LO}"/></linearGradient>')


def colour(small=False):
    w = 14 if small else 10
    parts = [f'<path fill-rule="evenodd" fill="{RING}" d="{RING_SHAPE}"/>']
    if not small:
        parts.append(f'<path fill-rule="evenodd" fill="{BEVEL}" d="{BEVEL_SHAPE}"/>')
    parts += [f'<path fill="url(#tf-ember)" {ink(w)} d="{EYE}"/>',
              f'<path fill="{LID}" d="{LID_SHAPE}"/>',
              f'<path fill="{INK}" d="{circle(128, 130, 34 if small else 30)}"/>',
              f'<path fill="{FLAME}" {ink(w - 2)} d="{TIP if not small else flame(128, 62, 154, 26)}"/>']
    if not small:
        parts.append(f'<path fill="{CORE}" d="{CORE_SHAPE}"/>')
        parts += [f'<path fill="{c}" {ink(s)} d="{d}"/>' for d, c, s in SPARKS]
    return "".join(parts)


def mono(color, bg_hole=True):
    """One colour: ring, eye with the iris and a gap around the flame cut out, flame, sparks.
    The cut-outs use a mask (exports for print can flatten it in a vector editor)."""
    cut = (f'<mask id="m"><rect width="256" height="256" fill="#fff"/>'
           f'<path d="{IRIS}" fill="#000"/><path d="{TIP}" fill="#000" stroke="#000" stroke-width="16" stroke-linejoin="round"/>'
           f'</mask>')
    return (f'<defs>{cut}</defs><g fill="{color}">'
            f'<path fill-rule="evenodd" d="{RING_SHAPE}"/>'
            f'<path mask="url(#m)" d="{EYE}"/>'
            f'<path d="{TIP}"/>' + "".join(f'<path d="{d}"/>' for d, _, _ in SPARKS) + '</g>')


def svg(w, h, body, title="Tenebris Forge"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t"><title id="t">{title}</title>{body}</svg>\n')


WORDMARK = json.loads((Path(__file__).resolve().parent.parent / "brand" / "wordmark.json").read_text())


def name(x, baseline, size, anchor="start", color="#ffffff", accent=FLAME):
    """"Tenebris Forge" as outlines (Geist 800, scripts/wordmark.py), `size` the em in px."""
    w = WORDMARK["words"]
    s = size / WORDMARK["em"]
    total = (w["Tenebris"]["width"] + WORDMARK["space"] + w["Forge"]["width"]) * s
    x0 = x - total / 2 if anchor == "middle" else x
    x1 = x0 + (w["Tenebris"]["width"] + WORDMARK["space"]) * s
    return (f'<path fill="{color}" transform="translate({x0:.1f} {baseline}) scale({s:.4f})" d="{w["Tenebris"]["d"]}"/>'
            f'<path fill="{accent}" transform="translate({x1:.1f} {baseline}) scale({s:.4f})" d="{w["Forge"]["d"]}"/>')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    defs = f"<defs>{GRADIENT}</defs>"
    files = {
        "mark.svg": svg(256, 256, defs + colour()),
        "mark-small.svg": svg(256, 256, defs + colour(small=True), "Tenebris Forge, small sizes"),
        "mark-black.svg": svg(256, 256, mono("#111111")),
        "mark-white.svg": svg(256, 256, mono("#ffffff")),
        "mark-mono.svg": svg(256, 256, mono(FLAME)),
        "avatar.svg": svg(512, 512, f'<defs>{GRADIENT}<radialGradient id="g" cx="50%" cy="42%" r="60%">'
                                    f'<stop offset="0" stop-color="#3b1564"/><stop offset="1" stop-color="{VOID}"/></radialGradient></defs>'
                                    f'<rect width="512" height="512" fill="url(#g)"/><g transform="translate(36 36) scale(1.72)">{colour()}</g>'),
        "app-icon.svg": svg(512, 512, f'<defs>{GRADIENT}</defs><rect width="512" height="512" fill="{VOID}"/>'
                                      f'<g transform="translate(96 96) scale(1.25)">{colour(small=True)}</g>'),
        "lockup-horizontal.svg": svg(1040, 256, defs + colour() + name(282, 164, 96)),
        "lockup-stacked.svg": svg(560, 400, defs + f'<g transform="translate(152 0)">{colour()}</g>' + name(280, 352, 64, "middle")),
    }
    for f, s in files.items():
        (OUT / f).write_text(s)
    print("brand/:", " ".join(files))
