# Holon Pokémon Emerald — Feature Branch Plan

Base: pokeemerald-expansion (rh-hideout)
Sources cross-referenced against Team Aqua's Hideout Feature Branches wiki (github.com/TeamAquasHideout/Team-Aquas-Asset-Repo/wiki/Feature-Branches) and pret/pokeemerald's Feature Branches wiki.

---

## 1. Community Feature Branches

| # | Feature | Author / Branch | Description |
|---|---------|------------------|-------------|
| 1 | HGSS Darkest Mode | RavePossum — `hgss_dex_darkest_mode` | Adds a true darkest color mode to the HGSS-style Pokédex, refactoring color-mode handling for easier future additions. |
| 2 | Registered Item Menu | TheXaman / iriv24 — `tx_registered_items_menu` | ORAS-style key item wheel; register up to 4 key items for quick field access without digging through the bag. |
| 3 | Fishing Minigame | Bivurnum — `fishing-minigame` | Stardew Valley-style interactive fishing minigame replacing the vanilla instant-catch fishing rod interaction. |
| 4 | Castform Weather Change | wiz1989 — `castform_weather_change` | Standalone branch (not just a config flag) — adds sandstorm-form sprites, makes weather-based moves trigger Castform's Forecast change *before* the attack resolves (for potential STAB), and handles Primal weather / Gastro Acid / Neutralizing Gas interactions. |
| 5 | Ditto Face Support | AsparagusEduardo | Named branch confirmed on the wiki; preserves/handles Ditto's face during transform-related animations. |
| 6 | Gacha Expansion | AGSMGMaster64 — Expansion-Compatible Game Corner Expansion | No standalone "Gacha" branch exists; Gacha Machines are bundled into this Game Corner Expansion port alongside other arcade games. |
| 7 | Unbound Quest Menu + Quest Icons | psf (menu) + Belle (icons) | Quest tracking menu ported from Pokémon Unbound, extended with Belle's Quest Icon bubbles that appear over NPCs who have available quests. |
| 8 | DNS in Battles | Kasen — `battle-dns` (Expansion 1.14.2) | Applies the Day/Night System's palette shading to battle backgrounds (and optionally battler sprites). Requires Expansion's built-in DNS already enabled; compatibility with other DNS forks (Sierraffinity, Merrp) not guaranteed. |

---

## 2. Optional

| # | Feature | Author / Branch | Description |
|---|---------|------------------|-------------|
| 9 | Mudskip Player Face Sprites | mudskip — Field Mugshot System | Displays a character portrait/mugshot during dialogue via `createfieldmugshot` / `{CREATE_MUGSHOT}`. Confirm scope — if a main-menu or trainer-card mugshot was intended instead, that's a separate branch (Archie's "New Main Menu with Mudskip"). |

---

## 3. Custom / Holon-Original Branches

No existing community source — built from scratch for this game.

### 10. Overworld Camp
Start-menu option that opens a simplified, square/rectangular version of the player's current map, using the same tileset/vibe as the source location. Full party wanders freely; supports player-to-Pokémon and Pokémon-to-Pokémon interaction, including feeding.

- **Base systems to lean on:** follower Pokémon movement code (for multi-Mon autonomous wandering), a feed/interact script bank per species or species group, saveblock flag for affection/friendship gain if feeding should matter mechanically.
- **Key risk:** up to 6 simultaneous autonomous party-object events in one map — object-event slot budget needs prototyping with 2–3 Mons first before scaling to a full party.

### 11. Shiny Party/Box Icons
Adds shiny-awareness to the icon rendering system across party menu, PC box, trade screen, mail, and Battle Dome roster.

- **Why it's needed:** confirmed that current pokeemerald-expansion mainline does not carry this — the "icons share palettes with front sprites" feature exists only in aarant's older `lighting` branch (never merged into rh-hideout mainline per their own 1.9.0 changelog), and the icon system has since been refactored (old `gMonIconTable` removed in 1.8.0), so that older branch's diff won't apply cleanly.
- **Proven precedent:** front sprites already do this exact shiny/palette branch via `GetMonSpritePalFromSpeciesIsEgg(species, isShiny, isFemale, isEgg)` in current mainline `pokemon.c`. The icon version follows the same pattern.
- **Scope:** add a shiny check to whatever populates the icon palette index at each of the 5 render call sites; add or derive a shiny icon palette per species (deriving from existing shiny front-sprite work is far less art labor than hand-painting).

### 12. HMs — Unlearnable / Overwritable
Keep HMs in the game as actual moves (no Devon Key or item-based replacement), but change how they occupy moveset slots: HMs become forgettable/overwritable like any normal TM move, instead of being permanently stuck once taught. Removes the classic "HM slave" problem without removing HMs from the game or adding a new key-item system.

- **Scope:** likely a config-level change to the move-learning/forgetting logic (removing the special-case check that blocks forgetting HM moves via Move Deleter or level-up replacement), rather than new UI or new items.
- **Submarine Icon still applies:** the player's overworld sprite still swaps to a submarine graphic while Dive is active in the field — this stays as its own small visual branch even without the Devon Key consolidation.

### 13. Delta Pokédex / Delta Filter
Two implementation options, final call pending:

- **Option A — Filter/sort mode on existing HGSS Pokédex:** add a toggle or sort category isolating Delta Species within the current dex list. Smaller lift — hooks into existing list-generation/sort logic.
- **Option B — Dedicated Delta Registry screen:** standalone research-log-style menu, one entry per Delta Species showing original form, Delta form, type change, and location/lore blurb. Larger lift (new UI screen, new data table) but stronger thematic payoff — reinforces the "player as field researcher" identity and can gate entries behind discovery status for investigation pacing.

### 14. Custom Start Menu
A redesigned start menu UI reflecting Holon's identity rather than the vanilla Emerald layout — new background art/theme, icon set, and entry ordering that surfaces the game's own systems (e.g. Camp, Delta Registry) alongside the standard Pokémon/Bag/Save options. Scope and exact entry list TBD — flag any specific layout, art direction, or menu behavior you want and this entry can be filled in with detail.

---

## Notes on Overall Scope

The identity-defining items are **Overworld Camp**, **Shiny Icons**, **Submarine Icon**, and **DNS in Battles** — these are the ones that will read as "Holon feels different" rather than "Holon has QoL polish." Community branches like Gacha Expansion, HGSS Darkest Mode, Registered Item Menu, and Castform Weather Change are good hygiene but don't build distinctiveness on their own. Given the number of custom systems plus eight community branches to integrate and test, consider prioritizing the identity-defining items first if scope needs to be trimmed.
