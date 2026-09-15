#!/usr/bin/env python3
"""Title-screen BG0 master: gradient backdrop + Deoxys silhouette + glow.

Style is copied from the STOCK Rayquaza title screen, which is deliberately
minimal: a dithered gradient, the legendary as ONE perfectly flat block of
colour (no interior shading, no outline, no rim light), and a couple of small
bright accent (Rayquaza's fangs).  Deoxys' is its chest CORE, and that is the
only thing on the body that lights up.

Deoxys therefore uses exactly three tones:
  * the body silhouette   (index 4, flat)
  * the core centre       (index 15)
  * the core's bloom ring (index 9, static)
Only the core centre animates: the game re-writes index 15 every 4 frames in
UpdateLegendaryMarkingColor().

Shape source: graphics/pokemon/deoxys/anim_front.png frame 0 (Normal Forme,
whip-tentacle pose), except for the right hand: frame 0's is clenched, so it is
cut off and an open, spread-fingered hand is drawn onto the wrist instead.  The
core position is still derived from the sprite.
"""
import math
import os
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "graphics/pokemon/deoxys/anim_front.png")
OUT = os.path.join(ROOT, "art/title_screen_masters/deoxys_bg.png")
SWATCH = os.path.join(ROOT, "art/title_screen_masters/palette16.png")

PAL = [
    (0x06, 0x06, 0x0F),  # 0  transparent / black
    (0x1A, 0x1F, 0x42),  # 1  backdrop deep (bottom)
    (0x27, 0x30, 0x5F),  # 2  backdrop mid
    (0x3A, 0x48, 0x90),  # 3  backdrop top
    (0x0F, 0x0A, 0x24),  # 4  THE silhouette -- one flat tone, like stock Rayquaza
    (0x2C, 0x20, 0x48),  # 5  (spare)
    (0x42, 0x33, 0x66),  # 6  (spare)
    (0x52, 0x42, 0x7E),  # 7  (spare)
    (0x86, 0x70, 0xB2),  # 8  helix strand, near side (BG1)
    (0x6A, 0x46, 0xC0),  # 9  core bloom ring (static)
    (0x2A, 0x22, 0x42),  # 10 helix strand, far side (BG1)
    (0x2E, 0x6E, 0x9E),  # 11 helix rung (BG1)
    (0x8F, 0xE3, 0xF0),  # 12 helix highlight (BG1)
    (0x1B, 0x8C, 0xB4),  # 13 (spare)
    (0x46, 0xE0, 0xFF),  # 14 (spare)
    # The game overwrites this entry every 4 frames (UpdateLegendaryMarkingColor),
    # pulsing it from a mid blue to near-white cyan; this is the midpoint, so the
    # master previews roughly the way the screen actually looks.
    (0x90, 0xC0, 0xF8),  # 15 animated glow: core centre
]

W = H = 256
VIS_W, VIS_H = 240, 160
DEOXYS_H = 190
CENTER_X = 120
TOP_Y = 44
FRAME = 0                       # whip-tentacle pose: the arms read as DNA-helix strands

# Open right hand.  Frame 0's is clenched into a lump, so it gets cut off at the
# wrist and replaced.  The hand is DRAWN rather than lifted from frame 1: frame
# 1's open hand is a solid mass in silhouette (its fingers are picked out by the
# sprite's black outline pixels, not by gaps), so grafting it just yields a
# different lump.  A palm plus splayed prongs is the only thing that still reads
# as an open hand at this size.  All coordinates are MASTER canvas pixels.
HAND_CUT = (52, 17)             # frame 0 pixels at x >= 52 AND y >= 17 are the old hand
HAND_WRIST = (178, 104)         # where the drawn hand meets the forearm
HAND_PALM = (190, 99)           # palm centre
HAND_PALM_R = (11, 10)          # palm radii
# (angle in degrees, length, radius at base, radius at tip); 0 deg points right
HAND_FINGERS = [
    (-92, 25, 5.5, 3.0),
    (-55, 29, 5.5, 3.0),
    (-16, 30, 5.5, 3.0),
    (22, 27, 5.5, 3.0),
    (74, 18, 6.0, 3.8),         # thumb
]

# Silhouette smoothing.  Thresholding a 3x upscale of a 64px mask leaves a
# staircase on every diagonal; blurring at a supersampled size and thresholding
# there rounds the contour off without eating the thin tendrils.  Repeating that
# blur+threshold is curvature flow on the outline: each pass shaves off whatever
# bumps remain while leaving straight runs and the overall shape alone, which is
# what gets the tentacle arms reading as smooth curves instead of pixel stairs.
# The hand is drawn straight into the supersampled buffer and never smoothed:
# curvature flow erases anything thinner than its radius, so running it over the
# fingers closes them back into a lump.
SS = 3                          # supersample factor
SMOOTH_BLUR = 6                 # gaussian radius, at supersampled scale
SMOOTH_PASSES = 4               # blur+threshold iterations

CORE_ROW_MIN = 16               # the chest gem is below this row; the face is above
SRC_CORE = {6, 9, 13}           # violet chest gem

src = Image.open(SRC).convert("P")
frame = src.crop((0, FRAME * 64, 64, FRAME * 64 + 64))
sp = frame.load()
body = Image.new("L", (64, 64), 0)
bl = body.load()
for y in range(64):
    for x in range(64):
        if sp[x, y] != 0 and not (x >= HAND_CUT[0] and y >= HAND_CUT[1]):
            bl[x, y] = 255

