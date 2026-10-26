#!/usr/bin/env python3
"""Add a white meme footer caption (and optional name labels) to a photo.

Usage:
  python3 add_caption.py INPUT OUTPUT --caption "Text" [--label "x,y,Text" ...]

  --label positions are fractions of the photo: x=0..1 from the left,
  y=0..1 from the top, marking the CENTER of the label.

Requires Pillow (pip install pillow).
"""
import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is missing: run  pip install pillow  (add --break-system-packages if pip asks)")

BOLD_FONTS = [
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def load_font(size):
    for path in BOLD_FONTS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    try:
        return ImageFont.load_default(size=size)  # Pillow >= 10.1
    except TypeError:
        return ImageFont.load_default()


def text_width(draw, text, font, stroke=0):
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    return box[2] - box[0]


def wrap(draw, text, font, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if text_width(draw, trial, font) <= max_width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit_caption(draw, text, width, max_lines=2):
    size = int(width * 0.06)
    while size > 12:
        font = load_font(size)
        lines = wrap(draw, text, font, width * 0.9)
        if len(lines) <= max_lines:
            return font, lines
        size -= 2
    font = load_font(12)
    return font, wrap(draw, text, font, width * 0.9)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--caption", required=True)
    ap.add_argument("--label", action="append", default=[], help='"x,y,Text" with x,y as 0..1 fractions')
    args = ap.parse_args()

    photo = Image.open(args.input).convert("RGB")
    w, h = photo.size
    scratch = ImageDraw.Draw(photo)

    # Labels on the photo: white text with a thick black outline, classic meme style.
    for spec in args.label:
        try:
            x, y, text = spec.split(",", 2)
            x, y = float(x), float(y)
        except ValueError:
            sys.exit(f'Bad --label "{spec}". Use "x,y,Text", e.g. "0.5,0.1,GA4"')
        size = int(min(w, h) * 0.055)
        font = load_font(size)
        stroke = max(2, size // 12)
        tw = text_width(scratch, text, font, stroke)
        box = scratch.textbbox((0, 0), text, font=font, stroke_width=stroke)
        th = box[3] - box[1]
        px = min(max(int(x * w - tw / 2), 4), w - tw - 4)
        py = min(max(int(y * h - th / 2), 4), h - th - 4)
        scratch.text((px - box[0], py - box[1]), text, font=font, fill="white",
                     stroke_width=stroke, stroke_fill="black")

    # Footer: extend the canvas with a white bar and centered black caption.
    font, lines = fit_caption(scratch, args.caption, w)
    line_h = font.getbbox("Ag")[3] - font.getbbox("Ag")[1]
    gap = int(line_h * 0.35)
    text_h = len(lines) * line_h + (len(lines) - 1) * gap
    footer_h = max(int(h * 0.18), text_h + int(line_h * 1.4))

    out = Image.new("RGB", (w, h + footer_h), "white")
    out.paste(photo, (0, 0))
    draw = ImageDraw.Draw(out)
    y = h + (footer_h - text_h) // 2
    for line in lines:
        lw = text_width(draw, line, font)
        top = font.getbbox("Ag")[1]
        draw.text(((w - lw) // 2, y - top), line, font=font, fill="black")
        y += line_h + gap

    out.save(args.output)
    print(f"Saved {args.output} ({out.size[0]}x{out.size[1]})")


if __name__ == "__main__":
    main()
