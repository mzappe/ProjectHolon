# START Menu — Custom Wants

Running list of desired additions to the START menu. Newest ideas at the bottom of each section.

Status key: `idea` · `planned` · `wip` · `done`

---

## Done

| Feature | Notes |
|---|---|
| In-game clock window (top-left) | `done` — time-only, auto-sizing, 12/24h toggle. See BUILD-LOG 2026-08-31. |

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
