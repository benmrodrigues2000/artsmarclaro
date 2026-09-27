#!/usr/bin/env python3
"""One-off: draws the on-brand placeholder images for shop products that
don't have real photos yet (earring models 1-5, presépio model 3).
Replace the generated files with real photos (same names) when available."""
from PIL import Image, ImageDraw
import os

W = H = 1000
SAND_TOP = (240, 228, 205)      # light sand
SAND_BOT = (226, 205, 168)      # --sand-ish
INK = (138, 106, 76)            # darker taupe for the line icon
FRAME = (152, 117, 85, 90)      # faint frame line


def bg():
    im = Image.new("RGB", (W, H), SAND_TOP)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(round(SAND_TOP[i] + (SAND_BOT[i] - SAND_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    d.rounded_rectangle([42, 42, W - 42, H - 42], radius=48, outline=FRAME, width=3)
    return im


def earring(d, cx, top, s=1.0):
    """A dangle earring: hook arc + bead + line + round disc with dots."""
    r = int(52 * s)
    # hook (top half circle)
    d.arc([cx - r, top, cx + r, top + 2 * r], start=180, end=360, fill=INK, width=int(15 * s))
    # small bead at hook end
    br = int(13 * s)
    d.ellipse([cx - br, top + 2 * r - br, cx + br, top + 2 * r + br], fill=INK)
    # drop line
    d.line([(cx, top + 2 * r + br), (cx, top + 2 * r + br + int(64 * s))], fill=INK, width=int(11 * s))
    # disc
    dr = int(58 * s)
    dy = top + 2 * r + br + int(64 * s)
    d.ellipse([cx - dr, dy - dr, cx + dr, dy + dr], outline=INK, width=int(15 * s))
    # inner dots (simple pattern)
    for ox, oy in ((0, -int(dr * 0.42)), (-int(dr * 0.42), int(dr * 0.28)), (int(dr * 0.42), int(dr * 0.28))):
        dot = int(9 * s)
        d.ellipse([cx + ox - dot, dy + oy - dot, cx + ox + dot, dy + oy + dot], fill=INK)


def star(d, cx, cy, r_out, r_in, w):
    import math
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(pts + [pts[0]], fill=INK, width=w, joint="curve")


def make(path, kind):
    im = bg()
    d = ImageDraw.Draw(im)
    if kind == "earring":
        earring(d, 360, 268, 1.0)
        earring(d, 640, 320, 1.0)
    else:  # nativity star
        star(d, 500, 470, 210, 84, 20)
        # little base line beneath the star
        d.line([(380, 780), (620, 780)], fill=INK, width=14)
    im.save(path, "JPEG", quality=88, optimize=True)
    print(path, os.path.getsize(path))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for i in range(1, 6):
        make(os.path.join(here, f"brinco-{i}.jpg"), "earring")
    make(os.path.join(here, "presepio-3.jpg"), "star")
