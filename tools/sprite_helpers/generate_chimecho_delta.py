#!/usr/bin/env python3
"""Deterministic generator for Chimecho delta -- Psychic/Steel alien craft.

Design contract
---------------
Chimecho's wind chime is reinterpreted as a small hovering alien craft: a pale
bone-metal hull, dusky lavender shading, indigo void shadow and spectral-green
glow. The canonical silhouette, pose and animation are preserved; the only
geometry change is a lens-shaped saucer brim grown from the body's own span.

Per-surface budget
------------------
| Surface   | Method                                                          |
| --------- | --------------------------------------------------------------- |
| Front     | Palette + saucer brim, running-lights, under-hull, beacon glint  |
| Back      | Saucer brim, continuous metal shading, violet tail              |
| Icon      | Shared palette 0, silver hull, outlined brim following the bob  |
| Overworld | Small outlined saucer, directional face, violet tail and lights |
| Footprint | Exact copy (canonical Chimecho's is empty)                       |

Both battle surfaces share one semantic index plan so a single pair of 16-colour
tables drives normal and shiny without a second PNG.

Every output is rebuilt from the canonical source on each run, and validation
proves dimensions, indexed mode, index-0 transparency, palette agreement, the
exact change set and the silhouette contract before anything reaches the build.
"""

from pathlib import Path
from shutil import copyfile

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "graphics/pokemon/chimecho"
TARGET = ROOT / "graphics/pokemon/chimecho_delta"

FRAME_YS = (0, 64)

# ---------------------------------------------------------------- palettes --

# Semantic index plan, shared by the front and back battle sprites:
#   1        outline
#   3/4/5    hull mid / highlight / shadow      6  specular
#   7        saucer brim plate                 10  void shadow / brim underside
#   8/9      crown dome                        14  running-lights / beacon
#   2/13     glow markings                     11/12 tail tones
#   15       secondary edge
BATTLE_NORMAL = [
    (152, 208, 160),  # 0: transparent
    (24, 16, 32),     # 1: violet-black outline
    (150, 240, 190),  # 2: spectral glow light
    (170, 175, 195),  # 3: bone hull midtone
    (220, 225, 235),  # 4: bone hull highlight
    (110, 110, 140),  # 5: dusky lavender shadow
    (245, 250, 255),  # 6: pale specular
    (196, 202, 218),  # 7: saucer hull plate
    (200, 240, 215),  # 8: pale ghost-green (crown dome)
    (120, 205, 165),  # 9: ghost-green (crown dome)
    (58, 44, 80),      # 10: indigo void / brim underside
    (92, 70, 120),     # 11: muted violet (tail)
    (40, 28, 60),      # 12: dark violet (tail)
    (90, 200, 150),     # 13: spectral green markings
    (170, 250, 205),   # 14: bright spectral (running-lights / beacon)
    (70, 58, 95),      # 15: violet-grey edge
]

# Shiny: the same craft in night-ops livery -- graphite hull, hot magenta glow.
BATTLE_SHINY = [
    (152, 208, 160),  # 0: transparent
    (20, 12, 24),     # 1: outline
    (255, 170, 235),  # 2: magenta glow light
    (86, 84, 104),     # 3: graphite hull midtone
    (132, 130, 152),  # 4: graphite hull highlight
    (52, 50, 68),      # 5: hull shadow
    (200, 196, 216),  # 6: pale specular
    (110, 108, 132),  # 7: saucer hull plate
    (255, 200, 245),  # 8: pale magenta (crown dome)
    (232, 96, 200),    # 9: magenta (crown dome)
    (26, 18, 34),      # 10: void / brim underside
    (110, 34, 86),     # 11: deep magenta (tail)
    (60, 16, 48),      # 12: darkest magenta (tail)
    (214, 74, 180),    # 13: magenta markings
    (255, 190, 240),   # 14: bright magenta (running-lights / beacon)
    (72, 48, 80),      # 15: secondary edge
]

