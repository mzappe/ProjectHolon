#!/usr/bin/env python3
"""Build the front-only Dark/Fire Jirachi delta proposal from canonical GBA art.

Design contract: preserve both canonical poses, silhouettes, face, and closed
belly eye. Recolor the star as obsidian, tags/tails as embers, and the body as
warm ash. Add one small, frame-attached incandescent fault in the star.
Story basis: GDDs/story/world-lore-story-timeline.md, IV.12, VI, and Act 4.
The material treatment is an art proposal, not additional story canon.
"""

from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "graphics/pokemon/jirachi/anim_front_gba.png"
TARGET = ROOT / "graphics/pokemon/jirachi_delta_dark_fire"
REVIEW = ROOT / "art/jirachi_delta_dark_fire"

NORMAL = [
    (112, 192, 160),  # 0: transparent
    (184, 168, 160),  # 1: ash body midtone
    (120, 112, 120),  # 2: ash body shadow
    (80, 24, 40),     # 3: cooled ember outline
    (232, 216, 192),  # 4: warm ash highlight
    (240, 88, 40),    # 5: ember orange; original blue eyes/tags
    (248, 192, 80),   # 6: golden wish-tag core
    (64, 56, 72),     # 7: body deepest shade
    (160, 40, 40),    # 8: tail ember shadow (unused in source)
    (248, 152, 56),   # 9: tail heat highlight (unused in source)
    (32, 24, 40),     # 10: obsidian deepest shade
    (56, 48, 64),     # 11: obsidian shadow
    (80, 72, 96),     # 12: obsidian midtone
    (120, 112, 144),  # 13: obsidian glint
    (248, 240, 224),  # 14: eye catchlight
    (16, 16, 24),     # 15: outline / pupils / sealed eye
]

SHINY = [
    (112, 192, 160), (176, 192, 208), (112, 136, 168), (24, 40, 88),
    (224, 232, 240), (64, 160, 248), (160, 240, 248), (56, 72, 112),
    (48, 88, 184), (96, 208, 248), (32, 24, 48), (64, 48, 80),
    (96, 72, 120), (144, 120, 168), (240, 248, 248), (16, 16, 32),
]

# Anatomical regions in local frame coordinates. Only canonical gold indices
# may change here: body, outline, and transparent pixels remain untouched.
HEAT_REGIONS = (
    ((0, 40, 64, 51), (29, 35, 34, 40)),
    ((0, 39, 64, 49), (30, 34, 35, 39)),
)
HEAT_REMAP = {10: 3, 11: 8, 12: 5, 13: 9}

# A narrow meteor-like seam stays within the crown, behind the wish tags.
# The crown translates (+2, -1) in the second canonical animation frame.
CROWN_FAULT = {
    (30, 16): 9,
    (30, 17): 5,
    (31, 18): 5,
    (31, 19): 9,
    (32, 20): 5,
    (33, 20): 5,
    (34, 19): 8,
    (32, 21): 8,
}


def palette(image, colors):
    image.putpalette([c for rgb in colors for c in rgb])
    image.info["transparency"] = 0


def write_palette(path, colors):
    path.write_text("JASC-PAL\n0100\n16\n" + "".join(
        f"{r} {g} {b}\n" for r, g, b in colors))


def transformed(source):
    result = source.copy()
    changes = {}
    for frame, regions in enumerate(HEAT_REGIONS):
        for x0, y0, x1, y1 in regions:
            for y in range(y0, y1):
                for x in range(x0, x1):
                    point = x, y + 64 * frame
                    index = source.getpixel(point)
                    if index in HEAT_REMAP:
                        changes[point] = HEAT_REMAP[index]
        for (x, y), index in CROWN_FAULT.items():
            point = x + 2 * frame, y - frame + 64 * frame
            if source.getpixel(point) not in HEAT_REMAP:
                raise ValueError(f"Crown fault left canonical gold: {point}")
            changes[point] = index
    for point, index in changes.items():
        result.putpixel(point, index)
    palette(result, NORMAL)
    return result, changes


