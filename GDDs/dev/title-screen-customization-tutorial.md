# Customizing the Emerald Title Screen

This tutorial explains how to replace the game title and background on Project Holon's Emerald title screen. It is written for this repository's current `pokeemerald-expansion` layout.

> This guide applies to the default Emerald build (`make`). FireRed and LeafGreen use a different implementation in `src/title_screen_frlg.c` and assets under `graphics/title_screen_frlg/`.

## What the title screen is made of

The title screen is not a single 240x160 image. The GBA composes it from background layers and sprites:

| Visible element | Source asset | Format and current size | Runtime layer |
| --- | --- | --- | --- |
| Large Pokémon logo | `graphics/title_screen/pokemon_logo.png` and `.pal` | 8bpp indexed, 256x64 | BG2 |
| `EMERALD VERSION` subtitle | `graphics/title_screen/emerald_version.png` | 8bpp sprite using 16 colors, 128x32 | Two 64x32 OBJ sprites |
| Rayquaza artwork | `graphics/title_screen/rayquaza.png` and `.bin` | 4bpp tile sheet, currently 128x128 | BG0 |
| Moving clouds | `graphics/title_screen/clouds.png` and `.bin` | 4bpp tile sheet, currently 128x56 | BG1 |
| `PRESS START` and copyright | `graphics/title_screen/press_start.png` | 4bpp sprite strip, 160x24 | OBJ sprites |
| Shine mask | `graphics/title_screen/logo_shine.png` | 4bpp, 64x64 | OBJ-window sprite |

The most important distinction is between an image and a tile sheet. `pokemon_logo.png` and `emerald_version.png` can be replaced directly if their dimensions and palette constraints stay the same. `rayquaza.png` and `clouds.png` are tile sheets whose tiles are arranged on screen by their matching `.bin` tilemaps. A brand-new background therefore needs both new tiles and a new tilemap.

The relevant code is split between:

- `src/graphics.c`, which includes the graphics in the ROM.
- `src/title_screen.c`, which loads the layers and controls their animation, position, visibility, and timing.
- `graphics_file_rules.mk`, which converts `pokemon_logo.pal` to a 224-color GBA palette.

## Before editing

Create a working branch and keep master copies of your art outside `graphics/title_screen/`. The PNG placed in that folder may be a generated tile sheet rather than the original full-screen composition.

```bash
git switch -c art/custom-title-screen
mkdir -p art/title_screen_masters
```

Do not hand-edit generated files such as `.4bpp`, `.8bpp`, `.gbapal`, `.smol`, or `.smolTM`. The build recreates those from the source PNG, PAL, and BIN files.

Useful GBA constraints:

- The visible screen is 240x160 pixels.
- Tile backgrounds use 8x8-pixel tiles.
- 4bpp artwork has 16 palette entries. Palette index 0 is transparent on a background layer, leaving 15 normally visible colors.
- The GBA stores colors at 5 bits per RGB channel, so colors may shift slightly after conversion.
- Resize pixel art with nearest-neighbor sampling. Anti-aliasing creates unwanted colors.
- Export genuine indexed-color PNGs, not RGB/RGBA PNGs that merely look low-color.

## Part 1: Replace the game title

The stock title is two assets: the large Pokémon logo and the smaller `EMERALD VERSION` banner. They can be customized independently.

### 1. Replace the large logo

1. Open `graphics/title_screen/pokemon_logo.png` in an indexed-color editor.
2. Keep the canvas exactly 256x64 pixels.
3. Draw or paste the new logo. Keep every used palette index between 0 and 223; the build deliberately loads only 224 colors from this asset.
4. Keep palette index 0 as the transparent/background color.
5. Export over `graphics/title_screen/pokemon_logo.png` as an indexed PNG.
6. Regenerate the source JASC palette from the PNG:

```bash
tools/gbagfx/gbagfx \
  graphics/title_screen/pokemon_logo.png \
  graphics/title_screen/pokemon_logo.pal
```

