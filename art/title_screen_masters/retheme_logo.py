#!/usr/bin/env python3
"""Re-theme + shrink the Pokemon logo for the Holon title screen.

- RGB-classifies every palette entry: yellow letter shades -> cyan/white ramp,
  blue outline shades -> deep-violet ramp, neutrals -> muted violet-grey.
- Scales the wordmark to ~66% and re-centres it in the fixed 256x64 canvas so it
  reads smaller on screen (no code/tilemap change needed).

Reads the untouched stock wordmark from art/title_screen_masters/pokemon_logo_src.png,
so this is re-runnable; writes graphics/title_screen/pokemon_logo.png and
regenerates pokemon_logo.pal.
"""
import os, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "art/title_screen_masters/pokemon_logo_src.png")
LOGO = os.path.join(ROOT, "graphics/title_screen/pokemon_logo.png")
PAL = os.path.join(ROOT, "graphics/title_screen/pokemon_logo.pal")
GBAGFX = os.path.join(ROOT, "tools/gbagfx/gbagfx")

SCALE = 0.66
# The affine BG2 renders the canvas at ~0.74x and screen_x ~= 0.74*canvas_x + 54,
# so to land the wordmark centred (screen x 120) put its canvas centre near 89.
PLACE_CX = 89
PLACE_TOP = 0
# Box (canvas coords) wiping the small (TM) glyph at the wordmark's lower-right.
# It has to hug the glyph: the final N's bottom-right tail runs out to x=156 and
# down to y=58, so a wider or taller box bites a chunk out of the wordmark.
TM_BOX = (157, 52, 170, 60)

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

CYAN_DARK, CYAN_LIGHT = (0x4E, 0x9A, 0xC0), (0xEC, 0xFB, 0xFF)   # letter fill ramp
VIO_DARK, VIO_LIGHT = (0x12, 0x0A, 0x2C), (0x6A, 0x46, 0xA6)     # outline ramp

im = Image.open(SRC).convert("P")
pal = im.getpalette()
used = set(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata())

for i in range(256):
    if i in (0, 1):            # transparent key + its dupe
        continue
    r, g, b = pal[i * 3:i * 3 + 3]
    lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255.0
    is_yellow = r > 110 and g > 100 and b < 140 and (r + g) > 2.2 * b
    is_blue = b > 110 and b >= r and b >= g and not is_yellow
    if is_yellow:
        pal[i * 3:i * 3 + 3] = lerp(CYAN_DARK, CYAN_LIGHT, max(0.0, min(1.0, (lum - 0.45) / 0.5)))
    elif is_blue:
        pal[i * 3:i * 3 + 3] = lerp(VIO_DARK, VIO_LIGHT, max(0.0, min(1.0, lum / 0.35)))
    elif i == 21:              # the art's near-black shadow
        pal[i * 3:i * 3 + 3] = [0x0C, 0x08, 0x1E]
    else:                      # neutrals / browns -> muted violet-grey
        v = max(0.0, min(1.0, lum))
        pal[i * 3:i * 3 + 3] = lerp((0x2A, 0x24, 0x3E), (0xB8, 0xB0, 0xD0), v)

im.putpalette(pal)

px = im.load()
# wipe the (TM) glyph
for y in range(TM_BOX[1], min(TM_BOX[3], im.height)):
    for x in range(TM_BOX[0], min(TM_BOX[2], im.width)):
        px[x, y] = 0

xs = [x for y in range(im.height) for x in range(im.width) if px[x, y] != 0]
ys = [y for y in range(im.height) for x in range(im.width) if px[x, y] != 0]
crop = im.crop((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
nw, nh = max(1, round(crop.width * SCALE)), max(1, round(crop.height * SCALE))
crop = crop.resize((nw, nh), Image.NEAREST)

out = Image.new("P", (im.width, im.height), 0)
out.putpalette(pal)
ox = max(0, min(im.width - nw, PLACE_CX - nw // 2))
oy = PLACE_TOP
out.paste(crop, (ox, oy))
out.save(LOGO)

subprocess.run([GBAGFX, LOGO, PAL], check=True)
print(f"logo: {crop.size} in {im.size} at ({ox},{oy}); {len(used)} idx recoloured; pal regenerated")
