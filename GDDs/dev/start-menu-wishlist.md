# START Menu — Custom Wants

Running list of desired additions to the START menu. Newest ideas at the bottom of each section.

Status key: `idea` · `planned` · `wip` · `done`

## Current implementation — 2026-09-16

The approved native GBA design from `art/start_menu_mockups/pass_05/` is integrated.

- Frame 20 now contains a muted silver helix band, purple edging, and green corners.
  The outer edge and corner cutouts are transparent; bright checkerboard detailing
  was removed after the first in-game review. Rebuild its native tiles with
  `python3 tools/build_holon_menu_frame.py`. Frame 1
  is unchanged. New games default to Frame 20; START always uses the Holon frame,
  including on existing saves, and restores the player's chosen frame on exit.
  Corners use distinct 5×5 faceted green crystals with dark octagonal settings
  (the preceding 3×3 restoration was too subtle). Transparent outer edges and
  muted silver rails are retained.
- The left panel has a fixed 128×64 interior: location, clock, weather, and save age.
  The 32×32 Metal Energy watermark uses a pale palette color. Clock and weather use
  8×8 icons; all nine weather labels have distinct icons. Moon phase is omitted.
- The action window has a 72px interior, 16px rows, a green selection highlight,
  and a purple pointer. Nine existing actions fit with the frame inside 240×160.
  No actions were added or removed. Unusually long labels fall back to the small
  font and truncate only if needed.
- Panel contents refresh in place when the minute, weather label, or save-age
  minute changes. Safari/Pyramid counters sit below the panel. Save, retire,
  DexNav, and link-card transitions clean up the extra windows.
- The save timestamp occupies four previously unused bytes at SaveBlock2 offset
  0x90; following fields and struct size are unchanged. It stores playtime + 1,
  with zero meaning unknown. Normal save writes and recovery retries include the
  timestamp and restore the prior value in RAM on failure. Successful/recovered
  loads seed the timestamp from the loaded playtime, including older saves.
  New games clear the timestamp and show "Not saved yet". Older emulator save
  states that bypass loading show "Save to set timer" until saved. Incremental
  link saves retain their prior timestamp during the session; loading them seeds
  it from their saved playtime. This measures elapsed playtime, not time switched off.
  User confirmed this behavior: showing zero immediately after loading is intended.

Validation: `make -j8` succeeds; graphics retain the approved indexed palettes and
tile sizes. Window bounds and tile allocations were checked. Save-age host checks
using the actual C function bodies cover new/legacy/recovered saves, invalid
timestamps, and minute/hour changes. In-emulator review of the refinement remains
manual. Earlier design notes below are historical
where they conflict with this implementation.

---

## Done

| Feature | Notes |
|---|---|
| In-game clock window (top-left) | `done` — time-only, auto-sizing, 12/24h toggle. Superseded by the panel below. |
| START panel: Time · Location · Weather · Saved-X-ago | `done` — grew into 4 fixed rows instead of 3 (Saved Xm ago was pulled in from the idea list below during the same build). |

---

## v1 scope — Time · Location · Weather  `done`, shipped as 4 rows

Grew the shipped clock window into a **fixed-row** info panel — 4 rows in the end (Time ·
Location · Weather · Saved-X-ago), since Saved Xm ago got pulled forward into the same
build. All rows always render — nothing is dynamically hidden. One file: `src/start_menu.c`
(+ a `SaveBlock2` field and a `save.c` hook for the Saved-X-ago row). Kept below for the
row-by-row rationale.

### Rows (all `FONT_NORMAL` for v1, no icons)

| Row | Example | Source |
|---|---|---|
| Time | `1:27 AM` / `13:27` | existing clock code (`FormatDecimalTimeWithoutSeconds`, `gLocalTime`) |
| Location | `LITTLEROOT TOWN` | `GetMapNameGeneric(buf, gMapHeader.regionMapSectionId)` — always populated (Holon has a section everywhere) |
| Weather | `CLEAR` / `RAIN` / `INDOORS` | see below |

### Weather row logic

1. If `IsMapTypeIndoors(gMapHeader.mapType)` (covers `MAP_TYPE_INDOOR` / `SECRET_BASE`; add `MAP_TYPE_UNDERGROUND` explicitly for caves) → `INDOORS`.
2. Else map `GetCurrentWeather()` through the label table; `WEATHER_NONE` → `CLEAR`.
3. Anything unmapped falls through to `CLEAR`. Row is never blank, never hidden.