The existing `pokemon_logo.bin` is a sequential affine tilemap for the fixed 256x64 canvas, so it does not need to change when the replacement remains that size.

Why the 224-color limit exists: the title screen loads the logo into background palette entries 0-223, then loads the shared Rayquaza/cloud palette into entries 224-239. Using logo indices 224-255 would collide with palettes reserved by the rest of the scene.

### 2. Replace the subtitle

1. Open `graphics/title_screen/emerald_version.png`.
2. Keep the canvas exactly 128x32 pixels.
3. Use no more than 16 indexed palette entries, with transparent pixels assigned to palette index 0.
4. Replace the wording with the game's subtitle—for example, `HOLON LEGENDS`—and export over the same file as an indexed PNG.

No separate `.pal` source needs editing for this asset. `src/graphics.c` generates `emerald_version.gbapal` directly from the PNG.

Do not change the dimensions unless you also rewrite the OBJ setup. The code splits this image into two 64x32, 8bpp sprites and expects exactly `0x1000` bytes of uncompressed graphics.

### 3. Reposition the subtitle if needed

The subtitle's final placement is controlled near the top of `src/title_screen.c`:

```c
#define VERSION_BANNER_LEFT_X 98
#define VERSION_BANNER_RIGHT_X 162
#define VERSION_BANNER_Y_GOAL 66
```

The X values are the centers of the left and right 64x32 halves. Keep them 64 pixels apart unless the sprite layout is intentionally being changed. Increase Y to move the banner down; decrease it to move the banner up.

The initial `VERSION_BANNER_Y` value controls where the slide-in animation begins.

## Part 2: Replace the background with one custom image

The cleanest static-background workflow is to repurpose the existing Rayquaza BG0 layer, generate a new 4bpp tile sheet and tilemap, and stop displaying the cloud BG1 layer.

### 1. Prepare a background master

Create `art/title_screen_masters/background.png` with these properties:

- Canvas: 256x256 pixels.
- Visible composition: the upper-left 240x160 pixels.
- Unused right 16 pixels and bottom 96 pixels: fill with the transparent/index-0 color.
- Color mode: indexed.
- Palette: no more than 16 entries total.
- Visible pixels: preferably use indices 1-15. Pixels using index 0 reveal the backdrop color and can be affected by the logo-shine flash.

The 256x256 canvas matches a 32x32 regular GBA tilemap. Keeping the art in the upper-left is important because the game displays that portion of BG0 without an offset.

For the most dependable result, simplify gradients and textured areas. A single 4bpp character block can hold at most 512 unique 8x8 tiles. Repeated and mirrored tiles reduce the count; a noisy or dithered full-screen image can exceed it.

### 2. Convert the image in Tilemap Studio

Project Holon's existing map-preview tutorial describes the same general Image-to-Tiles workflow in `docs/tutorials/how_to_map_preview_screen.md`. In Tilemap Studio:

1. Open the 256x256 background master.
2. Use **Tools → Image to Tiles**.
3. Select **GBA 4bpp** tiles and a **regular/text background** tilemap, not an affine map.
4. Enable duplicate-tile removal and horizontal/vertical flip matching.
5. Export the tile sheet as an indexed PNG and the map as a binary GBA tilemap.
6. Open the generated map and assign every used map entry to palette **E** (hexadecimal E, decimal 14).
7. Confirm the generated tile sheet contains no more than 512 tiles.

Palette E is mandatory with the current loader: `gTitleScreenBgPalettes` places the shared background palette in slot 14. A tilemap that still points at palette 0 will borrow colors from the logo and look corrupted.

Copy the generated files into place:

```bash
cp path/to/generated_tiles.png graphics/title_screen/rayquaza.png
cp path/to/generated_tilemap.bin graphics/title_screen/rayquaza.bin
```

Then derive the shared 16-color palette from the new tile sheet:

