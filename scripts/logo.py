#!/usr/bin/env python3
"""Draw the Tenebris Forge logo: the hooded smith with the raised hammer over the anvil,
in flat faceted shapes with dark outlines (the style of the Forja marks).

    python3 scripts/logo.py

Writes brand/emblem.svg (transparent), brand/avatar.svg (square, dark background) and
brand/lockup.svg (emblem over the name).
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "brand"
INK = "#1b1e24"
P1, P2, P3, P4 = "#a155b9", "#713989", "#52216a", "#3d1752"
CLOAK, CLOAK2, VOID = "#2a1838", "#3a2250", "#0b0610"
RED, EMBER, SPARK = "#ff3b3b", "#fb8e31", "#ffd28a"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"


def poly(points, fill, stroke=INK, width=10, extra=""):
    pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in points)
    s = f' stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" paint-order="stroke"' if stroke else ""
    return f'<polygon points="{pts}" fill="{fill}"{s}{extra}/>'


def flame(x, base, h, w, color, lean=0.0):
    """One curved tongue of fire: wide at the base, a hooked tip."""
    tip = x + lean * h * 0.25
    d = (f"M{x - w:.0f},{base:.0f} "
         f"C{x - w * 1.25:.0f},{base - h * .45:.0f} {x - w * .2:.0f},{base - h * .5:.0f} {x - w * .45:.0f},{base - h * .78:.0f} "
         f"C{x - w * .1:.0f},{base - h * .7:.0f} {tip - w * .1:.0f},{base - h * .9:.0f} {tip:.0f},{base - h:.0f} "
         f"C{tip + w * .35:.0f},{base - h * .8:.0f} {x + w * 1.3:.0f},{base - h * .5:.0f} {x + w:.0f},{base:.0f} Z")
    return (f'<path d="{d}" fill="{color}" stroke="{INK}" stroke-width="10" stroke-linejoin="round" '
            f'paint-order="stroke"/>')


def flames():
    out = []
    tongues = [(-3.1, 150, 40, P4, -1), (3.1, 150, 40, P4, 1), (-2.1, 215, 44, P3, -.6), (2.1, 215, 44, P3, .6),
               (-1.05, 255, 46, P3, -.3), (1.05, 255, 46, P3, .3), (0, 285, 50, P2, .1)]
    for k, h, w, color, lean in tongues:
        out.append(flame(256 + k * 58, 330, h, w, color, lean))
    return "".join(out)


def smith():
    hood = [(256, 112), (300, 132), (326, 182), (334, 250), (360, 300), (152, 300), (178, 250), (186, 182), (212, 132)]
    lit = [(256, 112), (212, 132), (186, 182), (178, 250), (152, 300), (206, 300), (210, 200), (232, 140)]
    face = [(228, 172), (284, 172), (296, 222), (256, 248), (216, 222)]
    eyes = poly([(232, 200), (250, 205), (248, 212), (230, 208)], RED, stroke=None) + \
           poly([(280, 200), (262, 205), (264, 212), (282, 208)], RED, stroke=None)
    glow = f'<g opacity=".55" filter="url(#eye)">{eyes}</g>'
    arm = poly([(192, 236), (214, 252), (170, 186), (150, 196)], CLOAK2)
    handle = poly([(150, 202), (162, 196), (128, 110), (116, 116)], P3, width=8)
    head = poly([(84, 104), (142, 80), (154, 110), (96, 134)], P1)
    head_side = poly([(96, 134), (154, 110), (158, 120), (100, 144)], P2, width=8)
    return (poly(hood, CLOAK) + poly(lit, CLOAK2, stroke=None) + poly(face, VOID, width=8) + glow + eyes +
            handle + head + head_side + arm)


def anvil():
    # the anvil of the Forja mark, scaled under the smith
    parts = [([(28, 180), (98, 150), (98, 182)], P1), ([(28, 180), (98, 182), (98, 218)], P2),
             ([(98, 144), (452, 144), (478, 166), (98, 166)], P1), ([(98, 166), (478, 166), (458, 234), (98, 234)], P2),
             ([(178, 234), (398, 234), (374, 330), (202, 330)], P3), ([(202, 330), (374, 330), (432, 370), (144, 370)], P2),
             ([(144, 370), (432, 370), (456, 424), (120, 424)], P4)]
    s, dx, dy = 0.58, 256 - 253 * 0.58, 292 - 144 * 0.58
    return "".join(poly([(dx + x * s, dy + y * s) for x, y in pts], c, width=12) for pts, c in parts)


def sparks():
    items = [(256, 268, 9, RED), (232, 252, 6, EMBER), (284, 246, 7, RED), (300, 266, 5, SPARK), (214, 270, 5, EMBER),
             (268, 230, 5, SPARK), (244, 226, 4, RED)]
    return "".join(poly([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], c, width=4) for x, y, r, c in items)


DEFS = f'''<defs>
<filter id="eye" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="5"/></filter>
<radialGradient id="g" cx="50%" cy="46%" r="52%"><stop offset="0" stop-color="{P3}" stop-opacity=".55"/><stop offset="1" stop-color="{P3}" stop-opacity="0"/></radialGradient>
<radialGradient id="f" cx="50%" cy="62%" r="22%"><stop offset="0" stop-color="{RED}" stop-opacity=".45"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
</defs>'''


def emblem():
    return flames() + smith() + anvil() + sparks()


def write(name, body, w=512, h=512):
    (OUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Tenebris Forge">{DEFS}{body}</svg>\n')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    write("emblem.svg", f'<g transform="translate(0 20)">{emblem()}</g>')
    write("avatar.svg", f'<rect width="512" height="512" fill="{VOID}"/><rect width="512" height="512" fill="url(#g)"/>'
                        f'<rect width="512" height="512" fill="url(#f)"/><g transform="translate(0 24)">{emblem()}</g>')
    text = (f'<text x="256" y="530" text-anchor="middle" font-family="{FONT}" font-size="58" font-weight="800" '
            f'letter-spacing="8" fill="#ffe2c4">TENEBRIS</text>'
            f'<text x="256" y="590" text-anchor="middle" font-family="{FONT}" font-size="58" font-weight="800" '
            f'letter-spacing="8" fill="{EMBER}">FORGE</text>')
    write("lockup.svg", f'<rect width="512" height="620" fill="{VOID}"/><rect width="512" height="512" fill="url(#g)"/>'
                        f'<g transform="translate(0 6)">{emblem()}</g>{text}', 512, 620)
    print("brand/ written")