# The bounding box is taken from the WHOLE of frame 0, hand included, so cutting
# the hand off does not change the figure's scale or where it sits on screen.
xs = [x for y in range(64) for x in range(64) if sp[x, y] != 0]
ys = [y for y in range(64) for x in range(64) if sp[x, y] != 0]
bx0, bx1, by0, by1 = min(xs), max(xs) + 1, min(ys), max(ys) + 1
bw, bh = bx1 - bx0, by1 - by0
scale = DEOXYS_H / bh
dw, dh = round(bw * scale), DEOXYS_H
x0 = CENTER_X - dw // 2


def to_master(sx, sy):
    """sprite pixel centre -> master canvas coords"""
    return (round(x0 + (sx - bx0 + 0.5) * scale),
            round(TOP_Y + (sy - by0 + 0.5) * scale))


core_pts = [(x, y) for y in range(CORE_ROW_MIN, 64) for x in range(64) if sp[x, y] in SRC_CORE]
CORE_X, CORE_Y = to_master(sum(p[0] for p in core_pts) / len(core_pts),
                           sum(p[1] for p in core_pts) / len(core_pts))
CORE_R = max(5, round(2.4 * scale))

# smooth silhouette: supersample -> blur -> threshold -> downsample -> threshold
sil = body.crop((bx0, by0, bx1, by1)).resize((dw * SS, dh * SS), Image.LANCZOS)
for _ in range(SMOOTH_PASSES):
    sil = sil.filter(ImageFilter.GaussianBlur(SMOOTH_BLUR)).point(lambda v: 255 if v >= 128 else 0)


def draw_open_hand():
    """Palm + splayed fingers, drawn in the supersampled figure buffer."""
    m = Image.new("L", (dw * SS, dh * SS), 0)
    d = ImageDraw.Draw(m)

    def local(mx, my):
        return ((mx - x0) * SS, (my - TOP_Y) * SS)

    def capsule(x_a, y_a, x_b, y_b, r_a, r_b):
        steps = max(2, int(math.hypot(x_b - x_a, y_b - y_a) / SS))
        for i in range(steps + 1):
            t = i / steps
            cx, cy = x_a + (x_b - x_a) * t, y_a + (y_b - y_a) * t
            r = (r_a + (r_b - r_a) * t) * SS
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)

    wx, wy = local(*HAND_WRIST)
    px_, py_ = local(*HAND_PALM)
    capsule(wx, wy, px_, py_, 7, 10)                       # wrist -> palm
    d.ellipse((px_ - HAND_PALM_R[0] * SS, py_ - HAND_PALM_R[1] * SS,
               px_ + HAND_PALM_R[0] * SS, py_ + HAND_PALM_R[1] * SS), fill=255)
    for ang, length, r0, r1 in HAND_FINGERS:
        a = math.radians(ang)
        capsule(px_, py_,
                px_ + math.cos(a) * length * SS,
                py_ + math.sin(a) * length * SS, r0, r1)
    return m


sil = ImageChops.lighter(sil, draw_open_hand())
sil = sil.resize((dw, dh), Image.LANCZOS).point(lambda v: 255 if v >= 128 else 0)
sil = sil.filter(ImageFilter.MedianFilter(3))
sd = sil.load()

canvas = Image.new("P", (W, H), 0)
px = canvas.load()

BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
STOPS = [(0.00, 3), (0.50, 2), (1.00, 1)]
for y in range(VIS_H):
    t = y / (VIS_H - 1)
    for i in range(len(STOPS) - 1):
        p0, c0 = STOPS[i]
        p1, c1 = STOPS[i + 1]
        if t <= p1 or i == len(STOPS) - 2:
            f = max(0.0, min(1.0, (t - p0) / (p1 - p0) if p1 > p0 else 0.0))
            break
    for x in range(VIS_W):
        px[x, y] = c1 if f > (BAYER4[y & 3][x & 3] + 0.5) / 16.0 else c0


def put(cx, cy, val):
    # rows >= VIS_H are never shown; leaving them blank keeps the tile count down
    if 0 <= cx < VIS_W and 0 <= cy < VIS_H:
        px[cx, cy] = val


draw = ImageDraw.Draw(canvas)


def blob(cx, cy, rx, ry, val):
    """Filled ellipse.  Hand-rasterising this from a distance test leaves a 1px
    spur at each pole -- the shape reads as a plus sign, not a dot."""
    draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=val)


for y in range(dh):
    cy = TOP_Y + y
    if cy >= VIS_H:
        break
    for x in range(dw):
        if sd[x, y]:
            put(x0 + x, cy, 4)          # the flat silhouette, and nothing else

blob(CORE_X, CORE_Y, CORE_R, CORE_R, 9)                  # chest core: bloom ring
blob(CORE_X, CORE_Y, CORE_R - 3, CORE_R - 3, 15)         # ... and bright centre

flat = []
for c in PAL:
    flat += list(c)
flat += [0, 0, 0] * (256 - len(PAL))
canvas.putpalette(flat)
canvas.save(OUT)

sw = Image.new("P", (16 * 8, 8), 0)
sp2 = sw.load()
for i in range(16):
    for yy in range(8):
        for xx in range(8):
            sp2[i * 8 + xx, yy] = i
sw.putpalette(flat)
sw.save(SWATCH)
print(f"wrote {OUT}  (deoxys {dw}x{dh} top_y={TOP_Y}, "
      f"core ({CORE_X},{CORE_Y}) r={CORE_R})")
