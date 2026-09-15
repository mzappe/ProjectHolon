# START Menu — Custom Wants

Running list of desired additions to the START menu. Newest ideas at the bottom of each section.

Status key: `idea` · `planned` · `wip` · `done`

---

## Done

| Feature | Notes |
|---|---|
| In-game clock window (top-left) | `done` — time-only, auto-sizing, 12/24h toggle. See BUILD-LOG 2026-08-31. |

---

## v1 scope — Time · Location · Weather  `planned`

Grow the shipped clock window into a **fixed 3-row** info panel. All three rows always
render — nothing is dynamically hidden in v1. One file: `src/start_menu.c`. No new strings
(label tables are local `COMPOUND_STRING`). Est. ~half a day.

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

- Safari Balls / Pyramid Floor window collision with the taller panel (they sit at `tilemapTop 5`).
- Dynamic row hiding / conditional rows.

### Open decision

- One `FONT_NORMAL` size for all rows, or time larger / sub-rows `FONT_SMALL`?

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

### Panel design notes
- Sits top-left; Safari Balls / Pyramid Floor windows already shifted to `tilemapTop 5` for the clock — panel height may need more clearance, push those further down or make the panel width-only.
- `baseBlock` must stay clear of the Safari/Pyramid windows (`0x8`) and the START menu window (`0x139`). Clock currently at `0x38`.
- Conditional lines make the panel variable-height — size it after deciding which lines render.
- Config header `HOLON_START_MENU_*` with one toggle per widget.