```bash
tools/gbagfx/gbagfx \
  graphics/title_screen/rayquaza.png \
  graphics/title_screen/rayquaza_and_clouds.pal
```

The generated tile sheet does not have to remain 128x128. Its width and height must be multiples of 8, and its total tile count must be 512 or fewer.

### 3. Command-line conversion alternative

The repository's devkitPro installation includes `grit`, so the tiles, reduced map, and palette can also be generated from the 256x256 master without Tilemap Studio. Run this from the repository root:

```bash
work_dir=$(mktemp -d /tmp/holon-title-bg.XXXXXX)

grit art/title_screen_masters/background.png \
  -gB4 -mRtpf -mLs -mp14 -pT0 \
  -ftb -fh! -o"$work_dir/generated"

cp "$work_dir/generated.img.bin" "$work_dir/rayquaza.4bpp"
cp "$work_dir/generated.pal.bin" "$work_dir/rayquaza.gbapal"

tools/gbagfx/gbagfx \
  "$work_dir/rayquaza.4bpp" \
  graphics/title_screen/rayquaza.png \
  -palette "$work_dir/rayquaza.gbapal" -width 1

tools/gbagfx/gbagfx \
  "$work_dir/rayquaza.gbapal" \
  graphics/title_screen/rayquaza_and_clouds.pal

cp "$work_dir/generated.map.bin" graphics/title_screen/rayquaza.bin
```

The deliberately narrow generated `rayquaza.png` is a tile sheet, not a preview of the finished scene. The tilemap reconstructs the original composition in-game. Keep the readable 256x256 master under `art/title_screen_masters/` for future edits.

Check the generated sizes before building:

```bash
wc -c "$work_dir/generated.img.bin" "$work_dir/generated.map.bin"
```

- The image data must be no larger than 16,384 bytes (512 4bpp tiles).
- The regular 32x32 map must be exactly 2,048 bytes.

If the image data is too large, reduce visual noise, remove dithering, reuse more 8x8 patterns, or mirror repeated shapes.

### 4. Disable the old cloud overlay

In `Task_TitleScreenPhase2` in `src/title_screen.c`, find the `REG_OFFSET_DISPCNT` setup and remove `DISPCNT_BG1_ON`:

```diff
 SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_1
                             | DISPCNT_OBJ_1D_MAP
                             | DISPCNT_BG0_ON
-                            | DISPCNT_BG1_ON
                             | DISPCNT_BG2_ON
                             | DISPCNT_OBJ_ON);
```

This keeps the custom BG0 background and logo BG2 visible but prevents the original scrolling clouds from drawing over the new art. It is safe to leave the old cloud assets and update logic in place; with BG1 disabled, they are not visible.

By default, BG0 appears only when the title animation reaches phase 2, matching the original late Rayquaza reveal. To show the background from the beginning, also add `DISPCNT_BG0_ON` to the display-control setup in state 4 of `CB2_InitTitleScreen`:

```diff
 SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_1
                             | DISPCNT_OBJ_1D_MAP
+                            | DISPCNT_BG0_ON
                             | DISPCNT_BG2_ON
                             | DISPCNT_OBJ_ON
                             | DISPCNT_WIN0_ON
                             | DISPCNT_OBJWIN_ON);
```

Choose only one timing intentionally:

- Leave state 4 unchanged for the original delayed background reveal.
- Add BG0 there for a background that is visible throughout the logo animation.

## Part 3: Keep a two-layer animated background

If moving clouds, fog, particles, or another overlay suit the design, keep BG1 enabled and replace both background layers instead of disabling it.

The two layers must share the same 16-color `rayquaza_and_clouds.pal`:

- BG0: `rayquaza.png` plus `rayquaza.bin`.
- BG1: `clouds.png` plus `clouds.bin`.

Generate both tilemaps with palette E. Reserve index 0 as transparent in the overlay so BG0 shows through it. Both tile sheets must use exactly the same palette entries in the same order.

