# Prologue Implementation Plan (v2)

Status: Step 0 in planning. Branch: TBD (must contain the StarterTown porymap commit `9961e0da68` from `first-porymap` — either branch off `first-porymap` or cherry-pick that one commit onto a fresh branch off the current work branch).
Target flow (player-facing):

0. Choose player gender + name
1. Boat intro with Steven's recruitment letter (interspersed with sailing visuals)
2. Player, Ty, and Grandma arrive together
3. Exit boat, through reception, greeted by aide
4. Goodbye to Grandma; aide gives a quick town tour (reception, houses, lab)
5. Tour ends back at reception; told to settle into the house
6. Go home, see Grandma, set clock / check room
7. Go to lab, meet Cozmo (Ty already there); player confirms/edits Ty's name
8. Cozmo speech + starter choice (balls on table)
9. Pick starter, receive Pokedex
10. Leave lab — Ty battles outside, then gives running shoes
11. Prologue ends — free roam town/reception before Route 1

Decisions locked:
- Step 0 is a **Steven reskin of the existing Birch intro cutscene** (`CB2_NewGameBirchSpeech` in `src/main_menu.c`) — keep the whole task chain, swap sprite + text + released species, insert the shiny menu. NOT a rewrite/strip. Full breakdown in the Step 0 section.
- The recruitment letter is **delivered in Step 0** (Steven reads it to you). Step 1's boat cutaways are therefore the **player's internal monologue**, not letter fragments.
- Boat scene uses the **FRLG Seagallop ferry cutscene** (`src/seagallop.c`), NOT the Emerald SS Tidal porthole.
- Boat scene uses **option (c): alternating short legs** — black-screen thought fragment, then one full-screen ferry leg, alternating sail direction, repeat; final leg fades in on the dock.
- `DoSeagallopFerryScene` is **already a registered special** (`data/specials.inc:597`) — reuse it. No new special, no new header, no new constants file.
- Ty battle (step 10) is **narrative-only** (proceed win or lose) unless changed.

---

## Step 0 — Character creation (before the player spawns)

Gender, name, and a new custom **shiny-rate** menu, delivered as a **Steven reskin of the existing Birch intro cutscene**. No boat in this step.

### Design: reskin, don't rebuild

The gender menu, naming screen, and the Brendan/May preview sprites are **scaffolding inside the Birch-speech task chain** in `src/main_menu.c` (`CB2_NewGameBirchSpeech` + `Task_NewGameBirchSpeech_*`, ~line 1290-2310). "Birch" is only: the intro sprite, the Lotad release beat, and the narrator text. This expansion's the chain ends `AreYouReady -> ShrinkPlayer -> FadePlayerToWhite -> Cleanup -> CB2_NewGame`.

So instead of deleting ~15 tasks and rewiring, **keep the whole chain and reskin it**: Birch sprite -> Steven, Birch narration -> Steven's recruitment letter, Lotad -> a Delta Pokémon, plus the shiny menu inserted before the wrap-up. The floating-platform void is read as stylized/dreamlike (Steven addressing you), not a literal location; the shrink-to-white ending leads into the boat (Step 1).

**Ordering hazard:** the screen runs **before** `NewGameInitData()` (`Task_NewGameBirchSpeech_Cleanup` -> `SetMainCallback2(CB2_NewGame)` `src/overworld.c:1927` -> `NewGameInitData()` `:1932`). `NewGameInitData` calls `InitEventData()`, which **zeroes every var**. Player name/gender survive (they live in `gSaveBlock2`, untouched by the save clear); anything written to a `VAR_` during the menu would be wiped — see 0.3.

### 0.2 — Reskin the cutscene as Steven + letter

Flow is unchanged from vanilla except text/art and the inserted shiny menu:
`Init` -> Steven fades in -> letter (welcome / "this is Holon" + Delta mon release / main body / sign-off) -> gender menu -> naming -> name yes/no confirm -> **shiny-rate menu** -> Steven closing line -> shrink player -> fade white -> `Cleanup` -> `CB2_NewGame`.

