---
title: "Pokémon Holon Legends — Codebase Reading Guide"
doc-id: HL-TEC-005
version: 1.1
status: Stable
category: Technical
last-updated: 2026-05-01
author: Matt Zappe
---

# Pokémon Holon Legends — Codebase Reading Guide

> **Status:** Stable | **Version:** 1.1 | **Updated:** 2026-05-01

---

A practical onboarding guide for learning how to read this repo, understand the `pokeemerald` / `pokeemerald-expansion` decomp model, and build the right mental habits before adding custom game content.

This version of the guide assumes you are already technically strong: comfortable with large codebases, abstraction, stateful systems, debugging, and formal reasoning. The gap it is trying to close is not "how to program," but:

- how game engines decompose work across frames,
- how a decomp-era codebase expresses architecture,
- how content pipelines interact with runtime systems,
- and how to trace player-visible behavior back to code and data.

This document is not a "how to code in C" tutorial and not a "how to add one specific feature" walkthrough. It is the bridge between:

- "I understand software and systems well"
- "I understand Pokemon Emerald as a player"
- and "I can open this repo, model it correctly, and extend it without getting lost"

---

## Table of Contents

- [1. What This Guide Is For](#1-what-this-guide-is-for)
- [2. The Four Engine Concepts to Translate First](#2-the-four-engine-concepts-to-translate-first)
  - [2.1 The Game Loop as a Real-Time Simulation Step](#21-the-game-loop-as-a-real-time-simulation-step)
  - [2.2 State as the Primary Object of Reasoning](#22-state-as-the-primary-object-of-reasoning)
  - [2.3 Modes as Top-Level State Machines](#23-modes-as-top-level-state-machines)
  - [2.4 Data-Driven Design as Domain-Specific Programming](#24-data-driven-design-as-domain-specific-programming)
- [3. How to Reuse Your Existing Technical Background](#3-how-to-reuse-your-existing-technical-background)
- [4. What a Pokemon Decomp Actually Is](#4-what-a-pokemon-decomp-actually-is)
- [5. The Three Layers You Are Working In](#5-the-three-layers-you-are-working-in)
- [6. Repo Map — What Lives Where](#6-repo-map--what-lives-where)
- [7. How the Engine Is Organized at Runtime](#7-how-the-engine-is-organized-at-runtime)
  - [7.1 Boot and Main Loop](#71-boot-and-main-loop)
  - [7.2 Main Callbacks and Modes](#72-main-callbacks-and-modes)
  - [7.3 Tasks](#73-tasks)
  - [7.4 Scripts](#74-scripts)
  - [7.5 Maps, Tiles, and Object Events](#75-maps-tiles-and-object-events)
  - [7.6 Battles](#76-battles)
  - [7.7 Pokemon Data](#77-pokemon-data)
  - [7.8 Save Data](#78-save-data)
- [8. Naming Patterns That Make the Code Easier to Read](#8-naming-patterns-that-make-the-code-easier-to-read)
- [9. File Types and Why They Exist](#9-file-types-and-why-they-exist)
- [10. How to Read Any Feature Without Getting Lost](#10-how-to-read-any-feature-without-getting-lost)
- [11. Concrete Reading Walkthroughs](#11-concrete-reading-walkthroughs)
  - [11.1 Walking One Step in the Overworld](#111-walking-one-step-in-the-overworld)
  - [11.2 Talking to an NPC](#112-talking-to-an-npc)
  - [11.3 Starting a Wild Battle](#113-starting-a-wild-battle)
  - [11.4 Opening the Pokedex](#114-opening-the-pokedex)
- [12. Where to Look for Common Types of Work](#12-where-to-look-for-common-types-of-work)
- [13. Low-Risk Workflow for Making Changes](#13-low-risk-workflow-for-making-changes)
- [14. Rules for Staying Sane in a Decomp Project](#14-rules-for-staying-sane-in-a-decomp-project)
- [15. A 4-Week Onboarding Plan for This Repo](#15-a-4-week-onboarding-plan-for-this-repo)
- [16. Recommended Reading Order Inside the Repo](#16-recommended-reading-order-inside-the-repo)
- [17. Useful Search Commands](#17-useful-search-commands)
- [18. Glossary](#18-glossary)
- [19. Final Mental Model](#19-final-mental-model)

---

## 1. What This Guide Is For

Use this document when you need to answer questions like:

- "Where do I even start in this codebase?"
- "What is code, what is data, and what is script?"
- "Why are there so many globals?"
- "What do `CB2_`, `Task_`, and `ScrCmd_` mean?"
- "How do maps, NPCs, scripts, and battles connect?"
- "How do I trace a feature from player action to engine behavior?"

The main goal is to help you stop reading the repo as a giant wall of files and start reading it as a set of cooperating systems with explicit ownership, state transitions, and data dependencies.

Assumed background:

- You are already comfortable reading production code.
- You do not need basic explanations of control flow, memory, or abstraction.
- You are new specifically to game architecture, GBA-era engine patterns, and Pokemon decomp conventions.

---

## 2. The Four Engine Concepts to Translate First

Before you try to understand the decomp, lock in these four translations from general software thinking into game-engine thinking.

### 2.1 The Game Loop as a Real-Time Simulation Step

A game is usually just a program that repeats this cycle:

1. Read input
2. Update game state
3. Draw the current state
4. Repeat

If you come from numerical methods or systems work, treat this as a discrete-time dynamical system with side effects and rendering. Each frame is a bounded update step over a mutable state vector, subject to hardware and latency constraints.

That loop is the heartbeat of the game. In this repo, the boot and per-frame loop begin in [src/main.c](../src/main.c).

### 2.2 State as the Primary Object of Reasoning

State means "everything the game currently knows."

Examples:

- The player's coordinates
- Which map is loaded
- Which story flags are set
- What Pokemon are in the party
- Which menu is open
- Whether the game is in battle

For an experienced programmer, this is the main reframing: do not read the game primarily as a call graph. Read it as a state-transition system. The important questions are:

- what state exists,
- who owns it,
- which transitions mutate it,
- which transitions are persistent,
- and which transitions are only transient/render-facing.

If you reason from state ownership first, the codebase becomes much easier to navigate.

### 2.3 Modes as Top-Level State Machines

The game is not running every system equally at all times. It switches between high-level modes, such as:

- Title screen
- Overworld
- Battle
- Menu
- Cutscene

You can think of these as coarse-grained state machines with mode-specific dispatch. Each mode has its own callback, input rules, update behavior, and allowed transitions. The same A button means different things depending on mode because the input is interpreted through the currently active state machine.

### 2.4 Data-Driven Design as Domain-Specific Programming

Most Pokemon content is not implemented as custom code per room or per NPC.

Instead, the engine is built once, then content is fed into it through:

- Map data
- Event definitions
- Scripts
- Text tables
- Encounter tables
- Species and move data
- Flags and variables

The right analogy is not "config files." It is closer to domain-specific programming against a fixed runtime. The script engine, map event model, and data tables collectively form a constrained authoring language for content and progression.

This is why decomp projects are so powerful. You are not hand-coding every event. You are authoring content against a reusable engine.

---

## 3. How to Reuse Your Existing Technical Background

If you already know software engineering, numerical reasoning, and systems thinking, the fastest way to learn this repo is to map familiar ideas to their game-dev equivalents.

| Existing intuition | Closest equivalent in this repo |
|---|---|
| Event loop / simulation loop | [src/main.c](../src/main.c) frame loop |
| Finite-state machine | Main callbacks, menu flows, battle phases, script execution states |
| Scheduler for lightweight jobs | [src/task.c](../src/task.c) task system |
| Bytecode interpreter / DSL runtime | [src/script.c](../src/script.c) and [src/scrcmd.c](../src/scrcmd.c) |
| Data-oriented design | Large tables in [src/data/](../src/data/) and [data/](../data/) driving behavior |
| Serialization / checkpoint state | Save blocks in [src/load_save.c](../src/load_save.c) |
| Object templates / instance realization | Map object event templates becoming runtime object events |
| Static dispatch by ID / enum | `SPECIES_*`, `MOVE_*`, `ITEM_*`, `FLAG_*`, `VAR_*` and table lookups |
| Hard real-time-ish budget awareness | Per-frame work kept incremental through callbacks, tasks, and waits |

What is likely unfamiliar is not the underlying logic but the style of expression:

- heavy globals instead of injected dependencies,
- compile-time IDs instead of dynamic registries,
- scripts and `.inc` content instead of modern editor-backed assets,
- and control flow split across callbacks, tasks, and data tables instead of a more centralized OO architecture.

Once you accept that translation, the repo becomes much less mysterious.

---

## 4. What a Pokemon Decomp Actually Is

`pokeemerald` is a decompilation of the original Pokemon Emerald ROM into human-readable source code and data. `pokeemerald-expansion` builds on that base and adds newer mechanics, QoL systems, and tooling.

Important consequences:

- You are working with a real codebase, not a ROM editor project.
- Some code patterns reflect old GBA-era constraints.
- Some names reflect reverse-engineering history.
- Some low-level code is still in assembly.
- Many systems are heavily global and data-table-driven because that matched the original game.

Do not think of this as "editing Emerald." Think of it as:

- an engine inherited from pret,
- extended by RHH expansion,
- customized by your project.

That mindset matters because it changes how you search, modify, and maintain the game.

---

## 5. The Three Layers You Are Working In

For practical development, treat the repo as three stacked layers:

| Layer | What it means | Typical examples |
|---|---|---|
| Base decomp layer | Original Emerald structure and systems | Main loop, field engine, battle engine, save system |
| Expansion layer | Modernized engine features added by `pokeemerald-expansion` | Fairy type, modern battle mechanics, config flags, HGSS-style Pokedex, follower systems |
| Holon project layer | Your game-specific content and custom behavior | Holon maps, Delta species data, scripts, text, custom story systems |

When you read any file, ask:

1. Is this vanilla Emerald architecture?
2. Is this expansion-added functionality?
3. Is this Holon-specific content or modification?

That question keeps you from changing engine code when you only needed content changes.

---

## 6. Repo Map — What Lives Where

This is the repo structure you should memorize first.

| Path | What it mainly contains | How to think about it |
|---|---|---|
| [src/](../src/) | C implementation files | Engine and gameplay logic |
| [include/](../include/) | Headers, constants, config, shared declarations | The public interface of systems |
| [data/](../data/) | Map files, scripts, text, layout data | Content authoring layer |
| [src/data/](../src/data/) | C-compiled data tables | Large engine-facing data definitions |
| [graphics/](../graphics/) | Sprites, tiles, UI graphics | Visual assets |
| [sound/](../sound/) | Music and audio data | Audio assets |
| [asm/](../asm/) | Assembly leftovers and low-level code | Usually not beginner territory |
| [tools/](../tools/) | Build and conversion utilities | Asset and data pipeline support |
| [test/](../test/) | Automated test scaffolding | Verification for engine behavior |
| [GDDs/](./) | Project-facing design and technical docs | Your reference layer |
| [docs/](../docs/) | Upstream / expansion documentation and tutorials | Read these before reinventing things |
| [build/](../build/) | Generated build artifacts | Do not hand-edit |

Also memorize these file classes:

- `include/constants/` = IDs, enums, labels, compile-time names
- `include/config/` = feature toggles and engine behavior switches
- `data/maps/` = individual maps and their events/scripts/connections
- `data/scripts/` = shared script libraries
- `data/text/` = text content tables
- `src/data/pokemon/` = species-facing data tables
- `src/data/` = battle, item, trainer, encounter, and UI tables

---

## 7. How the Engine Is Organized at Runtime

This is the most important section in the guide.

### 7.1 Boot and Main Loop

The GBA entry and per-frame loop live in [src/main.c](../src/main.c).

At a high level:

1. Hardware and memory are initialized
2. Audio, interrupts, save hardware, and callbacks are set up
3. The game enters an infinite loop
4. Each frame, it reads keys, updates systems, runs callbacks, updates music/time, and waits for VBlank

If you ever want to understand the entire runtime shape of the game, start here.

### 7.2 Main Callbacks and Modes

The game uses callbacks to define the currently active mode. The main shared struct is declared in [include/main.h](../include/main.h).

The important fields are:

- `callback1`
- `callback2`
- `savedCallback`

In practice, `callback2` often represents the active top-level mode:

- Overworld callback
- Battle callback
- Menu callback
- Screen-specific callback

You will see functions named like:

- `CB2_InitBattle`
- `CB2_OpenPokedex`
- `CB2_ReturnToField`
- `CB2_InitOptionMenu`

That `CB2_` prefix is your signal that you are looking at a mode-level or screen-level flow.

### 7.3 Tasks

Tasks are small per-frame jobs managed by a scheduler. Their implementation is in [src/task.c](../src/task.c).

Why tasks exist:

- Some work should continue over multiple frames
- Some animations or UI steps should update independently
- Some transitions need lightweight state machines

Common task examples:

- Menu animation
- Fade transition
- Timed field effect
- Post-message cleanup
- Battle UI helper behavior

Task functions are usually named `Task_*`.

When you see a task, think:

- it runs every frame,
- it usually owns a tiny slice of behavior,
- it stores its local state in `gTasks[taskId].data[]`.

### 7.4 Scripts

Most event behavior is not hardcoded directly in C. The field engine uses a script interpreter.

Key files:

- [src/script.c](../src/script.c)
- [src/scrcmd.c](../src/scrcmd.c)
- [data/script_cmd_table.inc](../data/script_cmd_table.inc)

Important idea:

- `script.c` runs the interpreter
- `scrcmd.c` implements commands
- map and shared `.inc` files define the actual content scripts

Example script actions:

- lock player
- face player
- show message
- wait for button
- move NPC
- start battle
- set flag
- warp

This is the backbone of progression design in a Pokemon game.

### 7.5 Maps, Tiles, and Object Events

Map runtime structure is defined mainly by:

- [include/global.fieldmap.h](../include/global.fieldmap.h)
- [src/overworld.c](../src/overworld.c)
- [src/field_control_avatar.c](../src/field_control_avatar.c)
- [data/maps/](../data/maps/)

Each map is built from several kinds of data:

- layout
- tilesets
- warps
- object events
- coord events
- bg events
- map scripts
- connections to adjacent maps

Important structures to understand:

- `MapHeader`
- `MapLayout`
- `MapEvents`
- `ObjectEventTemplate`
- `WarpEvent`
- `CoordEvent`
- `BgEvent`

When the player walks, the field engine is constantly checking:

- what tile they are on,
- whether the tile has special behavior,
- whether a script trigger exists,
- whether a warp should fire,
- whether a wild encounter should start.

### 7.6 Battles

The main battle runtime begins in [src/battle_main.c](../src/battle_main.c).

Battles are their own world:

- separate main callbacks
- separate graphics state
- separate battler state
- separate turn-resolution logic
- separate script system for effects

The battle engine is large because it must handle:

- move selection
- turn order
- abilities and items
- damage and status
- animations
- switching and fainting
- AI
- links and special battle modes

Important reading rule:

Do not start battle study by reading every battle file. Start from one visible behavior and trace only that path.

### 7.7 Pokemon Data

Pokemon storage structures are declared in [include/pokemon.h](../include/pokemon.h), with implementation in [src/pokemon.c](../src/pokemon.c).

The key distinction is:

- `BoxPokemon` = compact stored data
- `Pokemon` = stored data plus active battle/party-facing fields like HP and level-derived values

You will see lots of generic access through functions like:

- `GetMonData`
- `SetMonData`
- `GetBoxMonData`
- `SetBoxMonData`

This is normal. The game does not treat Pokemon like modern class instances. It treats them like packed save-friendly records with helper accessors.

### 7.8 Save Data

Save loading and block setup live in:

- [src/load_save.c](../src/load_save.c)
- [include/save.h](../include/save.h)

The save system is built around large blocks of persistent state:

- player progress
- party
- bag
- object state
- flags and variables
- PC storage

When you think "where does the game remember this?", the answer is usually:

- save blocks
- event flags / vars
- special runtime globals

---

## 8. Naming Patterns That Make the Code Easier to Read

These patterns save a huge amount of confusion.

| Pattern | Meaning |
|---|---|
| `CB2_*` | A top-level callback, screen callback, or mode transition |
| `Task_*` | A scheduled per-frame task |
| `ScrCmd_*` | A script command implementation |
| `EventScript_*` | A script label used by map/shared event content |
| `gSomething` | Global data |
| `sSomething` | File-local static data |
| `Try*` | Attempt behavior, usually conditional |
| `Init*` | Initialize a system or state block |
| `Setup*` | Prepare a system or register behavior |
| `Create*` | Allocate, spawn, or instantiate something |
| `Handle*` | Mid-level control logic |
| `Load*` | Bring data/assets into runtime |
| `Set*` / `Get*` | Read/write access helpers |

Other naming conventions worth learning:

- `EWRAM_DATA`, `IWRAM_DATA`, `COMMON_DATA`
  - Memory placement macros for GBA hardware
  - Important technically, but not usually the first thing to care about as a designer
- `gSpecialVar_*`
  - Special script variables shared between script and C code
- `FLAG_*`, `VAR_*`
  - Persistent progression state names
- `SPECIES_*`, `MOVE_*`, `ITEM_*`
  - Compile-time IDs for data tables

If you internalize these naming patterns, file scanning becomes much faster.

---

## 9. File Types and Why They Exist

| File type | What it usually means |
|---|---|
| `.c` | C implementation |
| `.h` | Header declarations, structs, prototypes, constants |
| `.inc` | Included content data or script/text fragments |
| `.json` | Source data used by build tools for content generation |
| `.s` | Assembly, usually low-level or not yet rewritten |
| `.bin` | Raw binary asset data generated by the toolchain |

Important reading rule:

Do not assume `.inc` means unimportant. In this repo, `.inc` files often hold the actual content layer for:

- event scripts
- text
- map definitions
- data tables

Also note:

- `build/` output is generated, not hand-authored
- `.gba`, `.elf`, `.map` at repo root are build outputs
- many graphics and data assets are pulled into C through `INCBIN` or generated headers

---

## 10. How to Read Any Feature Without Getting Lost

This is the method to use every time.

If you are already used to tracing distributed systems or scientific software, the right workflow is:

1. identify the observable behavior,
2. identify the state owner,
3. identify the dispatch mechanism,
4. identify the data tables involved,
5. identify the persistence boundary.

That is more reliable than reading files sequentially.

### Step 1: Start from a player-visible behavior

Bad starting point:

- "I will read battle_main.c front to back."

Good starting point:

- "I want to understand how talking to an NPC works."
- "I want to understand how wild encounters start."
- "I want to understand where the Pokedex screen gets its data."

Always start from a concrete feature.

### Step 2: Classify the feature

Ask which layer it belongs to:

- config
- data table
- map content
- script
- engine code
- battle code
- UI code

Many beginner mistakes come from editing engine code when the real answer lived in a content file.

### Step 3: Find the entry point

Use search to find:

- callback names
- event scripts
- constants
- struct names
- UI labels

Examples:

```bash
rg -n "CB2_OpenPokedex" src include
rg -n "EventScript_" data/maps data/scripts
rg -n "SPECIES_PIKACHU" src include data
rg -n "FLAG_" data/maps src
```

### Step 4: Find the owner of the state

Ask:

- Which struct owns this data?
- Which global stores it?
- Is it saved or temporary?

Examples:

- player party -> [include/pokemon.h](../include/pokemon.h)
- loaded map state -> [src/overworld.c](../src/overworld.c)
- flags and vars -> [include/event_data.h](../include/event_data.h)
- save blocks -> [src/load_save.c](../src/load_save.c)

### Step 5: Trace the control flow

Look for:

- input
- condition checks
- helper functions
- callbacks
- tasks
- scripts

Your question is always:

"What function decides the next thing that happens?"

In software-architecture terms, you are looking for the dispatch boundary, not just the next linearly adjacent helper.

### Step 6: Identify data inputs

Look for:

- constants
- tables
- map event definitions
- config headers
- species/move/item data

### Step 7: Confirm where the final effect happens

Examples:

- text appears in a message box
- a flag is set
- an NPC movement starts
- a battle callback is installed
- a save block field is updated

This is the point where your mental model becomes complete.

---

## 11. Concrete Reading Walkthroughs

These are the kinds of paths you should practice until they feel normal.

### 11.1 Walking One Step in the Overworld

High-level flow:

1. [src/main.c](../src/main.c) runs the frame loop
2. The overworld callback is active
3. [src/field_control_avatar.c](../src/field_control_avatar.c) gathers player input
4. It determines whether the player moved, interacted, triggered a warp, or rolled for encounters
5. Tile behavior and map events are checked
6. The world state updates, and the result is drawn

Key lesson:

Walking is not just movement. It is the trigger point for many systems:

- step counters
- poison/follower updates
- encounter checks
- tile events
- arrow warps
- sign scripts

### 11.2 Talking to an NPC

High-level flow:

1. Player presses A while facing an object or background event
2. [src/field_control_avatar.c](../src/field_control_avatar.c) resolves what is in front of the player
3. It finds the relevant script
4. [src/script.c](../src/script.c) starts or continues the script
5. [src/scrcmd.c](../src/scrcmd.c) executes commands one by one
6. Text, movement, flags, choices, or battles occur

Key lesson:

Most "story logic" in a Pokemon decomp is script-driven, not hardcoded scene-by-scene in C.

### 11.3 Starting a Wild Battle

High-level flow:

1. The player takes a valid step
2. The field engine checks encounter rules
3. Encounter logic in [src/wild_encounter.c](../src/wild_encounter.c) determines whether a battle starts
4. Battle setup code prepares enemy Pokemon and battle flags
5. The active mode switches into battle callbacks in [src/battle_main.c](../src/battle_main.c)

Key lesson:

A battle is a mode transition from the overworld, not a small overlay on top of it.

### 11.4 Opening the Pokedex

High-level flow:

1. A menu or callback calls a Pokedex entry point such as `CB2_OpenPokedex`
2. The game switches into Pokedex screen callbacks
3. [src/pokedex.c](../src/pokedex.c) and related Pokedex files build the screen state
4. Species/order/caught-seen data is pulled from Pokemon and save-facing systems

Relevant files in this repo:

- [src/pokedex.c](../src/pokedex.c)
- [src/pokedex_plus_hgss.c](../src/pokedex_plus_hgss.c)
- [include/pokedex.h](../include/pokedex.h)
- [src/data/pokemon/pokedex_orders.h](../src/data/pokemon/pokedex_orders.h)

Key lesson:

Most UI screens are their own little applications inside the game, with their own callbacks, tasks, and data-prep paths.

---

## 12. Where to Look for Common Types of Work

Use this as your practical map.

| If you want to work on... | Start here |
|---|---|
| Story dialogue and cutscenes | [data/maps/](../data/maps/), [data/scripts/](../data/scripts/), [data/text/](../data/text/) |
| Map structure, warps, NPC placement | [data/maps/](../data/maps/), Porymap, [include/global.fieldmap.h](../include/global.fieldmap.h) |
| Tile behavior and movement rules | [src/field_control_avatar.c](../src/field_control_avatar.c), [src/metatile_behavior.c](../src/metatile_behavior.c), tileset data |
| Wild encounters | [src/wild_encounter.c](../src/wild_encounter.c), [src/data/wild_encounters.json](../src/data/wild_encounters.json), [include/constants/wild_encounter.h](../include/constants/wild_encounter.h) |
| Trainer data and parties | [src/data/trainers.h](../src/data/trainers.h), [src/data/trainer_parties.h](../src/data/trainer_parties.h), trainer scripts |
| Pokemon species data | [src/data/pokemon/species_info.h](../src/data/pokemon/species_info.h), [include/constants/species.h](../include/constants/species.h), [src/pokemon.c](../src/pokemon.c) |
| Moves and move behavior | [src/data/moves_info.h](../src/data/moves_info.h), [include/constants/moves.h](../include/constants/moves.h), battle scripts and command handlers |
| Items | [src/data/items.h](../src/data/items.h), [include/constants/items.h](../include/constants/items.h), item-use code |
| Battle flow | [src/battle_main.c](../src/battle_main.c), [src/battle_script_commands.c](../src/battle_script_commands.c), AI and controller files |
| Pokedex behavior | [src/pokedex.c](../src/pokedex.c), [src/pokedex_plus_hgss.c](../src/pokedex_plus_hgss.c), Pokedex constants/data |
| Save behavior | [src/load_save.c](../src/load_save.c), [include/save.h](../include/save.h), [include/event_data.h](../include/event_data.h) |
| Configurable engine behavior | [include/config/](../include/config/) |

---

## 13. Low-Risk Workflow for Making Changes

When you want to build content, work in this order.

### 13.1 Ask "Can this be done without engine changes?"

The answer is often yes.

Prefer this order of solutions:

1. Config change
2. Data table change
3. Script change
4. Map/event change
5. Engine C code change
6. New subsystem

### 13.2 Make the smallest possible change

Good first changes:

- edit a line of text
- change an NPC script
- change a wild encounter table
- add a simple trainer
- edit a species stat or type

Bad first changes:

- rewrite battle flow
- invent a custom save format
- refactor half the overworld
- merge large upstream changes before understanding the base

### 13.3 Always find the current implementation first

Before adding something new, find the closest existing example and copy the pattern.

Pokemon decomp work is pattern-driven. Reusing an established pattern is usually safer than inventing your own.

For an experienced programmer, this is less about lack of skill and more about local convention density. The engine has many hidden assumptions encoded in tables, callbacks, and script flows. Matching an existing pattern minimizes the chance that you violate one of those assumptions.

### 13.4 Build and test after each small step

Do not queue twenty unrelated edits before your next build.

Best habit:

- make one small change
- build
- run
- verify in-game
- commit

---

## 14. Rules for Staying Sane in a Decomp Project

These rules will save you a lot of time.

### 14.1 Read feature-first, not file-first

Do not try to understand the repo by reading giant files straight through.

Instead:

- choose a feature
- trace its path
- learn the participating systems

### 14.2 Learn ownership

Every behavior has an owner.

Examples:

- movement input -> field control
- map loading -> overworld
- dialogue progression -> script engine
- species data -> Pokemon data tables
- seen/caught state -> save + Pokedex systems

If you do not know the owner, you will wander.

### 14.3 Do not fight the engine shape

This codebase is old-school C with:

- globals
- packed structs
- generated tables
- data includes
- file-local statics
- manual callbacks
- lots of compile-time constants

That is normal here. Do not try to mentally force modern game engine architecture onto it.

### 14.4 Expect indirection

A visible behavior may pass through:

- callback
- helper
- task
- script
- data table
- UI routine

That does not mean the code is broken. It means the engine is composed.

### 14.5 Prefer existing docs before deep engine surgery

This repo already ships useful upstream documentation in [docs/tutorials/](../docs/tutorials/).

Especially relevant:

- [docs/tutorials/how_to_new_pokemon.md](../docs/tutorials/how_to_new_pokemon.md)
- [docs/tutorials/how_to_new_move.md](../docs/tutorials/how_to_new_move.md)
- [docs/tutorials/how_to_follower_npc.md](../docs/tutorials/how_to_follower_npc.md)
- [docs/tutorials/how_to_time_of_day_encounters.md](../docs/tutorials/how_to_time_of_day_encounters.md)
- [docs/tutorials/how_to_testing_system.md](../docs/tutorials/how_to_testing_system.md)
- [docs/tutorials/how_to_code_entry.md](../docs/tutorials/how_to_code_entry.md)

Also keep [HL-200-technical-guide.md](HL-200-technical-guide.md) nearby for the build/tooling model.

---

## 15. A 4-Week Onboarding Plan for This Repo

This is the path I would recommend for an experienced programmer who is new to game development and to Pokemon decomps.

### Week 1: Learn the runtime skeleton

Goals:

- understand the main loop
- understand modes and callbacks
- understand tasks
- understand scripts at a high level

Read:

- [src/main.c](../src/main.c)
- [include/main.h](../include/main.h)
- [src/task.c](../src/task.c)
- [src/script.c](../src/script.c)
- [src/scrcmd.c](../src/scrcmd.c)

Exercise:

- sketch the boot-to-overworld control flow
- identify which state is transient vs persistent in the startup path
- explain what a task is in scheduler terms
- explain what a script command is in interpreter terms

### Week 2: Learn the overworld and map/event model

Goals:

- understand maps as data
- understand object events, warps, coord events, bg events
- understand the interaction pipeline

Read:

- [include/global.fieldmap.h](../include/global.fieldmap.h)
- [src/overworld.c](../src/overworld.c)
- [src/field_control_avatar.c](../src/field_control_avatar.c)
- a few folders inside [data/maps/](../data/maps/)

Exercise:

- pick one map and identify its scripts, warps, NPCs, and connections
- write the state transition path for "player presses A facing an NPC"
- note which parts are content-authored vs engine-authored

### Week 3: Learn content data pipelines

Goals:

- understand how encounters, trainers, species, and items are stored
- get used to constants and data tables

Read:

- [src/data/wild_encounters.json](../src/data/wild_encounters.json)
- [src/data/trainers.h](../src/data/trainers.h)
- [src/data/trainer_parties.h](../src/data/trainer_parties.h)
- [src/data/pokemon/species_info.h](../src/data/pokemon/species_info.h)
- [src/data/items.h](../src/data/items.h)

Exercise:

- change one encounter table in a scratch branch
- find one trainer's party definition
- find one species' base stats and typing
- write down which tables define identity, balance, and progression separately

### Week 4: Learn one deeper system

Choose one:

- battle
- Pokedex
- follower system
- save system
- day/night / time systems

Suggested files:

- battle -> [src/battle_main.c](../src/battle_main.c)
- Pokedex -> [src/pokedex.c](../src/pokedex.c)
- save -> [src/load_save.c](../src/load_save.c)

Exercise:

- write a short note in your own words describing that system's main state, entry points, dispatch boundaries, and data dependencies

---

## 16. Recommended Reading Order Inside the Repo

If you want the shortest path from experienced programmer to functional contributor, use this order:

1. [HL-200-technical-guide.md](HL-200-technical-guide.md)
2. [src/main.c](../src/main.c)
3. [include/main.h](../include/main.h)
4. [src/task.c](../src/task.c)
5. [src/script.c](../src/script.c)
6. [src/scrcmd.c](../src/scrcmd.c)
7. [include/global.fieldmap.h](../include/global.fieldmap.h)
8. [src/overworld.c](../src/overworld.c)
9. [src/field_control_avatar.c](../src/field_control_avatar.c)
10. One sample map folder in [data/maps/](../data/maps/)
11. [src/pokemon.c](../src/pokemon.c)
12. [include/pokemon.h](../include/pokemon.h)
13. [src/load_save.c](../src/load_save.c)
14. [src/pokedex.c](../src/pokedex.c) or [src/battle_main.c](../src/battle_main.c), depending on what you want to build next

Do not read all battle files before you understand the field/script/map model. Most early game production work happens outside the battle engine.

---

## 17. Useful Search Commands

These are the most useful search patterns for repo navigation.

Find where a callback is declared and used:

```bash
rg -n "CB2_OpenPokedex|CB2_InitBattle|CB2_ReturnToField" src include
```

Find where a script or script label is defined:

```bash
rg -n "EventScript_|MapScript_" data/maps data/scripts src
```

Find all uses of a constant:

```bash
rg -n "SPECIES_DEOXYS|MOVE_THUNDERBOLT|ITEM_MASTER_BALL|FLAG_SYS_POKEDEX_GET"
```

Find the owner of a struct:

```bash
rg -n "struct MapHeader|struct Pokemon|struct SaveBlock1|struct Task" include src
```

Find who sets or reads a flag or var:

```bash
rg -n "FlagSet|FlagClear|FlagGet|VarSet|VarGet" src data
```

Find entry points for a visible feature:

```bash
rg -n "Pokedex|wild encounter|follower|summary screen|trainer battle" src include data
```

This is why strong search habits matter so much in a decomp project.

---

## 18. Glossary

| Term | Meaning |
|---|---|
| Callback | A function the engine stores and calls later as the active mode or handler |
| Task | A small scheduled per-frame job |
| Script | A bytecode-driven event sequence used for field progression and interactions |
| Decomp | Decompiled or reconstructed source version of a ROM/game |
| Data-driven | Behavior/content defined by tables, scripts, and config rather than custom code each time |
| Flag | Persistent boolean state, usually used for progression |
| Var | Persistent numeric state, often used by scripts |
| Object event | An NPC or field object template on a map |
| Coord event | A trigger tied to stepping on specific coordinates |
| Bg event | A background interaction such as a sign or hidden item |
| Save block | Large persistent structure storing player/game state |
| `INCBIN` | Macro that embeds raw asset data into the build |
| Expansion | `pokeemerald-expansion`, the modernized fork built on top of pret's decomp |

---

## 19. Final Mental Model

If you only remember one model from this guide, remember this:

The game is:

1. a frame loop,
2. running one active mode at a time,
3. using callbacks, tasks, and scripts to update state,
4. while pulling most actual content from data tables and map files.

So when you are reading the repo, always ask:

1. What mode am I in?
2. What system owns this behavior?
3. Where does its state live?
4. Is this driven by config, data, script, or code?
5. What existing example already does something similar?

If you keep asking those five questions, this codebase stops feeling huge and starts feeling legible.

---

*Pokémon Holon Legends — Codebase Reading Guide | HL-TEC-005 v1.1 | Last updated 2026-05-01*
