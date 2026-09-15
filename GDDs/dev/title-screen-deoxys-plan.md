# Title Screen Rework — Illuminated Deoxys + DNA Helix

Implementation plan. Builds on `GDDs/dev/title-screen-customization-tutorial.md` (asset pipeline)
and the stock Emerald flow in `src/title_screen.c` / `src/intro.c`.

## Locked decisions

| Topic | Decision |
| --- | --- |
| Background subject | **Deoxys, Normal Forme, front-facing, large** — symmetrical, centered, bleeds off top and bottom (like the Pokémon Pisces reference). |
| Glow | **Psychic violet ↔ cyan** pulse on the animated palette entry. |
| Overlay layer (BG1) | **DNA double helix**, scrolls upward forever + reuses the existing horizontal scanline sine so the strands appear to twist/rotate. |
| Copyright / boot screen | **Full replace, single line:** `POD OF WAILMERS - alpha0.1`. Drops the Nintendo/GF legal notice (matches Pisces). Static art, hand-edited per release. |
| Subtitle banner | Redraw `EMERALD VERSION` → stacked 2-line **`HOLON LEGENDS`** wordmark with a heavy dark outline. Same 128×32 / two-64×32-sprite footprint (no code change). *Assumption from mockups 07/08/11 — confirm the game name.* |
| Deoxys motion | **Static silhouette** for v1. Life comes from the pulsing glow + moving helix. Real floating motion is a later, optional phase. |

## How the effect works (reference)

The stock Rayquaza scene is the exact template:

- **BG0** = static 4bpp silhouette tile sheet (`rayquaza.png` + `rayquaza.bin`), drawn with shared BG **palette slot 14**. Loaded at `title_screen.c:602-603`, `BG_CHAR_ADDR(2)` / `BG_SCREEN_ADDR(26)`, priority 3 (backmost). 512-tile / 16,384-byte budget.
- **Glow** = `UpdateLegendaryMarkingColor()` (`title_screen.c:861-873`) rewrites **one** entry — `BG_PLTT_ID(14) + 15` — every 4th frame on a `Cos` curve. The silhouette art paints its glowing bits with palette index 15.
- **BG1** = overlay tile sheet (`clouds.png` + `clouds.bin`), also palette slot 14, priority 2 (in front of BG0, behind logo). Vertical scroll via `tBg1Y` in `Task_TitleScreenPhase3` (`title_screen.c:813-818`); per-scanline horizontal sine from `ScanlineEffect_InitWave(..., SCANLINE_EFFECT_REG_BG1HOFS, TRUE)` at `title_screen.c:667`.
- **BG2** = affine Pokémon logo, priority 1. **OBJ** = version banner, PRESS START, logo shine.

All three BG lanes are occupied — new elements must reuse a lane.

## Shared 16-color palette budget (`rayquaza_and_clouds.pal`, slot 14)

BG0 (Deoxys + backdrop) and BG1 (helix) must share these 16 entries in the same order.

| Idx | Role | Used by |
| --- | --- | --- |
| 0 | Transparent (shows backdrop color — keep near-black; minimize index-0 pixels in the art) | both |
| 1–3 | Blue vertical backdrop gradient (dark → mid) | BG0 |
| 4–8 | Deoxys body shading, deep violet → near-black (5 steps) | BG0 |
| 9 | Body rim / ambient edge light | BG0 |
| 10–12 | Helix strand + rungs (3 steps) | BG1 |
| 13 | Helix highlight / sparkle | BG1 |
| 14 | Secondary **steady** glow — cyan (core ring, eye) — set once from the .pal, never animated | BG0 |
| 15 | Primary **animated** glow — violet ↔ cyan pulse (Deoxys core, chest facet, tendril tips) | BG0 (+ optional helix accent) |

If 3 backdrop shades band too hard, borrow one from the body ramp (4 steps is plenty for a silhouette).

---

## Phase 1 — Art + trivial constants (fully reversible, no engine work)

### 1.1 Deoxys silhouette → replaces BG0

1. Author `art/title_screen_masters/deoxys_bg.png`: **256×256 indexed**, composition in the **top-left 240×160**, right 16px + bottom 96px filled with index 0.
   - Blue gradient backdrop (idx 1–3), large front-facing Normal Forme Deoxys in dark violet/black (idx 0,4–9), glow pixels on **idx 15** (core, chest facet, tendril tips) and **idx 14** (core ring, eyes).
   - Symmetric pose → rely on horizontal tile mirroring to stay ≤ 512 unique tiles.
2. Convert with the grit recipe from the tutorial (Part 2.3), targeting palette **E (14)**:
   - image data ≤ 16,384 bytes, map exactly 2,048 bytes.
3. Drop results over `graphics/title_screen/rayquaza.png` + `rayquaza.bin`; regenerate `graphics/title_screen/rayquaza_and_clouds.pal` from the new sheet.
4. No code change — BG0 wiring is subject-agnostic.

### 1.2 DNA double-helix → replaces BG1 (`clouds`)

1. Author `art/title_screen_masters/helix_overlay.png`: **256×256 indexed**, **same 16-color palette, same order** as 1.1.
   - 2–3 faint vertical double-helix strands spanning the full height, built as a short **vertically tiling** segment repeated down the map (cheap tile count). Rungs on idx 12–13, strands idx 10–11, occasional idx-13 sparkle in the gaps.
   - Index 0 everywhere the silhouette must show through.
   - Design the segment so its top edge matches its bottom edge → seamless infinite upward scroll.