- **Art swap** — point at the existing Steven battle pic; no new asset needed:
  - The intro sprite is loaded via `sNewGameBirch_Gfx` / `sNewGameBirch_Pal` (`src/field_effect.c:272-274`, `INCGFX_U32/U16("graphics/birch_speech/birch.png", ...)`) + `sSpriteTemplate_NewGameBirch` (`:380`); instantiated by `AddNewGameBirchObject` (`field_effect.c:1025`), called from `AddBirchSpeechObjects` (`src/main_menu.c:1919`) at spawn point `(0x88, 0x3C)` = (136, 60).
  - Repoint **both** `sNewGameBirch_Gfx` and `sNewGameBirch_Pal` to `graphics/trainers/front_pics/steven.png` — already 64x64 / 4bpp / 16-colour, same format as `birch.png`. Use the Emerald `steven.png`, not `champion_steven_frlg.png`.
  - Expected tweaks: (a) a Y nudge at the spawn point — `steven.png` is a VS-screen battle pose, framed differently from Birch's full-body intro pose; (b) eyeball the palette against the Brendan/May trainer palettes loaded alongside.
  - Optional later polish: a bespoke intro-pose Steven if the battle stance reads stiff on the platform.
- **Delta mon release beat** (keep the choreography, swap the species):
  - `NewGameBirchSpeech_CreateLotadSprite` (`main_menu.c:1907`) hardcodes `SPECIES_LOTAD` in `CreateMonPicSprite_Affine`. Change to a **non-starter Delta species** (`SPECIES_<DELTA_TBD>` — pick one that isn't one of the 3 lab starters; repo already has delta Dratini / Bagon / Ralts sets).
  - `Task_NewGameBirchSpeechSub_InitPokeBall` (`main_menu.c:1400`) passes `SPECIES_LOTAD` to `CreatePokeballSpriteToReleaseMon` — change to the same species.
  - Retext `_ThisIsAPokemon` (`main_menu.c:1377`): Steven introduces Holon / Delta Pokémon as the hook instead of "This is a Pokémon."
- **Text swap** — replace the `gText_Birch_*` strings referenced by `_WaitForSpriteFadeInWelcome` (`gText_Birch_Welcome`), `_ThisIsAPokemon` (`gText_ThisIsAPokemon`), `_MainSpeech` (`gText_Birch_MainSpeech`), `_AndYouAre` (`gText_Birch_AndYouAre`), `_BoyOrGirl` (`gText_Birch_BoyOrGirl`), `_WhatsYourName` (`gText_Birch_WhatsYourName`), `_SoItsPlayerName` (`gText_Birch_SoItsPlayer`), `_AreYouReady` with new `gText_Intro_*` strings: letter fragments + Steven-voiced (or neutral) gender/name prompts + a closing line. Same `msgbox` / `StringExpandPlaceholders` / `AddTextPrinterForMessage` calls.
- **BGM** — `Task_NewGameBirchSpeech_Init` plays `MUS_ROUTE122`; swap for Steven's theme or something calm/wistful. Minor, can defer to the art/music pass.
- **Insert the shiny menu** — `_ProcessNameYesNoMenu` case 0 (confirmed, `main_menu.c:1660`) currently -> `_SlidePlatformAway2`. Reroute -> new `Task_NewGameIntro_ShinyRateMenu` (0.3), which on completion -> `_SlidePlatformAway2` (unchanged from there on).
- **Rename** (optional, do last): `*BirchSpeech*` -> `*Intro*` throughout `main_menu.c`. Skip for now if it balloons the diff.
- No truck: nothing from `InsideOfTruck_EventScript_SetIntroFlags` is needed.

### 0.3 — Shiny-rate menu

New task `Task_NewGameIntro_ShinyRateMenu`, entered from `_ProcessNameYesNoMenu` case 0 and exiting to `_SlidePlatformAway2` (see 0.2). Reuse the existing list-menu primitives already in `main_menu.c` (same style as the gender/yes-no menus). Prompt text can be Steven-voiced or neutral, e.g. "How often should Shiny Pokémon cross your path?".

Odds in pokeemerald are **numerator / 65536** (`SHINY_ODDS` = 16 in `include/constants/pokemon.h:104` -> 1/4096). Ladder (menu shows labels; table in C is source of truth, tweak freely):

No "Off" and no "Always" — every choice is a real, playable rate.

| Index | Label | num/65536 | Approx rate |
|---|---|---|---|
| 0 | Rare | 8 | 1/8192 |
| 1 | Uncommon | 16 | 1/4096 |
| 2 | **Classic** (default cursor) | **32** | **1/2048** |
| 3 | Frequent | 128 | 1/512 |
| 4 | Common | 512 | 1/128 |

- **Storage:** repurpose a second unused var as `VAR_HOLON_SHINY_RATE`, holding the **index 0-4**, not the raw numerator.
- **Ordering hazard (0.1):** the menu writes an **EWRAM global** (e.g. `static u8 sNewGameShinyRateIndex;`), NOT the var. The var is set from that global at the **tail of `NewGameInitData()`** — same guard pattern `NewGameInitData` already uses to carry `rivalName` across the clear (`src/new_game.c:164-220`). Reset the global to index 2 (Classic) at `Init`.
- **Consumption:** add `u32 GetPlayerShinyOdds(void)` — reads `VarGet(VAR_HOLON_SHINY_RATE)`, returns `sShinyOddsTable[index]`. Store `index + 1` so 0 = "not chosen yet" -> treat as Classic (index 2); clamp out-of-range to Classic. Swap the `SHINY_ODDS` literals in the shiny-value comparisons for `GetPlayerShinyOdds()`: `src/pokemon.c:893`, `:899` (`ComputePlayerShinyOdds`), `:983` (`CreateBoxMon`), `:2502` (`MON_DATA_IS_SHINY`), `:2934` (`SetBoxMonData` shinyModifier). Leave the `SHINY_ODDS` `#define` as the compile-time default.

### 0.4 — Warp repoint (`src/new_game.c:136`)

Rename `WarpToTruck()` -> `WarpToPrologueStart()`. Non-FRLG branch (this is an Emerald base, `IS_FRLG == 0`):
`SetWarpDestination(MAP_GROUP(MAP_STARTER_TOWN), MAP_NUM(MAP_STARTER_TOWN), WARP_ID_NONE, dockX, dockY);`
Leave the FRLG branch as-is. Update the one caller in `NewGameInitData()` (`new_game.c:214`). `MAP_STARTER_TOWN` / `MAP_GROUP` / `MAP_NUM` macros are generated from `map_groups.json` in commit `9961e0da68` — that commit must be in the branch. `dockX/dockY` come from the Porymap layout (below).

### 0.5 — State var + StarterTown script stub

- `#define VAR_HOLON_PROLOGUE_STATE VAR_UNUSED_0x404E` in `include/constants/vars.h:100`. Value 0 after new game (automatic — `InitEventData` zeroes it).
- New `data/maps/StarterTown/scripts.pory` replacing the `scripts.inc` stub. Poryscript is already wired in the Makefile on the work branch (`Makefile:418`, `:442`); the `.include data/maps/StarterTown/scripts.inc` line into `data/event_scripts.s` is in commit `9961e0da68`. Delete the hand-written `scripts.inc` (autogen replaces it).
- Step 0 content = **no boat**:
  ```
  StarterTown_MapScripts {
      MAP_SCRIPT_ON_TRANSITION: StarterTown_OnTransition
  }
  StarterTown_OnTransition {
      // Step 0: nothing — player just spawns on the dock and can walk.
      // (the boat step adds MAP_SCRIPT_ON_FRAME_TABLE gated on VAR_HOLON_PROLOGUE_STATE == 0 for the boat intro.)
  }
  ```
  Optionally `setvar(VAR_HOLON_PROLOGUE_STATE, 1)` at the end so the boat step's state machine has a starting hook — but leaving it 0 is fine; the boat step will own that transition.

### 0.6 — Dependencies on Matt (outside code)

1. Branch that contains `9961e0da68` (StarterTown porymap setup).
2. A rough walkable dock area + player spawn painted in Porymap. `LAYOUT_STARTER_TOWN` = 28x24, `gTileset_General` (primary) + `gTileset_Slateport` (secondary — has harbor/dock metatiles). Provide the spawn tile `(x, y)` for 0.4.

### 0.7 — Step 0 sub-order

Two independent halves — do them in either order, they only meet at "new game -> intro -> walk on the dock".

**Intro half (map-independent, `main_menu.c` / `pokemon.c` / `new_game.c`):**
1. Text swap: new `gText_Intro_*` strings, repoint the `_WaitForSpriteFadeInWelcome` / `_ThisIsAPokemon` / `_MainSpeech` / `_AndYouAre` / `_BoyOrGirl` / `_WhatsYourName` / `_SoItsPlayerName` / `_AreYouReady` message calls. Build + verify the cutscene still flows.
2. Delta mon in the release beat: swap `SPECIES_LOTAD` in `NewGameBirchSpeech_CreateLotadSprite` + `Task_NewGameBirchSpeechSub_InitPokeBall`.
3. Shiny-rate menu (0.3): EWRAM global + `Task_NewGameIntro_ShinyRateMenu` (entered from `_ProcessNameYesNoMenu` case 0, exits to `_SlidePlatformAway2`) + `sShinyOddsTable` + `GetPlayerShinyOdds()` + swap the 5 `pokemon.c` call sites + write-back at the tail of `NewGameInitData`. Verify with a debug print / known seed.
4. (Optional) spawn-point Y nudge for the Steven pic; BGM swap.

**Map half (needs commit `9961e0da68` in the branch):**
5. `VAR_HOLON_PROLOGUE_STATE` define + `scripts.pory` stub + delete `scripts.inc`.
6. Warp repoint in `new_game.c` -> `MAP_STARTER_TOWN` at the Porymap spawn coords.
7. Build + verify: new game -> intro -> stand on the dock, walkable.

8. (Optional, last) rename pass `*BirchSpeech*` -> `*Intro*`.

---

## Shared infrastructure

Script style: Poryscript (build auto-generates `.inc` from `data/**/*.pory`). New `data/maps/StarterTown/scripts.pory` replaces the stub `.inc`.

State vars:
- `VAR_HOLON_PROLOGUE_STATE` = repurpose `VAR_UNUSED_0x404E`.
- `VAR_HOLON_SHINY_RATE` = repurpose a second unused var (pick from the `VAR_UNUSED_*` block; not `VAR_LOTAD_SIZE_RECORD 0x404F` — that one is live). Holds `shinyRateIndex + 1` (index 0-4, 0 = not chosen -> Classic).

| Value | Meaning |
|---|---|
| 0 | New game — boat intro pending |
| 1 | Disembark + reception + aide greeting |
| 2 | Goodbye to Grandma + town tour |
| 3 | Tour done — free to walk home |
| 4 | Met Grandma / clock set — free to go to lab |
| 5 | In lab — name confirm + Cozmo speech + starter |
| 6 | Got starter + Pokedex — leaving lab |
| 7 | Ty battle done + running shoes given |
| 8 | Prologue complete — full free roam, Route 1 open |

"Normal town" logic gates on `>= 8`.

Flags (from `FLAG_UNUSED_0x02x` block): `FLAG_HIDE_PROLOGUE_TY_DOCK`, `_TY_RECEPTION`, `_TY_LAB`, `_TY_TOWN`, `_GRANDMA_DOCK`, `_GRANDMA_HOME`, `_AIDE_RECEPTION`, `_COZMO_LAB`, `FLAG_HOLON_PROLOGUE_DONE`, `FLAG_HOLON_ROUTE1_BLOCKED`.

New maps: `StarterTown` (exists — add dock tiles, reception + 2 house + lab exteriors, Route 1 exit/blocker), `StarterTown_Reception`, `StarterTown_PlayersHouse_1F`, `StarterTown_TysHouse`, `StarterTown_Lab`, Route 1 stub.

Object gfx: Ty (reuse OW rival sprites), Grandma (reuse elderly-woman OW), Aide (reuse scientist OW). Cozmo needs a NEW OW sprite — none in this base; use a scientist gfx interim.

---

## Step 1 — Boat / introspection scene (FRLG Seagallop, alternating legs)

Player spawns hidden on the dock; StarterTown `ON_FRAME` (runs while black, before fade-in) plays: **a thought fragment** on black -> one ferry leg -> next thought -> next leg (opposite direction) -> ... -> final leg fades in on the dock with Ty + Grandma beside the player.

The letter was already read in Step 0, so these black-screen boxes are the player's **internal monologue** — turning the letter over, picturing Holon, wondering why Steven picked them, half-listening to Ty. Text symbols: `Prologue_Text_Thought1..N` (was `Prologue_Text_Letter1..5`). Mechanically identical — `msgbox` on black between `DoSeagallopFerryScene` legs; count/length flexible.

### C changes — one file, `src/seagallop.c`, all gated on `gSpecialVar_0x8005 != 0`

Add 3 `#define`s to the EXISTING `include/constants/seagallop.h`:
`PROLOGUE_BOAT_LEG_W 1`, `PROLOGUE_BOAT_LEG_E 2`, `PROLOGUE_BOAT_LEG_FINAL 3` (0 = normal ferry, untouched).

1. `GetDirectionOfTravel()` — early return: `LEG_W` -> `DIRN_WESTBOUND`; `LEG_E` / `LEG_FINAL` -> `DIRN_EASTBOUND`. Drives water tilemap + ferry-sprite flip = the directional beat.
2. `Task_Seagallop_1` — if `gSpecialVar_0x8005 != 0`, skip `Overworld_FadeOutMapMusic()` so the sea theme is continuous across legs. Still runs `WarpFadeOutScreen()` (want black at leg end).
3. `Task_Seagallop_2` — if `gSpecialVar_0x8005 != 0`, call `ReturnFromPrologueLeg()` + `DestroyTask` instead of `Task_Seagallop_3()`.
4. New `static void ReturnFromPrologueLeg(void)`:
```c
FreeFerrySpriteResources();
Free(sBg3TilemapBuffer);
FreeAllWindowBuffers();
if (gSpecialVar_0x8005 == PROLOGUE_BOAT_LEG_FINAL)
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);   // fades in -> reveals dock
else {
    gFieldCallback = FieldCB_ContinueScript;   // resumes script, screen stays black
    SetMainCallback2(CB2_ReturnToField);
}
```
`FieldCB_ContinueScript` only calls `ScriptContext_Enable()` (no fade) so mid-intro legs return on black and the next `msgbox` renders on black. Confirm `gFieldCallback` vs `gFieldCallback2` in this base.

Fixed 140-frame legs. No per-leg frame-count hook. No new function/special/header/file beyond the above.

### Script — `data/maps/StarterTown/scripts.pory`

```
StarterTown_MapScripts {
    MAP_SCRIPT_ON_TRANSITION: StarterTown_OnTransition
    MAP_SCRIPT_ON_FRAME_TABLE [ VAR_HOLON_PROLOGUE_STATE, 0: Prologue_EventScript_BoatIntro ]
}

StarterTown_OnTransition {
    if (var(VAR_HOLON_PROLOGUE_STATE) == 1)   // place Ty + Grandma on the dock beside player
    ...
}

Prologue_EventScript_BoatIntro {
    lockall
    setflag(FLAG_HIDE_MAP_NAME_POPUP)
    playbgm(MUS_<sea theme>, TRUE)
    msgbox(Prologue_Text_Thought1)                      // screen already black

    setvar(VAR_0x8005, PROLOGUE_BOAT_LEG_W)
    special(DoSeagallopFerryScene); waitstate
    msgbox(Prologue_Text_Thought2)

    setvar(VAR_0x8005, PROLOGUE_BOAT_LEG_E)
    special(DoSeagallopFerryScene); waitstate
    msgbox(Prologue_Text_Thought3)

    setvar(VAR_0x8005, PROLOGUE_BOAT_LEG_W)
    special(DoSeagallopFerryScene); waitstate
    msgbox(Prologue_Text_Thought4)
    msgbox(Prologue_Text_Thought5)                      // "...whatever's waiting, I guess I'll find out."

    setvar(VAR_HOLON_PROLOGUE_STATE, 1)
    setvar(VAR_0x8005, PROLOGUE_BOAT_LEG_FINAL)
    special(DoSeagallopFerryScene); waitstate           // fades IN on the dock

    applymovement(player, disembark); applymovement(LOCALID_TY, disembark_behind)
    waitmovement(0)
    setvar(VAR_0x8005, 0)                               // reset so real ferries work
    clearflag(FLAG_HIDE_MAP_NAME_POPUP)
    releaseall
}
```
---

## Steps 2-5 — reception, aide, goodbye, tour

- State 1 -> reception: entering `StarterTown_Reception`, `ON_FRAME` runs the aide greeting, walk everyone out front, set state 2.
- State 2 -> goodbye + tour: Grandma farewell, `removeobject` Grandma. Aide leads with paired `applymovement` (aide N tiles; player follows one beat behind). One-line `msgbox` at reception desk -> houses -> lab exterior. Ty tags along via `create_follower_npc` (`FNPC_ENABLE_NPC_FOLLOWERS` already on). End at reception, set state 3.
- State 3: aide "settle into your house," `removeobject` aide, `releaseall`.

## Step 6 — home

`StarterTown_PlayersHouse_1F` `ON_TRANSITION` at state <= 3: Grandma downstairs. Talk -> clock-set (reuse `EventScript_SetWallClock` body) -> optional bedroom beat. Leaving with clock set -> state 4.

## Steps 7-9 — lab, name confirm, starter, Pokedex

Port from `data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc`:
- `ON_TRANSITION` state 4: Cozmo at desk, Ty by the table.
- Greetings, then rival-name confirm: `msgbox("...{RIVAL}, right?", YES_NO)` -> on NO `namingscreen(NAMING_SCREEN_RIVAL)`, re-confirm.
- Speech + starter table: adapt `PalletTown_ProfessorOaksLab_ChooseStarterScene` (line 199) — 3 balls as objects, YES/NO each.
- On pick: `givemon`, `setflag(FLAG_STARTER_CHOSEN)`, hide other balls, nickname prompt, Cozmo gives Pokedex (`setflag FLAG_SYS_POKEDEX_GET` + give-dex special). Set state 6.

## Steps 10-11 — Ty battle, running shoes, cleanup

Adapt `PalletTown_ProfessorOaksLab_EventScript_RivalBattle` (line 288) on the lab exterior:
- Lab-exterior `ON_FRAME` state 6: Ty blocks path, `msgbox`, `trainerbattle_no_intro` with the type-disadvantaged starter.
- After battle (win or lose — narrative only): Ty gives running shoes — `setflag(FLAG_SYS_B_DASH)` + give-item message (reuse Littleroot `ReceiveRunningShoes` body). Set state 7.
- Cleanup: `setflag(FLAG_HOLON_PROLOGUE_DONE)`, `setvar(VAR_HOLON_PROLOGUE_STATE, 8)`, clear temp hide flags, move Ty to permanent spot, `setrespawn` to player's house, `clearflag(FLAG_HOLON_ROUTE1_BLOCKED)`.

---

## Build order

| M | Deliverable |
|---|---|
| M1 | Step 0 (see full breakdown above): Steven reskin of the Birch intro (repoint sprite at `steven.png` + text swap + Delta mon in the release beat), shiny-rate menu (`VAR_HOLON_SHINY_RATE` + `GetPlayerShinyOdds()`), `new_game.c` warp -> StarterTown dock, `VAR_HOLON_PROLOGUE_STATE` define + `scripts.pory` stub. No boat. Intro half (main_menu/pokemon) is map-independent; can land before the StarterTown map exists. |
| M2 | `seagallop.c` branch + one leg fired from a script, returning to field on black. |
| M3 | Full boat intro: 3 legs + ~5 introspection boxes + final leg dock reveal with Ty & Grandma. |
| M4 | Reception + aide greeting + Grandma farewell (stub dialogue). |
| M5 | Tour choreography. |
| M6 | Home + Grandma + clock. |
| M7 | Lab: name confirm + speech + starter + Pokedex (port from FRLG Oak's Lab). |
| M8 | Ty battle + running shoes + cleanup. |
| M9 | Art (optional bespoke Steven intro pose, Cozmo sprite, dock tiles), music (Steven intro BGM, sea theme), final text (letter, thoughts). |

## Open items

1. ~~Step 0 gender menu~~ — RESOLVED: keep the sprite-preview menu.
2. ~~Step 0 approach~~ — RESOLVED: Steven reskin of the Birch cutscene, not a strip/rewrite.
3. Ty battle loss: narrative-only (assumed) vs heal + retry.
4. Shiny ladder labels/values (0.3 table) — placeholder, Matt to finalize wording and denominators. (No "Off"/"Always" — cut as too gimmicky.)
5. **Which Delta species** appears in the Step 0 release beat — must be a non-starter Delta (repo has delta Dratini / Bagon / Ralts sets). Decide once the 3 lab starters are locked.
6. ~~Step 0 intro sprite~~ — RESOLVED: repoint `sNewGameBirch_Gfx`/`_Pal` at `graphics/trainers/front_pics/steven.png` (existing 64x64 pic). Bespoke intro pose optional later.
7. Rename pass `*BirchSpeech*` -> `*Intro*` — do now or defer to a later cleanup commit.

## Reference points already located in the codebase

- `src/new_game.c:136` — `WarpToTruck()` sets the first warp (FRLG branch -> PalletTown 2F; Emerald/normal -> InsideOfTruck). Caller: `NewGameInitData()` at `new_game.c:214`; `rivalName` preserve pattern across the save clear at `new_game.c:164-220`.
- `src/main_menu.c` — `CB2_NewGameBirchSpeech`, `Task_NewGameBirchSpeech_*` gender + naming flow. Task chain map in the file's header comment ~line 111-165. Key tasks: `_Init` 1297, `_BoyOrGirl` 1516, `_ChooseGender` 1533, `_WhatsYourName` 1608, `_StartNamingScreen` 1631 (`DoNamingScreen` 1639), `CB2_..._ReturnFromNamingScreen` 1822, `_SoItsPlayerName` 1643, `_ProcessNameYesNoMenu` 1660 (case 0 = confirmed -> reroute point), `_FadePlayerToWhite` 1796, `_Cleanup` 1810, `AddBirchSpeechObjects` 1912 (creates Birch+Lotad+Brendan+May), `NewGameBirchSpeech_ShowGenderMenu` 2121. No Poochyena battle in this expansion's Emerald path.
- `src/overworld.c:1927` — `CB2_NewGame` -> `NewGameInitData()` at `:1932`. Confirms the intro screen runs before the var-zeroing save clear.
- `include/constants/pokemon.h:104` — `#define SHINY_ODDS 16` (numerator / 65536). `include/pokemon.h:687` — `GET_SHINY_VALUE`. `src/pokemon.c` shiny comparisons to swap: `:893`, `:899`, `:983`, `:2502`, `:2934`.
- `include/constants/vars.h:100` — `VAR_UNUSED_0x404E` (free). `:99`/`:101` neighbours (`VAR_POKELOT_PRIZE_PLACE`, `VAR_LOTAD_SIZE_RECORD`) are live — pick `VAR_HOLON_SHINY_RATE` from the dedicated `VAR_UNUSED_*` block instead.
- Poryscript wired on the work branch: `Makefile:225` (`SCRIPT`), `:418` (auto-gen `.pory` -> `.inc`), `:442` (rule). `tools/poryscript/` has the binary + configs.
- StarterTown porymap setup = single commit `9961e0da68` on `first-porymap`: `data/maps/StarterTown/{map.json,scripts.inc}`, `data/layouts/StarterTown/*.bin`, `data/layouts/layouts.json` (`LAYOUT_STARTER_TOWN` 28x24, `gTileset_General` + `gTileset_Slateport`), `data/maps/map_groups.json`, `src/data/region_map/region_map_sections.json`, `data/event_scripts.s` (+`.include`). Layout is undesigned (uniform fill) — needs a walkable patch + spawn.
- `src/seagallop.c` — full FRLG ferry cutscene: `DoSeagallopFerryScene`, `Task_Seagallop_0/1/2/3`, `GetDirectionOfTravel`, `ScrollBG`, `sSeag[]`, `sTravelDirectionMatrix`.
- `data/specials.inc:597` — `def_special DoSeagallopFerryScene`.
- `include/overworld.h:177-178` — `CB2_ReturnToFieldContinueScript`, `CB2_ReturnToFieldContinueScriptPlayMapMusic`.
- `include/field_screen_effect.h:12` — `FieldCB_ContinueScript`.
- `data/maps/StarterTown/` — new map, currently stub `scripts.inc` + `map.json` (`MAP_STARTER_TOWN`, `LAYOUT_STARTER_TOWN`, `MAPSEC_STARTER_TOWN`), already in `map_groups.json`, already `.include`d in `data/event_scripts.s`.
- `data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc` — `ChooseStarterScene` (line 199), `EventScript_RivalBattle` (line 288) for steps 7-10.
- Poryscript wired in `Makefile` (auto-gen `.inc` from any `data/**/*.pory`), config in `tools/poryscript/`.
