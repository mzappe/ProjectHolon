---
title: "Pokémon Holon Legends — pokeemerald-expansion Features & Branch Guide"
doc-id: HL-TEC-002
version: 1.0
status: Stable
category: Technical
last-updated: 2026-03-22
author: Matt Zappe
---

# Pokémon Holon Legends — pokeemerald-expansion Features & Branch Guide

A comprehensive reference for deciding which **pokeemerald-expansion** features to enable, disable, or configure for **Pokémon Holon**, plus a catalog of community **feature branches** worth considering.

> **Status:** Stable | **Version:** 1.0 | **Updated:** 2026-03-22

> [!NOTE]
> All built-in features are controlled through config header files in `include/config/`. Feature branches are **separate Git branches** maintained by community developers and pulled into your project via `git remote add` + `git pull`.

---

## Table of Contents

- [1. How Config Files Work](#1-how-config-files-work)
- [2. Built-In Features — Master Table](#2-built-in-features--master-table)
  - [2.1 Battle Engine](#21-battle-engine)
  - [2.2 Trainer Customization](#22-trainer-customization)
  - [2.3 Pokémon Data & Species](#23-pokémon-data--species)
  - [2.4 Overworld & Field Mechanics](#24-overworld--field-mechanics)
  - [2.5 Interface & UI](#25-interface--ui)
  - [2.6 Engine / QoL Improvements](#26-engine--qol-improvements)
  - [2.7 Developer Tools](#27-developer-tools)
  - [2.8 Save Space Management](#28-save-space-management)
  - [2.9 Level & EV Caps](#29-level--ev-caps)
  - [2.10 DexNav](#210-dexnav)
- [3. Config File Quick Reference](#3-config-file-quick-reference)
- [4. Community Feature Branches — Master Table](#4-community-feature-branches--master-table)
  - [4.1 Overworld & Visual](#41-overworld--visual)
  - [4.2 UI & Menus](#42-ui--menus)
  - [4.3 Gameplay Systems](#43-gameplay-systems)
  - [4.4 Battle & Mechanics](#44-battle--mechanics)
  - [4.5 Audio & Polish](#45-audio--polish)
  - [4.6 Developer / Utility](#46-developer--utility)
  - [4.7 Other Notable Branches](#47-other-notable-branches)
- [5. How to Pull a Feature Branch](#5-how-to-pull-a-feature-branch)
- [6. Recommendations for Pokémon Holon](#6-recommendations-for-pokémon-holon)
- [Sources](#sources)
- [Changelog](#changelog)

---

## 1. How Config Files Work

Expansion exposes most feature toggles as C `#define` directives in header files under `include/config/`. You change a value (usually `TRUE`/`FALSE`, a generation constant like `GEN_LATEST`, or a specific integer), rebuild with `make`, and the feature is enabled or disabled.

**Key pattern:**
- `GEN_LATEST` = use the most modern behavior (Gen 9 by default)
- Specific `GEN_X` = lock behavior to that generation
- `TRUE` / `FALSE` = simple toggle
- `0` = disabled (for flag/var-based features, assign a real flag ID to enable)
- `DISABLED_ON_RELEASE` = enabled in dev builds, disabled in release builds

---

## 2. Built-In Features — Master Table

### 2.1 Battle Engine

| Feature | Config File | Key Define(s) | Default | Holon Recommendation | Notes |
|---|---|---|---|---|---|
| **Battle gimmicks** (Mega, Z-Move, Dynamax, Tera) | `battle.h` | Various `B_FLAG_*` per gimmick | Enabled | **Disable all** | None of these gimmicks exist in the Holon TCG arc. Delta Species is the game's unique mechanic and lives at the species/type data layer, not the battle gimmick layer. |
| **Physical/Special split** | Built-in | Always on | On | **Keep** | Essential modern mechanic. |
| **Fairy/Stellar types** | Built-in | Always on | On | **Keep Fairy; disable Stellar** | Stellar is Tera-specific. Fairy is standard and relevant. |
| **Gen-based mechanics toggles** | `battle.h` | `B_*` defines using `GEN_LATEST` | Gen 9 | **Tune per-feature; lean Gen 6–7** | The game is rooted in a Gen 3 TCG era but should feel modern. Review per define. |
| **Critical capture** | `battle.h` | Included | On | **Keep** | Standard QoL. |
| **Frostbite support** | `battle.h` | Toggle available | Off | **Leave off** | Non-standard; would confuse players. |
| **Move descriptions in battle** | `battle.h` | `B_SHOW_MOVE_DESCRIPTION` | `TRUE` | **Keep** | Helpful, especially with Delta types changing type matchups. |
| **Type effectiveness indicator** | `battle.h` | `B_SHOW_EFFECTIVENESS` | `SHOW_EFFECTIVENESS_SEEN` | **Keep** | Critical for a game where type matchups are non-standard due to Delta mutations. |
| **Faster battles** (HP drain, intro, AI) | Built-in | Various | On | **Keep** | Smooth gameplay. |
| **Sleep Clause** | `battle.h` | Toggle available | Configurable | **Consider enabling** | Prevents cheap AI sleep-stacking. |
| **No badge stat boosts** | `battle.h` | `B_BADGE_BOOST` | Configurable | **Consider disabling boosts** | Invisible Gen 3 badge boosts are confusing. |
| **Affection mechanics** | `battle.h` | `B_AFFECTION_MECHANICS` | Configurable | **Disable** | Breaks difficulty balance. |
| **Double Wild Battles** | Built-in | Available | Configurable | **Keep available** | Useful in specific Holon locations — Holon Lake and Dragon Frontiers could have interesting double encounters. |
| **Sky Battles** | Built-in | Available | Configurable | **Disable** | No mechanical value for Holon. |
| **Inverse Battles** | Built-in | Available | Configurable | **Consider for specific trainers** | Could be interesting for a researcher whose entire team is Delta (inverted normal expectations). |
| **AI improvements** | `ai.h` | Many smart-AI defines | On | **Keep defaults** | AI is significantly smarter than vanilla Emerald. |
| **Trainer difficulty variable** | `battle.h` | `B_VAR_DIFFICULTY` | `0` (disabled) | **Consider enabling** | Useful if Holon has an optional difficulty mode. |
| **Disable bag in battle** | `battle.h` | `B_VAR_NO_BAG_USE` | `0` (disabled) | **Consider for specific encounters** | Could restrict bag use during the Delta Deoxys encounters to force adaptive play. |

### 2.2 Trainer Customization

| Feature | Notes | Holon Recommendation |
|---|---|---|
| **Pokémon Showdown team syntax** | Paste teams from the teambuilder directly | **Use** — massive time saver for authoring trainer teams |
| **Custom Pokémon data** (nicknames, EVs, IVs, moves, abilities, balls, nature, gender, shininess) | Per-trainer Pokémon customization | **Use** — essential for researcher NPCs whose teams should feel deliberate and scientific |
| **Ace Pokémon** (saved for last) | Trainer AI holds back a specific mon | **Use** — adds drama to key researcher battles |
| **Trainer Pools** (randomized from a pool) | Random team selection from a pool | **Consider** — useful for generic researcher grunts; gives repeat encounters variety |
| **Custom sliding messages** | Trainer says things on first turn, super-effective hits, etc. | **Use** — researchers commenting on Delta types in battle is a great storytelling layer |
| **AI flag customization** | Fine-tune per-trainer intelligence | **Use** — senior researchers should be notably harder than junior field staff |
| **Trainer class Poké Balls** | Class-specific default balls | **Use** — researchers using specialized balls is an immersive detail |

### 2.3 Pokémon Data & Species

| Feature | Config File | Key Define(s) | Default | Holon Recommendation | Notes |
|---|---|---|---|---|---|
| **Species toggles** (by generation) | `species_enabled.h` | `P_GEN_1_POKEMON` through `P_GEN_9_POKEMON` | All `TRUE` | **Enable Gens 1–4; evaluate 5–6 selectively; disable 7–9 initially** | The TCG Delta Species arc is firmly Gen 3 era. Gen 4 gives you great options (Lucario, Garchomp, Electivire, etc.) and the arc ran into Gen 4. Later gens add ROM overhead for diminishing return unless specific species are needed for Delta variants. |
| **Mega Evolutions** | `species_enabled.h` | `P_MEGA_EVOLUTIONS` | `TRUE` | **Disable** | Not part of Holon's lore or the TCG arc. Delta Species is the game's transformation mechanic. |
| **Regional Forms** | `species_enabled.h` | `P_REGIONAL_FORMS` | `TRUE` | **Disable or very selective** | Regional forms conceptually compete with Delta Species and may confuse the game's identity. Disable unless a specific form is needed. |
| **Fusion Forms** | `species_enabled.h` | `P_FUSION_FORMS` | `TRUE` | **Disable** | Not relevant. |
| **Cross-gen evolutions** | `species_enabled.h` | `P_CROSS_GENERATION_EVOS` | `TRUE` | **Keep** | Valuable for roster diversity within the Gen 1–4 range. |
| **Updated learnsets** | `pokemon.h` | `P_LVL_UP_LEARNSETS` | `GEN_LATEST` | **Keep GEN_LATEST** | Modern movesets are better balanced. |
| **Breeding mechanics** | `pokemon.h` | Various | `GEN_LATEST` | **Keep** | Modern breeding is expected. |
| **DS-style sprites** | Built-in | Default | On | **Keep** | Better visuals; also closer to the era the TCG art evokes. |
| **12-character names** | Built-in | Default | On | **Keep** | Required if Delta Pokémon have name variants (e.g. "Charizard δ"). |
| **Force shiny / no-shiny flags** | `pokemon.h` | `P_FLAG_FORCE_SHINY`, `P_FLAG_FORCE_NO_SHINY` | `0` (disabled) | **Assign flags** | Useful for scripted Delta Deoxys encounters and development. |

> [!IMPORTANT]
> **Delta Species are implemented at the species/type data layer, not through any expansion gimmick.** Each Delta Pokémon is effectively a separate species entry with modified typing, custom sprites, and adjusted learnsets. This is significant custom work and is not controlled by any single config toggle. Plan for this early — it affects species slot budgeting, saveblock space, and Pokédex structure.

### 2.4 Overworld & Field Mechanics

| Feature | Config File | Key Define(s) | Default | Holon Recommendation | Notes |
|---|---|---|---|---|---|
| **Follower Pokémon** | Built-in | Various `OW_*` | Enabled | **Keep** | Adds life to the overworld; Delta follower sprites will make the unusual typing visually apparent in the field. |
| **Day/Night System** | Built-in | `OW_ENABLE_DNS` | `TRUE` | **Keep** | Atmospheric value. Deoxys's aurora EM communication has a natural visual hook here — aurora effects at night near the Tower. |
| **NPC Followers** | `follower_npc.h` | `FNPC_ENABLE_NPC_FOLLOWERS` | `FALSE` | **Enable** | Key researchers may travel with the player in certain sections. |
| **BW Map Pop-ups** | `overworld.h` | `OW_POPUP_GENERATION` | `GEN_3` | **Change to `GEN_5`** | BW-style location pop-ups feel more modern and polished. |
| **Running indoors** | Built-in | Default | On | **Keep** | Expected QoL. |
| **B2W2+ Repel system** | Built-in + `item.h` | `I_REPEL_LURE_MENU` | `TRUE` | **Keep** | Standard QoL. |
| **VS. Seeker** | Built-in | Available | Configurable | **Enable** | Useful for researcher rematches without the Match Call system. |
| **Chain fishing** | Built-in | Default | On | **Keep** | Useful shiny-hunting mechanic. |
| **Defog field move** | Built-in | Default | On | **Consider** | Alpha blended fog effects in Mirage Forest could be paired with this. |
| **XY Berry Mechanics** | Built-in | Default | On | **Consider** | Adds depth but may be more complexity than Holon needs. |
| **Slow movement on stairs** | `overworld.h` | `SLOW_MOVEMENT_ON_STAIRS` | `FALSE` | **Leave off** | Annoying in practice. |
| **Synchronize Nature (OW)** | `overworld.h` | `OW_SYNCHRONIZE_NATURE` | `GEN_LATEST` | **Keep** | Players expect this. |
| **Compressed OW Graphics** | `overworld.h` | `OW_GFX_COMPRESS` | `TRUE` | **Keep** | Saves ROM space. Delta species sprites will add significant graphic overhead — conserve where possible. |

### 2.5 Interface & UI

| Feature | Config File | Key Define(s) | Default | Holon Recommendation | Notes |
|---|---|---|---|---|---|
| **Summary Screen: Nature colors** | `summary_screen.h` | `P_SUMMARY_SCREEN_NATURE_COLORS` | `TRUE` | **Keep** | Intuitive red/blue stat coloring. |
| **Summary Screen: Move Relearner** | `summary_screen.h` | `P_SUMMARY_SCREEN_MOVE_RELEARNER` | `TRUE` | **Keep** | Convenient. |
| **Summary Screen: EV/IV display** | `summary_screen.h` | `P_SUMMARY_SCREEN_IV_EV_INFO` | `FALSE` | **Gate behind a story item** | Use `P_FLAG_SUMMARY_SCREEN_IV_EV_INFO` — could be unlocked via a research tool the player receives from the Holon team. Thematically fitting. |
| **Summary Screen: Rename** | `summary_screen.h` | `P_SUMMARY_SCREEN_RENAME` | `TRUE` | **Keep** | Convenient. |
| **HGSS-style Pokédex** | `pokedex_plus_hgss.h` | Configurable | Available | **Strongly consider** | More detailed dex fits a research game. Could display Delta type information prominently. |
| **Party Menu: "Move Item"** | Built-in | Default | On | **Keep** | Standard QoL. |
| **Box Link** | Built-in | Default | Available | **Enable** | Access PC boxes anywhere; useful for a game spanning remote locations. |
| **Pokéball quick menu** | Built-in | Default | On | **Keep** | Faster ball selection in battle. |

### 2.6 Engine / QoL Improvements

| Feature | Config File | Default | Holon Recommendation | Notes |
|---|---|---|---|---|
| **All pokeemerald bugfixes** | `general.h` | `BUGFIX` defined | **Keep** | Always fix known bugs. |
| **HQ RNG (SFC32)** | `general.h` | `HQ_RANDOM = TRUE` | **Keep** | Better randomness than vanilla. |
| **Modern compiler support** | Built-in | On | **Keep** | Better error detection. |
| **Improved sprite compression** | Built-in | On | **Keep** | Saves ROM space — important with custom Delta sprites. |
| **Dynamic Multichoice** | Built-in | On | **Keep** | Easier scripting menus. |
| **Expansion intro** | `general.h` | `EXPANSION_INTRO = TRUE` | **Disable** | Replace with a Holon-specific intro or remove entirely. |
| **Measurement units** | `general.h` | `UNITS_IMPERIAL` | **Your choice** | No strong reason to deviate from default. |
| **Reusable TMs** | `item.h` | `I_REUSABLE_TMS = FALSE` | **Enable** | Modern expectation. |
| **Exp. Share as Key Item** | `item.h` | `I_EXP_SHARE_ITEM = GEN_5` | **Set to `GEN_6`** | Party-wide XP share reduces grinding across five locations. |

### 2.7 Developer Tools

| Feature | Config File | Default | Holon Recommendation | Notes |
|---|---|---|---|---|
| **Overworld Debug Menu** | `debug.h` | `DISABLED_ON_RELEASE` | **Keep** | Stripped from release; essential during development. |
| **Battle Debug Menu** | `debug.h` | `DISABLED_ON_RELEASE` | **Keep** | Crucial for testing Delta Deoxys encounter behavior. |
| **Sprite Visualizer** | `debug.h` | `DISABLED_ON_RELEASE` | **Keep** | Invaluable for testing custom Delta sprites. |
| **Integrated Testing** | Built-in | Available | **Keep** | Catch regressions early, especially with custom type data. |
| **Learnset Helper** | `pokemon.h` | `P_LEARNSET_HELPER_TEACHABLE = TRUE` | **Keep** | Auto-generates movesets; useful for Delta species with modified learnsets. |
| **Script flags** (no wilds, no trainers, force shinies) | `pokemon.h` | `0` (disabled) | **Assign flags** | Essential for development and scripted Delta Deoxys encounters. |

### 2.8 Save Space Management

All in `save.h`. These free unused saveblock space by removing legacy features you won't use. Delta species data will consume additional saveblock space, so free as much as possible early.

| Feature to Free | Bytes Saved | Holon Recommendation |
|---|---|---|
| `FREE_MYSTERY_EVENT_BUFFERS` | 1104 | **Enable** — no ramScript/e-reader events |
| `FREE_MYSTERY_GIFT` | 876 | **Enable** — no Mystery Gift in a ROM hack |
| `FREE_RECORD_MIXING_HALL_RECORDS` | 1032 | **Enable** — no record mixing |
| `FREE_UNION_ROOM_CHAT` | 212 | **Enable** — no Union Room chat |
| `FREE_LINK_BATTLE_RECORDS` | 88 | **Enable** — no link battles with official games |
| `FREE_ENIGMA_BERRY` | 52 | **Enable** — no E-Reader berries |
| `FREE_EXTRA_SEEN_FLAGS_*` | 160 total | **Enable** — frees dex flags |
| `FREE_BATTLE_TOWER_E_READER` | 188 | **Enable** — no E-Reader |
| `FREE_POKEMON_JUMP` | 16 | **Enable** — no Pokémon Jump |
| `FREE_TRAINER_HILL` | 28 | **Enable** — repurpose the space |
| `FREE_MATCH_CALL` | 104 | **Enable** — using VS Seeker instead |
| **Total potential savings** | **~3790 bytes** | Reserve freed space for Delta species flags, fragment tracking, and ancient record discovery state |

### 2.9 Level & EV Caps

All in `caps.h`.

| Feature | Default | Holon Recommendation | Notes |
|---|---|---|---|
| **Exp Level Cap Type** | `EXP_CAP_NONE` | **Consider `EXP_CAP_SOFT`** | Soft caps prevent overleveling across five locations without hard walls. |
| **Level Cap Type** | `LEVEL_CAP_NONE` | **Consider `LEVEL_CAP_FLAG_LIST`** | Tie caps to story progression milestones (e.g. finding each Delta Deoxys fragment). |
| **Rare Candy Cap** | `FALSE` | **Match to your cap decision** | If using caps, Rare Candies should respect them. |
| **EV Cap** | `EV_CAP_NONE` | **Leave `NONE`** | Most ROM hacks skip EV caps; adds complexity without narrative value here. |

### 2.10 DexNav

All in `dexnav.h`.

| Feature | Default | Holon Recommendation | Notes |
|---|---|---|---|
| **DexNav enabled** | `FALSE` | **Enable** | ORAS-style DexNav fits a research-themed game extremely well. Could be reframed as the research team's field scanner — thematically appropriate for a game about studying the Delta phenomenon. |
| **Search Levels** | `FALSE` | **Enable with DexNav** | Gives depth to wild encounters. Warning: uses 1 byte per species in saveblock — account for this in space planning. |

---

## 3. Config File Quick Reference

| Config File | Path | Purpose |
|---|---|---|
| `ai.h` | `include/config/ai.h` | AI switching chances, prediction, smart battle behavior |
| `battle.h` | `include/config/battle.h` | Battle mechanics, gen-based behavior toggles, gimmicks, flags/vars |
| `caps.h` | `include/config/caps.h` | Level caps, EV caps, experience scaling |
| `debug.h` | `include/config/debug.h` | Debug menus, sprite visualizer, AI timer |
| `dexnav.h` | `include/config/dexnav.h` | DexNav feature toggle and parameters |
| `follower_npc.h` | `include/config/follower_npc.h` | NPC follower system |
| `general.h` | `include/config/general.h` | RNG, expansion intro, units, compiler flags |
| `item.h` | `include/config/item.h` | TM reusability, Exp Share, Repels/Lures, VS Seeker |
| `overworld.h` | `include/config/overworld.h` | DNS, followers, map popups, field mechanics |
| `pokedex_plus_hgss.h` | `include/config/pokedex_plus_hgss.h` | HGSS-style Pokédex options |
| `pokemon.h` | `include/config/pokemon.h` | Learnsets, breeding, evolution, species graphics, shiny flags |
| `save.h` | `include/config/save.h` | Freeing saveblock space from unused legacy data |
| `species_enabled.h` | `include/config/species_enabled.h` | Toggle entire generations/form groups of Pokémon |
| `summary_screen.h` | `include/config/summary_screen.h` | Summary screen stats/IV/EV display, move relearner |

---

## 4. Community Feature Branches — Master Table

These are **not** part of pokeemerald-expansion by default. They are community-made additions stored as Git branches on individual developers' forks. You pull them into your project with Git.

> [!WARNING]
> Feature branches may conflict with each other or with your existing changes. Always create a new Git branch before pulling, test thoroughly, and be prepared to resolve merge conflicts. Branches targeting base `pokeemerald` may need adaptation for `pokeemerald-expansion`.

### 4.1 Overworld & Visual

| Branch | Author | Description | Source | Holon Fit | Rationale |
|---|---|---|---|---|---|
| **Follower Pokémon** | @aarant | Pokémon follow you in the overworld | [Branch](https://github.com/aarant/pokeemerald/tree/followers-expanded-id) | ✅ **Already in expansion** | Built-in. Delta followers showing non-standard typing is a passive storytelling tool. |
| **Day/Night System** | @aarant | DNS with lighting, supports non-RTC | [Branch](https://github.com/aarant/pokeemerald/tree/lighting-expanded-id) | ✅ **Already in expansion** | Built-in. Aurora effects near the Tower at night are a key visual. |
| **Seasons** | @Rioluwott | Season system (visual + mechanical) | [Branch](https://github.com/BelialClover/pokeemerald/tree/seasons) | ⭐ **Low–Med** | Could add atmosphere but not essential to Holon's story. Lower priority than other branches. |
| **Overworld Character Shadows** | @Pawkkie | Shadows beneath all overworld characters | [Branch](https://github.com/Pawkkie/pokeemerald-expansion/tree/overworld-character-shadows) | ⭐ **Medium** | Visual polish. |
| **Dynamic Palettes** | @Kyphii | Dynamic palette swapping for overworld | [Branch](https://github.com/kyphii/pokeemerald/tree/feature/dynpal) | ⭐ **High** | Useful for showing the Delta phenomenon's spread visually — palette shifts as you move deeper into Delta territory. |
| **Alpha Blended Maps** | @KittyPBoxx | Alpha blending for top-layer map tiles | [Branch](https://github.com/KittyPBoxx/pokeemerald/tree/alpha-blended-top-layer-maps) | ⭐ **High** | Mirage Forest fog and mist effects. Ancient ruins atmosphere. Strong fit for this game's locations. |
| **Ambient Pond Ripples** | @OriginalGRE | Animated ripple effects on water tiles | [Branch](https://github.com/OriginalGRE/pokeemerald-expansion/tree/ambient_pond_ripples) | ⭐ **Medium** | Holon Lake specifically would benefit from this. |
| **Variant Colours** | @SpaceOtter | Color variant system for Pokémon | [Branch](https://github.com/SpaceOtter99/pokeemerald-expansion/tree/colour-variants) | ⭐ **Low** | Delta Species are handled as separate species entries; this branch may not be the right tool for that. |
| **Ditto Face Support** | @AsparagusEduardo | Ditto shows the face of what it transforms into | [Wiki](https://github.com/Pawkkie/Team-Aquas-Asset-Repo/wiki/Ditto-face-support) | ⭐ **Low** | Minor detail; Ditto is not a focus. |

### 4.2 UI & Menus

| Branch | Author | Description | Source | Holon Fit | Rationale |
|---|---|---|---|---|---|
| **BW Map Pop-ups** | @BSBob / @RavePossum | Unova-style animated location name pop-ups | [Branch](https://github.com/ravepossum/pokeemerald/tree/bsbob_map_popups) | ✅ **Already in expansion** | Built-in and configurable via `overworld.h`. |
| **HGSS Battle UI** | @RavePossum | HeartGold/SoulSilver-style battle interface | [Branch](https://github.com/ravepossum/pokeemerald-expansion/tree/hgss_battle_ui_expansion) | ⭐ **Medium** | Clean visual upgrade. HGSS era is close to the Delta Species arc's time period. |
| **Nico's Cool UI** | @NicoSwag | Aesthetic UI overhaul | [Branch](https://github.com/NicoSwag/pokeemerald-expansion/tree/nicos_cool_ui) | ⭐ **Medium** | Worth evaluating for overall visual polish. |
| **SwSh Summary Screen** | @Montblanc | Sword/Shield-style summary | [Wiki](https://github.com/montmoguri/pokeemerald-expansion/wiki/Sword-&-Shield-Summary-Screen) | ⭐ **Low–Med** | Could work but SwSh aesthetic may be too modern for Holon's tone. |
| **SwSh Party Menu** | @Montblanc | Sword/Shield-style party menu | [Wiki](https://github.com/montmoguri/pokeemerald-expansion/wiki/Sword-&-Shield-Party-Menu) | ⭐ **Low–Med** | Pairs with SwSh Summary if chosen. |
| **SwSh Message Box** | @Montblanc | Sword/Shield-style dialogue boxes | [Branch](https://github.com/montmoguri/pokeemerald-expansion/tree/swsh_message_box) | ⭐ **Low–Med** | Visual consistency if going SwSh route. |
| **New Main Menu** (with Mugshot) | @Archie + @Mudskip | Custom main menu with character portrait | [Wiki](https://github.com/pret/pokeemerald/wiki/New-Main-Menu-UI-With-Mugshot-by-Archie-and-Mudskip) | ⭐ **High** | Sets tone immediately on boot. Could show the stone tablet / Mirage Forest imagery. |
| **Full Screen Start Menu** | @Archie + @Mudskip | Expanded start menu | [Wiki](https://github.com/pret/pokeemerald/wiki/Full-Screen-Start-Menu-by-Archie-and-Mudskip) | ⭐ **Medium** | More room for quest log and research tools in the menu. |
| **Rotom Phone Start Menu** | @HashtagMarky | Rotom Phone aesthetic for start menu | [Branch](https://github.com/HashtagMarky/pokeemerald/tree/rotom_start_menu) | ⭐ **Low** | SwSh-specific aesthetic; doesn't fit Holon's tone. |
| **Start Menu Clock** | @Pawkkie | Shows current time in the start menu | [Branch](https://github.com/Pawkkie/pokeemerald-expansion/tree/start-menu-clock) | ⭐ **Medium** | With DNS active, showing the time is a practical addition. |
| **Custom Start Menu** | @Vol | Customizable start menu layout | [Branch](https://github.com/vol8/pokeemerald/tree/start_menu_1) | ⭐ **Medium** | Flexibility to add a Delta Scanner / Research Log entry point. |
| **Town Map Port** | @Vol | Enhanced town map | [Branch](https://github.com/vol8/pokeemerald/tree/expansion-town-map) | ⭐ **High** | Holon's five-location spread across land and ocean needs a clear, well-designed region map. |
| **Registered Items Menu** | @iriv24 | Quick-access registered items | [Branch](https://github.com/iriv24/pokeemerald-expansion/tree/iriv24/tx_registered_items_menu) | ⭐ **Medium** | QoL for a game where the player carries research tools. |
| **HGSS Pokédex Darkest Mode** | @RavePossum | Dark theme for HGSS Pokédex | [Branch](https://github.com/ravepossum/pokeemerald-expansion/tree/hgss_dex_darkest_mode) | ⭐ **Low–Med** | If using HGSS dex, the darker theme suits Holon's atmosphere. |
| **Help Window** | @Linathan | In-game help/info window system | [Branch](https://github.com/LinathanZel/pokeemerald-expansion/tree/help_window) | ⭐ **Medium** | Could surface Delta type information and research notes in-field. |
| **Talk And Think Icons** | @Leonix | Thought/speech bubble icons over NPCs | [Branch](https://github.com/TheLeonix/Pokeemerald-Expansion-TalkAndThink) | ⭐ **Medium** | Useful for researchers in the field — differentiating thinking vs. speaking. |
| **FRLG Map Previews** | @Bivurnum | Map preview images when entering new areas | [Wiki](https://github.com/Bivurnum/decomps-resources/wiki/FRLG-Map-Previews) | ⭐ **Medium** | Strong arrival moment for each of the five main locations. |
| **Namebox** | @tustin | Speaker name boxes in dialogue | [Repo](https://github.com/tustin2121/pokeemerald/) | ⭐ **High** | Story-heavy game with multiple researcher NPCs needs clear speaker identification. |

### 4.3 Gameplay Systems

| Branch | Author | Description | Source | Holon Fit | Rationale |
|---|---|---|---|---|---|
| **Fully Custom Starters** | @Archie + @Mudskip | Briefcase UI with any starter choices | [Wiki](https://github.com/pret/pokeemerald/wiki/New-Birch's-Briefcase-With-Fully-Custom-Starters-by-Archie-and-Mudskip) | ⭐ **High** | Holon needs three Delta Species starters — this is essential. |
| **Unbound Quest Menu** | @PokemonSanFran | Quest journal system (from Pokémon Unbound) | [Wiki](https://github.com/PokemonSanFran/pokeemerald/wiki/Unbound-Quest-Menu) | ⭐ **High** | If Holon uses an investigation/expedition progression structure instead of gyms, a quest log is critical infrastructure. |
| **Quest Icons** | @Belle | Quest bubbles above NPCs with available quests | [Commit](https://github.com/lienne/pokemon-starbound/commit/6fc1ea7046e10402eb068fb338d2076045b8c104) | ⭐ **High** | Pairs with Quest Menu. Visual cue for researcher NPCs with new information. |
| **Dynamic Level Scaling** | @Graion Dilach | Trainer/wild levels scale dynamically | [Branch](https://github.com/GraionDilach/spinarakgreen/tree/dynamic-scaling-on-113) | ⭐ **High** | If Holon allows non-linear exploration between the five locations, scaling is essential. |
| **Level Scaling** | @fisham33 | Alternative level-scaling implementation | [Wiki](https://github.com/fisham-org/pokeemerald-expansion-features/wiki/Level-Scaling) | ⭐ **High** | Evaluate alongside Graion Dilach's approach; pick one. |
| **Modern QoL Field Moves** | @fisham33 and @PokemonSanFran | HMs replaced with key items/contextual actions | [Wiki](https://github.com/fisham-org/pokeemerald-expansion-features/wiki/Modern-QoL-Field-Moves) | ⭐ **High** | Essential. No HM slavery; modern exploration. Research tools as key items is a thematic fit. |
| **Crafting System** | @hedara | Item crafting menu | [Branch](https://github.com/hedara90/pokeemerald-expansion/tree/crafting) | ⭐ **Low–Med** | Could tie into research (synthesizing items from Delta materials) but adds significant scope. Lower priority. |
| **Outfits System** | @mudskip | Player outfit changes | [Branch](https://github.com/mudskipper13/pokeemerald/tree/feature/outfits-system-rhh) | ⭐ **Medium** | Field researcher gear for different locations; thematically appropriate. |
| **Apricorn Trees** | @Graion Dilach | Apricorn harvesting for custom Poké Balls | [Branch](https://github.com/GraionDilach/spinarakgreen/tree/pokeemerald-expansion-apricorntrees) | ⭐ **Low** | Could fit the ancient/natural theme but is a significant side system for uncertain payoff. |
| **Variable Shop Pricing** | @Archie | Dynamic shop prices | [Branch](https://github.com/TeamAquasHideout/pokeemerald/tree/shop_pricing) | ⭐ **Low** | Not a strong fit for Holon's narrative. |
| **Fishing Minigame** (Stardew Valley style) | @Bivurnum | Interactive fishing minigame | [Wiki](https://github.com/Bivurnum/decomps-resources/wiki/Fishing-Minigame-(Stardew-Valley-style)) | ⭐ **Low–Med** | Holon Lake and Dragon Frontiers could benefit from a dedicated fishing feel. Optional side content. |
| **Select Pokémon for Battle** | @fisham33 | Choose which Pokémon to use before battle | [Wiki](https://github.com/fisham-org/pokeemerald-expansion-features/wiki/Select-Pokemon-for-Battle) | ⭐ **Medium** | Tactical depth for key encounters, especially Delta Deoxys battles. |
| **Set Preferred Follower** | @Kasen | Choose which Pokémon follows from party menu | [Branch](https://github.com/Kasenn/pokeemerald-expansion-kasen/tree/toggle_follower_from_party_menu) | ⭐ **Medium** | QoL addition; lets players show off their Delta Pokémon in the overworld. |
| **Multiuse EXP Candies / EV Items** | @Kasen | Use Exp Candies and EV items in bulk | [Branch](https://github.com/Kasenn/pokeemerald-expansion-kasen/tree/multiuse-candies-evitems) | ⭐ **Medium** | QoL for training. |
| **Upgradable Fishing Rod** | @HashtagMarky | Single fishing rod that upgrades | [Commit](https://github.com/HashtagMarky/pokeemerald/commit/d98aa33b603d26ecf536d75e2d301771198f666c) | ⭐ **Low–Med** | Cleaner than three rods if fishing is a mechanic. |
| **No Whiteout After Player Loss** | @PokemonSanFran | Player doesn't white out after losing | [Wiki](https://github.com/PokemonSanFran/pokeemerald/wiki/No-Whiteout-After-Player-Loss) | ⭐ **Low** | Expansion already has `B_FLAG_NO_WHITEOUT`; redundant. |
| **Pokémon Randomizer** | @Zetraphes | Built-in randomizer mode | [Branch](https://github.com/Zetraphes/pokeemerald-expansion/tree/tertu-randomizer) | ⭐ **Low** | Not a priority for Holon's curated Delta roster. |
| **Game Corner Expansion** | @AGSMGMaster64 | Gacha/minigame expansion | [Branch](https://github.com/agsmgmaster64/worldlinkdeluxe-ame/tree/gacha-expansion) | ⭐ **Low** | Skip unless Holon has a game corner, which doesn't fit the setting. |

### 4.4 Battle & Mechanics

| Branch | Author | Description | Source | Holon Fit | Rationale |
|---|---|---|---|---|---|
| **Mid-battle Evolutions** | @Zetraphes / @Shachar700 | Pokémon evolve during battle when conditions met | [Branch (Z)](https://github.com/Zetraphes/pokeemerald-expansion/tree/MidBattleEvo) / [Branch (S)](https://github.com/shachar700/pokeemerald-fork/tree/rhh-13.2-midBattleEvo) | ⭐ **Medium** | Transformation moments fit the Delta theme well. |
| **Dynamic Move Descriptions** | @Flash1Lucky | Move descriptions update based on context | [Branch](https://github.com/Flash1Lucky/pokeemerald-expansion/tree/dynamic-move-descriptions) | ⭐ **Medium** | Better player information; useful when Delta types change move effectiveness. |
| **Trainer Class Switch Chance** | @Pawkkie | AI switch chance varies by trainer class | [Branch](https://github.com/Pawkkie/pokeemerald-expansion/tree/trainer-class-switch-chance) | ⭐ **Medium** | Senior researchers should switch more intelligently than field staff. |
| **Ability Changer** | @Pawkkie | NPC that changes Pokémon abilities | [Branch](https://github.com/Pawkkie/pokeemerald-expansion/tree/ability-changer) | ⭐ **Low–Med** | Could be framed as a research service at the Holon lab. |
| **Use DNS in Battles** | @Kasen | Day/Night tinting applies to battle backgrounds | [Branch](https://github.com/Kasenn/pokeemerald-expansion-kasen/tree/battle-dns) | ⭐ **High** | Visual consistency between overworld and battle. Aurora effects at night during Deoxys encounters would be a strong visual moment. |
| **Camomons** | @PCG | Pokémon types match their first two moves | [Branch](https://github.com/PCG06/pokeemerald/tree/camomons) | ⭐ **Low** | Gimmick that would compete with and confuse the Delta type system. Skip. |
| **Scalemons** | @PCG | Stats scale based on BST | [Branch](https://github.com/PCG06/pokeemerald/tree/scalemons) | ⭐ **Low** | Challenge gimmick; not a fit. |
| **Wild Encounter Message Changed** | @Kaixer | Custom wild encounter text | [Branch](https://github.com/KaixerRealNewAcc/dynastic-emerald/tree/Wild-Encounter-Message-Changed) | ⭐ **Medium** | Custom encounter text for Delta Pokémon ("A Delta Charizard appeared!") would be a nice touch. |
| **OW Encounter Tools** | @HashtagMarky | Overworld encounter management tools | [Branch](https://github.com/HashtagMarky/pokeemerald/tree/ikigai/ow-encounters) | ⭐ **Low–Med** | Encounter utilities; useful for managing the Delta encounter tables across five locations. |

### 4.5 Audio & Polish

| Branch | Author | Description | Source | Holon Fit | Rationale |
|---|---|---|---|---|---|
| **B2W2 Music** | @Aichiya | Black 2/White 2 soundtrack port | [Branch](https://github.com/aichiya/pokeemerald-expansion/tree/pokeemerald-expansion-bw2-music) | ⭐ **Medium** | High quality soundtrack; good placeholder while original music is developed. BW2's atmospheric tracks suit Holon's tone. |
| **GameBoy Sounds** | @ShinyDragonHunter | Retro Game Boy-style sound option | [Branch](https://github.com/ShinyDragonHunter/pokeemerald/tree/GameboySounds) | ⭐ **Low** | Nostalgia feature; not a fit for Holon's intended tone. |
| **Trainer Voices** | @ShinyDragonHunter | Voice clips for trainers | [Branch](https://github.com/ShinyDragonHunter/pokeemerald/tree/TrainerVoices) | ⭐ **Low–Med** | Could add personality to researcher NPCs but requires significant audio work. |
| **Generic Pokémon Cries** | @HashtagMarky | Simplified cry system | [Commit](https://github.com/HashtagMarky/pokeemerald/commit/9707bda305f978e59da58aef9e8f9aa14c619696) | ⭐ **Low** | ROM space optimization if needed. |
| **Mega Cries Removal** | @lordraindance | Remove mega evolution cries to save space | [Branch](https://github.com/magical-ice-winged-otter/pokeemerald-expansion/tree/reduce-mega-cries) | ⭐ **Medium** | Mega is disabled for Holon — removing the cries saves space. |
| **Bard Phonemes Removal** | @lordraindance | Remove bard phonemes to save space | [Branch](https://github.com/magical-ice-winged-otter/pokeemerald-expansion/tree/remove-bard-audio) | ⭐ **Medium** | Saves ROM space; bard NPCs won't appear in Holon. |
| **Field Mugshot System** | @mudskip | Character mugshots in dialogue | [Branch](https://github.com/mudskipper13/pokeemerald/tree/feature/field-mugshot) | ⭐ **High** | Story-heavy game with researcher NPCs needs character portraits. Deoxys and the four fragment encounters would benefit enormously from this. |
| **Cutscene Skipping** | @HashtagMarky | Skip cutscenes on replay | [Branch](https://github.com/HashtagMarky/pokeemerald/tree/dev-cutscene-skipping) | ⭐ **Medium** | QoL for replaying and testing. |
| **Decapitalized** | @Prof. Harpe | Proper capitalization (not ALL CAPS text) | [Branch](https://github.com/prof-harpe/pokeemerald-expansion/tree/Decapitalized) | ⭐ **High** | Essential for modern text presentation. "A DELTA CHARIZARD APPEARED!" is the wrong vibe. |
| **Menu Palette Switching** | @Vol / @Phantonomy | Switch menu color palette from options | [Branch](https://github.com/Ddaretrogamer/Sun-and-Moon-Eclipse/tree/vol_start_menu_pal_switcher) | ⭐ **Low** | Nice player option but low priority. |

### 4.6 Developer / Utility

| Branch | Author | Description | Source | Holon Fit | Rationale |
|---|---|---|---|---|---|
| **Saveblock Cleansing** | @ghoulslash | Clean up saveblock data | [Branch](https://github.com/ghoulslash/pokeemerald/tree/saveblock) | ✅ **Already in expansion** | |
| **Species JSON Export** | @hedara | Export species data to JSON | [Branch](https://github.com/hedara90/pokeemerald-expansion/tree/print-mons-json) | ⭐ **Medium** | Useful for managing and auditing Delta Species data across the full roster. |
| **Givemon Competitive Sets** | @PCG | Give debug Pokémon with competitive movesets | [Branch](https://github.com/PCG06/pokeemerald/tree/givemon_sets) | ⭐ **Low** | Dev/testing utility. |
| **Technique Manual** | @Yoshord | Alternative TM system as manuals | [Branch](https://github.com/rayrobdod/pokeemerald/tree/technique_manual) | ⭐ **Low–Med** | Could be reframed as research documents distributed by the Holon team. Thematic fit if pursued. |

### 4.7 Other Notable Branches

| Source | Notes |
|---|---|
| **merrp (@aarant)** | Bundles followers, dynamic palettes, day/night, custom lighting — many are now integrated into expansion. Check [README](https://github.com/aarant/pokeemerald?tab=readme-ov-file) for any remaining unique features. |
| **tustin** | Multiple branches including the popular **Namebox** branch. Check [repo](https://github.com/tustin2121/pokeemerald/). Essential for Holon's dialogue-heavy researcher scenes. |
| **PokemonSanFran** | Excellent documentation. Branches include No Whiteout, Quest Menu, QoL Field Moves. Quest Menu especially is important if Holon uses investigation-style progression. |
| **pret pokeemerald wiki** | The base [Tutorials](https://github.com/pret/pokeemerald/wiki/Tutorials) and [Feature Branches](https://github.com/pret/pokeemerald/wiki/Feature-Branches) pages have additional branches not listed in Team Aqua's wiki. |

---

## 5. How to Pull a Feature Branch

```bash
# 1. Add the developer's repo as a remote
git remote add <remote-name> <github-url>

# Example:
git remote add Pawkkie https://github.com/Pawkkie/pokeemerald-expansion

# 2. Pull the specific branch
git pull <remote-name> <branch-name>

# Example:
git pull Pawkkie start-menu-clock
```

> [!IMPORTANT]
> **Always** create a dedicated branch in your project before pulling a feature branch:
> ```bash
> git checkout -b feature/start-menu-clock
> git pull Pawkkie start-menu-clock
> # Test thoroughly, then merge into your main working branch
> ```

---

## 6. Recommendations for Pokémon Holon

Based on Holon's core elements — scientific accident, five-location spread, ancient ruins and carvings, Delta Species type mutations, four fractured Deoxys fragments, researcher NPCs, investigation-style discovery — here are the **priority tiers**.

### 6.1 Tier 1 — Essential (Enable or Pull Early)

| Feature/Branch | Why |
|---|---|
| **Disable all battle gimmicks** (built-in, config) | Mega, Z-Moves, Dynamax, Tera all conflict with or dilute Delta Species as the game's identity. |
| **Delta Species as custom species entries** (custom work) | This is the game's core mechanic and requires early architectural decisions about species slots, Pokédex structure, and saveblock. Not a toggle — it's a design commitment. |
| **Day/Night System** (built-in) | Atmosphere and aurora visual hooks near the Holon Tower. |
| **Follower Pokémon** (built-in) | Delta type followers make the phenomenon visible in the overworld without any dialogue. |
| **Decapitalized** (feature branch) | Modern text presentation. Pull this early before writing any dialogue. |
| **Modern QoL Field Moves** (feature branch) | No HM slavery; research tools as key items fits the setting. |
| **Fully Custom Starters** (feature branch) | Three Delta Species starters; not Hoenn defaults. |
| **Namebox** (feature branch) | Multiple researcher NPCs in a story-heavy game need speaker identification. |
| **Free saveblock space** (config) | Delta species data and fragment tracking will need the room. Free everything you're not using. |
| **DexNav** (built-in, enable in config) | Reframe as the research team's field scanner. Thematically essential. |

### 6.2 Tier 2 — Strongly Recommended

| Feature/Branch | Why |
|---|---|
| **Field Mugshot System** (feature branch) | Researcher portraits in dialogue, and especially for the four Delta Deoxys encounters. |
| **Alpha Blended Maps** (feature branch) | Mirage Forest fog; ancient ruin atmosphere; the Tower's visual weight. |
| **Dynamic Palettes** (feature branch) | Show the Delta spread's progression visually as the player moves between locations. |
| **Unbound Quest Menu** (feature branch) | Critical if using investigation/expedition progression instead of gyms. |
| **Quest Icons** (feature branch) | Pairs with Quest Menu for researcher NPC interactions. |
| **New Main Menu** (feature branch) | Sets Holon's tone immediately on boot — stone tablet imagery, Mirage Forest. |
| **Town Map Port** (feature branch) | Five locations across land and ocean need a clear, well-built region map. |
| **Dynamic Level Scaling** (feature branch) | Non-linear exploration between the five locations requires this. |
| **HGSS-style Pokédex** (built-in) | More detailed dex; could surface Delta type information prominently. |
| **Battle DNS** (feature branch) | Aurora lighting during nighttime Deoxys encounters is a strong visual moment. |
| **Reusable TMs** (built-in, config) | Modern expectation. |
| **Level Caps** (built-in, config) | Tie to fragment discovery milestones rather than badges. |

### 6.3 Tier 3 — Worth Considering

| Feature/Branch | Why |
|---|---|
| **NPC Followers** | Researcher NPCs traveling with the player in specific sections |
| **Help Window** | Delta type info and research notes accessible in the field |
| **Wild Encounter Message Changed** | Custom text for Delta encounters |
| **Talk and Think Icons** | Researcher NPC expressiveness |
| **Start Menu Clock** | Practical with DNS active |
| **FRLG Map Previews** | Arrival moment for each major location |
| **Mega Cries / Bard Phonemes Removal** | ROM space — Mega is disabled; Bard NPCs won't appear |
| **Mid-battle Evolutions** | Transformation moments fit the Delta theme |
| **Species JSON Export** | Audit and manage Delta species data |
| **Outfits System** | Field researcher gear; location-appropriate clothing |
| **Select Pokémon for Battle** | Tactical depth for Delta Deoxys encounters |
| **B2W2 Music** | Atmospheric placeholder while original tracks are composed |
| **Cutscene Skipping** | QoL for development and replay |
| **Ambient Pond Ripples** | Holon Lake environmental polish |
| **Fishing Minigame** | Optional side content at Holon Lake / Dragon Frontiers |

### 6.4 Tier 4 — Low Priority / Skip

| Feature/Branch | Why |
|---|---|
| Sky Battles, Inverse Battles (most cases), Camomons, Scalemons, Game Corner Expansion, Pokémon Randomizer, Rotom Phone Menu, Seasons, Pokevial, Catch Mode Toggle | Niche, gimmicky, tonally off, or actively conflicts with Delta Species as the game's central mechanic |
| Affection mechanics | Breaks difficulty balance |
| Frostbite | Non-standard status; would confuse players |
| Mega Evolutions, Regional Forms, Fusion Forms | Not part of Holon's lore; disable to keep Delta Species as the sole transformation identity |
| SwSh UI branches | SwSh aesthetic is too recent and tonally mismatched for a TCG Gen 3 arc setting |

---

## Sources

| Source | URL |
|--------|-----|
| pokeemerald-expansion GitHub | https://github.com/rh-hideout/pokeemerald-expansion |
| FEATURES.md | https://github.com/rh-hideout/pokeemerald-expansion/blob/master/FEATURES.md |
| INSTALL.md | https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md |
| Team Aqua's Asset Repo — Feature Branches Wiki | https://github.com/Pawkkie/Team-Aquas-Asset-Repo/wiki/Feature-Branches |
| pret pokeemerald wiki | https://github.com/pret/pokeemerald/wiki |
| pokeemerald-expansion Documentation | https://rh-hideout.github.io/pokeemerald-expansion/ |
| Config files | `include/config/*.h` in the expansion repo |

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 1.0 | 2026-03-22 | Reorganized from original GDD; no content changes |

---

*Pokémon Holon Legends — pokeemerald-expansion Features & Branch Guide | HL-TEC-002 v1.0 | Last updated 2026-03-22*
