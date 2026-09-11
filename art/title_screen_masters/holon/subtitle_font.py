#!/usr/bin/env python3
"""A native 14px pixel face for the one-line HOLON LEGENDS subtitle.

The letters are drawn at final size rather than resampled from the logo art, so
the stems stay an even three pixels and the corners keep the soft cut that the
official GBA subtitles use. Faces get a vertical silver ramp, a hard dark
outline, and a one-pixel drop shadow so the wordmark survives the busy sunset.
"""
import numpy as np

CAP_H = 14
# '#' is letter face, '.' is empty. Every stem is three pixels wide and every
# outer corner loses its extreme pixel, matching the rounded official face.
GLYPHS = {
    "H": [
        ".##.....##.",
        "###.....###",
        "###.....###",
        "###.....###",
        "###.....###",
        "###.....###",
        "###########",
        "###########",
        "###########",
        "###.....###",
        "###.....###",
        "###.....###",
        "###.....###",
        ".##.....##.",
    ],
    "O": [
        "....####....",
        "..########..",
        ".##########.",
        "###......###",
        "###......###",
        "###......###",
        "###......###",
        "###......###",
        "###......###",
        "###......###",
        "###......###",
        ".##########.",
        "..########..",
        "....####....",
    ],
    "L": [
        ".##.......",
        "###.......",
        "###.......",
        "###.......",
        "###.......",
        "###.......",
        "###.......",
        "###.......",
        "###.......",
        "###.......",
        "###.......",
        "##########",
        "##########",
        ".########.",
    ],
    "N": [
        "######...##.",
        "######...###",
        "######...###",
        "###.###..###",
        "###.###..###",
        "###..###.###",
        "###..###.###",
        "###...######",
        "###...######",
        "###...######",
        "###....#####",
        "###....#####",
        "###.....####",
        ".##.....####",
    ],
    "E": [
        ".########.",
        "##########",
        "##########",
        "###.......",
        "###.......",
        "###.......",
        "########..",
        "########..",
        "########..",
        "###.......",
        "###.......",
        "##########",
        "##########",
        ".########.",
    ],
    "G": [
        "....####....",
        "..########..",
        ".##########.",
        "###......###",
        "###.........",
        "###.........",
        "###...######",
        "###...######",
        "###...######",
        "###......###",
        "###......###",
        ".##########.",
        "..########..",
        "....####....",
    ],
    "D": [
        ".#######...",
        "#########..",
        "##########.",
        "###.....###",
        "###.....###",
        "###.....###",
        "###.....###",
        "###.....###",
        "###.....###",
        "###.....###",
        "###.....###",
        "##########.",
        "#########..",
        ".#######...",
    ],
    "S": [
        "..#######..",
        ".#########.",
        "###.....###",
        "###........",
        "###........",
        "####.......",
        ".########..",
        "..########.",
        ".......####",
        "........###",
        "........###",
        "###.....###",
        ".#########.",
        "..#######..",
    ],
}
SPACE_W = 7
LETTER_GAP = 3

# Face ramp, brightest at the cap line, then a per-row lookup into it. A 4bpp
# bank holds sixteen entries, so the fourteen rows share five silver shades.
FACE_RAMP = [
    (255, 255, 255),
    (240, 244, 252),
    (219, 226, 242),
    (192, 202, 226),
    (161, 174, 206),
]
ROW_SHADE = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4]
OUTLINE = (20, 22, 36)
SHADOW = (58, 62, 86)


def measure(text):
    width = 0
    for i, ch in enumerate(text):
        if i:
            width += LETTER_GAP
        width += SPACE_W if ch == " " else len(GLYPHS[ch][0])
    return width


def face_mask(text):
    """Rasterise the letter faces alone, one row per ramp entry."""
    mask = np.zeros((CAP_H, measure(text)), dtype=bool)
    x = 0
    for i, ch in enumerate(text):
        if i:
            x += LETTER_GAP
        if ch == " ":
            x += SPACE_W
            continue
        rows = GLYPHS[ch]
        assert len(rows) == CAP_H, ch
        assert len({len(r) for r in rows}) == 1, ch
        for y, row in enumerate(rows):
            for dx, pixel in enumerate(row):
                if pixel == "#":
                    mask[y, x + dx] = True
        x += len(rows[0])
    return mask


def grow(mask, dy, dx):
    out = np.zeros_like(mask)
    ys, xs = np.where(mask)
    out[np.clip(ys + dy, 0, mask.shape[0] - 1),
        np.clip(xs + dx, 0, mask.shape[1] - 1)] = True
    return out


def render(text):
    """Return (indexed array, palette) for the finished wordmark.

    Layer order is shadow, then outline, then face, so the drop shadow only
    shows on the lower right where the outline does not already cover it.
    """
    face = face_mask(text)
    # One pixel of margin for the outline and two more for the offset shadow.
    canvas = np.zeros((CAP_H + 3, face.shape[1] + 3), dtype=bool)
    canvas[1:1 + CAP_H, 1:1 + face.shape[1]] = face
    face = canvas
    outline = np.zeros_like(face)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            outline |= grow(face, dy, dx)
    # Flood the true exterior so the shadow never creeps into a counter, which
    # at this size would close up the middles of O, G, D and E.
    exterior = np.zeros_like(outline)
    exterior[0, 0] = True
    while True:
        grown = exterior.copy()
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            grown |= grow(exterior, dy, dx)
        grown &= ~outline
        grown[0, 0] = True
        if np.array_equal(grown, exterior):
            break
        exterior = grown
    shadow = grow(outline, 1, 1) & exterior

    out = np.zeros(face.shape, dtype=np.uint8)
    palette = [(255, 74, 238), OUTLINE, SHADOW]
    ramp_base = len(palette)
    palette += FACE_RAMP
    out[shadow] = 2
    out[outline] = 1
    ys, xs = np.where(face)
    out[ys, xs] = ramp_base + np.take(ROW_SHADE, ys - 1)
    assert len(palette) <= 16, len(palette)
    palette += [(0, 0, 0)] * (16 - len(palette))
    return out, palette
