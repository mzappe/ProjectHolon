#!/usr/bin/env python3
"""Generate the standalone Bagon Delta Water graphics from canonical Bagon."""

from pathlib import Path
from shutil import copyfile

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "graphics/pokemon/bagon"
TARGET = ROOT / "graphics/pokemon/bagon_delta_water"


BATTLE_NORMAL = [
    (160, 160, 80),   # 0: transparent
    (24, 48, 64),     # 1: deepest dorsal teal
    (32, 80, 96),     # 2: dorsal shadow
    (48, 120, 136),   # 3: dorsal midtone
    (104, 184, 184),  # 4: dorsal highlight
    (136, 48, 48),    # 5: mouth shadow
    (232, 96, 72),    # 6: mouth highlight
    (72, 144, 152),   # 7: unused accent
    (48, 64, 80),     # 8: helmet deepest shadow
    (72, 104, 120),   # 9: helmet shadow
    (136, 176, 184),  # 10: helmet light
    (224, 240, 232),  # 11: helmet and tooth highlight
    (80, 152, 144),   # 12: underside shadow
    (160, 224, 200),  # 13: underside highlight
    (248, 184, 56),   # 14: amber eye
    (16, 24, 32),     # 15: outline
]

# The shiny is an abyssal-water counterpart: near-black navy hide, muted
# blue-violet armor, a dark purple underside, magenta accents, and a small
# bioluminescent cyan eye.
BATTLE_SHINY = [
    (160, 160, 80),   # 0: transparent
    (8, 16, 32),      # 1: deepest abyssal navy
    (16, 40, 64),     # 2: body shadow
    (24, 72, 104),    # 3: body midtone
    (64, 136, 160),   # 4: cold body highlight
    (64, 16, 48),     # 5: mouth shadow
    (184, 40, 112),   # 6: magenta mouth highlight
    (56, 88, 120),    # 7: unused accent
    (16, 16, 32),     # 8: helmet deepest shadow
    (32, 40, 72),     # 9: helmet shadow
    (72, 80, 120),    # 10: helmet light
    (152, 168, 200),  # 11: helmet and tooth highlight
    (48, 40, 88),     # 12: underside shadow
    (120, 72, 152),   # 13: underside highlight
    (72, 224, 248),   # 14: bioluminescent cyan eye
    (8, 8, 24),       # 15: outline
]

OVERWORLD_NORMAL = [
    (152, 208, 160),  # 0: transparent
    (48, 64, 80),     # 1: helmet deepest shadow
    (136, 176, 184),  # 2: helmet light
    (72, 104, 120),   # 3: helmet shadow
    (16, 24, 32),     # 4: outline
    (72, 104, 120),   # 5: helmet shadow duplicate
    (136, 176, 184),  # 6: helmet light duplicate
    (232, 96, 72),    # 7: coral accent highlight
    (32, 80, 96),     # 8: body shadow
    (224, 240, 232),  # 9: eye and tooth highlight
    (48, 120, 136),   # 10: body midtone
    (104, 184, 184),  # 11: body highlight
    (136, 48, 48),    # 12: coral accent shadow
    (24, 48, 64),     # 13: deepest body teal
    (248, 184, 56),   # 14: amber eye
    (160, 224, 200),  # 15: seafoam underside
]

OVERWORLD_SHINY = [
    (152, 208, 160),  # 0: transparent
    (16, 16, 32),     # 1: helmet deepest shadow
    (72, 80, 120),    # 2: helmet light
    (32, 40, 72),     # 3: helmet shadow
    (8, 8, 24),       # 4: outline
    (48, 56, 88),     # 5: helmet midtone
    (152, 168, 200),  # 6: helmet highlight
    (184, 40, 112),   # 7: magenta accent highlight
    (16, 40, 64),     # 8: body shadow
    (152, 168, 200),  # 9: tooth highlight
    (24, 72, 104),    # 10: body midtone
    (64, 136, 160),   # 11: cold body highlight
    (64, 16, 48),     # 12: magenta accent shadow
    (8, 16, 32),      # 13: deepest body navy
    (72, 224, 248),   # 14: bioluminescent cyan eye
    (120, 72, 152),   # 15: dark purple underside
]

