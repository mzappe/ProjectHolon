#!/usr/bin/env python3
"""Generate standalone Delta Grass Dratini graphics from canonical GBA assets."""

from pathlib import Path
from shutil import copyfile

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "graphics/pokemon/dratini"
TARGET = ROOT / "graphics/pokemon/dratini_delta_grass"


BATTLE_NORMAL = [
    (160, 160, 80),   # 0: transparent
    (248, 248, 200),  # 1: underside highlight
    (216, 232, 144),  # 2: underside light
    (144, 176, 88),   # 3: underside shadow
    (64, 104, 48),    # 4: underside deepest shadow
    (248, 224, 184),  # 5: tropical flower highlight
    (248, 144, 120),  # 6: tropical flower light
    (232, 72, 88),    # 7: tropical flower midtone
    (152, 40, 72),    # 8: tropical flower shadow
    (88, 72, 160),    # 9: reserved original-Dratini accent
    (248, 200, 56),   # 10: flower centers and eye
    (176, 232, 112),  # 11: body highlight
    (88, 192, 80),    # 12: body light
    (32, 128, 64),    # 13: body midtone
    (16, 72, 48),     # 14: body shadow
    (8, 32, 24),      # 15: outline
]

BATTLE_SHINY = [
    (160, 160, 80),
    (232, 248, 248),  # 1: aqua underside highlight
    (184, 232, 232),  # 2: aqua underside light
    (104, 176, 184),  # 3: aqua underside shadow
    (40, 96, 120),    # 4: aqua underside deepest shadow
    (248, 248, 248),  # 5: moon-white flower highlight
    (176, 232, 248),  # 6: icy flower light
    (88, 168, 232),   # 7: icy flower midtone
    (48, 80, 168),    # 8: icy flower shadow
    (72, 184, 160),   # 9: reserved tropical accent
    (248, 88, 184),   # 10: hot-pink flower centers and eye
    (176, 152, 240),  # 11: body highlight
    (112, 88, 200),   # 12: body light
    (72, 48, 152),    # 13: body midtone
    (32, 24, 88),     # 14: body shadow
    (16, 16, 40),     # 15: outline
]

OVERWORLD_NORMAL = [
    (152, 208, 160),  # 0: transparent
    (16, 40, 32),     # 1: secondary outline
    (216, 232, 144),  # 2: underside light
    (0, 0, 0),        # 3: outline
    (16, 72, 48),     # 4: body deepest shadow
    (224, 240, 168),  # 5: underside highlight
    (32, 128, 64),    # 6: body shadow
    (88, 192, 80),    # 7: body light
    (48, 144, 72),    # 8: body midtone
    (248, 248, 200),  # 9: highlight
    (104, 128, 72),   # 10: neutral shadow
    (248, 200, 56),   # 11: eye
    (248, 224, 184),  # 12: flower highlight
    (248, 144, 120),  # 13: flower light
    (152, 40, 72),    # 14: flower shadow
    (248, 200, 56),   # 15: reserved flower center
]

OVERWORLD_SHINY = [
    (152, 208, 160),
    (24, 24, 64),
    (184, 232, 232),
    (0, 0, 0),
    (32, 24, 88),
    (216, 240, 240),
    (72, 48, 152),
    (112, 88, 200),
    (88, 64, 176),
    (232, 248, 248),
    (88, 120, 144),
    (248, 88, 184),
    (248, 248, 248),
    (176, 232, 248),
    (48, 80, 168),
    (248, 88, 184),
]

# The canonical fins already form pointed, three-lobed silhouettes. These
# frame-local boxes isolate their light pixels so the transformed fins read as
# tropical blossoms without changing Dratini's anatomy or silhouette.
FRONT_FLOWER_BOXES = {
    0: (
        (range(8, 15), range(17, 23)),
        (range(23, 32), range(14, 31)),
    ),
    1: (
        (range(14, 21), range(10, 19)),
        (range(23, 35), range(13, 28)),
    ),
}

FRONT_FLOWER_CENTERS = {
    0: {(13, 21), (13, 22), (24, 27), (25, 27), (26, 28)},
    1: {(18, 16), (18, 17), (25, 23), (26, 23), (26, 24)},
}

BACK_FLOWER_BOXES = (
    (range(24, 34), range(11, 31)),
    (range(40, 49), range(9, 32)),
)

BACK_FLOWER_CENTERS = {
    (28, 29),
    (29, 29),
    (29, 30),
    (42, 29),
    (43, 29),
    (43, 30),
}

FLOWER_INDEX_REMAP = {1: 5, 2: 6, 3: 7, 4: 8}

ICON_BODY_REMAP = {8: 5, 9: 4}
ICON_FLOWER_REMAP = {2: 7, 3: 13}
ICON_FLOWER_BOXES = (
    (range(12, 14), range(15, 17)),
    (range(17, 21), range(15, 20)),
    (range(11, 13), range(48, 50)),
    (range(16, 20), range(48, 53)),
)
ICON_FLOWER_CENTERS = {(12, 15), (17, 18), (11, 48), (16, 51)}