2. Convert to 4bpp tiles + tilemap, palette E, same size limits as BG0 (BG1 char block is also `0x4000` at `BG_CHAR_ADDR(3)`).
3. Drop over `graphics/title_screen/clouds.png` + `clouds.bin`.
4. No code change — the existing `tBg1Y` scroll + `ScanlineEffect_InitWave` already produce "scroll up + twist". Amplitude/speed tuning is Phase 2.

### 1.3 Glow color → `UpdateLegendaryMarkingColor` (`src/title_screen.c:861`)

Swap the red/gold curve for violet ↔ cyan. Sketch:

```c
static void UpdateLegendaryMarkingColor(u8 frameNum)
{
    if ((frameNum % 4) == 0)
    {
        s32 t = Cos(frameNum, Q_8_8(0.5)) + Q_8_8(0.5); // 0..1 pulse
        u32 r = 12 + Q_8_8_TO_INT(t * 12);   // violet has red; cyan doesn't
        u32 g = 18 + Q_8_8_TO_INT(t * 13);   // cyan is green-heavy
        u32 b = 31;                          // both endpoints are blue-max
        u16 color = RGB(r, g, b);
        LoadPalette(&color, BG_PLTT_ID(14) + 15, sizeof(color));
    }
}
```

Tune the constants against the actual art in mGBA. Index 14 (steady cyan) needs no code — it just lives in the .pal.

### 1.4 Subtitle → `emerald_version.png`

- Redraw the existing **128×32**, ≤16-color indexed PNG as a stacked `HOLON` / `LEGENDS` wordmark, heavy near-black outline, glow-friendly palette.
- Keep index 0 transparent, keep it splitting cleanly at the 64px seam.
- No `.pal` edit (generated from the PNG). No code change — `VERSION_BANNER_LEFT_X 88` / `RIGHT_X 152` are already centered on 120.

### 1.5 Copyright / boot screen → `graphics/intro/copyright.png`

Currently a **312×8** 4bpp strip + `copyright.bin` (32×32 tilemap that positions/centers it). Shown at cold boot **and** after the title (`SetUpCopyrightScreen`, `src/intro.c:1052`; `LoadCopyrightGraphics`, `intro.c:1040`).

1. Redraw `graphics/intro/copyright.png` as a single 8px-tall strip reading `POD OF WAILMERS - alpha0.1` (width a multiple of 8, ≤15 colors + index 0).
2. If the tile count changes, rebuild `copyright.bin` (Tilemap Studio, or regenerate) so the strip stays centered near the bottom; otherwise leave the tilemap.
3. No code change. Bump the `alpha0.1` text by hand per release.
   *(Prefixing `©` or a year is a free art tweak if wanted — current spec is the literal string above.)*

### 1.6 Build & verify

```bash
make -j8            # -> pokeemerald.gba
```

Checklist in mGBA (watch the whole sequence, and test pressing A early to skip):

- Deoxys reconstructs correctly (not scrambled tiles), transparent where the logo/helix should show.
- Glow pulses violet↔cyan on the core/facets only; index-0 backdrop never flashes an unintended color during the logo shine.
- Helix scrolls upward seamlessly (no visible segment seam) and twists with the scanline wave.
- Subtitle halves meet with no seam; slides to `VERSION_BANNER_Y_GOAL 70`.
- PRESS START + `POD OF WAILMERS - alpha0.1` legible; copyright line correct at cold boot and post-title.
- A / Start still reaches the main menu; the "no input" timeout still fades to the copyright screen.

### 1.7 Rollback

`git checkout master -- graphics/title_screen/ graphics/intro/copyright.* src/title_screen.c` then `make clean-assets && make`.

---

## Phase 2 — Motion & polish (small code, after Phase 1 looks right)

- **Helix tuning:** raise the `ScanlineEffect_InitWave` amplitude arg (`title_screen.c:667`) and/or the `tBg1Y` step (`title_screen.c:815`) for a stronger twist / faster rise.
- **Multi-index shimmer:** extend `UpdateLegendaryMarkingColor` to also drive idx 13–14 with a phase offset so the glow ripples across the core instead of pulsing flat.
- **Heat-haze on Deoxys:** add a gentle per-scanline sine on `REG_OFFSET_BG0HOFS` (BG1 owns `BG1HOFS`; BG0HOFS is free) so the silhouette itself shimmers.
- **Slow float:** ease `BG0VOFS` a few px on a long sine in `Task_TitleScreenPhase3`.
- **Banner glow:** give the subtitle its own pulsing palette entry, or a `StartPokemonLogoShine` pass on reveal.

## Phase 3 — Optional: actually-moving Deoxys

BG0 can't be affine in mode 1 (only BG2 is). Real float-bob / forme-shimmer means a **sprite-based Deoxys**: a set of 64×64 OBJ frames with anim tables, spawned in `Task_TitleScreenPhase2/3`, costing OBJ VRAM + one sprite-palette slot. Its own task; only pursue if the static silhouette reads as too flat.

## Open confirmations

1. **Game name on the subtitle** — plan assumes `HOLON LEGENDS` (mockups). Confirm vs. any newer title.
2. Copyright string is exactly `POD OF WAILMERS - alpha0.1` (no `©`, no year) — confirm or adjust.