# Canonical Bagon shares indices 5 and 6 between its mouth and belly. Only the
# connected belly components are moved to dedicated seafoam palette slots.
FRONT_BELLY_BOXES = {
    0: (range(29, 39), range(40, 48)),
    1: (range(30, 40), range(40, 48)),
}
BACK_BELLY_BOX = (range(14, 22), range(54, 56))

# Only the eye-white components move to the amber accent slot. Tooth pixels
# using the same canonical index remain untouched.
FRONT_EYE_PIXELS = {
    0: {(29, 24), (28, 25), (29, 25), (27, 26), (28, 26)},
    1: {(38, 21), (39, 21), (38, 22), (39, 22), (37, 23), (38, 23)},
}
BACK_EYE_PIXELS = {(48, 25), (48, 26), (48, 27), (48, 28)}

# A restrained slate spine follows the rear helmet in each front pose. The
# neck, back, hands, and tail keep Bagon's canonical silhouettes. The canonical
# back sprite already has a strong rear helmet profile and needs no overlay.
FRONT_SPINES = {
    0: {
        (35, 17): 15,
        (35, 18): 10,
        (36, 18): 9,
        (37, 18): 15,
        (35, 19): 9,
        (36, 19): 15,
    },
    1: {
        (45, 14): 15,
        (45, 15): 10,
        (46, 15): 9,
        (47, 15): 15,
        (45, 16): 9,
        (46, 16): 15,
    },
}

# The canonical follower shares its orange slots between cheek/mouth accents
# and the small front-facing belly mark, while its eyes use a shared white
# highlight. Split those surfaces into Delta Bagon's coral, amber, and seafoam
# roles without changing any follower silhouette or animation frame.
OVERWORLD_EYE_PIXELS = {
    0: {(12, 20), (18, 20), (12, 21), (18, 21)},
    1: {(12, 20), (18, 20), (12, 21), (18, 21)},
    4: {(17, 21), (17, 22)},
    5: {(17, 21), (17, 22)},
}
OVERWORLD_BELLY_PIXELS = {
    0: {(14, 27), (15, 27), (16, 27)},
    1: {(14, 27), (15, 27), (16, 27)},
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


def remap_belly(image: Image.Image, xs: range, ys: range, frame_y: int = 0) -> None:
    for y in ys:
        for x in xs:
            index = image.getpixel((x, y + frame_y))
            if index == 5:
                image.putpixel((x, y + frame_y), 12)
            elif index == 6:
                image.putpixel((x, y + frame_y), 13)


def generate_front() -> None:
    image = Image.open(SOURCE / "anim_front_gba.png").copy()
    if image.mode != "P" or image.size != (64, 128):
        raise ValueError(f"Expected indexed 64x128 source, got {image.mode} {image.size}")

    for frame, frame_y in enumerate((0, 64)):
        remap_belly(image, *FRONT_BELLY_BOXES[frame], frame_y)
        for x, y in FRONT_EYE_PIXELS[frame]:
            if image.getpixel((x, y + frame_y)) == 11:
                image.putpixel((x, y + frame_y), 14)
        for (x, y), index in FRONT_SPINES[frame].items():
            image.putpixel((x, y + frame_y), index)

    apply_palette(image, BATTLE_NORMAL)
    save_indexed(image, TARGET / "anim_front.png")


def generate_back() -> None:
    image = Image.open(SOURCE / "back_gba.png").copy()
    if image.mode != "P" or image.size != (64, 64):
        raise ValueError(f"Expected indexed 64x64 source, got {image.mode} {image.size}")

    remap_belly(image, *BACK_BELLY_BOX)
    for x, y in BACK_EYE_PIXELS:
        if image.getpixel((x, y)) == 11:
            image.putpixel((x, y), 14)

    apply_palette(image, BATTLE_NORMAL)
    save_indexed(image, TARGET / "back.png")


def generate_icon() -> None:
    image = Image.open(SOURCE / "icon_gba.png").copy()
    # Shared icon palette 3 supplies slate greys and aquatic blues. Canonical
    # orange accent pixels become pale blue to echo the seafoam underside.
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y] == 10:
                pixels[x, y] = 6
    apply_palette(
        image,
        read_jasc_palette(ROOT / "graphics/pokemon/icon_palettes/pal3.pal"),
    )
    save_indexed(image, TARGET / "icon.png")


