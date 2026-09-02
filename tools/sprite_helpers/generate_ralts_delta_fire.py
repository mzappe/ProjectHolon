#!/usr/bin/env python3
"""Generate the standalone Ralts Delta Fire graphics from canonical Ralts assets."""

from pathlib import Path
from shutil import copyfile

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "graphics/pokemon/ralts"
TARGET = ROOT / "graphics/pokemon/ralts_delta_fire"


BATTLE_NORMAL = [
    (160, 160, 80),   # 0: transparent
    (248, 240, 224),  # 1: warm body highlight
    (224, 208, 192),  # 2: warm body light
    (192, 168, 152),  # 3: warm body shadow
    (144, 104, 96),   # 4: deep body shadow
    (112, 40, 32),    # 5: horn outline
    (32, 64, 144),    # 6: hand flame outline
    (248, 232, 104),  # 7: horn highlight
    (248, 144, 40),   # 8: horn midtone
    (48, 168, 248),   # 9: hand flame blue
    (184, 240, 248),  # 10: hand flame core
    (248, 208, 96),   # 11: helmet highlight
    (248, 144, 48),   # 12: helmet light
    (216, 72, 40),    # 13: helmet midtone
    (128, 32, 32),    # 14: helmet shadow
    (16, 16, 16),     # 15: outline
]

BATTLE_SHINY = [
    (160, 160, 80),
    (240, 240, 248),
    (208, 216, 232),
    (168, 184, 208),
    (112, 128, 160),
    (32, 64, 112),
    (96, 32, 144),
    (184, 240, 248),
    (48, 168, 248),
    (216, 96, 248),
    (248, 200, 248),
    (184, 240, 248),
    (80, 200, 248),
    (48, 104, 216),
    (32, 48, 128),
    (16, 16, 24),
]

OVERWORLD_NORMAL = [
    (0, 176, 232),
    (112, 40, 32),
    (248, 232, 104),
    (0, 0, 0),
    (112, 24, 24),
    (232, 88, 40),
    (248, 208, 96),
    (248, 144, 48),
    (200, 56, 32),
    (80, 64, 64),
    (160, 144, 136),
    (200, 184, 168),
    (240, 232, 216),
    (128, 104, 96),
    (32, 64, 144),
    (72, 184, 248),
]

OVERWORLD_SHINY = [
    (152, 208, 160),
    (32, 64, 112),
    (184, 240, 248),
    (0, 0, 0),
    (24, 48, 112),
    (48, 104, 216),
    (184, 240, 248),
    (80, 200, 248),
    (48, 104, 216),
    (64, 72, 96),
    (144, 160, 192),
    (184, 200, 224),
    (232, 240, 248),
    (112, 128, 160),
    (96, 32, 144),
    (216, 96, 248),
]

# The wisp overlays the visible viewer-right hand in each 64x64 front frame.
HAND_FLAME = {
    (37, 36): 9,
    (36, 37): 9,
    (37, 37): 10,
    (36, 38): 6,
    (37, 38): 10,
    (38, 38): 6,
    (35, 39): 6,
    (36, 39): 9,
    (37, 39): 10,
    (38, 39): 6,
    (35, 40): 6,
    (36, 40): 10,
    (37, 40): 9,
    (36, 41): 6,
    (37, 41): 6,
}

# Place the wisp one pixel lower, behind the canonical viewer-left hand.
BACK_HAND_FLAME = {
    (27, 42): 9,
    (26, 43): 9,
    (27, 43): 10,
    (26, 44): 6,
    (27, 44): 10,
    (28, 44): 6,
    (25, 45): 6,
    (26, 45): 9,
    (27, 45): 10,
    (28, 45): 6,
    (25, 46): 6,
    (26, 46): 10,
    (27, 46): 9,
    (26, 47): 6,
    (27, 47): 6,
}

