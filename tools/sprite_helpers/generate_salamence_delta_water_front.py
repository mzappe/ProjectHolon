#!/usr/bin/env python3
"""Generate a Water/Fire Delta Salamence front proposal from GBA Salamence."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "graphics/pokemon/salamence/anim_front_gba.png"
TARGET = ROOT / "graphics/pokemon/salamence_delta_water/anim_front.png"


# Delta Salamence combines Bagon's ancient-aquatic hide and seafoam underside
# with Shelgon's basalt shell, ember heat, and pressure-fissure motif. Canonical
# wings become dark hydrothermal vent-sails rather than ordinary red wings.
BATTLE_NORMAL = [
    (160, 160, 80),   # 0: transparent
    (8, 24, 48),      # 1: deepest abyssal navy-blue
    (16, 48, 80),     # 2: body shadow
    (24, 72, 112),    # 3: body midtone
    (56, 120, 152),   # 4: cold body highlight
    (8, 16, 24),      # 5: vent-sail deepest basalt
    (24, 32, 32),     # 6: vent-sail basalt
    (144, 32, 24),    # 7: flame and magma shadow
    (248, 80, 24),    # 8: flame and magma highlight
    (40, 56, 72),     # 9: underside deepest slate
    (72, 144, 136),   # 10: seafoam underside shadow
    (152, 216, 192),  # 11: seafoam underside light
    (224, 240, 232),  # 12: claw and tooth highlight
    (112, 32, 40),    # 13: unused heated accent
    (248, 208, 64),   # 14: flame core and amber eye
    (8, 8, 16),       # 15: outline
]


# Branching magma veins continue Shelgon's glowing pressure cracks across the
# two differently posed wing frames. Every coordinate lies on canonical wing
# pixels, so the wing silhouette and animation remain untouched.
MAGMA_VEINS = {
    0: {
        (53, 16): 7,
        (52, 17): 7,
        (50, 18): 8,
        (49, 19): 8,
        (48, 20): 7,
        (47, 21): 8,
        (41, 22): 7,
        (46, 22): 7,
        (48, 22): 7,
        (41, 23): 7,
        (45, 23): 8,
        (49, 23): 7,
        (50, 23): 7,
        (42, 24): 7,
        (44, 24): 7,
        (43, 25): 8,
        (42, 26): 7,
        (41, 27): 8,
        (40, 28): 7,
        (39, 29): 7,
        (38, 30): 7,
    },
    1: {
        (52, 14): 7,
        (51, 15): 7,
        (49, 16): 8,
        (48, 17): 7,
        (47, 18): 7,
        (46, 19): 8,
        (45, 20): 7,
        (38, 21): 7,
        (44, 21): 8,
        (38, 22): 7,
        (43, 22): 7,
        (45, 22): 7,
        (39, 23): 7,
        (42, 23): 8,
        (46, 23): 7,
        (47, 23): 7,
        (41, 24): 7,
        (40, 25): 8,
        (39, 26): 7,
        (38, 27): 8,
        (37, 28): 7,
        (36, 29): 7,
    },
}

# A curled shoulder flare feeds a line of yellow, orange, and ember-red nodes
# along the flank. This is fire-like deep-sea bioluminescence embedded beneath
# the scales, while the underside remains seafoam as the separate Water cue.
BODY_BIOLUMINESCENCE = {
    0: {
        (31, 32): 7,
        (32, 33): 8,
        (33, 34): 14,
        (35, 34): 14,
        (36, 34): 8,
        (34, 35): 8,
        (33, 36): 7,
        (39, 36): 8,
        (40, 36): 7,
        (32, 37): 7,
        (44, 37): 14,
        (45, 37): 8,
        (49, 38): 8,
        (50, 38): 7,
        (54, 39): 14,
        (55, 39): 8,
    },
    1: {
        (31, 33): 7,
        (32, 34): 8,
        (33, 35): 14,
        (35, 35): 14,
        (36, 35): 8,
        (34, 36): 8,
        (33, 37): 7,
        (40, 37): 8,
        (41, 37): 7,
        (32, 38): 7,
        (45, 38): 14,
        (46, 38): 8,
        (50, 39): 8,
        (51, 39): 7,
        (55, 40): 14,
        (56, 40): 8,
    },
}

EYE_PIXELS = {
    0: {(11, 24)},
    1: {(23, 17)},
}


def apply_palette(image: Image.Image) -> None:
    flat = [channel for color in BATTLE_NORMAL for channel in color]
    image.putpalette(flat + [0] * (768 - len(flat)))
    image.info["transparency"] = 0


def generate_front() -> None:
    image = Image.open(SOURCE).copy()
    if image.mode != "P" or image.size != (64, 128):
        raise ValueError(f"Expected indexed 64x128 source, got {image.mode} {image.size}")

    for frame, frame_y in enumerate((0, 64)):
        for (x, y), index in MAGMA_VEINS[frame].items():
            image.putpixel((x, y + frame_y), index)
        for (x, y), index in BODY_BIOLUMINESCENCE[frame].items():
            image.putpixel((x, y + frame_y), index)
        for x, y in EYE_PIXELS[frame]:
            if image.getpixel((x, y + frame_y)) == 12:
                image.putpixel((x, y + frame_y), 14)

    apply_palette(image)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    image.save(TARGET, bits=4, optimize=False)


def validate() -> None:
    source = Image.open(SOURCE)
    output = Image.open(TARGET)
    if output.mode != "P" or output.size != (64, 128):
        raise ValueError(f"Expected indexed 64x128 output, got {output.mode} {output.size}")
    if output.info.get("transparency") != 0:
        raise ValueError("Palette index 0 must remain transparent")
    used = {index for _, index in output.getcolors(maxcolors=256)}
    if not used.issubset(set(range(16))):
        raise ValueError("Output uses a palette index above 15")

    allowed_changes = set()
    for frame, frame_y in enumerate((0, 64)):
        allowed_changes.update((x, y + frame_y) for x, y in MAGMA_VEINS[frame])
        allowed_changes.update((x, y + frame_y) for x, y in BODY_BIOLUMINESCENCE[frame])
        allowed_changes.update((x, y + frame_y) for x, y in EYE_PIXELS[frame])

    actual_changes = {
        (x, y)
        for y in range(128)
        for x in range(64)
        if source.getpixel((x, y)) != output.getpixel((x, y))
    }
    if not actual_changes.issubset(allowed_changes):
        unexpected = sorted(actual_changes - allowed_changes)
        raise ValueError(f"Unexpected canonical pixel changes: {unexpected[:8]}")

    for frame, frame_y in enumerate((0, 64)):
        for x, y in MAGMA_VEINS[frame]:
            if source.getpixel((x, y + frame_y)) not in (5, 6, 7, 8):
                raise ValueError(f"Magma vein left canonical wing at {(x, y + frame_y)}")
        for x, y in BODY_BIOLUMINESCENCE[frame]:
            if source.getpixel((x, y + frame_y)) not in (1, 2, 3, 4):
                raise ValueError(f"Body glow left canonical body at {(x, y + frame_y)}")


def main() -> None:
    generate_front()
    validate()


if __name__ == "__main__":
    main()