def validate(source, expected_changes):
    output = Image.open(TARGET / "anim_front_gba.png")
    assert output.mode == "P" and output.size == (64, 128)
    assert output.info.get("transparency") == 0
    assert {index for _, index in output.getcolors(256)} <= set(range(16))
    assert list(output.getpalette()) == [c for rgb in NORMAL for c in rgb]
    # PNG IHDR bit-depth field: the stored file must actually be 4bpp.
    assert (TARGET / "anim_front_gba.png").read_bytes()[24] == 4
    actual_changes = {}
    for y in range(128):
        for x in range(64):
            before, after = source.getpixel((x, y)), output.getpixel((x, y))
            assert (before == 0) == (after == 0), "Silhouette changed"
            if before != after:
                actual_changes[x, y] = after
    assert actual_changes == expected_changes
    for name, colors in (("normal_gba.pal", NORMAL), ("shiny_gba.pal", SHINY)):
        rows = (TARGET / name).read_text().splitlines()
        assert rows[:3] == ["JASC-PAL", "0100", "16"] and len(rows) == 19
        assert [tuple(map(int, row.split())) for row in rows[3:]] == colors
        assert all(0 <= c <= 248 and c % 8 == 0 for rgb in colors for c in rgb)
    return len(actual_changes)


def build_review(source, normal):
    REVIEW.mkdir(parents=True, exist_ok=True)
    shiny = normal.copy()
    palette(shiny, SHINY)
    sheet = Image.new("RGB", (1040, 660), (24, 27, 36))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 18), "JIRACHI DELTA  /  DARK + FIRE", fill=(248, 216, 160))
    draw.text((24, 40), "Comet arrival - Crystal Isles volcano - front sprite proposal", fill=(192, 196, 208))
    for column, (label, sprite) in enumerate((("CANONICAL GBA", source), ("DELTA / NORMAL", normal), ("DELTA / SHINY", shiny))):
        left = 24 + column * 344
        draw.text((left, 74), label, fill=(232, 232, 240))
        for frame in range(2):
            tile = sprite.crop((0, frame * 64, 64, (frame + 1) * 64)).convert("RGBA")
            zoom = tile.resize((256, 256), Image.Resampling.NEAREST)
            top = 96 + frame * 280
            sheet.paste(zoom, (left, top), zoom)
            sheet.paste(tile, (left + 256, top + 96), tile)
    sheet.save(REVIEW / "overview.png")
    html = '''<!doctype html>
<meta charset="utf-8"><title>Delta Jirachi - Dark / Fire</title>
<style>body{background:#181b24;color:#eee;font:16px system-ui;margin:32px auto;max-width:1080px}img{max-width:100%;image-rendering:pixelated}a{color:#ffc050}.sprite{display:inline-block;width:256px;height:256px;background-size:256px 512px;image-rendering:pixelated;animation:frames 1s steps(1) infinite}@keyframes frames{0%,80%{background-position:0 0}35%{background-position:0 -256px}}</style>
<h1>Jirachi δ · Dark / Fire</h1>
<p>An obsidian star, warm ash body, ember wish tags and comet tails. A small incandescent seam echoes its approach from space and the Crystal Isles volcano.</p>
<div class="sprite" style="background-image:url('../../graphics/pokemon/jirachi_delta_dark_fire/anim_front_gba.png')" role="img" aria-label="Animated Delta Jirachi front sprite"></div>
<p>Preview timing only; preserves both canonical GBA poses. Front-only art proposal.</p>
<img src="overview.png" alt="Canonical Jirachi, normal Delta Jirachi, and shiny Delta Jirachi; both frames at four times and actual size">
<p><a href="../../graphics/pokemon/jirachi_delta_dark_fire/anim_front_gba.png">Indexed sprite sheet</a> · <a href="README.md">Design notes and validation</a></p>
'''
    (REVIEW / "review.html").write_text(html)


def main():
    original_digest = sha256(SOURCE.read_bytes()).hexdigest()
    source = Image.open(SOURCE)
    assert source.mode == "P" and source.size == (64, 128)
    assert not ({8, 9} & {index for _, index in source.getcolors(256)}), "Reserved heat indices now used"
    TARGET.mkdir(parents=True, exist_ok=True)
    result, changes = transformed(source)
    result.save(TARGET / "anim_front_gba.png", bits=4, optimize=False, transparency=0)
    write_palette(TARGET / "normal_gba.pal", NORMAL)
    write_palette(TARGET / "shiny_gba.pal", SHINY)
    count = validate(source, changes)
    build_review(source, result)
    assert sha256(SOURCE.read_bytes()).hexdigest() == original_digest
    print(f"Validated two 64x64 frames, 4bpp, 16-color palettes, transparency, "
          f"canonical silhouette, and {count} intentional index changes.")


if __name__ == "__main__":
    main()