# The follower keeps the flower transformation but omits center pixels because
# they do not remain legible at the native 32x32 display scale.
OVERWORLD_FLOWER_BOXES = {
    0: ((range(8, 15), range(10, 20)), (range(17, 24), range(10, 20))),
    1: ((range(8, 15), range(9, 19)), (range(17, 24), range(9, 19))),
    2: ((range(8, 15), range(9, 20)), (range(17, 24), range(9, 20))),
    3: ((range(9, 15), range(10, 20)), (range(18, 24), range(10, 20))),
    4: ((range(16, 23), range(10, 19)),),
    5: ((range(16, 22), range(10, 19)),),
}
OVERWORLD_FLOWER_REMAP = {1: 14, 2: 12, 5: 13}


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


def remap_boxes(
    image: Image.Image,
    boxes: tuple[tuple[range, range], ...],
    remap: dict[int, int],
    frame_y: int = 0,
    frame_x: int = 0,
) -> None:
    for xs, ys in boxes:
        for y in ys:
            for x in xs:
                point = (x + frame_x, y + frame_y)
                source_index = image.getpixel(point)
                if source_index in remap:
                    image.putpixel(point, remap[source_index])


def generate_front() -> None:
    image = Image.open(SOURCE / "anim_front_gba.png").copy()
    for frame, frame_y in enumerate((0, 64)):
        remap_boxes(image, FRONT_FLOWER_BOXES[frame], FLOWER_INDEX_REMAP, frame_y=frame_y)
        for x, y in FRONT_FLOWER_CENTERS[frame]:
            point = (x, y + frame_y)
            if image.getpixel(point) not in FLOWER_INDEX_REMAP.values():
                raise ValueError(f"Front flower center is outside transformed petals: {point}")
            image.putpixel(point, 10)
    apply_palette(image, BATTLE_NORMAL)
    save_indexed(image, TARGET / "anim_front.png")


def generate_back() -> None:
    image = Image.open(SOURCE / "back_gba.png").copy()
    remap_boxes(image, BACK_FLOWER_BOXES, FLOWER_INDEX_REMAP)
    for point in BACK_FLOWER_CENTERS:
        if image.getpixel(point) not in FLOWER_INDEX_REMAP.values():
            raise ValueError(f"Back flower center is outside transformed petals: {point}")
        image.putpixel(point, 10)
    apply_palette(image, BATTLE_NORMAL)
    save_indexed(image, TARGET / "back.png")


def generate_icon() -> None:
    image = Image.open(SOURCE / "icon_gba.png").copy()
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            pixels[x, y] = ICON_BODY_REMAP.get(pixels[x, y], pixels[x, y])
    remap_boxes(image, ICON_FLOWER_BOXES, ICON_FLOWER_REMAP)
    for point in ICON_FLOWER_CENTERS:
        if image.getpixel(point) not in ICON_FLOWER_REMAP.values():
            raise ValueError(f"Icon flower center is outside transformed petals: {point}")
        image.putpixel(point, 10)
    apply_palette(image, read_jasc_palette(ROOT / "graphics/pokemon/icon_palettes/pal4.pal"))
    save_indexed(image, TARGET / "icon.png")


def generate_overworld() -> None:
    image = Image.open(SOURCE / "overworld.png").copy()
    for frame in range(6):
        remap_boxes(
            image,
            OVERWORLD_FLOWER_BOXES[frame],
            OVERWORLD_FLOWER_REMAP,
            frame_x=frame * 32,
        )
    apply_palette(image, OVERWORLD_NORMAL)
    save_indexed(image, TARGET / "overworld.png")


def opaque_mask(image: Image.Image) -> set[tuple[int, int]]:
    return {
        (x, y)
        for y in range(image.height)
        for x in range(image.width)
        if image.getpixel((x, y)) != 0
    }


def changed_points(source: Image.Image, output: Image.Image) -> set[tuple[int, int]]:
    return {
        (x, y)
        for y in range(source.height)
        for x in range(source.width)
        if source.getpixel((x, y)) != output.getpixel((x, y))
    }


def expected_box_changes(
    source: Image.Image,
    boxes: tuple[tuple[range, range], ...],
    remap: dict[int, int],
    frame_y: int = 0,
    frame_x: int = 0,
) -> set[tuple[int, int]]:
    return {
        (x + frame_x, y + frame_y)
        for xs, ys in boxes
        for y in ys
        for x in xs
        if source.getpixel((x + frame_x, y + frame_y)) in remap
    }


def require_exact_changes(
    name: str,
    source: Image.Image,
    output: Image.Image,
    expected_changes: set[tuple[int, int]],
) -> None:
    actual_changes = changed_points(source, output)
    if actual_changes != expected_changes:
        unexpected = sorted(actual_changes - expected_changes)
        missing = sorted(expected_changes - actual_changes)
        raise ValueError(
            f"{name}: pixel-change contract failed; "
            f"unexpected={unexpected[:8]}, missing={missing[:8]}"
        )


