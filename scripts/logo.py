#!/usr/bin/env python3
"""Draw the Tenebris Forge logo in the line of the Forja mark: the faceted anvil with a
hexagon at its heart and three sparks. Where Forja's hexagon holds a flame, Tenebris
Forge's holds the hooded smith of the first logo, eyes burning red.

    python3 scripts/logo.py

Writes brand/mark.svg (transparent), brand/avatar.svg (square, dark) and
brand/lockup.svg (mark beside the name).
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "brand"
INK = "#120810"
HORN, TOP, BODY, WAIST, FOOT = "#8e3a8f", "#6b2a73", "#4e1d5a", "#6b2a73", "#2f1238"
RING, BLOOD, EMBER = "#120810", "#9e1630", "#d62839"
EYE, SPARK1, SPARK2, SPARK3 = "#ff4d4d", "#ff3b3b", "#e84fc0", "#fb8e31"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"


def poly(points: str, fill: str, width: int = 14) -> str:
    return (f'<polygon points="{points}" fill="{fill}" stroke="{INK}" stroke-width="{width}" '
            f'stroke-linejoin="round" paint-order="stroke"/>')


def mark() -> str:
    """Same geometry as the Forja mark (viewBox 0 0 512 480)."""
    anvil = [
        poly("28,180 98,150 98,182", HORN), poly("28,180 98,182 98,218", TOP),
        poly("98,144 452,144 478,166 98,166", HORN), poly("98,166 478,166 458,234 98,234", TOP),
        poly("178,234 398,234 374,330 202,330", BODY), poly("202,330 374,330 432,370 144,370", WAIST),
        poly("144,370 432,370 456,424 120,424", FOOT),
    ]
    heart = (
        f'<polygon points="288,170 367.7,216 367.7,308 288,354 208.3,308 208.3,216" fill="{RING}"/>'
        f'<polygon points="288,190 350.4,226 350.4,298 288,334 225.6,298 225.6,226" fill="{BLOOD}"/>'
        f'<polygon points="288,204 338.2,233 338.2,291 288,320 237.8,291 237.8,233" fill="{EMBER}"/>'
        # the hood
        f'<path d="M288 214 C312 222 326 246 328 272 C330 288 334 300 338 310 L238 310 C242 300 246 288 248 272 '
        f'C250 246 264 222 288 214Z" fill="{RING}"/>'
        f'<path d="M288 244 C302 246 310 258 308 274 C306 286 298 292 288 294 C278 292 270 286 268 274 '
        f'C266 258 274 246 288 244Z" fill="#000"/>'
        f'<g filter="url(#glow)"><polygon points="271,266 284,270 283,275 271,272" fill="{EYE}"/>'
        f'<polygon points="305,266 292,270 293,275 305,272" fill="{EYE}"/></g>'
    )
    sparks = (
        f'<polygon points="402,74 420,92 402,110 384,92" fill="{SPARK1}" stroke="{INK}" stroke-width="8" stroke-linejoin="round" paint-order="stroke"/>'
        f'<polygon points="440,43 451,54 440,65 429,54" fill="{SPARK2}" stroke="{INK}" stroke-width="6" stroke-linejoin="round" paint-order="stroke"/>'
        f'<polygon points="356,50 364,58 356,66 348,58" fill="{SPARK3}" stroke="{INK}" stroke-width="5" stroke-linejoin="round" paint-order="stroke"/>'
    )
    return "<g>" + "".join(anvil) + heart + sparks + "</g>"


DEFS = ('<defs><filter id="glow" x="-100%" y="-300%" width="300%" height="700%">'
        '<feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<radialGradient id="g" cx="50%" cy="40%" r="62%"><stop offset="0" stop-color="#7a1d5a" stop-opacity=".65"/>'
        '<stop offset="1" stop-color="#7a1d5a" stop-opacity="0"/></radialGradient></defs>')


def svg(w: int, h: int, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Tenebris Forge">{DEFS}{body}</svg>\n'


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for old in ("emblem.svg", "emblem.png"):
        (OUT / old).unlink(missing_ok=True)
    (OUT / "mark.svg").write_text(svg(512, 480, mark()))
    (OUT / "avatar.svg").write_text(svg(512, 512, '<rect width="512" height="512" fill="#0b0610"/>'
                                              '<rect width="512" height="512" fill="url(#g)"/>'
                                              f'<g transform="translate(23.2 38.0) scale(0.92)">{mark()}</g>'))
    name = (f'<text x="520" y="232" font-family="{FONT}" font-size="104" font-weight="800" letter-spacing="6" fill="#f3e6ff">TENEBRIS</text>'
            f'<text x="522" y="352" font-family="{FONT}" font-size="104" font-weight="800" letter-spacing="6" fill="{SPARK1}">FORGE</text>')
    (OUT / "lockup.svg").write_text(svg(1180, 480, mark() + name))
    print("brand/ written")