def generate_overworld() -> None:
    image = Image.open(SOURCE / "overworld.png").copy()
    for frame in range(6):
        frame_x = frame * 32
        for x, y in OVERWORLD_EYE_PIXELS.get(frame, set()):
            if image.getpixel((x + frame_x, y)) == 9:
                image.putpixel((x + frame_x, y), 14)
        for x, y in OVERWORLD_BELLY_PIXELS.get(frame, set()):
            if image.getpixel((x + frame_x, y)) in (7, 12):
                image.putpixel((x + frame_x, y), 15)
    apply_palette(image, OVERWORLD_NORMAL)
    save_indexed(image, TARGET / "overworld.png")


def expected_front_changes(source: Image.Image) -> set[tuple[int, int]]:
    allowed = set()
    for frame, frame_y in enumerate((0, 64)):
        xs, ys = FRONT_BELLY_BOXES[frame]
        allowed.update(
            (x, y + frame_y)
            for y in ys
            for x in xs
            if source.getpixel((x, y + frame_y)) in (5, 6)
        )
        allowed.update((x, y + frame_y) for x, y in FRONT_EYE_PIXELS[frame])
        allowed.update((x, y + frame_y) for x, y in FRONT_SPINES[frame])
    return allowed


def validate_index_changes(
    source: Image.Image,
    output: Image.Image,
    allowed: set[tuple[int, int]],
    name: str,
) -> None:
    actual = {
        (x, y)
        for y in range(source.height)
        for x in range(source.width)
        if source.getpixel((x, y)) != output.getpixel((x, y))
    }
    if not actual.issubset(allowed):
        unexpected = sorted(actual - allowed)
        raise ValueError(f"{name}: unexpected canonical pixel changes: {unexpected[:8]}")


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

    for name, colors in {
        "normal.pal": BATTLE_NORMAL,
        "shiny.pal": BATTLE_SHINY,
        "overworld_normal.pal": OVERWORLD_NORMAL,
        "overworld_shiny.pal": OVERWORLD_SHINY,
    }.items():
        if read_jasc_palette(TARGET / name) != colors:
            raise ValueError(f"{name}: generated palette does not match declared colors")

    front_source = Image.open(SOURCE / "anim_front_gba.png")
    front_output = Image.open(TARGET / "anim_front.png")
    validate_index_changes(
        front_source,
        front_output,
        expected_front_changes(front_source),
        "anim_front.png",
    )

    # Guard the two canonical upturned-tail regions explicitly.
    for xs, ys, frame_y in (
        (range(35, 41), range(28, 34), 0),
        (range(42, 47), range(30, 35), 64),
    ):
        for y in ys:
            for x in xs:
                if front_source.getpixel((x, y + frame_y)) != front_output.getpixel((x, y + frame_y)):
                    raise ValueError(f"Canonical tail changed at {(x, y + frame_y)}")

    back_source = Image.open(SOURCE / "back_gba.png")
    back_output = Image.open(TARGET / "back.png")
    back_xs, back_ys = BACK_BELLY_BOX
    allowed_back = {
        (x, y)
        for y in back_ys
        for x in back_xs
        if back_source.getpixel((x, y)) in (5, 6)
    } | BACK_EYE_PIXELS
    validate_index_changes(back_source, back_output, allowed_back, "back.png")

    icon_source = Image.open(SOURCE / "icon_gba.png")
    icon_output = Image.open(TARGET / "icon.png")
    allowed_icon = {
        (x, y)
        for y in range(icon_source.height)
        for x in range(icon_source.width)
        if icon_source.getpixel((x, y)) == 10
    }
    validate_index_changes(icon_source, icon_output, allowed_icon, "icon.png")

    overworld_source = Image.open(SOURCE / "overworld.png")
    overworld_output = Image.open(TARGET / "overworld.png")
    allowed_overworld = {
        (x + frame * 32, y)
        for frame, pixels in OVERWORLD_EYE_PIXELS.items()
        for x, y in pixels
    } | {
        (x + frame * 32, y)
        for frame, pixels in OVERWORLD_BELLY_PIXELS.items()
        for x, y in pixels
    }
    validate_index_changes(
        overworld_source,
        overworld_output,
        allowed_overworld,
        "overworld.png",
    )

    if (SOURCE / "footprint.png").read_bytes() != (TARGET / "footprint.png").read_bytes():
        raise ValueError("footprint.png must remain byte-identical to canonical Bagon")


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