BG1 receives a moving vertical offset and a horizontal scanline wave. The key locations in `src/title_screen.c` are:

- `ScanlineEffect_InitWave(...)` starts the wave after the first fade-in.
- `REG_OFFSET_BG1VOFS` is updated during VBlank.
- `tBg1Y` advances the vertical scroll in `Task_TitleScreenPhase3`.

For a stationary overlay, keep BG1 enabled but remove the `ScanlineEffect_InitWave(...)` call and stop incrementing `tBg1Y`. For a different motion, change those values gradually and test on hardware-accurate timing in mGBA.

## Part 4: Build and test

Build the Emerald ROM:

```bash
make -j8
```

The output is `pokeemerald.gba`. Boot it in mGBA and watch the entire title sequence, not just the final frame. Test both normal timing and pressing A early to skip the animation.

Use this visual checklist:

- The large logo has the correct colors and transparent background.
- The subtitle's two halves meet without a seam.
- The subtitle slides to the intended Y position.
- The background reconstructs correctly instead of showing scrambled tiles.
- No original clouds remain if BG1 was disabled.
- `PRESS START` and copyright remain legible.
- The logo shine does not expose an unintended index-0 color.
- Pressing A or Start still reaches the main menu.

Inspect only the relevant source changes:

```bash
git diff -- \
  graphics/title_screen/pokemon_logo.png \
  graphics/title_screen/pokemon_logo.pal \
  graphics/title_screen/emerald_version.png \
  graphics/title_screen/rayquaza.png \
  graphics/title_screen/rayquaza.bin \
  graphics/title_screen/rayquaza_and_clouds.pal \
  src/title_screen.c
```

## Troubleshooting

### `Image does not contain a palette`

The PNG was exported as RGB or RGBA. Convert the document to indexed mode and export it again. Reducing the visible color count is not enough; the file itself must contain a PNG palette.

### The background has the logo's colors

The background tilemap points at palette 0 instead of palette E. Reopen the map and set its entries to palette 14, or regenerate it with grit's `-mp14` option.

### The background is scrambled

The tile sheet changed but the matching `.bin` tilemap did not, or they came from different conversion runs. Regenerate and replace them as a pair.

### The background is black or has holes

Visible pixels use palette index 0, which is transparent for BG0/BG1. Move the intended visible color to an index from 1 through 15 and remap those pixels.

### The build reports too many tiles or graphics overwrite other data

The BG0 tile sheet exceeded 512 unique 8x8 tiles (16,384 bytes at 4bpp). Reduce noise and dithering, simplify the image, or redesign repeated regions to share tiles.

### The subtitle colors are wrong

`emerald_version.png` has more than 16 meaningful colors or the transparent color is not palette index 0. Re-index it to one 16-entry palette.

### The large logo colors are wrong

Regenerate `pokemon_logo.pal` from the new PNG and confirm the image does not use palette indices 224-255.

### Make appears to reuse stale graphics

First rebuild normally after touching the source PNG/PAL/BIN. If an interrupted build left stale generated assets, run:

```bash
make clean-assets
make -j8
```

`make clean-assets` deletes generated graphics formats throughout the repository and recreates them on the next build. It does not delete source PNG, PAL, or BIN files, but it makes the following build take longer.

## Optional polish

Once the core replacement works, the same file offers several safe finishing controls:

- `START_BANNER_X` moves `PRESS START` and copyright horizontally.
- The `108` and `148` arguments passed to `CreatePressStartBanner` and `CreateCopyrightBanner` control their vertical positions.
- `MUS_TITLE` selects the title-screen song.
- `SHINE_SPEED` changes how quickly the shine travels across the large logo.
- `RGB(24, 31, 12)` in `SpriteCB_PokemonLogoShine` is the stock green flash color.

Change one behavior at a time and rebuild after each change. That keeps art, palette, tilemap, and animation problems easy to distinguish.
