#!/usr/bin/env python3
"""Rebuild the subtitle from the ORIGINAL stacked art, kept plain:
- same letterforms / palette as the stock emerald_version.png
- HOLON over LEGENDS (vertical / stacked), both words at the SAME cap height
- 128x32, index 0 = magenta transparent key

Re-runnable from the stacked source backup.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "art/title_screen_masters/emerald_version_src.png")
OUT = os.path.join(ROOT, "graphics/title_screen/emerald_version.png")

CANVAS_W, CANVAS_H = 128, 32
CAP_H = 13          # both words normalised to this height
GAP = 1             # px between the two lines

im = Image.open(SRC).convert("P")
pal = im.getpalette()
px = im.load()

def extract(y0, y1):
    xs = [x for y in range(y0, y1) for x in range(im.width) if px[x, y] != 0]
    ys = [y for y in range(y0, y1) for x in range(im.width) if px[x, y] != 0]
    return im.crop((min(xs), min(ys), max(xs) + 1, max(ys) + 1))

def norm(word):
    w = max(1, round(word.width * CAP_H / word.height))
    w = min(w, CANVAS_W - 2)
    return word.resize((w, CAP_H), Image.NEAREST)

holon = norm(extract(0, 18))
legends = norm(extract(18, 32))

out = Image.new("P", (CANVAS_W, CANVAS_H), 0)
out.putpalette(pal)
total_h = CAP_H + GAP + CAP_H
y = (CANVAS_H - total_h) // 2
out.paste(holon, ((CANVAS_W - holon.width) // 2, y))
out.paste(legends, ((CANVAS_W - legends.width) // 2, y + CAP_H + GAP))
out.save(OUT)
print(f"subtitle stacked, equal size: HOLON {holon.size} / LEGENDS {legends.size}")