# Follower sheet retains the canonical slots, with 13-15 reserved for the rim.
OVERWORLD_NORMAL = [
    (152, 208, 160),  # 0: transparent
    (46, 110, 90),     # 1: dome shadow
    (150, 240, 190),  # 2: dome light
    (226, 230, 240),  # 3: hull highlight
    (24, 16, 32),     # 4: outline
    (110, 110, 140),  # 5: hull shadow
    (90, 180, 145),    # 6: dome midtone
    (170, 175, 195),  # 7: hull midtone
    (206, 212, 226),  # 8: hull light
    (92, 70, 120),    # 9: violet tail midtone
    (40, 28, 60),     # 10: violet tail edge
    (100, 190, 155),   # 11: dome accent
    (92, 96, 124),     # 12: deep hull shadow
    (196, 202, 218),   # 13: saucer plate
    (170, 250, 205),   # 14: running lights
    (58, 44, 80),      # 15: saucer underside
]

OVERWORLD_SHINY = [
    (152, 208, 160),  # 0: transparent
    (110, 34, 86),     # 1: dome shadow
    (255, 170, 235),  # 2: dome light
    (150, 148, 170),  # 3: hull highlight
    (20, 12, 24),     # 4: outline
    (52, 50, 68),      # 5: hull shadow
    (214, 74, 180),    # 6: dome midtone
    (86, 84, 104),     # 7: hull midtone
    (124, 122, 146),  # 8: hull light
    (110, 34, 86),     # 9: deep magenta tail
    (60, 16, 48),      # 10: magenta tail edge
    (198, 60, 164),    # 11: dome accent
    (44, 42, 58),      # 12: deep hull shadow
    (110, 108, 132),   # 13: saucer plate
    (255, 190, 240),   # 14: running lights
    (26, 18, 34),      # 15: saucer underside
]

# ------------------------------------------------------- shared transforms --

# Canonical 11/12 edge the markings and 10 doubles as plain edge shading; this
# palette renders all three near-black, which reads as dirt on the pale hull.
EDGE_REMAP = {11: 5, 12: 5}
SHADE_REMAP = {10: 5}

UNDER_HULL_REMAP = {6: 4, 4: 3, 3: 5}

# Saucer brim: local row -> (pixels grown each side, fill tone).
FRONT_BRIM = {24: (1, 4), 25: (3, 7), 26: (4, 7), 27: (2, 10)}
FRONT_BRIM_LIGHT_ROW = 26
FRONT_CROWN_MAX_Y = 13          # crown knob sits above this row
FRONT_DOME_ROWS = range(14, 18)  # dome above the eyes; the face keeps rows 18-22
FRONT_UNDER_HULL = range(28, 31)
FRONT_NECK_Y = 31               # rows >= this are the tail, palette-only

BACK_BRIM = {32: (1, 4), 33: (3, 7), 34: (4, 7), 35: (2, 10)}
BACK_BRIM_LIGHT_ROW = 34
BACK_BODY_TOP = 21              # the crown ring occupies rows 7-20
BACK_DOME_ROWS = range(21, 32)
BACK_UNDER_HULL = range(36, 43)
BACK_TAIL_Y = 44

# Icon: canonical index -> shared icon palette 0 index.
ICON_PAL_INDEX = 0
ICON_REMAP = {5: 13, 4: 13, 12: 3, 8: 2, 1: 2, 11: 1, 9: 14, 14: 15}
ICON_TAIL_REMAP = {12: 2, 11: 9, 9: 13}
ICON_FRAME_YS = (0, 32)
# The second canonical icon bobs down one pixel. Local coordinates below follow
# that motion, including the brim, instead of cutting across the face in frame 1.
ICON_BOB = (0, 1)
ICON_BRIM = {
    19: (9, "f222222222222f"),
    20: (10, "f1d11111d11f"),
    21: (11, "ffffffffff"),
}

