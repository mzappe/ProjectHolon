#!/usr/bin/env python3
"""Generate a hydrothermal Delta Shelgon front proposal from GBA Shelgon."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "graphics/pokemon/shelgon/anim_front_gba.png"
TARGET = ROOT / "graphics/pokemon/shelgon_delta_water/anim_front.png"


# The middle stage is a Fire-type hydrothermal chrysalis: its exposed body
# heats to ember red while the deep-ocean shell becomes dark basalt threaded
# with glowing pressure fissures. This bridges Water Bagon to Water/Fire
# Salamence without relying on a generic orange shell.
BATTLE_NORMAL = [
    (160, 160, 80),   # 0: transparent
    (48, 16, 24),     # 1: deepest ember body
    (96, 24, 24),     # 2: body shadow
    (160, 48, 32),    # 3: heated body midtone
    (232, 96, 48),    # 4: unused body highlight
    (96, 16, 16),     # 5: unused ember shadow
    (248, 112, 32),   # 6: heated claw accent
    (72, 144, 152),   # 7: unused aquatic accent
    (8, 16, 24),      # 8: basalt deepest shadow
    (24, 32, 40),     # 9: basalt shadow
    (48, 56, 64),     # 10: basalt light
    (88, 96, 96),     # 11: basalt highlight
    (248, 224, 64),   # 12: yellow-hot eye highlight
    (208, 104, 16),   # 13: eye and heat shadow
    (248, 80, 24),    # 14: glowing pressure fissures
    (8, 8, 16),       # 15: outline
]

# A rear-swept dorsal crest breaks the egg-like silhouette without changing
# Shelgon's pose. The second animation frame is the same feature translated by
# the canonical frame's one-pixel-right, two-pixel-down movement.
DORSAL_CREST = {
    (37, 7): 15,
    (36, 8): 10,
    (37, 8): 9,
    (38, 8): 15,
    (35, 9): 10,
    (36, 9): 14,
    (37, 9): 9,
    (38, 9): 15,
    (34, 10): 10,
    (35, 10): 10,
    (36, 10): 14,
    (37, 10): 9,
    (38, 10): 15,
    (34, 11): 10,
    (35, 11): 9,
    (36, 11): 14,
    (37, 11): 15,
}

# The viewer-right spiral is now a geothermal fissure: a visible hot path
# curling through the pressure-darkened shell.
CARAPACE_SPIRAL = {
    (40, 25): 14,
    (41, 25): 14,
    (42, 25): 14,
    (39, 26): 14,
    (43, 26): 14,
    (38, 27): 14,
    (43, 27): 14,
    (38, 28): 14,
    (40, 28): 8,
    (41, 28): 8,
    (43, 28): 14,
    (38, 29): 14,
    (40, 29): 8,
    (42, 29): 14,
    (43, 29): 14,
    (39, 30): 14,
    (40, 30): 14,
    (41, 30): 14,
    (42, 30): 14,
}

FEATURES = DORSAL_CREST | CARAPACE_SPIRAL
FRAME_OFFSETS = ((0, 0, 0), (1, 2, 64))


def apply_palette(image: Image.Image) -> None:
    flat = [channel for color in BATTLE_NORMAL for channel in color]
    image.putpalette(flat + [0] * (768 - len(flat)))
    image.info["transparency"] = 0


def generate_front() -> None:
    image = Image.open(SOURCE).copy()
    if image.mode != "P" or image.size != (64, 128):
        raise ValueError(f"Expected indexed 64x128 source, got {image.mode} {image.size}")

    for delta_x, delta_y, frame_y in FRAME_OFFSETS:
        for (x, y), index in FEATURES.items():
            image.putpixel((x + delta_x, y + delta_y + frame_y), index)

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

    allowed_changes = {
        (x + delta_x, y + delta_y + frame_y)
        for delta_x, delta_y, frame_y in FRAME_OFFSETS
        for x, y in FEATURES
    }
    actual_changes = {
        (x, y)
        for y in range(128)
        for x in range(64)
        if source.getpixel((x, y)) != output.getpixel((x, y))
    }
    if not actual_changes.issubset(allowed_changes):
        unexpected = sorted(actual_changes - allowed_changes)
        raise ValueError(f"Unexpected canonical pixel changes: {unexpected[:8]}")


def main() -> None:
    generate_front()
    validate()


if __name__ == "__main__":
    main()
