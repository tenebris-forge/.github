#!/usr/bin/env python3
"""Build the Tenebris Forge logo files from the mark (brand/mark.svg, the same faceted anvil
with the ember hexagon used by Forja's side menu).

    python3 scripts/logo.py

Writes brand/avatar.svg (square, dark background with a violet glow) and brand/lockup.svg
(mark beside the name).
"""

import re
from pathlib import Path

BRAND = Path(__file__).resolve().parent.parent / "brand"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
GLOW = ('<defs><radialGradient id="g" cx="50%" cy="40%" r="62%"><stop offset="0" stop-color="#7a2fd6" stop-opacity=".6"/>'
        '<stop offset="1" stop-color="#7a2fd6" stop-opacity="0"/></radialGradient></defs>')


def inner() -> str:
    return re.search(r"<g>.*</g>", (BRAND / "mark.svg").read_text(), re.S).group(0)


def svg(w: int, h: int, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Tenebris Forge">{body}</svg>\n'


if __name__ == "__main__":
    mark = inner()
    (BRAND / "avatar.svg").write_text(svg(512, 512, GLOW + '<rect width="512" height="512" fill="#120a1a"/>'
                                          '<rect width="512" height="512" fill="url(#g)"/>'
                                          f'<g transform="translate(23.2 38.0) scale(0.92)">{mark}</g>'))
    name = (f'<text x="520" y="232" font-family="{FONT}" font-size="104" font-weight="800" letter-spacing="6" fill="#ffffff">TENEBRIS</text>'
            f'<text x="522" y="352" font-family="{FONT}" font-size="104" font-weight="800" letter-spacing="6" fill="#fb8e31">FORGE</text>')
    (BRAND / "lockup.svg").write_text(svg(1180, 480, mark + name))
    print("brand/avatar.svg and brand/lockup.svg written")