# Hex strings are palette indices, with an explicit origin in each 32px frame.
# The shallow lens leaves the face above the plate and the original tail below.
OVERWORLD_BRIM = {
    20: (9, "4ddedddedddedd4"),
    21: (10, "44fffffffff44"),
    22: (12, "444444444"),
}
OVERWORLD_SIDE_BRIM = {
    20: (9, "4dedddeddddddd4"),
    21: (10, "44fffffffff44"),
    22: (12, "444444444"),
}


def read_jasc(path: Path) -> list[tuple[int, int, int]]:
    lines = path.read_text().splitlines()
    if len(lines) != 19 or lines[:3] != ["JASC-PAL", "0100", "16"]:
        raise ValueError(f"{path}: not a 16-colour JASC palette")
    colors = [tuple(int(v) for v in line.split()) for line in lines[3:]]
    if any(len(c) != 3 or any(v < 0 or v > 255 for v in c) for c in colors):
        raise ValueError(f"{path}: invalid RGB entry")
    return colors


def write_jasc(path: Path, colors: list[tuple[int, int, int]]) -> None:
    if len(colors) != 16:
        raise ValueError(f"{path}: expected 16 colours, got {len(colors)}")
    body = "\n".join(f"{r} {g} {b}" for r, g, b in colors)
    text = f"JASC-PAL\n0100\n16\n{body}\n"
    # Preserve existing line endings when the runtime colors are unchanged.
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def open_indexed(name: str, size: tuple[int, int]) -> Image.Image:
    img = Image.open(SOURCE / name)
    if img.mode != "P" or img.size != size:
        raise ValueError(f"{name}: expected indexed {size}, got {img.mode} {img.size}")
    return img


def apply_palette(img: Image.Image, colors: list[tuple[int, int, int]]) -> None:
    flat = [c for color in colors for c in color]
    img.putpalette(flat + [0] * (768 - len(flat)))
    img.info["transparency"] = 0