| Label | Weather ids |
|---|---|
| `CLEAR` | `WEATHER_NONE` + any unmapped id |
| `SUNNY` | `SUNNY_CLOUDS`, `SUNNY`, `DROUGHT` |
| `CLOUDY` | `SHADE` |
| `RAIN` | `RAIN`, `DOWNPOUR`, `RAIN_THUNDERSTORM`, `ABNORMAL` |
| `FOG` | `FOG_HORIZONTAL`, `FOG_DIAGONAL`, `FOG` |
| `SANDSTORM` | `SANDSTORM` |
| `ASHFALL` | `VOLCANIC_ASH` |
| `SNOW` | `SNOW` |

### Build details

- **Refactor:** `ShowStartClockWindow` → `ShowStartPanelWindow`; `sStartClockWindowId` → `sStartPanelWindowId`. Same lifecycle: built in `InitStartMenuStep` case 3, torn down in `RemoveExtraStartMenuWindows`.
- **Refresh:** build all 3 rows once on menu-open. Keep the minute-rollover refresh (from `HandleStartMenuInput`) for the time only — location can't change with the menu open, weather changes are rare enough to leave until the next open.
- **Window size:** fixed 3 rows. Keep the per-draw width auto-size, measured against the widest rendered row (location, up to `MAP_NAME_LENGTH` = 15 chars ≈ 15 tiles / 120px). Height = 3 × line height.
- **baseBlock `0x38`** unchanged. Verify the taller window still clears the menu window (`0x139`); bump if needed.
- **Config:** reuse `START_CLOCK_24_HOUR`. No per-row toggles in v1 (all rows always on).

### Deferred (not v1, per MZ)

- Safari Balls / Pyramid Floor window collision with the taller panel (they sit at `tilemapTop 5`) — still unresolved, panel is now 4 rows tall.
- Dynamic row hiding / conditional rows.

### Resolved

- Font: all rows `FONT_NORMAL`, matching the original clock. See chat discussion 2026-09-14.
- Rows are left-aligned at a small inset, not centered per-row — centering independently made short rows (`CLEAR`) and long ones (`LITTLEROOT TOWN`) zigzag against each other.

---

## Right side — menu options (`MENU_ACTION_*`)

| Feature | Status | Notes |
|---|---|---|
| **MAP** | idea | New entry. Viewer already exists (`FieldInitRegionMap`, read-only wall map). Gate to outdoor maps. Decide: plain viewer vs fly-from-menu (`CB2_OpenFlyMap`). |
| **PC / STORAGE** | idea | Box access from the menu. Reuse `CB2_PokeStorage`. Decide where it's allowed (towns only? anywhere?). |
| DEXNAV | already built in | Enum + callback + flag-gated add already present. Just enable DexNav config + set `DN_FLAG_DEXNAV_GET`. No code. |

---

## Left side — multi-widget info panel

Replace the single clock window with one multi-line panel. Each line individually
toggleable (config header). Lines that have no data are skipped, not blank.

| Widget | Status | Data source | Notes |
|---|---|---|---|
| **Time-of-day icon** | idea | `GetTimeOfDay()` | Sun / moon / dawn / dusk glyph next to the clock. |
| **Weather icon** | idea | `GetCurrentWeather()` | Current map weather. |
| **Objective tracker** | idea | quest system (TBD) | One line of active-quest text. Only shown if a quest is active. |
| **DexNav chain** | idea | expansion DexNav state | Chain length / search level for current area. Only if a search is active. |
| **Repel counter** | idea | `VAR_REPEL_STEP_COUNT` | Steps remaining. Only shown if > 0. |
| **Location name** | idea | map name / region section | Current town or route. |
| **Delta Dex seen/caught** | idea | custom regional/Delta dex | `n seen / n caught` of δ species. |
| **Money** | idea | `GetMoney(&gSaveBlock1Ptr->money)` | Maybe — could feel cluttered. |
| **Pokédex count** | idea | `GetHoennPokedexCount` / national | Seen / caught. Maybe (Delta Dex may cover this). |
| **Moon phase icon** | idea | `(gLocalTime.days * 8 / MOON_CYCLE_LEN) % 8` — same day counter that drives the weekday | No new save data. 8 tiny icon tiles (new/waxing-crescent/first-quarter/…/waning-crescent). Refresh once per menu-open (day granularity). Cycle isn't tied to a real date — same quirk as the weekday, fine for a fictional region's moon. |

`Saved Xm ago` shipped as row 4 of the panel — see Done, above.

### Panel design notes
- Sits top-left; Safari Balls / Pyramid Floor windows already shifted to `tilemapTop 5` for the clock — panel height may need more clearance, push those further down or make the panel width-only.
- `baseBlock` must stay clear of the Safari/Pyramid windows (`0x8`) and the START menu window (`0x139`). Clock currently at `0x38`.
- Conditional lines make the panel variable-height — size it after deciding which lines render.
- Config header `HOLON_START_MENU_*` with one toggle per widget.

---

## Visual style — Delta Species-styled window frame  `reverted`

