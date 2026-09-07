#!/usr/bin/env python3
"""Title-screen BG1 overlay master: a faint DNA double-helix that tiles vertically
(so it scrolls upward forever) and twists under the scanline wave the title code
already applies. Shares palette E with the Deoxys BG0 layer.

Output: art/title_screen_masters/helix_overlay.png (256x256, indexed)
Convert with:  bash art/title_screen_masters/build_title_bg.sh \\
                    art/title_screen_masters/helix_overlay.png clouds
"""
import os, math
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "art/title_screen_masters/helix_overlay.png")

# same 16 colours / order as gen_deoxys_bg.py
PAL = [
    (0x06, 0x06, 0x0F), (0x10, 0x12, 0x2E), (0x1E, 0x24, 0x50), (0x34, 0x40, 0x7E),
    (0x0B, 0x07, 0x16), (0x2C, 0x20, 0x48), (0x42, 0x33, 0x66), (0x52, 0x42, 0x7E),
    (0x86, 0x70, 0xB2), (0x6A, 0x46, 0xC0), (0x2A, 0x22, 0x42), (0x2E, 0x6E, 0x9E),
    (0x8F, 0xE3, 0xF0), (0xFF, 0xF6, 0xD0), (0x46, 0xE0, 0xFF), (0xB4, 0x72, 0xFF),
]

W = H = 256
PERIOD = 128          # 256 / 128 = 2 whole turns -> seamless vertical wrap
AMP = 44
CX = 128
STRAND_HW = 1        # half-width of a strand (px), so ~3px thick
RUNG_EVERY = 16      # rows between rungs

STRAND_BACK = 7
STRAND_FRONT = 8
STRAND_HI = 12
RUNG = 11

im = Image.new("P", (W, H), 0)
flat = []
for c in PAL:
    flat += list(c)
flat += [0, 0, 0] * (256 - len(PAL))
im.putpalette(flat)
px = im.load()

def strand_x(y, phase):
    return CX + AMP * math.sin(2 * math.pi * y / PERIOD + phase)

def dot(x, y, val, hw=STRAND_HW):
    for oy in range(-hw, hw + 1):
        for ox in range(-hw, hw + 1):
            xx, yy = int(round(x)) + ox, y + oy
            if 0 <= xx < W and 0 <= yy < H:
                px[xx, yy] = val

for y in range(H):
    ph = 2 * math.pi * y / PERIOD
    ax, bx = strand_x(y, 0.0), strand_x(y, math.pi)
    a_front = math.cos(ph) >= 0
    b_front = math.cos(ph + math.pi) >= 0
    # rungs first (drawn under the strands)
    if y % RUNG_EVERY == 0:
        x0, x1 = int(round(min(ax, bx))), int(round(max(ax, bx)))
        for xx in range(x0, x1 + 1, 2):
            if 0 <= xx < W:
                px[xx, y] = RUNG
    dot(ax, y, STRAND_FRONT if a_front else STRAND_BACK)
    dot(bx, y, STRAND_FRONT if b_front else STRAND_BACK)
    if a_front:
        dot(ax, y, STRAND_HI, 0)
    if b_front:
        dot(bx, y, STRAND_HI, 0)

im.save(OUT)
print(f"wrote {OUT}")
