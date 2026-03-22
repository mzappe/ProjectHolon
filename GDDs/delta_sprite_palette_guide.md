# Pokémon Holon Legends — Delta Species Sprite Palette Swapping Guide

A practical workflow for creating placeholder Delta Species sprites by recoloring existing Pokémon sprites in Pixelorama. Covers every step from opening the source sprite to dropping the finished file into the repo.

---

## Before You Start — Understanding the Constraints

The expansion's DS-style sprites are **indexed-color PNGs**. This is not the same as a regular photo or illustration. An indexed PNG does not store a color per pixel — it stores a **palette index** per pixel, and the palette is a separate list of up to 16 colors. Every pixel that shares a palette slot shares a color. Change the slot, and every pixel using it updates instantly.

This is what makes palette swapping fast and safe:
- You never paint over pixels
- You never risk misaligned edges or anti-aliasing artifacts
- The sprite structure is completely untouched — only the color table changes

**What this means for Pixelorama:** You must set the project to **Indexed** color mode when opening the sprite. In indexed mode, any color you pick from the color picker is automatically snapped to the nearest palette slot — you cannot paint colors that aren't in the palette. This is correct behavior, not a bug. The palette is your instrument.

---

## File Locations in the Repo

| Asset | Path |
|---|---|
| Front battle sprite | `graphics/pokemon/<SPECIES>/front.png` |
| Back battle sprite | `graphics/pokemon/<SPECIES>/back.png` |
| Icon sprite | `graphics/pokemon/<SPECIES>/icon.png` |
| Overworld follower sprite | `graphics/object_events/pics/pokemon/<species>.png` |

For a Delta, you will create a new species entry (e.g. `DELTA_CHARIZARD`) with its own folder. During placeholder phase, copy the base species sprites into that folder and recolor as needed.

---

## Step 1 — Open the Source Sprite in Indexed Mode

1. In Pixelorama: **File → Open** and navigate to the base species front sprite (e.g. `graphics/pokemon/CHARIZARD/front.png`)
2. An import dialog will appear. Before clicking OK, look for the color mode option and confirm it is set to **Indexed**. If it defaults to RGBA, change it to Indexed here — it is much easier to set this on import than to convert afterward.
3. Click OK to open the sprite.
4. Double-check the mode was applied: **Image menu → Color Mode** should show **Indexed** with a checkmark.

> **If you accidentally opened in RGBA:** Go to **Image → Color Mode → Indexed**. Pixelorama will convert the existing colors to the nearest palette equivalents. This usually works, but importing as Indexed from the start is cleaner and avoids any color drift.

---

## Step 2 — Load the Sprite's Palette

When you open a PNG with an embedded palette, Pixelorama may or may not automatically load that palette into the palette panel. Do the following to make sure you're working with the sprite's actual colors:

1. Open the **Palettes panel** — it should be visible by default on the right side of the UI. If not: **Window → Palettes**
2. At the top of the Palettes panel, click the **import palette** button (the folder/import icon)
3. Choose **Import palette from current sprite** — this extracts the colors directly from the open image and loads them as the active palette
4. You should now see a grid of color swatches matching the sprite's actual colors — typically 16 slots for a DS-style Pokémon sprite

This step is important. If the palette panel is showing Pixelorama's default colors rather than the sprite's colors, editing slots will not update the sprite correctly.

---

## Step 3 — Read the Palette Before Touching Anything

Spend 60 seconds identifying which slots do what before you change anything.

Click each palette swatch and look at the canvas to see which pixels use that color. You are looking for:

| Slot type | What to look for |
|---|---|
| **Primary body color** | The dominant hue — for Charizard, the main orange |
| **Shadow/dark variant** | The darker version of the primary — used for shading |
| **Highlight/light variant** | The lighter version — used for highlights and edges |
| **Accent color** | Wings, underbelly, markings — contrasting color |
| **Outline** | Usually near-black, used for the hard edges of the sprite |
| **Background/transparent** | Slot 0 is the transparent color — **never touch this slot** |

