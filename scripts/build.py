#!/usr/bin/env python3
"""Draw the banner of the organization profile.

    python3 scripts/build.py

Dark, ember and magenta: the Tenebris Forge mood. System fonts only (GitHub serves SVGs
as images, so web fonts do not load).
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "profile"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"


def hexagon(cx, cy, r, rot=30):
    return " ".join(f"{cx + r * math.cos(math.radians(a + rot)):.1f},{cy + r * math.sin(math.radians(a + rot)):.1f}"
                    for a in range(0, 360, 60))


def embers(n, w, h, seed):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y, s = rnd.uniform(0, w), rnd.uniform(h * 0.6, h + 10), rnd.uniform(1.5, 4)
        dur, delay = rnd.uniform(5, 11), rnd.uniform(0, 10)
        c = rnd.choice(["#fb8e31", "#e95904", "#ffd28a", "#e84fc0"])
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.1f}" fill="{c}" opacity="0">'
                   f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{rnd.uniform(-40, 40):.0f} -{h * 0.8:.0f}" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0;.95;0" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def banner():
    w, h = 1200, 340
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Tenebris Forge">
<defs>
<radialGradient id="fire" cx="50%" cy="115%" r="70%"><stop offset="0" stop-color="#e95904" stop-opacity=".55"/><stop offset=".5" stop-color="#7a1d6a" stop-opacity=".25"/><stop offset="1" stop-color="#0b0610" stop-opacity="0"/></radialGradient>
<radialGradient id="veil" cx="50%" cy="0%" r="80%"><stop offset="0" stop-color="#3b1060" stop-opacity=".5"/><stop offset="1" stop-color="#0b0610" stop-opacity="0"/></radialGradient>
<linearGradient id="t" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ffe2c4"/><stop offset="1" stop-color="#fb8e31"/></linearGradient>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="c"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="{w}" height="{h}" fill="#0b0610"/>
<rect width="{w}" height="{h}" fill="url(#veil)"/>
<rect width="{w}" height="{h}" fill="url(#fire)"><animate attributeName="opacity" values="1;.8;1" dur="4s" repeatCount="indefinite"/></rect>
{embers(40, w, h, 13)}
<polygon points="{hexagon(600, 92, 30)}" fill="none" stroke="#e84fc0" stroke-opacity=".7" stroke-width="2.5"/>
<polygon points="{hexagon(600, 92, 18)}" fill="#fb8e31" filter="url(#glow)"><animate attributeName="opacity" values="1;.7;1" dur="3s" repeatCount="indefinite"/></polygon>
<text x="600" y="196" text-anchor="middle" font-family="{FONT}" font-size="66" font-weight="800" letter-spacing="10" fill="url(#t)" filter="url(#glow)">TENEBRIS FORGE</text>
<text x="600" y="244" text-anchor="middle" font-family="{FONT}" font-size="22" letter-spacing="2" fill="#c9b8d8">Horror games, web apps and tools, forged in darkness</text>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="none" stroke="#3a1f45"/>
</svg>'''


if __name__ == "__main__":
    (OUT / "banner.svg").write_text(banner())
    print("profile/banner.svg written")