Built and shipped as a first pass, then **pulled the same day — MZ didn't love the look**.
Unhooked cleanly: `InitStartMenuStep` case 2 is back to `LoadMessageBoxAndBorderGfx()`
(player's normal Options frame), `LoadStartMenuFrameGfx()` and the
`gTextWindowFrameHolonDelta_Gfx/Pal` declarations/definitions are removed, and
`graphics/text_window/holon_delta.png` is deleted. The panel above (time/location/weather/
saved-ago) is untouched by this.

The wiring technique below is proven and cheap to redo if a custom START menu frame comes
back later — it's the *art direction* that needs to change, not the approach. Keeping the
rest of this section as reference for a future attempt.

Original framing: restyle the whole start menu (panel + action list) instead of reusing
the stock Emerald window frame, drawing from the Pokémon TCG's δ Delta Species card design
— whose home region in the TCG lore is literally also called Holon.

### What's swappable
Every dialog box (including everything above) is drawn by `DrawStdWindowFrame`, which
loads a **3×3 tile set, 24×24px, 4bpp/16-color palette** — the entire border look. There
are already 20 of these (`WINDOW_FRAMES_COUNT`, `include/text_window.h:4`,
`graphics/text_window/1.png`…`20.png`), player-selectable in Options via
`optionsWindowFrameType`. Proof this is a small, well-defined asset to author, not an
engine change.

### Art direction (refreshed against the actual cards)
- **Border motif:** the double-helix / twisted-ladder line pattern that ran along Delta
  Species cards' artwork-window border — simplified to a repeating zigzag at 8px scale.
- **Corners:** a small δ-triangle notch, echoing the δ mark on the cards' Evolution box,
  rather than trying to render the literal Greek letter at 8×8.
- **Color:** warm gold-to-bronze gradient standing in for the cards' holofoil refractor
  border (a real-time refractor shimmer isn't free on GBA).
- **Interior fill:** stays light/neutral for text legibility — the cards' dark cosmic
  backgrounds don't translate to a readable text box, so the Delta flavor lives in the
  border only.
- **Stretch, optional:** fake the refractor shimmer with a slow palette-cycle on 1–2
  border indices, the same trick the overworld uses for shiny water. Not required for v1.

### Technical spec
- 24×24px indexed PNG, 3×3 tile grid, 4bpp/16-color palette — same format as the existing
  20 frames.
- Budget ~6–8 of the 16 palette slots to the gold/bronze gradient + helix line colors, the
  rest to interior fill/text shading.

### Wiring — scoped, not global (as built, now removed)
- ~~True 21st frame~~ (bump `WINDOW_FRAMES_COUNT`, add to `sWindowFrames[]` in
  `src/text_window.c`, becomes selectable in Options / usable everywhere) — bigger
  footprint, and a gold metallic border would clash on ordinary dialogue/shop boxes.
- **Went with: scoped to the start menu.** `gTextWindowFrameHolonDelta_Gfx/Pal` declared
  in `src/text_window.c` / `include/text_window.h`, deliberately outside `sWindowFrames[]`.
  A `LoadStartMenuFrameGfx()` in `src/start_menu.c` force-loaded them into the std
  window's tile/palette slot, replacing the `LoadMessageBoxAndBorderGfx()` call in
  `InitStartMenuStep` case 2 — the same direct-load pattern `save_failed_screen.c` uses
  for `gTextWindowFrame1_Gfx/Pal`. Since the panel, action list, and Safari/Pyramid
  windows all share that one loaded tile block, this reskinned the whole START menu as one
  piece for a single call-site change. Every other std-window screen in the game kept
  calling the real `LoadMessageBoxAndBorderGfx()` throughout, untouched. All of the above
  is now removed — this is the record of how it worked, for next time.

### Cost (actual)
Wiring was one function + one call-site swap, as expected. The art (`graphics/text_window/
holon_delta.png`) was authored programmatically (Python/PIL) rather than iterated on
visually — gold-gradient border, alternating violet/teal corner accents standing in for
the double-helix motif, rounded corners via palette-index-0 transparency. It read fine in
a static pixel-grid preview but didn't land once actually in the menu. **Takeaway for next
attempt:** iterate the art visually (mockup or in-emulator) before wiring it in, rather
than authoring blind from a spec.

### Sources (card design reference)
- [EX Delta Species (TCG) — Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/EX_Delta_Species_(TCG))
- [δ Delta Species (TCG) — Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/%CE%94_Delta_Species_(TCG))
- [A Holographic History Of The Pokémon TCG: Pokémon δ Delta Species — Bleeding Cool](https://bleedingcool.com/games/a-holographic-history-of-the-pokemon-tcg-pokemon-delta-species/)
- [Holofoil — Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Holofoil)