def embedded_palette(image: Image.Image) -> list[tuple[int, int, int]]:
    palette = image.getpalette()
    return [tuple(palette[index * 3 : index * 3 + 3]) for index in range(16)]


def validate() -> None:
    expected = {
        "anim_front.png": (64, 128),
        "back.png": (64, 64),
        "icon.png": (32, 64),
        "overworld.png": (192, 32),
        "footprint.png": (16, 16),
    }
    sources = {
        "anim_front.png": "anim_front_gba.png",
        "back.png": "back_gba.png",
        "icon.png": "icon_gba.png",
        "overworld.png": "overworld.png",
        "footprint.png": "footprint.png",
    }

    for name, size in expected.items():
        output = Image.open(TARGET / name)
        source = Image.open(SOURCE / sources[name])
        if output.mode != "P" or output.size != size:
            raise ValueError(f"{name}: expected indexed {size}, got {output.mode} {output.size}")
        used = {index for _, index in output.getcolors(maxcolors=256)}
        if not used.issubset(set(range(16))):
            raise ValueError(f"{name}: uses palette index above 15")
        if name != "footprint.png" and output.info.get("transparency") != 0:
            raise ValueError(f"{name}: palette index 0 is not transparent")
        if opaque_mask(source) != opaque_mask(output):
            raise ValueError(f"{name}: canonical silhouette changed")

    for name in ("normal.pal", "shiny.pal", "overworld_normal.pal", "overworld_shiny.pal"):
        read_jasc_palette(TARGET / name)

    if embedded_palette(Image.open(TARGET / "anim_front.png")) != BATTLE_NORMAL:
        raise ValueError("anim_front.png does not embed the normal battle palette")
    if embedded_palette(Image.open(TARGET / "back.png")) != BATTLE_NORMAL:
        raise ValueError("back.png does not embed the normal battle palette")
    if embedded_palette(Image.open(TARGET / "overworld.png")) != OVERWORLD_NORMAL:
        raise ValueError("overworld.png does not embed the normal follower palette")
    icon_palette = read_jasc_palette(ROOT / "graphics/pokemon/icon_palettes/pal4.pal")
    if embedded_palette(Image.open(TARGET / "icon.png")) != icon_palette:
        raise ValueError("icon.png does not embed shared icon palette 4")
    if BATTLE_NORMAL == BATTLE_SHINY or OVERWORLD_NORMAL == OVERWORLD_SHINY:
        raise ValueError("Normal and shiny palettes must be distinct")

    if (TARGET / "footprint.png").read_bytes() != (SOURCE / "footprint.png").read_bytes():
        raise ValueError("Canonical footprint was not copied exactly")

    source_front = Image.open(SOURCE / "anim_front_gba.png")
    output_front = Image.open(TARGET / "anim_front.png")
    expected_front = set()
    for frame, frame_y in enumerate((0, 64)):
        expected_front.update(
            expected_box_changes(
                source_front,
                FRONT_FLOWER_BOXES[frame],
                FLOWER_INDEX_REMAP,
                frame_y=frame_y,
            )
        )
        expected_front.update((x, y + frame_y) for x, y in FRONT_FLOWER_CENTERS[frame])
    require_exact_changes("anim_front.png", source_front, output_front, expected_front)

    source_back = Image.open(SOURCE / "back_gba.png")
    output_back = Image.open(TARGET / "back.png")
    expected_back = expected_box_changes(source_back, BACK_FLOWER_BOXES, FLOWER_INDEX_REMAP)
    expected_back.update(BACK_FLOWER_CENTERS)
    require_exact_changes("back.png", source_back, output_back, expected_back)

    source_icon = Image.open(SOURCE / "icon_gba.png")
    output_icon = Image.open(TARGET / "icon.png")
    expected_icon = {
        (x, y)
        for y in range(source_icon.height)
        for x in range(source_icon.width)
        if source_icon.getpixel((x, y)) in ICON_BODY_REMAP
    }
    expected_icon.update(
        expected_box_changes(source_icon, ICON_FLOWER_BOXES, ICON_FLOWER_REMAP)
    )
    expected_icon.update(ICON_FLOWER_CENTERS)
    require_exact_changes("icon.png", source_icon, output_icon, expected_icon)

    source_overworld = Image.open(SOURCE / "overworld.png")
    output_overworld = Image.open(TARGET / "overworld.png")
    expected_overworld = set()
    for frame in range(6):
        expected_overworld.update(
            expected_box_changes(
                source_overworld,
                OVERWORLD_FLOWER_BOXES[frame],
                OVERWORLD_FLOWER_REMAP,
                frame_x=frame * 32,
            )
        )
    require_exact_changes("overworld.png", source_overworld, output_overworld, expected_overworld)


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
