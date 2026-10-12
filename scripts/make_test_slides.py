"""Render 5 placeholder carousel slides (1080x1350 JPEG) to prove the pipeline.

Usage: python scripts/make_test_slides.py <output_dir>
Real content templates replace this in Phase 6; the size and format stay the same.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
IVORY, ESPRESSO, TAUPE = (246, 241, 232), (59, 42, 32), (150, 128, 108)

SLIDES = [
    ("Today's sky", "element sky slide (placeholder)"),
    ("Sign 1", "interaction + question (placeholder)"),
    ("Sign 2", "interaction + question (placeholder)"),
    ("Sign 3", "interaction + question (placeholder)"),
    ("Inner Moon Store", "daily prompting (placeholder CTA)"),
]


def font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # very old Pillow
        return ImageFont.load_default()


def centered(draw, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    for i, (title, sub) in enumerate(SLIDES, start=1):
        img = Image.new("RGB", (W, H), IVORY)
        d = ImageDraw.Draw(img)
        d.rectangle([40, 40, W - 40, H - 40], outline=TAUPE, width=3)
        d.ellipse([W / 2 - 90, 260, W / 2 + 90, 440], outline=ESPRESSO, width=6)
        d.ellipse([W / 2 - 40, 250, W / 2 + 120, 410], fill=IVORY)  # crescent
        centered(d, 560, title, font(84), ESPRESSO)
        centered(d, 690, sub, font(40), TAUPE)
        centered(d, 1120, f"Pipeline test  ·  slide {i}/{len(SLIDES)}", font(36), TAUPE)
        centered(d, 1175, stamp, font(30), TAUPE)
        path = out / f"slide-{i}.jpg"
        img.save(path, "JPEG", quality=92)
        print(path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "site")