Write these down or mentally map them. You will target 3–5 slots for a typical Delta recolor.

---

## Step 4 — Plan Your Delta Recolor

Before opening the color picker, decide what you are communicating. The goal is immediate visual legibility — a player should see the sprite and think "that's not a normal Charizard" without reading any text.

**Effective Delta recolor strategy:**

Target the **primary body color and its shadow/highlight variants** as a group. These three slots define the dominant color identity of the sprite. Shift them together toward the hue of the Delta type.

**Type-to-hue reference:**

| Delta Type | Hue direction | Example shift |
|---|---|---|
| Lightning / Electric | Yellow, yellow-gold | Orange → yellow |
| Steel / Metal | Blue-grey, silver | Orange → cool grey |
| Fire (on non-Fire base) | Red-orange | Blue → red-orange |
| Water | Blue, teal | Orange → blue |
| Grass | Green, olive | Any → green |
| Psychic | Pink, purple | Any → pale purple |
| Dark / Darkness | Deep purple, charcoal | Any → dark purple |
| Fighting | Brick red, ochre | Any → warm brown-red |
| Dragon | Teal, indigo | Any → teal |

**Dual Metal rule:** Pokémon with a Metal secondary type at Holon typically gain a grey/silver quality somewhere in their palette — often on the accent color or a lighter body variant — to visually suggest the Metal secondary without changing the primary type hue completely.

---

## Step 5 — Edit Palette Slots

1. In the **Palettes panel**, double-click the swatch you want to change
2. The **color picker dialog** opens
3. Switch to **HSV mode** in the color picker if it isn't already showing HSV sliders — this is easier than RGB for type-based recoloring:
   - **H (Hue):** Rotates the color around the color wheel — this is your primary shift
   - **S (Saturation):** How vivid vs grey — Delta Pokémon often benefit from slightly reduced saturation to feel "altered"
   - **V (Value/Brightness):** Keep this close to the original value for each slot — shadows stay dark, highlights stay bright
4. Confirm the change. In indexed mode, every pixel using that palette slot updates on the canvas instantly.
5. Repeat for each related slot — primary, shadow, highlight — keeping their relative brightness relationships intact.

**Maintaining tonal coherence:**

If the original primary body color is H:25 S:90 V:85, and you shift H to 50 (yellow), then shift the shadow to H:50 S:90 V:55 and the highlight to H:50 S:60 V:95. Same hue, adjusted saturation and brightness to preserve the shading logic.

> **Note on undo:** Pixelorama does not always include palette slot edits in the undo history. Save a backup copy of the original PNG before you start, so you can re-import the palette from scratch if needed.

---

## Step 6 — Handle the Accent Color

The accent color (wings, belly, markings) is a decision point for Delta identity:

- **Leave it unchanged** if you want the original color to read as a "trace" of the base species — a Charizard δ with blue body but still orange wings creates a visually interesting contrast
- **Shift it to complement the new primary** for a more fully transformed look
- **Shift it toward grey/silver** if the species has a Metal secondary type

There is no wrong answer — this is a visual and lore-driven choice per species. Charizard δ as a Lightning/Metal type might have a yellow primary body with silver-shifted wings, which visually suggests both types without any text.

---

## Step 7 — Never Touch These Slots

| Slot | Why |
|---|---|
| **Slot 0 (transparent)** | Always the background/transparent color. Changing it corrupts the sprite's transparency and will cause visual bugs in-game |
| **Outline/near-black** | The hard edge outlines should stay dark and consistent. Changing them makes the sprite look unfinished and breaks visual cohesion across the whole roster |
| **Eye whites and pupils** | Small details that read as "face" — changing these makes sprites look uncanny |

---

## Step 8 — Export Correctly

Pixelorama's native save format is `.pxo`. **Do not use File → Save for repo files** — `.pxo` files are not valid game assets. You need to export as PNG.

