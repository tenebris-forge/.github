# Tenebris Forge logo

**The watching ember**: an eye inside the hexagon, its pupil a flame that burns past the
upper lid, three sparks rising from it. Something in the dark is watching, and it is on
fire. The hexagon and the sparks come from the Forja mark, so the studio and its tools read
as one family. Approved on 2026-11-25.

## Files

| File | Use |
|---|---|
| `mark.svg`, `mark.png` | The logo in full colour on transparent: anything from 64 px up |
| `mark-small.svg`, `favicon-16/32/48.png` | 16 to 48 px: no sparks, no core, heavier lines |
| `mark-black.svg`, `mark-white.svg`, `mark-mono.svg` | One colour: print, stamps, engraving, light or dark single-colour backgrounds |
| `avatar.svg`, `avatar.png` | Square on the dark background: GitHub, social profiles |
| `app-icon.svg`, `app-icon-180/192/512.png` | App and PWA icons; the mark sits inside the safe zone for maskable icons |
| `lockup-horizontal.svg/.png`, `lockup-stacked.svg/.png` | Mark with the name, for headers, covers and signatures |

Everything is drawn by [`scripts/logo.py`](../scripts/logo.py) on a 256 grid; change the
geometry there, never by hand in an exported file. PNGs come from the SVGs with resvg.
The name in the lockups is live text: convert it to outlines before print or merchandise.

## Colours

| Role | HEX |
|---|---|
| Ring | `#7a2fd6`, bevel `#a155b9` |
| Eye (ember) | `#ffc66e` to `#fb8e31` to `#e95904`; lid `#e95904` |
| Flame | `#e84fc0`, core `#ffc2ee` |
| Ink (outlines, iris) | `#1b1e24` |
| Background | `#120a1a` |
| Sparks | `#ffd28a`, `#fb8e31`, `#e84fc0` |

One-colour version: `#e84fc0`, or black or white.

## Rules

- **Clear space**: keep empty space around the mark equal to the ring's thickness (22 units
  of 256, about 9 % of its width) on every side.
- **Minimum size**: full mark 64 px; below that use `mark-small`. The horizontal lockup
  needs at least 160 px of width.
- **Backgrounds**: the colour mark goes on `#120a1a` or any dark, quiet background. On light
  backgrounds use `mark-black` or the colour mark on a dark tile (`avatar`).
- **Do not**: recolour parts, stretch or rotate it, add shadows or glows, put it on busy
  photos, separate the flame from the eye, or redraw the sparks elsewhere.
