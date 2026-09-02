---
title: "Pokémon Holon Legends — Deterministic Delta Pokémon Production Pipeline"
doc-id: HL-TEC-006
version: 1.1
status: Living Document
category: Technical Art
last-updated: 2026-09-02
author: Matt Zappe
---

# Pokémon Holon Legends — Deterministic Delta Pokémon Production Pipeline

> **Status:** Living Document | **Version:** 1.1 | **Updated:** 2026-09-02

This guide documents the repeatable process used to derive the Fire-type Ralts δ and Grass-type Dratini δ sprite sets from their canonical assets and connect them to standalone species in Project Holon. It is intended to be the default pipeline for future Delta Species that preserve a canonical Pokémon's pose and silhouette while changing palette, markings, and small controlled details.

This is not an all-new image-generation workflow. Every output pixel is produced by a checked-in script from checked-in source assets, named palette tables, and explicit coordinate edits. Running the same script against the same inputs produces the same files.

The engine-integration sections are written for this repository's current `pokeemerald-expansion` 1.16.x layout. The upstream RHH tutorial remains the authority for general new-species requirements; this guide adds Project Holon's deterministic art method, naming rules, follower assets, validation, and lessons from the Ralts δ implementation.

Related references:

- [RHH: How to add a new Pokémon](https://rh-hideout.github.io/pokeemerald-expansion/tutorials/how_to_new_pokemon.html)
- [`docs/tutorials/how_to_new_pokemon.md`](../../docs/tutorials/how_to_new_pokemon.md)
- [Delta Species Sprite Palette Swapping Guide](sprite-palette-guide.md)
- [Visual Asset and Animation Production Guide](visual-asset-production-guide.md)
- [Ralts δ deterministic generator](../../tools/sprite_helpers/generate_ralts_delta_fire.py)
- [Dratini δ deterministic generator](../../tools/sprite_helpers/generate_dratini_delta_grass.py)

---

## 1. The Core Idea

The pipeline has two independent halves:

```text
Canonical source sprites
        ↓
Deterministic transformation script
        ↓
Standalone indexed Delta assets
        ↓
Graphics declarations and frame tables
        ↓
SpeciesInfo, Pokédex, learnsets, evolution, encounters/starters
        ↓
Build, debug-menu inspection, and in-game validation
```

The art half answers, “How do we produce stable, reviewable sprites?” The data half answers, “How does the engine recognize and display this as a separate Pokémon?” Do not mix the two concepts. A sprite can build correctly but still point at the wrong species data, and a complete species entry can still reuse the base Pokémon's graphics by accident.

### 1.1 What “deterministic” means here

A deterministic Delta sprite has all of these properties:

- The canonical source asset remains unchanged.
- The Delta owns a separate folder under `graphics/pokemon/`.
- Palette values are declared explicitly in code.
- Any changed pixels are declared as palette-index mappings or coordinate maps.
- Frame repetition is handled programmatically rather than by separately painting each frame.
- Output dimensions, indexed mode, transparency, and palette indices are validated.
- The generator can be rerun at any time without accumulating edits.
- A reviewer can inspect the script and identify exactly why every changed pixel exists.

This gives us a reliable provenance chain: source + transformation + configuration = output.

### 1.2 When to use this method

Use this method when the Delta should still clearly be the original species and the design can be expressed through:

- palette replacement;
- palette-index remapping;
- small markings, particles, horns, wisps, cracks, or other bounded overlays;
- small frame-consistent adjustments;
- reuse of the canonical animation and overworld sheet layout.

Use a manual pixel-art production workflow when the design requires a fundamentally new silhouette, pose, anatomy, or animation. A large structural redesign forced into coordinate overlays becomes harder to understand and easier to break than a purpose-built sprite.

---

## 2. Lock the Design Contract Before Editing

Write down the following decisions before creating files:

| Decision | Example from Ralts δ |
| --- | --- |
| New species identifier | `SPECIES_RALTS_DELTA_FIRE` |
| Asset folder | `graphics/pokemon/ralts_delta_fire/` |
| Canonical visual source | `graphics/pokemon/ralts/` |
| Species relationship | A separate Pokémon, not a Ralts form or subfolder |
| Preserved geometry | Canonical body, hands, icon silhouette, and follower frames |
| Allowed additions | A small blue flame on the front and back battle sprites |
| Explicit exclusions | No flame on the icon or overworld sprite |
| Normal identity | Warm white body, orange/red helmet, blue flame |
| Shiny identity | Cool white/blue body, blue helmet, purple/pink flame |
| Reused data | Ralts cry, footprint, and learnsets |

This contract prevents “helpful” changes from turning into invented anatomy. If an overlay must appear to sit in a hand, define whether it is in front of the hand, behind it, or partially occluded before editing coordinates.

### 2.1 Folder rule

A separate Delta species gets a separate peer folder:

```text
graphics/pokemon/ralts/
graphics/pokemon/ralts_delta_fire/
```

Do not place the Delta under `graphics/pokemon/ralts/delta_fire/`. Engine asset paths, ownership, future evolution-family work, and review are clearer when every distinct species has its own standard folder.

---

## 3. Audit the Canonical Source

Never assume every Pokémon folder uses the same filenames. Inspect the actual source folder before writing the generator.

Ralts δ used these inputs:

| Purpose | Canonical input | Dimensions | Format |
| --- | --- | --- | --- |
| Animated front | `ralts/anim_front_gba.png` | 64x128 | Indexed PNG, two stacked 64x64 frames |
| Back | `ralts/back_gba.png` | 64x64 | Indexed PNG |
| Icon | `ralts/icon_gba.png` | 32x64 | Indexed PNG, two stacked 32x32 frames |
| Follower | `ralts/overworld.png` | 192x32 | Indexed PNG, six 32x32 frames |
| Footprint | `ralts/footprint.png` | 16x16 | Two-index PNG |

The output contract is:

```text
graphics/pokemon/<delta_name>/
├── anim_front.png
├── back.png
├── footprint.png
├── icon.png
├── normal.pal
├── overworld.png
├── overworld_normal.pal
├── overworld_shiny.pal
└── shiny.pal
```

The generator belongs under `tools/sprite_helpers/`, not inside the graphics folder. The graphics folder contains game inputs; the helper folder contains provenance and transformation logic.

---

## 4. Understand the Three Palette Systems

The front/back sprites, icons, and overworld followers do not all use the same palette mechanism.

### 4.1 Battle sprites

Battle sprites are 4bpp indexed images:

- 16 palette indices total;
- index 0 is transparent;
- up to 15 visible colors;
- `normal.pal` and `shiny.pal` must each contain exactly 16 entries;
- the same image indices are recolored by the normal or shiny palette at runtime.

This means a shiny sprite normally does not need a second PNG. The image geometry stays the same while `.shinyPalette` selects a different 16-color table.

### 4.2 Icons

Pokémon icons use one of the shared palettes in `graphics/pokemon/icon_palettes/`. They do not use the species' `normal.pal`, and the standard species structure does not register a separate shiny icon asset.

For Ralts δ, the generator remaps canonical icon indices into shared icon palette 3:

```python
remap = {4: 8, 5: 13, 13: 10}
```

The matching species entry uses:

```c
.iconPalIndex = 3,
```

Choose the shared icon palette first, then remap indices to it. Do not create colors in the icon PNG that its selected shared palette cannot display.

### 4.3 Overworld followers

The follower sheet uses its own normal and shiny palettes when `OW_PKMN_OBJECTS_SHARE_PALETTES == FALSE`:

```text
overworld.png
overworld_normal.pal
overworld_shiny.pal
```

The same `overworld.png` indices are rendered through either palette. The follower system reads shininess from the party Pokémon; there is no separate “shiny follower” switch.

### 4.4 JASC-PAL source format

Project palette source files use this shape:

```text
JASC-PAL
0100
16
R G B
R G B
...
```

The generator should reject a palette that does not have the exact header and 16 RGB rows. Keep palette order stable because the pixels store indices, not literal RGB values.

---

## 5. Build the Generator Canonical-First

The generator should always reopen the canonical source and rebuild the Delta output. Never open last run's Delta PNG and paint more pixels into it; that makes repeated runs accumulate changes.

### 5.1 Recommended skeleton

```python
#!/usr/bin/env python3
from pathlib import Path
from shutil import copyfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "graphics/pokemon/base_species"
TARGET = ROOT / "graphics/pokemon/base_species_delta_type"

def apply_palette(image, colors):
    flat = [channel for color in colors for channel in color]
    image.putpalette(flat + [0] * (768 - len(flat)))
    image.info["transparency"] = 0

def save_indexed(image, path):
    if image.mode != "P":
        raise ValueError(f"Refusing to save non-indexed image: {path}")
    image.save(path, bits=4, optimize=False)

def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    # Reopen canonical sources and create every output.
    # Write normal, shiny, and overworld palettes.
    # Copy only deliberately unchanged assets.
    validate()

if __name__ == "__main__":
    main()
```

Pillow is used because it preserves and edits palette indices directly. Confirm the dependency before starting:

```bash
python3 -c "from PIL import Image; print(Image.__version__)"
```

### 5.2 Declare palettes as named data

Use a 16-entry list for each runtime palette and comment the semantic role of important slots:

```python
BATTLE_NORMAL = [
    (160, 160, 80),   # 0: transparent
    (248, 240, 224),  # 1: body highlight
    # ...
    (32, 64, 144),    # 6: flame outline
    (48, 168, 248),   # 9: flame blue
    (184, 240, 248),  # 10: flame core
    # ...
]
```

Semantic comments matter. They make future changes intentional instead of turning the palette into an unexplained list of numbers.

### 5.3 Use coordinate maps for small overlays

Represent a small detail as `(x, y) → palette index`:

```python
HAND_FLAME = {
    (37, 36): 9,
    (36, 37): 9,
    (37, 37): 10,
    # ...
}
```

Apply the same local map to every stacked frame instead of duplicating it:

```python
for frame_y in (0, 64):
    for (x, y), index in HAND_FLAME.items():
        image.putpixel((x, y + frame_y), index)
```

This guarantees that an accent remains attached to the same anatomical location in both animation frames.

### 5.4 Encode occlusion, not invented anatomy

The final back flame was moved down and drawn behind the original hand. The script preserves any canonical nontransparent pixel:

```python
for (x, y), index in BACK_HAND_FLAME.items():
    if image.getpixel((x, y)) == 0:
        image.putpixel((x, y), index)
```

This is preferable to drawing a new white “hand” over the flame. The canonical sprite remains the authority for anatomy, outline, and shading; the new effect only occupies transparent space behind it.

Use the same rule whenever an effect should be behind an existing body part. If it should be in front, write that decision explicitly and restrict the overwritten coordinates to the approved region.

### 5.5 Keep unapproved surfaces clean

Ralts δ's final art contract deliberately has:

- blue flame on both front animation frames;
- blue flame behind the viewer-left hand on the back sprite;
- no flame on the icon;
- no flame on any overworld frame.

The icon and overworld are still deterministic transformations: the icon remaps palette indices, while the overworld keeps canonical geometry and applies the Delta overworld palette.

### 5.6 Copy only truly unchanged assets

The footprint was intentionally reused:

```python
copyfile(SOURCE / "footprint.png", TARGET / "footprint.png")
```

Copying it in the generator is still useful because it makes the output folder complete and reproducible. If the Delta needs a distinct footprint, generate or supply it explicitly instead.

---

## 6. Validate the Generated Assets

Validation belongs inside the generator so invalid assets fail before the ROM build.

At minimum, validate:

```python
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
        raise ValueError(...)
    used = {index for _, index in image.getcolors(maxcolors=256)}
    if not used.issubset(set(range(16))):
        raise ValueError(...)
```

Also verify that non-footprint assets identify index 0 as transparent. For future generators, add these higher-value checks where applicable:

- exactly 16 entries in every `.pal` file;
- every overlay coordinate lies inside its frame;
- normal and shiny palettes have the same length;
- untouched assets match the canonical pixel-index geometry;
- outputs from two consecutive runs have identical checksums.

Run the generator from the repository root:

```bash
python3 tools/sprite_helpers/generate_ralts_delta_fire.py
```

An idempotence check can be done with:

```bash
shasum -a 256 graphics/pokemon/ralts_delta_fire/*
python3 tools/sprite_helpers/generate_ralts_delta_fire.py
shasum -a 256 graphics/pokemon/ralts_delta_fire/*
```

Both checksum lists should match.

### 6.1 Visual review is still required

Technical validity cannot determine whether a flame appears connected to the correct hand. Render or inspect the sprites at a large integer zoom with nearest-neighbor scaling and check:

- attachment point;
- silhouette continuity;
- occlusion order;
- consistent placement across frames;
- no accidental limb extensions;
- readable normal and shiny palettes;
- follower readability at actual 1x size.

Iterate by changing coordinates or palette data in the generator, never by silently editing the generated PNG afterward.

---

## 7. Register a Separate Species

The following is the full species pipeline. In the Ralts δ case, some custom-species and Pokédex scaffolding already existed; the standalone graphics declarations and species links replaced reuse of ordinary Ralts assets. Future species should audit every item in this section.

### 7.1 Add the species constant

Add the new entry at the end of the custom block in `include/constants/species.h`:

```c
SPECIES_CUSTOM_START = SPECIES_GLIMMORA_MEGA,
SPECIES_MY_DELTA,
SPECIES_CUSTOM_END,
```

Never insert a new species in the middle of already released custom species. Species numbers are stored in saves; shifting them can turn saved Pokémon into different species.

### 7.2 Add Pokédex identity and orders

Add a `NATIONAL_DEX_*` constant in `include/constants/pokedex.h` and ensure `NATIONAL_DEX_COUNT` reaches the final custom entry. If the species belongs in the regional dex, add it to this project's regional-order macro as well.

Then add it to all three hardcoded sorting tables in `src/data/pokemon/pokedex_orders.h`:

- alphabetical;
- weight;
- height.

Ralts δ is placed beside Ralts in alphabetical order and in the matching 6.6 kg and 0.4 m sections.

### 7.3 Declare the graphics

Add declarations in `src/data/graphics/pokemon.h`. Follow the compression suffix used by the current neighboring entries rather than copying an old tutorial literally:

```c
const u32 gMonFrontPic_MyDelta[] =
    INCGFX_U32("graphics/pokemon/my_delta/anim_front.png", ".4bpp.smol");
const u16 gMonPalette_MyDelta[] =
    INCGFX_U16("graphics/pokemon/my_delta/normal.pal", ".gbapal");
const u32 gMonBackPic_MyDelta[] =
    INCGFX_U32("graphics/pokemon/my_delta/back.png", ".4bpp.smol");
const u16 gMonShinyPalette_MyDelta[] =
    INCGFX_U16("graphics/pokemon/my_delta/shiny.pal", ".gbapal");
const u8 gMonIcon_MyDelta[] =
    INCGFX_U8("graphics/pokemon/my_delta/icon.png", ".4bpp");

#if P_FOOTPRINTS
const u8 gMonFootprint_MyDelta[] =
    INCGFX_U8("graphics/pokemon/my_delta/footprint.png", ".1bpp");
#endif

#if OW_POKEMON_OBJECT_EVENTS
const u32 gObjectEventPic_MyDelta[] =
    INCGFX_COMP("graphics/pokemon/my_delta/overworld.png", ".4bpp", "-mwidth 4 -mheight 4");
#if OW_PKMN_OBJECTS_SHARE_PALETTES == FALSE
const u16 gOverworldPalette_MyDelta[] =
    INCGFX_U16("graphics/pokemon/my_delta/overworld_normal.pal", ".gbapal");
const u16 gShinyOverworldPalette_MyDelta[] =
    INCGFX_U16("graphics/pokemon/my_delta/overworld_shiny.pal", ".gbapal");
#endif
#endif
```

For a 32x32 follower sheet, `-mwidth 4 -mheight 4` describes four 8x8 tiles in each direction. A 64x64 follower requires the corresponding 8x8 settings and `SIZE_64x64` in species data.

### 7.4 Add the follower frame table

In `src/data/object_events/object_event_pic_tables_followers.h`:

```c
static const struct SpriteFrameImage sPicTable_MyDelta[] = {
    overworld_ascending_frames(gObjectEventPic_MyDelta, 4, 4),
};
```

Use `sAnimTable_Following` for the normal symmetric six-frame layout. Use `sAnimTable_Following_Asym` only when the sheet deliberately contains separate east and west frames.

### 7.5 Define `gSpeciesInfo`

Add a complete entry in `src/data/pokemon/species_info.h`. A derived Delta may copy biological values from its base species, but every copied value should be reviewed rather than assumed.

The required groups are:

- stats, typing, catch rate, experience, EV yield;
- gender, egg cycles/groups, friendship, growth rate;
- abilities and body color;
- name, cry, Pokédex number/category/description, dimensions;
- front/back graphics, sizes, offsets, and animations;
- normal/shiny palettes, icon, shadow, footprint;
- overworld sheet, size, shadow, tracks, animation table, palettes;
- learnsets, egg moves, evolutions, and any relevant flags.

For expansion 1.11.0 and later, front-frame timing is declared directly in `SpeciesInfo`:

```c
.frontAnimFrames = ANIM_FRAMES(
    ANIMCMD_FRAME(0, 8),
    ANIMCMD_FRAME(1, 25),
    ANIMCMD_FRAME(0, 8),
),
```

Ralts δ links its standalone graphics like this:

```c
.frontPic = gMonFrontPic_RaltsDeltaFire,
.backPic = gMonBackPic_RaltsDeltaFire,
.palette = gMonPalette_RaltsDeltaFire,
.shinyPalette = gMonShinyPalette_RaltsDeltaFire,
.iconSprite = gMonIcon_RaltsDeltaFire,
.iconPalIndex = 3,
FOOTPRINT(RaltsDeltaFire)
OVERWORLD(
    sPicTable_RaltsDeltaFire,
    SIZE_32x32,
    SHADOW_SIZE_M,
    TRACKS_FOOT,
    sAnimTable_Following,
    gOverworldPalette_RaltsDeltaFire,
    gShinyOverworldPalette_RaltsDeltaFire
)
```

### 7.6 Decide whether data is reused or unique

Ralts δ currently reuses:

```c
.cryId = CRY_RALTS,
.levelUpLearnset = sRaltsLevelUpLearnset,
.teachableLearnset = sRaltsTeachableLearnset,
.eggMoveLearnset = sRaltsEggMoveLearnset,
```

That is a deliberate content decision, not a technical requirement. If a Delta has unique moves:

- add its level-up table in the configured generation file;
- add teachable moves to `src/data/pokemon/all_learnables.json` when the helper is enabled;
- add a unique egg-move table if needed;
- link the new table names in `SpeciesInfo`.

Do not manually edit generated teachable output while `P_LEARNSET_HELPER_TEACHABLE` is enabled.

### 7.7 Add evolution and acquisition

Define the evolution in `SpeciesInfo`, for example:

```c
.evolutions = EVOLUTION({EVO_LEVEL, 20, SPECIES_KIRLIA_DELTA_FIRE}),
```

Then make the species obtainable through the appropriate content surface:

- starter table;
- wild encounters;
- gift script;
- map object event;
- trainer party;
- evolution from another species.

Project Holon's Fire starter is selected in `src/starter_choose.c`:

```c
#define FIRE_STARTER (IS_FRLG ? SPECIES_CHARMANDER : SPECIES_RALTS_DELTA_FIRE)
```

The species existing in data is not enough; it must have an acquisition path to be testable in ordinary play.

---

## 8. Build and Test Matrix

Run the narrowest check first, then the full build:

```bash
python3 tools/sprite_helpers/generate_ralts_delta_fire.py
make -j4
```

Do not edit files under `build/assets/`. They are generated from the source PNG and PAL files.

### 8.1 Debug-menu testing

A normal development build enables the overworld debug menu. Hold **R** and press **START**, then use:

```text
Give X… → Pokémon (Complex)
```

Select the custom species and set `Shiny: TRUE` when testing shiny palettes. Put the Pokémon in the first non-fainted party slot to test its follower palette.

The sprite visualizer is available by pressing **SELECT** on a Pokémon's summary screen in development builds. Use it to inspect positioning and animation without repeatedly entering battles.

### 8.2 Required visual cases

| Surface | Normal | Shiny | What to check |
| --- | --- | --- | --- |
| Front battle | Yes | Yes | Both frames, palette, effect placement, grounding |
| Back battle | Yes | Yes | Hand/effect occlusion and battle alignment |
| Summary sprite | Yes | Yes | Palette selection and animation |
| Party icon | Yes | Same standard icon | Shared icon palette and silhouette |
| Follower | Yes | Yes | All directions/steps and correct palette switching |
| Pokédex | Yes | If supported by view | Entry, ordering, height/weight display |
| Evolution | Yes | Yes | Target species and retained shininess |

Also test a clean save when species constants, Pokédex counts, starter logic, or acquisition scripts change.

---

## 9. Common Failure Modes

### The sprite looks right in an editor but builds incorrectly

Cause: the file was exported as RGB/RGBA or has more than 16 indices.

Fix: reopen it as indexed, preserve index 0 transparency, and let generator validation reject the wrong mode.

### The shiny battle sprite does not change

Cause: `.shinyPalette` is missing, points to the base species, or the normal and shiny palette files are identical.

Fix: inspect the `SpeciesInfo` links and the generated JASC palettes.

### The shiny follower does not change

Cause: the overworld shiny palette is not declared or not passed to `OVERWORLD(...)`, or the tested party Pokémon is not actually shiny.

Fix: give a shiny Pokémon through the complex debug giver and put it in the first healthy party slot.

### The icon colors are wrong

Cause: the icon was designed for the battle palette instead of a shared icon palette, or `.iconPalIndex` does not match the remap.

Fix: choose one of the six icon palettes and remap the image indices to that palette.

### An effect looks like an extra limb

Cause: the overlay overwrote canonical anatomy or added body-colored pixels to connect itself.

Fix: restart from the canonical source, remove invented body pixels, anchor the effect to existing anatomy, and use a transparency check to place it behind the hand when appropriate.

### The effect moves between animation frames

Cause: each frame was edited independently.

Fix: define one local coordinate map and apply it with a frame offset.

### Re-running the generator changes the sprite again

Cause: the script reads its previous output rather than the canonical source.

Fix: make every generation function open the base species asset fresh.

### The species appears as another Pokémon on an old save

Cause: a new species constant was inserted before existing released custom constants.

Fix: append new species and preserve numeric IDs once saves depend on them.

---

## 10. Case Study: Grass-type Dratini δ

Dratini δ extended the pipeline from a small added effect to a bounded transformation of existing anatomy. The species and starter path already existed, but its `SpeciesInfo` reused ordinary Dratini graphics. The completed pass gave it a standalone asset folder and redirected every visual surface to Delta-owned assets.

The implementation is generated by:

```text
tools/sprite_helpers/generate_dratini_delta_grass.py
```

from canonical inputs under:

```text
graphics/pokemon/dratini/
```

and produces:

```text
graphics/pokemon/dratini_delta_grass/
```

No external illustration or TCG artwork was used as a visual source. The canonical GBA Dratini assets are the sole anatomical and pixel-geometry authority.

### 10.1 Design contract

The approved concept treats Dratini as an ordinary Pokémon changed by Delta transformation rather than a naturally occurring regional adaptation:

- preserve Dratini's complete canonical silhouette, pose, facial structure, belly, and tail;
- render the normal body as tropical emerald with a pale lime-cream underside;
- transform the existing head fins into coral tropical flowers with gold centers;
- keep every petal inside the canonical fin silhouette rather than growing new anatomy;
- use the eye's existing accent slot for the same gold used by the flower centers;
- render the shiny as a nocturnal tropical counterpart with a blue-violet body, aqua underside, moon-white and icy-blue flowers, and hot-pink centers;
- carry the flower transformation into the icon and follower because it is anatomy, not a temporary held effect;
- omit tiny flower-center pixels from the follower because they become noise at native 32x32 scale;
- copy the canonical footprint unchanged.

This differs from Ralts δ's flame treatment. The Ralts flame is a separate effect and is intentionally absent from its icon and follower. Dratini's flowers replace transformed fin tissue, so their simplified color identity must remain visible on every character surface.

### 10.2 Per-surface transformation

| Surface | Canonical source | Deterministic method | Runtime color handling |
| --- | --- | --- | --- |
| Front battle | `anim_front_gba.png` | Frame-local flower boxes remap only fin indices; explicit coordinates add gold centers in both stacked frames | `normal.pal` / `shiny.pal` |
| Back battle | `back_gba.png` | Two bounded fin regions use the same petal remap; explicit center coordinates remain on canonical fin pixels | `normal.pal` / `shiny.pal` |
| Icon | `icon_gba.png` | Global body-index remap plus bounded flower regions and one-pixel centers | Shared icon palette 4; `.iconPalIndex = 4` |
| Follower | `overworld.png` | Six frame-local boxes recolor only canonical fin-interior indices; centers are intentionally omitted | `overworld_normal.pal` / `overworld_shiny.pal` |
| Footprint | `footprint.png` | Exact file copy | Unchanged |

The front and back share one semantic index plan. Indices 1–4 remain the underside ramp, 5–8 become the flower ramp, index 10 is the flower-center and eye accent, indices 11–14 remain the body ramp, and index 15 remains the outline. Normal and shiny palettes assign different colors to those same roles, so no second shiny PNG is needed.

The follower has its own semantic palette because its canonical sheet uses a different index layout. New flower colors occupy previously unused follower slots while the generated PNG continues to serve both normal and shiny palettes.

### 10.3 Engine integration

Standalone declarations were added for:

- `gMonFrontPic_DratiniDeltaGrass`;
- `gMonPalette_DratiniDeltaGrass`;
- `gMonBackPic_DratiniDeltaGrass`;
- `gMonShinyPalette_DratiniDeltaGrass`;
- `gMonIcon_DratiniDeltaGrass`;
- `gMonFootprint_DratiniDeltaGrass`;
- `gObjectEventPic_DratiniDeltaGrass`;
- `gOverworldPalette_DratiniDeltaGrass`;
- `gShinyOverworldPalette_DratiniDeltaGrass`.

The follower table uses `sPicTable_DratiniDeltaGrass`, and `SPECIES_DRATINI_DELTA_GRASS` now points to the standalone battle, icon, footprint, follower, and palette symbols. Its existing stats, Grass typing, cry, learnsets, evolution, and starter acquisition path were not changed during the art pass.

The completed asset set passed `gbagfx` conversion and a full `make -j4` ROM build.

### 10.4 Lessons from Dratini δ

1. **Transform an existing feature before adding a new one.** Dratini's three-point fins already supplied a flower-like outline. Recoloring their internal pixels produced a clearer result than attaching new blossoms and guaranteed silhouette preservation.
2. **Combine spatial and semantic constraints.** A bounding box alone can catch adjacent muzzle, belly, or body pixels. The generator changes a pixel only when it is both inside the approved region and uses an approved source index.
3. **Use frame-local coordinates.** Front animation and follower edits are easier to review when coordinates are defined relative to a 64x64 or 32x32 frame and the generator supplies the sheet offset.
4. **Give each surface an appropriate detail budget.** Battle sprites can support multi-tone petals and explicit centers. The icon can support one-pixel centers. The follower reads better with a simplified flower ramp and no center pixels.
5. **Design normal and shiny palettes around semantic slots.** Planning both palettes before integration prevented the shiny from requiring separate geometry or a second PNG.
6. **Validate exact change sets, not only allowed subsets.** The generator computes every expected changed coordinate and requires equality with the actual changes. This catches both accidental edits and missing intended edits.
7. **Validate the silhouette independently.** Comparing the complete nontransparent masks detects any accidental growth, erosion, or transparency change even when a coordinate lies inside an approved box.
8. **Verify embedded and runtime palettes agree.** The generator checks that front, back, and follower PNGs embed their normal palettes and that the icon embeds the same shared palette selected by `iconPalIndex`.
9. **Consolidate prototypes into one authoritative generator.** A front-only prototype is useful for approving a design, but the production pass should replace it with one script that recreates the entire species folder and validates all surfaces together.
10. **Visual review and technical validation answer different questions.** Exact-coordinate checks prove provenance and format safety; integer-zoom and native-scale review determine whether the flowers actually read as flowers.

---

## 11. Reusable Checklist

### Design

- [ ] Decide base species, Delta type, and visual identity.
- [ ] Define allowed palette and geometry changes.
- [ ] Decide front/back effect placement and occlusion.
- [ ] Decide whether icon and overworld receive the effect.
- [ ] Design normal and shiny palettes together.

### Deterministic assets

- [ ] Create a peer folder under `graphics/pokemon/<delta_name>/`.
- [ ] Add a generator under `tools/sprite_helpers/`.
- [ ] Read only canonical source assets.
- [ ] Declare all palettes and coordinate maps in the generator.
- [ ] Preserve indexed mode, index 0 transparency, and dimensions.
- [ ] Generate battle, icon, follower, footprint, and palette sources.
- [ ] Validate palette indices and sizes.
- [ ] Confirm two consecutive runs are identical.
- [ ] Review at integer zoom and at 1x follower size.

### Species integration

- [ ] Append `SPECIES_*` without renumbering released custom species.
- [ ] Add `NATIONAL_DEX_*`, counts, and regional ordering as needed.
- [ ] Add alphabetical, height, and weight Pokédex orders.
- [ ] Declare front, back, palettes, icon, footprint, follower, and follower palettes.
- [ ] Add the follower frame table.
- [ ] Add or audit the complete `SpeciesInfo` entry.
- [ ] Add/reuse cry, learnsets, egg moves, and evolution deliberately.
- [ ] Add an acquisition method.

### Validation

- [ ] Run the generator.
- [ ] Build the full ROM.
- [ ] Test normal front and back.
- [ ] Test shiny front and back.
- [ ] Test icon palette.
- [ ] Test normal and shiny follower palettes.
- [ ] Test Pokédex entry and sorting.
- [ ] Test evolution and acquisition.
- [ ] Confirm unrelated canonical assets remain unchanged.

---

## 12. Definition of Done

A deterministic Delta Pokémon is complete when:

1. Its generated assets can be deleted and recreated from the script without manual repair.
2. The canonical species folder is untouched.
3. Every changed pixel is explained by a palette transformation or bounded coordinate rule.
4. Normal and shiny battle palettes work.
5. The icon uses the selected shared icon palette correctly.
6. Normal and shiny follower palettes work across every frame.
7. The species owns stable constants, data, graphics declarations, Pokédex placement, and an acquisition path.
8. The ROM builds successfully.
9. Debug-menu and in-game inspection show no alignment, silhouette, palette, or animation regressions.

The key discipline is simple: preserve the canonical sprite as the anatomical source of truth, express the Delta identity as reviewable data, and make the engine wiring as standalone as the species itself.

---

## Sources

- RHH, [How to add a new Pokémon](https://rh-hideout.github.io/pokeemerald-expansion/tutorials/how_to_new_pokemon.html), current tutorial for expansion 1.7.x onward and direct `SpeciesInfo` animation data in 1.11.0 onward.
- Project Holon local expansion documentation, [`docs/tutorials/how_to_new_pokemon.md`](../../docs/tutorials/how_to_new_pokemon.md).
- Project Holon implementation, [`tools/sprite_helpers/generate_ralts_delta_fire.py`](../../tools/sprite_helpers/generate_ralts_delta_fire.py).
- Project Holon implementation, [`tools/sprite_helpers/generate_dratini_delta_grass.py`](../../tools/sprite_helpers/generate_dratini_delta_grass.py).

## Changelog

| Version | Date | Changes |
| --- | --- | --- |
| 1.1 | 2026-09-02 | Added the Grass-type Dratini δ case study, including tropical flower-fin design, full asset integration, exact change-set validation, and production lessons. |
| 1.0 | 2026-08-31 | Initial reusable pipeline based on the Ralts δ Fire implementation and its sprite-placement iterations. |
