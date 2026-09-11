#!/usr/bin/env python3
"""Build the three static Holon title layers; preview with Emerald's prompt.

The landscape retains the approved composition. The title uses native pixel
lettering instead of reducing text extracted from the large illustration.
Requires Pillow and numpy; run from any working directory.
"""
import json
from pathlib import Path
import struct

import numpy as np
from PIL import Image, ImageFilter

import subtitle_font

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "graphics/title_screen"
SCREEN = (240, 160)
SUBTITLE = "HOLON LEGENDS"
# The wordmark ends at y=43; this clears it by three rows including the outline.
SUBTITLE_TOP = 46
# Source-space bounds separate the subtitle from the low corners of the logo.
BOUNDS = {
    "pokemon": (400, 25, 1140, 307),
    "legends": (566, 274, 979, 404),
    "press_start": (592, 929, 943, 970),
}

def title_layers(colors):
    """Recolor the original wordmark; simplify only the subtitle's finish."""
    source = Image.open(HERE.parent / "pokemon_logo_src.png")
    pixels = np.asarray(source).copy()
    # Keep the previously requested TM removal; do not redraw any letter pixels.
    pixels[52:60, 157:170] = 0
    rgb_palette = np.array(source.getpalette(), dtype=np.int16).reshape(-1, 3)
    ramp = np.array([c[0] for c in colors[1:]])
    lookup = np.zeros(256, dtype=np.uint8)
    for i, (r, g, b) in enumerate(rgb_palette):
        if i in (0, 1):
            continue
        # Yellow becomes silver; blue becomes charcoal. Intermediate source
        # shades keep their tonal ordering, including the original edge pixels.
        light = (0.3 * r + 0.59 * g + 0.11 * b) / 255
        if r > 110 and g > 100 and (r + g) > 2.2 * b:
            value = 164 + 91 * np.clip((light - 0.45) / 0.5, 0, 1)
        elif b > 110 and b >= r and b >= g:
            value = 40 * np.clip(light / 0.35, 0, 1)
        else:
            value = 255 * light
        lookup[i] = np.abs(ramp - value).argmin() + 1
    logo = lookup[pixels]
    ys, xs = np.where(logo)
    logo = Image.fromarray(logo[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    logo = np.asarray(logo.resize((122, 41), Image.Resampling.NEAREST))
    pokemon = np.zeros((160, 240), dtype=np.uint8)
    pokemon[3:44, 59:181] = logo

    # The subtitle is drawn at final size by subtitle_font, on one line, so no
    # letter pixel is ever resampled. Centre it under the wordmark.
    glyphs, subtitle_colors = subtitle_font.render(SUBTITLE)
    # Snap to the GBA's five bits per channel so the preview matches hardware.
    subtitle = indexed(glyphs, [tuple(gba(v) for v in c) for c in subtitle_colors])
    legends = Image.new("P", SCREEN, 0)
    legends.putpalette(subtitle.getpalette())
    width = glyphs.shape[1]
    assert width <= SCREEN[0], width
    legends.paste(subtitle, ((SCREEN[0] - width) // 2, SUBTITLE_TOP))
    return {"pokemon": indexed(pokemon, colors), "legends": legends}


def gba(v):
    return ((int(v) * 31 + 127) // 255 * 255 + 15) // 31


def palette_file(path, colors):
    path.write_text("JASC-PAL\n0100\n" + str(len(colors)) + "\n"
                    + "\n".join(" ".join(map(str, c)) for c in colors) + "\n")


def indexed(data, colors):
    im = Image.fromarray(np.asarray(data, dtype=np.uint8))
    im = im.convert("P")
    im.putpalette([v for c in colors for v in c])
    return im


def tiles_and_map(im, name, palette_bank=0, tile_offset=0, budget=0x1000):
    """Deduplicate 8x8 tiles; pad outside the visible screen with blank tile 0."""
    canvas = Image.new("P", (256, 256), 0)
    canvas.paste(im, (0, 0))
    tiles = [bytes(64)]
    lookup = {tiles[0]: 0}
    entries = []
    for y in range(0, 256, 8):
        for x in range(0, 256, 8):
            tile = canvas.crop((x, y, x + 8, y + 8)).tobytes()
            if tile not in lookup:
                lookup[tile] = len(tiles)
                tiles.append(tile)
            entries.append(lookup[tile] + tile_offset + (palette_bank << 12))
    bpp = 8 if name == "landscape" else 4
    size = len(tiles) * 8 * bpp
    assert size <= budget, (name, size, budget)
    sheet = Image.frombytes("P", (8, 8 * len(tiles)), b"".join(tiles))
    sheet.putpalette(im.getpalette())
    sheet.save(OUT / f"holon_{name}.png")
    (OUT / f"holon_{name}.bin").write_bytes(struct.pack("<1024H", *entries))
    # Round-trip the tilemap, including palette-bank and tile-offset handling.
    rebuilt = Image.new("P", (256, 256), 0)
    for i, entry in enumerate(entries):
        tile = tiles[(entry & 1023) - tile_offset]
        rebuilt.paste(Image.frombytes("P", (8, 8), tile), ((i % 32) * 8, (i // 32) * 8))
    assert rebuilt.crop((0, 0, *SCREEN)).tobytes() == im.tobytes()
    return {"tiles": len(tiles), "tile_bytes": size, "map_bytes": 2048}


def main():
    approved = Image.open(HERE / "approved.png").convert("RGB")
    fill = Image.open(HERE / "background_fill.png").convert("RGB")
    assert approved.size == fill.size == (1536, 1024)
    rgb = np.asarray(approved).astype(np.int16)
    # Silver, black and white lettering is neutral; the sky/forest is chromatic.
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    neutral = (chroma <= 32)
    masks = {}
    for name, (x0, y0, x1, y1) in BOUNDS.items():
        mask = np.zeros(neutral.shape, dtype=np.uint8)
        mask[y0:y1, x0:x1] = neutral[y0:y1, x0:x1] * 255
        if name == "pokemon":
            a, b, c, d = BOUNDS["legends"]
            mask[b:d, a:c] = 0
        masks[name] = Image.fromarray(mask)
    # Repair only the old text and its antialiased edge, retaining the approved
    # source everywhere else, including the tiny shapes of the forest and lake.
    all_text = Image.fromarray(np.maximum.reduce([np.asarray(m) for m in masks.values()]))
    repair = all_text.filter(ImageFilter.MaxFilter(13))
    background = Image.composite(fill, approved, repair).resize(SCREEN, Image.Resampling.BOX)
    background = background.filter(ImageFilter.UnsharpMask(radius=0.6, percent=45, threshold=2))
    quantized = background.quantize(colors=191, method=Image.Quantize.MEDIANCUT,
                                     dither=Image.Dither.NONE)
    landscape_colors = [tuple(gba(v) for v in quantized.getpalette()[i:i + 3])
                        for i in range(0, 191 * 3, 3)]
    # Index zero is transparent to the GBA. Visible landscape pixels use 1..191.
    landscape = indexed(np.asarray(quantized).astype(np.uint16) + 1,
                        [(0, 0, 0)] + landscape_colors)
    landscape.save(HERE / "landscape.png")

    tones = [gba(v) for v in (0, 16, 32, 48, 64, 90, 115, 140, 164, 181, 197, 214, 230, 247, 255)]
    logo_colors = [(255, 0, 255)] + [(v, v, v) for v in tones] + [(0, 0, 0)] * (15 - len(tones))
    layers = title_layers(logo_colors)
    for name, layer in layers.items():
        layer.save(HERE / f"{name}.png", transparency=0)

    palette = [(0, 0, 0)] + landscape_colors
    palette += [(0, 0, 0)] * (224 - len(palette))
    subtitle_palette = layers["legends"].getpalette()[:48]
    palette += [tuple(subtitle_palette[i:i + 3]) for i in range(0, 48, 3)]
    palette += [(0, 0, 0)] + logo_colors[1:]
    assert len(palette) == 256
    palette_file(OUT / "holon.pal", palette)
    stats = {
        "landscape": tiles_and_map(landscape, "landscape", budget=0xC000),
        "pokemon": tiles_and_map(layers["pokemon"], "pokemon", palette_bank=15),
        "legends": tiles_and_map(layers["legends"], "legends", palette_bank=14,
                                  tile_offset=128, budget=0x1000),
    }
    composite = landscape.convert("RGBA")
    for layer in layers.values():
        rgba = layer.convert("RGBA")
        rgba.putalpha(Image.fromarray((np.asarray(layer) != 0).astype(np.uint8) * 255))
        composite.alpha_composite(rgba)
    # Match Emerald's original five 32x8 prompt sprites, including their glyph
    # offsets. The game uses gTitleScreenPressStartGfx/Pal directly.
    press = Image.open(OUT / "press_start.png").crop((0, 0, 160, 8))
    rgba = press.convert("RGBA")
    rgba.putalpha(Image.fromarray((np.asarray(press) != 0).astype(np.uint8) * 255))
    composite.alpha_composite(rgba, (40, 144))
    composite.convert("RGB").save(HERE / "preview.png")
    composite.resize((960, 640), Image.Resampling.NEAREST).save(HERE / "preview-4x.png")
    stats["display"] = {"width": 240, "height": 160, "mode": 0,
                        "bg0": "8bpp landscape", "bg1": "4bpp Pokemon", "bg2": "4bpp Holon Legends",
                        "cloud_overlay": False}
    (HERE / "layout.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