def read_jasc_palette(path: Path) -> list[tuple[int, int, int]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"]:
        raise ValueError(f"Unexpected palette header: {path}")
    colors = [tuple(map(int, line.split())) for line in lines[3:19]]
    if len(colors) != 16 or any(len(color) != 3 for color in colors):
        raise ValueError(f"Expected exactly 16 RGB colors: {path}")
    return colors


def write_jasc_palette(path: Path, colors: list[tuple[int, int, int]]) -> None:
    if len(colors) != 16:
        raise ValueError(f"Expected 16 colors for {path}")
    body = "\n".join(f"{red} {green} {blue}" for red, green, blue in colors)
    path.write_text(f"JASC-PAL\n0100\n16\n{body}\n", encoding="ascii")


def apply_palette(image: Image.Image, colors: list[tuple[int, int, int]]) -> None:
    flat = [channel for color in colors for channel in color]
    image.putpalette(flat + [0] * (768 - len(flat)))
    image.info["transparency"] = 0


def save_indexed(image: Image.Image, path: Path) -> None:
    if image.mode != "P":
        raise ValueError(f"Refusing to save non-indexed image: {path}")
    image.save(path, bits=4, optimize=False)


def generate_front() -> None:
    image = Image.open(SOURCE / "anim_front_gba.png").copy()
    apply_palette(image, BATTLE_NORMAL)
    for frame_y in (0, 64):
        for (x, y), index in HAND_FLAME.items():
            image.putpixel((x, y + frame_y), index)
    save_indexed(image, TARGET / "anim_front.png")


def generate_back() -> None:
    image = Image.open(SOURCE / "back_gba.png").copy()
    apply_palette(image, BATTLE_NORMAL)
    for (x, y), index in BACK_HAND_FLAME.items():
        # Preserve every original hand pixel so the hand remains in front.
        if image.getpixel((x, y)) == 0:
            image.putpixel((x, y), index)
    save_indexed(image, TARGET / "back.png")


def generate_icon() -> None:
    image = Image.open(SOURCE / "icon_gba.png").copy()
    # Global icon palette 3 supplies greys, red/orange, yellow, and blue.
    remap = {4: 8, 5: 13, 13: 10}
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            pixels[x, y] = remap.get(pixels[x, y], pixels[x, y])
    apply_palette(image, read_jasc_palette(ROOT / "graphics/pokemon/icon_palettes/pal3.pal"))
    save_indexed(image, TARGET / "icon.png")


def generate_overworld() -> None:
    image = Image.open(SOURCE / "overworld.png").copy()
    apply_palette(image, OVERWORLD_NORMAL)
    save_indexed(image, TARGET / "overworld.png")


def validate() -> None:
    expected = {
        "anim_front.png": (64, 128),
        "back.png": (64, 64),
        "icon.png": (32, 64),
        "overworld.png": (192, 32),
        "footprint.png": (16, 16),
    }
    for name, size in expected.items():
        image = Image.open(TARGET / name)
        if image.mode != "P" or image.size != size:
            raise ValueError(f"{name}: expected indexed {size}, got {image.mode} {image.size}")
        used = {index for _, index in image.getcolors(maxcolors=256)}
        if not used.issubset(set(range(16))):
            raise ValueError(f"{name}: uses palette index above 15")
        if name != "footprint.png" and image.info.get("transparency") != 0:
            raise ValueError(f"{name}: palette index 0 is not transparent")


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    generate_front()
    generate_back()
    generate_icon()
    generate_overworld()
    copyfile(SOURCE / "footprint.png", TARGET / "footprint.png")
    write_jasc_palette(TARGET / "normal.pal", BATTLE_NORMAL)
    write_jasc_palette(TARGET / "shiny.pal", BATTLE_SHINY)
    write_jasc_palette(TARGET / "overworld_normal.pal", OVERWORLD_NORMAL)
    write_jasc_palette(TARGET / "overworld_shiny.pal", OVERWORLD_SHINY)
    validate()


if __name__ == "__main__":
    main()
