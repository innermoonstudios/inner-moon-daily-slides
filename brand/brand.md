---
client: inner-moon
type: brand-sheet
version: 1.0
locked: 2026-10-12
---

# Inner Moon brand sheet

**Direction:** Almanac layout × Flirty Moon. Uses A's serif type, double frame and star dividers, set on B's starry night with the flirty moon as mascot.
Source of truth for values: [[tokens.json]]. Voice: [[voice]].

## Palette (sampled from the profile picture)
| Name | Hex | Use |
| --- | --- | --- |
| Void | #16131C | Background, starfield base |
| Night | #1C1723 | Panels |
| Plum | #3C3242 | Secondary surfaces |
| Nebula | #89688D | Sky glows only, never text |
| Cream | #F7D59B | Headlines, frame, dividers |
| Gold | #FDF4CC | Body text, stars |
| Blush | #F2B191 | Accent: kickers, glyphs, "Ask yourself" rule |

## Type
- **Schola** (TeX Gyre Schola, a Century Schoolbook revival), bundled in `fonts/`. Bold for headlines, italic for questions and subs, regular for body.
- **DejaVu Sans** for zodiac glyphs only.
- Kicker: 26 px, uppercase, wide tracking, blush.

## The Moon (mascot)
- File: `assets/moon.png`, cut from `profile-picture.jpg`.
- Sizes: 400 px on the hook, 150 px in the sign-slide corner, 320 px on the CTA. Use one moon per slide.
- Never recolour, crop or distort her, and never regenerate her with AI. She is the original artwork.
- If a higher-resolution original of the profile picture exists, replace `profile-picture.jpg` and re-cut the moon.

## Layout rules
- Canvas 1080×1350. Keep all text above 1100 px; the app covers the bottom.
- Double cream frame at 40 px inset. Divider = two rules with a star between them.
- Sparkles live in the bottom zone only. A new starfield is generated each day.

## Fonts licence
TeX Gyre Schola: GUST Font License (free to use and redistribute). DejaVu Sans: free licence (Bitstream Vera derivative).