1. **File → Export** (or File → Export As)
2. File format: **PNG**
3. Navigate to your Delta species folder in the repo (e.g. `graphics/pokemon/DELTA_CHARIZARD/`)
4. Filename: `front.png`
5. In the export options, confirm the output will be an **Indexed PNG** — ensure it is not converting to RGBA on export

**Keep your `.pxo` working files** in your `Assets-Source/Sprites/` directory outside the repo. If you need to adjust the palette later, reopen the `.pxo` rather than starting from the exported PNG — the `.pxo` preserves your palette panel state and editing history.

---

## Step 9 — Repeat for Back and Icon

The back sprite and icon use the same palette structure. Once you've worked out your color decisions on the front sprite, the back and icon are quick:

- Open the back sprite following the same steps (File → Open, confirm Indexed, import palette from sprite)
- Make the same slot changes, export as `back.png`
- Open the icon sprite — icons often have a simplified 2–4 color palette; just shift the dominant color slot
- Export as `icon.png`

---

## Step 10 — Verify In-Game

After exporting all three sprites (front, back, icon) and adding the species entry to the repo:

1. Rebuild: `make -j$(sysctl -n hw.ncpu)`
2. Open your test map in the emulator
3. Find the Delta Pokémon in battle and on the summary screen
4. Check: does the sprite read clearly as a Delta? Is the type visually legible?

If something looks wrong in-game but looked correct in Pixelorama, the most common cause is the PNG being exported as RGBA rather than indexed. Recheck the export settings and confirm the output is an indexed PNG — you can verify by reopening the exported file in Pixelorama and checking **Image → Color Mode**.

---

## Quick Reference — Common Issues

| Problem | Likely cause | Fix |
|---|---|---|
| Colors look corrupted in-game | PNG exported as RGBA instead of Indexed | Re-export with Indexed PNG confirmed in export settings |
| Transparent areas show as solid color | Slot 0 was changed | Re-import palette from the original PNG backup; slot 0 must stay transparent |
| Palette panel shows wrong colors | Sprite palette not imported | Palettes panel → Import palette from current sprite |
| Color picker snaps to wrong color | Working in RGBA mode, not Indexed | Image → Color Mode → Indexed |
| Sprite looks fine but palette feels muddy | Saturation dropped too low on all slots | Bring S back up on highlight and midtone slots |
| Delta looks too similar to the original | Only shifted hue slightly | Try a more aggressive H rotation — 30+ degrees reads clearly |
| Outlines look colored rather than dark | Outline slot was accidentally modified | Reset outline slot to near-black (H: any, S: 10–20, V: 10–20) |
| Build fails after adding sprite | PNG dimensions don't match expected size | DS-style front and back sprites are 80×80 px; icons are 32×32 px |

---

## Minimum Viable Sprite Set Per Delta

For each Delta species to be functional in the game, you need these files:

| File | Size | Priority |
|---|---|---|
| `front.png` | 80×80 px | Required |
| `back.png` | 80×80 px | Required |
| `icon.png` | 32×32 px | Required |
| Overworld follower | Varies | Can lag behind — add during polish phase |

Front + back + icon is the threshold to clear for a Delta to be shippable as a placeholder.

---

## Workflow Summary

```
1.  Copy base species folder to graphics/pokemon/DELTA_SPECIES/
2.  Open front.png in Pixelorama — set color mode to Indexed on import
3.  Palettes panel → Import palette from current sprite
4.  Identify primary, shadow, highlight, accent, outline, and transparent slots
5.  Plan hue shift based on Delta type (see type-to-hue table)
6.  Double-click each target slot → adjust H in HSV picker (preserve S/V relationships)
7.  Leave slot 0, outlines, and eye detail slots unchanged
8.  File → Export → PNG → graphics/pokemon/DELTA_SPECIES/front.png
9.  Repeat for back.png and icon.png
10. Save .pxo working files to Assets-Source/Sprites/ outside the repo
11. Rebuild: make -j$(sysctl -n hw.ncpu)
12. Verify in-game — check battle sprite and summary screen
```