def save_indexed(img: Image.Image, path: Path) -> None:
    if img.mode != "P":
        raise ValueError(f"refusing to save non-indexed image: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, bits=4, optimize=False)


def grow_brim(px, put, brim_spec: dict, light_row: int) -> set:
    """Widen the hull into a lens-shaped saucer brim, from each row's own span."""
    brim: set[tuple[int, int]] = set()
    for y, (grow, tone) in brim_spec.items():
        xs = [x for x in range(64) if px(x, y) != 0]
        if not xs:
            continue
        lo, hi = min(xs), max(xs)
        for x in range(lo, hi + 1):
            if px(x, y) != 0:
                put(x, y, tone)
                brim.add((x, y))
        for d in range(1, grow + 1):
            for x in (lo - d, hi + d):
                if 0 <= x < 64:
                    put(x, y, tone)
                    brim.add((x, y))

    for x, y in sorted(brim):                       # outline the new boundary
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (nx, ny) in brim or not 0 <= nx < 64 or not 0 <= ny < 64:
                continue
            if px(nx, ny) == 0:
                put(nx, ny, 1)

    row = sorted(x for x, y in brim if y == light_row)
    if row:
        lo, hi = row[0], row[-1]
        for x in (lo + 2, (lo + hi) // 2, hi - 2):
            put(x, light_row, 14)
    return brim


def remap_rows(px, put, rows, table: dict) -> None:
    for y in rows:
        for x in range(64):
            v = px(x, y)
            if v in table:
                put(x, y, table[v])


# ------------------------------------------------------------- generators --

def build_front(touched: set) -> Image.Image:
    img = open_indexed("anim_front_gba.png", (64, 128)).copy()
    grid = img.load()

    for fy in FRAME_YS:
        px = lambda x, y: grid[x, y + fy]

        def put(x, y, i, _fy=fy):
            grid[x, y + _fy] = i
            touched.add((x, y + _fy))

        knob = [(x, y) for y in range(FRONT_CROWN_MAX_Y + 1) for x in range(64) if px(x, y)]
        if knob:                                     # beacon glint on the crest
            top = min(y for _, y in knob)
            tip = [x for x, y in knob if y == top]
            for x in range(min(tip), max(tip) + 1):
                if px(x, top) not in (0, 1):
                    put(x, top, 14)

        for y in range(FRONT_CROWN_MAX_Y + 1, FRONT_NECK_Y):
            table = EDGE_REMAP | SHADE_REMAP if y in FRONT_DOME_ROWS else EDGE_REMAP
            for x in range(64):
                if px(x, y) in table:
                    put(x, y, table[px(x, y)])

        grow_brim(px, put, FRONT_BRIM, FRONT_BRIM_LIGHT_ROW)
        remap_rows(px, put, FRONT_UNDER_HULL, UNDER_HULL_REMAP)

    apply_palette(img, BATTLE_NORMAL)
    return img


def build_back(touched: set) -> Image.Image:
    img = open_indexed("back_gba.png", (64, 64)).copy()
    grid = img.load()
    px = lambda x, y: grid[x, y]

    def put(x, y, i):
        grid[x, y] = i
        touched.add((x, y))

    remap_rows(px, put, range(BACK_BODY_TOP, BACK_TAIL_Y), EDGE_REMAP)
    remap_rows(px, put, BACK_DOME_ROWS, SHADE_REMAP)
    grow_brim(px, put, BACK_BRIM, BACK_BRIM_LIGHT_ROW)
    remap_rows(px, put, BACK_UNDER_HULL, UNDER_HULL_REMAP)

    # Consolidate the canonical checker highlights into continuous material
    # clusters. Only the original dome/hull indices may receive these shades.
    src = open_indexed("back_gba.png", (64, 64))
    for y in range(8, 20):
        for x in range(64):
            if src.getpixel((x, y)) in (8, 9):
                put(x, y, 8 if x + y <= 43 else 9)
    for y in range(24, 32):
        for x in range(64):
            if src.getpixel((x, y)) in (3, 4):
                put(x, y, 4 if x + y <= 58 else 3)
    # The hanging ribbon uses the front's violet material, not hull grey.
    remap_rows(px, put, range(45, 57), {5: 11, 10: 12})

    apply_palette(img, BATTLE_NORMAL)
    return img


def build_icon() -> Image.Image:
    img = open_indexed("icon_gba.png", (32, 64)).copy()
    grid = img.load()

    for fy, bob in zip(ICON_FRAME_YS, ICON_BOB):
        for y in range(32):
            for x in range(32):
                v = grid[x, y + fy]
                table = ICON_REMAP | ICON_TAIL_REMAP if y >= 23 + bob else ICON_REMAP
                grid[x, y + fy] = table.get(v, v)

        for y, (left, indices) in ICON_BRIM.items():
            for dx, index in enumerate(indices):
                grid[left + dx, y + bob + fy] = int(index, 16)
        # A compact top-left reflection gives the beacon a round, glassy read.
        for x, y in ((14, 11), (14, 12), (15, 12)):
            grid[x, y + bob + fy] = 3

    apply_palette(img, read_jasc(ROOT / "graphics/pokemon/icon_palettes/pal0.pal"))
    return img


def build_overworld() -> Image.Image:
    img = open_indexed("overworld.png", (192, 32)).copy()
    for frame in range(6):
        fx = frame * 32
        side = frame >= 4
        for y in range(16, 20):
            for x in range(32):
                v = img.getpixel((fx + x, y))
                # Red base-species markings become subdued hull shade, leaving
                # the green accent budget for the dome and tiny running lights.
                if v in (9, 10, 11):
                    img.putpixel((fx + x, y), {9: 7, 10: 5, 11: 5}[v])
        # Preserve readable eyes only on south/west views; north has no face.
        eyes = ((14, 19), (18, 19)) if frame < 2 else ((14, 19),) if side else ()
        for x, y in eyes:
            img.putpixel((fx + x, y), 4)
        brim = OVERWORLD_SIDE_BRIM if side else OVERWORLD_BRIM
        for y, (left, indices) in brim.items():
            for dx, index in enumerate(indices):
                img.putpixel((fx + left + dx, y), int(index, 16))
        # The ribbon retains its canonical swing, with a small spectral seam.
        for y in range(24, 28):
            for x in range(32):
                if img.getpixel((fx + x, y)) == 7:
                    img.putpixel((fx + x, y), 6)
    apply_palette(img, OVERWORLD_NORMAL)
    return img


# -------------------------------------------------------------- validation --

EXPECTED = {
    "anim_front.png": (64, 128),
    "back.png": (64, 64),
    "icon.png": (32, 64),
    "overworld.png": (192, 32),
    "footprint.png": (16, 16),
}


def validate(front_touched: set, back_touched: set) -> None:
    for name, size in EXPECTED.items():
        img = Image.open(TARGET / name)
        if img.mode != "P" or img.size != size:
            raise ValueError(f"{name}: expected indexed {size}, got {img.mode} {img.size}")
        used = {i for _, i in img.getcolors(maxcolors=256)}
        if not used.issubset(set(range(16))):
            raise ValueError(f"{name}: uses a palette index above 15")
        if name != "footprint.png" and img.info.get("transparency") != 0:
            raise ValueError(f"{name}: index 0 must be transparent")

    for name, colors in (
        ("normal.pal", BATTLE_NORMAL),
        ("shiny.pal", BATTLE_SHINY),
        ("overworld_normal.pal", OVERWORLD_NORMAL),
        ("overworld_shiny.pal", OVERWORLD_SHINY),
    ):
        if read_jasc(TARGET / name) != colors:
            raise ValueError(f"{name}: written palette does not match its table")

    if len(BATTLE_NORMAL) != len(BATTLE_SHINY):
        raise ValueError("normal and shiny battle palettes differ in length")

    # Embedded palettes must agree with the runtime tables.
    for name, colors in (("anim_front.png", BATTLE_NORMAL), ("back.png", BATTLE_NORMAL),
                         ("overworld.png", OVERWORLD_NORMAL)):
        emb = Image.open(TARGET / name).getpalette()[:48]
        if emb != [c for color in colors for c in color]:
            raise ValueError(f"{name}: embedded palette does not match its table")
    icon_pal = read_jasc(ROOT / "graphics/pokemon/icon_palettes/pal0.pal")
    if Image.open(TARGET / "icon.png").getpalette()[:48] != [c for col in icon_pal for c in col]:
        raise ValueError("icon.png: embedded palette must be shared icon palette 0")

    # Change sets and the silhouette contract.
    for name, src_name, touched, brim_rows, frames in (
        ("anim_front.png", "anim_front_gba.png", front_touched, set(FRONT_BRIM), FRAME_YS),
        ("back.png", "back_gba.png", back_touched, set(BACK_BRIM), (0,)),
    ):
        src = Image.open(SOURCE / src_name)
        out = Image.open(TARGET / name)
        w, h = out.size
        changed = {(x, y) for y in range(h) for x in range(w)
                   if src.getpixel((x, y)) != out.getpixel((x, y))}
        stray = sorted(changed - touched)
        if stray:
            raise ValueError(f"{name}: changes outside the declared edit set: {stray[:8]}")
        allowed = brim_rows | {min(brim_rows) - 1, max(brim_rows) + 1}
        for y in range(h):
            for x in range(w):
                src0 = src.getpixel((x, y)) == 0
                out0 = out.getpixel((x, y)) == 0
                if out0 and not src0:
                    raise ValueError(f"{name}: silhouette shrank at ({x}, {y})")
                if src0 and not out0 and (y % 64) not in allowed:
                    raise ValueError(f"{name}: silhouette grew off the brim at ({x}, {y})")

    # Small sprites keep canonical anatomy; new silhouette pixels are restricted
    # to the declared lens. Palette edits never turn a body pixel transparent.
    for name, source_name, frames, brim, remap in (
        ("icon.png", "icon_gba.png", 2, ICON_BRIM, ICON_REMAP),
        ("overworld.png", "overworld.png", 6, OVERWORLD_BRIM, {}),
    ):
        src = Image.open(SOURCE / source_name)
        out = Image.open(TARGET / name)
        for frame in range(frames):
            icon = name == "icon.png"
            fx, fy = (0, frame * 32) if icon else (frame * 32, 0)
            bob = ICON_BOB[frame] if icon else 0
            frame_brim = OVERWORLD_SIDE_BRIM if not icon and frame >= 4 else brim
            lens = {(left + dx, y + bob): int(index, 16)
                    for y, (left, indices) in frame_brim.items()
                    for dx, index in enumerate(indices)}
            glint = {(14, 11 + bob), (14, 12 + bob), (15, 12 + bob)} if icon else set()
            for y in range(32):
                for x in range(32):
                    a, b = src.getpixel((fx + x, fy + y)), out.getpixel((fx + x, fy + y))
                    if a and not b:
                        raise ValueError(f"{name}: silhouette shrank in frame {frame}")
                    if not a and b and (x, y) not in lens:
                        raise ValueError(f"{name}: silhouette grew off brim in frame {frame}")
                    if (x, y) in lens:
                        expected = lens[x, y]
                    elif (x, y) in glint:
                        expected = 3
                    elif icon:
                        table = remap | ICON_TAIL_REMAP if y >= 23 + bob else remap
                        expected = table.get(a, a)
                    else:
                        expected = a
                        if 16 <= y < 20:
                            expected = {9: 7, 10: 5, 11: 5}.get(a, a)
                        if y == 19 and ((frame < 2 and x in (14, 18)) or (frame >= 4 and x == 14)):
                            expected = 4
                        if 24 <= y < 28 and a == 7:
                            expected = 6
                    if b != expected:
                        raise ValueError(f"{name}: undeclared edit in frame {frame} at {(x, y)}")

        # Paired frames must retain the same head; only the source tail swings.
        if name == "overworld.png":
            for frame in (0, 2, 4):
                a = out.crop((frame * 32, 0, (frame + 1) * 32, 23))
                b = out.crop(((frame + 1) * 32, 0, (frame + 2) * 32, 23))
                if a.tobytes() != b.tobytes():
                    raise ValueError("overworld.png: head flickers between paired frames")
        elif out.crop((0, 0, 32, 22)).tobytes() != out.crop((0, 33, 32, 55)).tobytes():
            raise ValueError("icon.png: saucer does not follow the one-pixel bob")

    if (TARGET / "footprint.png").read_bytes() != (SOURCE / "footprint.png").read_bytes():
        raise ValueError("footprint.png: canonical footprint changed")


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    front_touched: set = set()
    back_touched: set = set()

    save_indexed(build_front(front_touched), TARGET / "anim_front.png")
    save_indexed(build_back(back_touched), TARGET / "back.png")
    save_indexed(build_icon(), TARGET / "icon.png")
    save_indexed(build_overworld(), TARGET / "overworld.png")
    copyfile(SOURCE / "footprint.png", TARGET / "footprint.png")

    write_jasc(TARGET / "normal.pal", BATTLE_NORMAL)
    write_jasc(TARGET / "shiny.pal", BATTLE_SHINY)
    write_jasc(TARGET / "overworld_normal.pal", OVERWORLD_NORMAL)
    write_jasc(TARGET / "overworld_shiny.pal", OVERWORLD_SHINY)

    validate(front_touched, back_touched)
    print(f"Wrote {len(EXPECTED) + 4} assets to {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
