# The pokeemerald-expansion Textbook

### A Working Reference for GBA Pokémon ROM Hack Development

---

## How to Use This Book

This book is built to be used two ways.

**First pass:** read Part I start to finish, once, before you touch the codebase. Everything after it assumes you have already built the project successfully at least one time.

**After that:** treat it as a reference. Jump directly to the chapter and numbered subsection you need mid-task. Each chapter is self-contained enough to be read on its own, with cross-references where topics overlap.

Two callout types appear throughout:

> **📝 Note** — context that clarifies without being essential. Safe to skip on a first read.

> **⚠ Pitfall** — a mistake worth slowing down for, usually one that costs real debugging time if you hit it unwarned.

Every chapter closes with a **Chapter Summary** (the two-minute recap) and **Try It Yourself** (small, concrete tasks that build the muscle memory the chapter describes — there's no answer key, because the ROM either does what you intended or it doesn't, and that's the feedback loop that matters).

### A Note on Version Drift

This codebase updates constantly. Struct field names, macro names, file paths, and exact command syntax shown in this book are accurate as of research conducted in mid-2026 and represent the *shape* of how things work — but any individual name can shift between versions. Where a code example gets specific about field or macro names, treat it as illustrative of the pattern rather than a guaranteed literal match to your checkout. Always cross-check against the [official documentation site](https://rh-hideout.github.io/pokeemerald-expansion/) and your own `include/` headers when something doesn't compile as written.

---

## Table of Contents

**Part I — Getting Started**
- Chapter 1: Foundations
- Chapter 2: Project Anatomy

**Part II — World Building**
- Chapter 3: Map Creation with Porymap
  - 3.1 Installing and Configuring Porymap
  - 3.2 The Map Hierarchy
  - 3.3 Tilesets in Depth
  - 3.4 Metatiles and Metatile Behaviors
  - 3.5 Painting a Map
  - 3.6 Map Connections
  - 3.7 Wild Encounters Configuration
  - 3.8 Map Header Properties
  - 3.9 The Events Tab in Depth
  - 3.10 A Complete Worked Example

**Part III — Logic and Behavior**
- Chapter 4: Scripting with Poryscript
  - 4.1 Why Poryscript Exists
  - 4.2 Installation and Editor Integration
  - 4.3 Converting Legacy Scripts
  - 4.4 Scripts, Text, and Map Script Types
  - 4.5 Core Command Reference
  - 4.6 Control Flow in Depth
  - 4.7 Flags and Variables
  - 4.8 The Text System in Depth
  - 4.9 Movement Scripting
  - 4.10 A Library of Common Patterns
- Chapter 5: NPCs, Object Events & Trainers
  - 5.1 Object Event Architecture
  - 5.2 Movement Types, Full Catalog
  - 5.3 Custom Movement and Paths
  - 5.4 The Trainer Battle System
  - 5.5 Trainer Data Structure
  - 5.6 Following Pokémon
  - 5.7 The Task System in Depth
  - 5.8 Field Effects and Special Functions

**Part IV — Content and Data**
- Chapter 6: Gameplay Data Entry
  - 6.1 The Species Pipeline in Depth
  - 6.2 Learnsets
  - 6.3 Evolution Data
  - 6.4 Pokédex Entries
  - 6.5 Trainer Data Entry in Depth
  - 6.6 Wild Encounter Tables in Depth
  - 6.7 Moves and Move Effects
  - 6.8 Abilities
  - 6.9 Items

**Part V — Art and Presentation**
- Chapter 7: Graphics & Sprites
  - 7.1 GBA Graphics Fundamentals
  - 7.2 Tool Chain Setup
  - 7.3 Overworld Sprite Pipeline in Depth
  - 7.4 Battle Sprite Pipeline in Depth
  - 7.5 Palette Management
  - 7.6 Tile and Tileset Art
  - 7.7 Animating Tiles and Field Effects
  - 7.8 UI and Menu Graphics

**Part VI — Advanced Topics**
- Chapter 8: Custom C Code
  - 8.1 When C Is Actually Necessary
  - 8.2 Reading the Codebase Before Writing In It
  - 8.3 The Callback Architecture
  - 8.4 Common Extension Points
  - 8.5 Battle Scripts vs. Poryscript
  - 8.6 Memory and Performance Considerations
  - 8.7 Safe Extension Practices
  - 8.8 Debugging Custom C
- Chapter 9: Troubleshooting & Debug Tools
  - 9.1 The Debug Menu, Full Tour
  - 9.2 Build System Troubleshooting
  - 9.3 Runtime Crash Diagnosis
  - 9.4 Graphics Debugging
  - 9.5 Version Migration Troubleshooting
  - 9.6 Git Workflow for Debugging

**Appendices**
- Appendix A: Glossary
- Appendix B: Quick Reference Tables
- Appendix C: Full Source Index

---

# Part I — Getting Started

## Chapter 1: Foundations

**Learning objectives.** By the end of this chapter you should be able to: explain what a decomp is and why it differs from traditional hex-editor ROM hacking; choose between pokeemerald and pokeemerald-expansion for a given goal; perform a first clone and build; and update or merge changes into an existing project without wrecking it.

### 1.1 What a Decomp Actually Is

A decompilation is the original game's assembly, painstakingly reverse-engineered back into readable, buildable C. You are not patching bytes in a hex editor — you are editing source files and recompiling a ROM from scratch. This distinction changes everything about how you work: normal software practices apply. Version control, diffing, incremental builds, and the ability to grep for a constant instead of hunting through a hex dump are all available to you in a way they simply aren't in traditional ROM hacking tools like Advance Map or XSE.

**pokeemerald** (maintained by the pret organization) is the base decompilation — it builds a ROM byte-identical to retail Pokémon Emerald. It is the foundation everything else in the Gen 3 decomp ecosystem forks from.

**pokeemerald-expansion** (maintained by ROM Hacking Hideout, RHH) is a hack base built on top of pokeemerald. It is not a playable game on its own and not ROM-identical to retail — it bundles hundreds of features and quality-of-life systems, most of them individually toggleable through configuration macros. Among them: the Fairy type, the physical/special/status category split, moves and abilities extended up through Scarlet/Violet, Mega Evolution, Primal Reversion, Z-Moves, battle terrain, modern damage calculation, 2v2 wild battles, and a substantial debug menu.

> **📝 Note** — pokeemerald-expansion supports link/multiplayer functionality with *other games also built on expansion*, but is not compatible with official retail cartridges for that purpose. If cross-compatibility with unmodified retail Emerald specifically matters to you, use plain pokeemerald. For the overwhelming majority of solo ROM hack projects, expansion is the correct starting point — the feature set it hands you for free would otherwise be months of custom C work.

### 1.2 First-Time Setup

```bash
# Never use GitHub's "Download Zip" button — it strips commit history,
# which you need later for updates and feature-branch merges.
git clone https://github.com/rh-hideout/pokeemerald-expansion.git
cd pokeemerald-expansion
```

Follow [INSTALL.md](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md) for your operating system's toolchain:

- **Windows** — MSYS2/MinGW, following the documented package list.
- **Linux** — `build-essential` plus the documented list of GBA dev packages.
- **macOS** — Xcode Command Line Tools plus Homebrew packages per INSTALL.md.

Then build:

```bash
make -j$(nproc)     # or just `make` if you're unsure of your core count
```

> **⚠ Pitfall** — Verify before you touch anything. A clean, freshly cloned build should match the checksum in `rom.sha1`. Confirm this *before* making any edits. If you skip this step and later hit a build failure, you won't know whether it's something you broke or a broken checkout to begin with — and you'll waste real time debugging the wrong problem.

### 1.3 Updating an Existing Project

```bash
# One-time setup of the upstream remote
git remote add RHH https://github.com/rh-hideout/pokeemerald-expansion

# Update to a specific released version. If you're several versions
# behind, update one minor version at a time rather than jumping —
# e.g. 1.5.3 -> 1.6.2 -> 1.7.4 -> 1.16.1, not straight to latest.
git pull RHH expansion/1.16.1

# Stable branch: unreleased bugfixes headed for the next patch release
git pull RHH master

# Unstable: unreleased features, may have bugs, use with caution
git pull RHH upcoming
```

Each incremental jump gives you a smaller, more reviewable diff and a much better chance of resolving conflicts correctly the first time.

### 1.4 Merging Feature Branches

Feature branches (see [Team Aqua's Asset Repo wiki](https://github.com/Pawkkie/Team-Aquas-Asset-Repo/wiki/Feature-Branches)) are a fundamentally different operation from updating expansion's version. A version update pulls from a lineage that already accounts for your history. A feature branch was built independently, against its own snapshot of expansion, and may touch many of the same shared files you've also touched — `config.h`, species tables, the Makefile.

> **⚠ Pitfall** — Because of that independent history, a raw `git pull` or `git merge` of a feature branch usually produces heavy, tedious conflicts, and blindly accepting "theirs" on those conflicts can silently roll back expansion updates or your own prior work.

**Working pattern:** treat your current expansion version's copy of any shared file as authoritative, and manually re-apply just the branch-specific hunks — new functions, new config toggles, new data table entries — rather than accepting the branch's whole-file version. It is slower than a merge, but it's the only approach that reliably preserves both your version's baseline and the branch's additions.

### Chapter 1 Summary

- A decomp is editable source you rebuild, not a binary you patch.
- Use pokeemerald-expansion unless retail-cartridge compatibility is a hard requirement.
- Verify a clean build against `rom.sha1` before making any changes.
- Update expansion versions incrementally, one minor version at a time.
- Merge feature branches by hand, treating your version's shared files as authoritative.

### Try It Yourself

1. Clone the repository, build it clean, and confirm the checksum matches `rom.sha1`.
2. Make one trivial change (e.g. a text string) and rebuild — confirm the ROM changed and the game still boots.
3. Read through `FEATURES.md` end to end once. You don't need to remember it; you need to know it exists so you stop writing custom C for things expansion already ships.

### Further Reading
- [INSTALL.md](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)
- [pokeemerald-expansion documentation site](https://rh-hideout.github.io/pokeemerald-expansion/)
- [Team Aqua's Asset Repo: Basics of GitHub](https://github.com/Pawkkie/Team-Aquas-Asset-Repo/wiki/The-Basics-of-GitHub)
- [Bivurnum's decomps-resources](https://github.com/Bivurnum/decomps-resources)

---

## Chapter 2: Project Anatomy

**Learning objectives.** By the end of this chapter you should be able to: locate the right file or folder for a given kind of change without searching blindly; explain the role of `config.h` in the project; and describe the build-verify loop you should be running continuously as you work.

### 2.1 Directory Map

| Path | What lives here |
|---|---|
| `data/maps/<MapName>/` | `map.json` (owned by Porymap — don't hand-edit), `scripts.pory`, `text.pory` |
| `src/` | Game logic C source: battle engine, overworld, menus, field effects |
| `include/` | Headers — function declarations, struct definitions |
| `include/config.h` | **The master toggle file.** Most "turn a feature on/off" work starts here |
| `constants/` | Named IDs — species, items, moves, abilities, flags, vars |
| `graphics/` | Sprites, tilesets, palettes, UI graphics |
| `src/data/pokemon/` | Species data tables — base stats, learnsets, evolution, Pokédex text |
| `src/data/trainers.h` (path varies by version) | Trainer parties, AI flags, classes |
| `tools/` | Build-time binaries: Poryscript, image converters, and their configs |
| `test/` | Automated unit/integration tests for battle mechanics and more |

### 2.2 The config.h Toggle System

Expansion's defining architectural choice is that most modern mechanics are opt-in, often with a choice of *which generation's version* of a mechanic you want:

```c
// include/config.h — illustrative; exact macro names drift by version
#define P_FAIRY_TYPE             GEN_6   // Fairy type introduced at Gen 6
#define P_PHYSICAL_SPECIAL_SPLIT GEN_4   // Physical/Special split at Gen 4
#define P_GENDER_DIFFERENCES     TRUE
```

This file is almost always your first stop before writing any custom code. A huge fraction of "I need to build a custom mechanic" requests turn out to already be a flag flip away — search here before you search anywhere else.

### 2.3 The Build-Verify Loop

This loop should run continuously, not just at milestones:

1. Make one small, isolated change.
2. `make -j$(nproc)`
3. Run the ROM in an emulator. **mGBA** is the standard choice — it has accurate timing, a built-in debugger, memory viewer, and logging console, all of which matter once you're past trivial edits.
4. Commit. Small, frequent commits mean `git bisect` can find a regression later without you having to re-derive what changed by memory.

> **📝 Note** — "Isolated" is doing real work in that first bullet. Bundling five unrelated changes into one build-test cycle means that when something breaks, you're debugging five things at once instead of one.

### Chapter 2 Summary

- `data/maps/` for map content, `src/` and `include/` for logic, `constants/` for named IDs, `graphics/` for art.
- `include/config.h` is the first place to check before writing custom code.
- Build small, test in mGBA, commit often — the loop is the workflow, not a checkpoint you occasionally return to.

### Try It Yourself

1. Open `include/config.h` and skim every macro once, even the ones you don't understand yet. You're building a mental index, not memorizing values.
2. Pick any one existing species and trace its data across every file listed in the directory map above, just to see the shape of a "complete" entry before you build your own.

### Further Reading
- [pokeemerald-expansion FEATURES.md](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/FEATURES.md)


---

# Part II — World Building

## Chapter 3: Map Creation with Porymap

**Learning objectives.** By the end of this chapter you should be able to: install and configure Porymap against a project; explain the difference between primary and secondary tilesets; paint a map using metatiles and assign correct behaviors; connect two maps seamlessly; configure a wild encounter table by hand and understand the probability math behind it; and place every event type Porymap supports.

### 3.1 Installing and Configuring Porymap

Download from the [Porymap releases page](https://github.com/huderlem/porymap) — prebuilt binaries exist for Windows and macOS; Linux users compile from source or use a package like Flathub or AUR.

On first launch, point Porymap at your project's root directory (the folder containing `data/`, `graphics/`, and your Makefile). Porymap reads `data/maps`, the tileset folders, and several project config files directly, so as long as you point it at the right root, it stays in sync with your decomp checkout without any separate export/import step.

Porymap ships its own preferences panel worth configuring early:

- **Default border metatile** — what appears in the "out of bounds" fringe around a map. Matters more than it sounds like once you start placing map connections.
- **Text editor integration** — Porymap can be told to open script files in an external editor (e.g. VS Code) directly from its Events tab, which is worth wiring up immediately since you'll be jumping between the two constantly.
- **Custom scripts / plugins** — recent Porymap versions support a small Lua-based scripting API for custom map validation or automation. Most projects never need this, but it exists if you find yourself repeating the same manual check across every map.

> **📝 Note** — Porymap owns `map.json`, `layout.json`, and related project files. Treat these as generated artifacts of the GUI, the same way you'd treat a compiled binary — hand-editing them is possible but throws away the entire benefit of using a GUI map editor in the first place, and a malformed hand-edit can corrupt the map silently.

### 3.2 The Map Hierarchy

Porymap's map organization has three nested concepts, and conflating them is a common source of early confusion:

- **Map** — a single named area with its own scripts, events, and header properties (e.g. "Route 101").
- **Layout** — the actual tile/metatile data and dimensions. Multiple maps can technically share a layout, though this is uncommon outside of things like weather variants.
- **Map Group** — an organizational bucket (not gameplay-relevant) used to keep the project's map list navigable — grouping all of one town's interiors together, for instance.

When you create a new map, you're choosing or creating all three at once: which group it organizes under, whether it uses a new layout or an existing one, and the map's own identity (name, header properties, events).

### 3.3 Tilesets in Depth

Every map uses exactly two tilesets simultaneously:

- **Primary tileset** — shared broadly across many maps. General terrain, common building pieces, generic doors and signs. Changes here ripple across your whole project, so primary tilesets are usually treated conservatively once a project is underway.
- **Secondary tileset** — local to one map or a small cluster of related maps (a single town's unique building facades, a specific cave's rock formations). This is where most of your custom, area-specific art lives.

GBA hardware constrains how many distinct colors can be on screen at once, and tilesets are where that constraint becomes concrete: palette slots are a shared, limited resource split between what the primary and secondary tileset are each allowed to use. Overflowing this budget is one of the more common "why does my new tileset look wrong" bugs — see the Pitfall below and Chapter 7's palette discussion for the underlying mechanics.

> **⚠ Pitfall** — Because primary tilesets are shared project-wide, editing one to fix a single map's problem can visually break every other map using it. If you need a one-off variant of an existing tile, put the variant in that map's secondary tileset instead of modifying the primary.

Metatiles are composited from up to three **layers** — bottom, middle, and top — each pulling from the raw tile images in the tileset. The bottom layer is typically opaque ground; middle and top layers allow transparency, which is how you get effects like a tree canopy overlapping a walking player sprite (top layer) while the trunk is behind them (bottom/middle).

### 3.4 Metatiles and Metatile Behaviors

A **metatile** is a pre-assembled block combining the layered tiles above into a single paintable unit — this is what you actually click and place in the map view, not individual raw tiles.

Separately from how a metatile *looks*, every metatile carries a **behavior** — a tag that tells the engine what it functionally *is*. Behaviors are assigned per-metatile in the Tileset Editor and are completely independent of the art; two visually different metatiles can share a behavior, and two identical-looking metatiles can have different behaviors (useful for things like a normal-looking floor tile that's secretly a hidden trigger).

Common behavior categories you'll use constantly:

| Category | Example behaviors |
|---|---|
| Encounter terrain | Tall grass, long grass, deep sand — each can have a different encounter table association |
| Water/traversal | Surfable water, waterfall, dive-capable water, whirlpool |
| Obstruction | Impassable, jump ledge (per direction), cracked ice |
| Interaction | Sign, PC, cuttable tree, rock-smashable, strength boulder push surface |
| Terrain effects | Ice (sliding), mud slope, sand (footprint-leaving), puddle (splash sound) |
| Special | Warp behaviors that pair with a warp event, secret base entrances |

> **⚠ Pitfall** — A metatile can *look* like grass and still be impassable, or *look* like solid ground and still be surfable, if its behavior was set (or copy-pasted) incorrectly. When a map "feels wrong" in ways that don't show up visually — the player can't walk somewhere that looks walkable, or wild encounters trigger somewhere they shouldn't — check the metatile behavior before assuming it's a scripting bug.

### 3.5 Painting a Map

The core loop in the Map view: select a metatile (or a multi-tile selection) from the tileset panel, then paint with it using the brush, fill, or shape tools. A few workflow habits that pay off:

- Work in layers of intent, not layers of the software: rough in walkable terrain first, then obstruction/borders, then decoration last. Painting decoration before you've confirmed the walkable space works means redoing decoration when the layout changes.
- Toggle the **metatile grid overlay** on while placing anything alignment-sensitive (doors, connections, ledges) and off when eyeballing the visual result.
- Use **undo liberally** — Porymap's undo history is per-map and reasonably deep; treat placement as cheap and iterate rather than planning every tile before touching the canvas.

### 3.6 Map Connections

The **Connections** tab links one map's edge to an adjacent map's edge with a positional offset, producing a seamless walk-off transition rather than a warp (no fade-and-reload, no loading a separate room).

Each connection needs:
- A **direction** (north, south, east, or west) — which edge of the current map connects out.
- The **target map** it connects to.
- An **offset** — how the target map's edge aligns against the current one, since two maps of different widths won't line up edge-to-edge by default.

> **⚠ Pitfall** — Get the offset wrong and the seam will "jump" — terrain that looks continuous in the editor preview will visibly misalign in-game, or worse, walkable terrain on one side lines up with impassable terrain on the other, letting the player get stuck exactly on the boundary. Always walk the actual seam in-emulator after adding or changing a connection; the editor's preview is a strong guide but not a substitute for testing the transition itself.

### 3.7 Wild Encounters Configuration

The **Wild Pokémon** tab edits per-map encounter tables, with separate slot groups for land, surfing, rock smash, and each fishing rod tier (old/good/super). Each slot holds a species and a level range; the slot's *position* in the table — not a separately configured number — determines its relative encounter weight, following the series' traditional fixed probability distribution.

For a standard 12-slot land encounter table, the classic distribution (inherited from the mainline games and still the default expansion assumes unless you override it) looks like this:

| Slot | Weight |
|---|---|
| 1 | 20% |
| 2 | 20% |
| 3 | 10% |
| 4 | 10% |
| 5 | 10% |
| 6 | 10% |
| 7 | 5% |
| 8 | 5% |
| 9 | 4% |
| 10 | 4% |
| 11 | 1% |
| 12 | 1% |

Fishing rods use their own, shorter tables with different weight distributions per rod tier (Old Rod is the least generous and most common-species-weighted; Super Rod opens up rarer catches). The practical implication: slot *position* is doing real design work. Putting your rarest planned encounter in slot 1 will make it common regardless of what species it is.

This data is backed by `wild_encounters.json` and can be hand-edited for bulk changes or scripted generation, though the Porymap GUI is the recommended path for normal day-to-day editing since it validates structure for you.

### 3.8 Map Header Properties

Beyond the visual layout, each map carries header-level properties:

- **Name and name popup** — whether the map's name banner displays on entry (typically on for towns/routes, off for most building interiors).
- **Music** — the background track, selectable independently of visuals.
- **Weather** — rain, sandstorm, fog, etc., which can also be overridden dynamically by scripts at runtime.
- **Map type** — outdoor, indoor (building), underwater, secret base, and a few specialized types — this affects things like whether certain field moves are usable and how the game's "location" logic (e.g. Fly destinations) treats the map.
- **Battle scene** — controls the background used in wild/trainer battles triggered on this map, independent of the map's own visual tileset.
- **Floor number** — for multi-floor buildings, used by things like the in-game map/elevator UI.
- **Movement permissions** — flags controlling whether running, biking, or using an Escape Rope/Dig is allowed on this map.
- **Dive/emerge pairing** — for maps that connect via Dive, the header links the surface map and underwater map to each other.

### 3.9 The Events Tab in Depth

Four event categories, each with its own property set:

**Object events** — the most common type: NPCs, pushable items, decorative sprites.
- Graphics ID (which sprite sheet/palette to use)
- Starting facing direction
- Movement type (see Chapter 5.2 for the full catalog)
- Movement range (how far a wandering NPC is allowed to roam from its start point)
- Trainer type and sight radius, if this object event is a trainer battle
- Script pointer — what runs on interaction (or, for trainers, what runs on being spotted)
- An "in-connection" consideration — object events generally shouldn't be placed directly on a map's connection edge, since behavior there can be inconsistent across the seam

**Warp events** — doors, cave mouths, ladders, stairs.
- Destination map
- Destination warp ID (warps are matched by ID, not by coordinate, so the destination map needs a warp event with a matching ID waiting on the other side)
- Elevation, for multi-level maps where more than one warp could otherwise occupy the same x/y

**Trigger (coordinate) events** — scripts that fire when the player's coordinates match, with no dialogue box or object sprite involved. Commonly gated by a variable check so the trigger only fires once, or only after certain story conditions.

**Background events** — signs (readable text, no NPC sprite), hidden items (revealed by Itemfinder or similar), and secret base entrance spots.

### 3.10 A Complete Worked Example

To tie the chapter together, here's the shape of the full workflow for adding one new connected area — the sequence you'll repeat, with variations, for every map you build:

1. Create the new map: choose a map group, create a new layout at your target dimensions, assign a primary tileset and an appropriate secondary tileset.
2. Rough in walkable terrain first — get the shape of the space right before decorating it.
3. Assign metatile behaviors as you go, not as an afterthought — it's much easier to catch "this looks like grass but isn't tagged as encounter terrain" while you're actively placing it than to audit the whole map later.
4. Add the map connection back to wherever the player is arriving from, get the offset right, and test the seam in-emulator immediately.
5. Configure the wild encounter table for this map's terrain types, if any.
6. Set header properties — name popup, music, weather, map type, battle scene.
7. Place object events (NPCs, trainers), warp events (any doors/entrances into buildings on this map), and any triggers or background events the design calls for.
8. Build, test the whole area in-emulator: walk every edge, trigger every event, fight any trainer, and confirm wild encounters are pulling from the table you expect.

### Chapter 3 Summary

- Porymap owns generated project files (`map.json`, etc.) — treat them as build artifacts, not hand-editable source.
- Maps, layouts, and map groups are three distinct, nestable concepts.
- Primary tilesets are shared and should be edited conservatively; secondary tilesets are where area-specific art belongs.
- A metatile's *behavior* is independent of its *appearance* — always verify behavior, not just visuals, when something feels wrong.
- Map connections need a correct offset and should always be walk-tested in-emulator, not just previewed.
- Wild encounter slot *position* determines probability weight via a fixed distribution — design your slot order accordingly.
- Header properties (music, weather, map type, battle scene) are configured independently of the visual layout.
- Four event types exist — object, warp, trigger, and background — each with its own property set and use case.

### Try It Yourself

1. Build two small test maps and connect them in both directions; walk across the seam repeatedly until you're confident the offset is correct.
2. Create a patch of tall grass, assign it the correct encounter behavior, configure a small wild encounter table for it, and confirm in-emulator that encounters trigger only in the tagged tiles.
3. Place one of each event type — object, warp, trigger, background — on a single test map, and confirm each fires correctly before moving on to scripting their actual content in Chapter 4.

### Further Reading
- [Official Porymap guide](https://huderlem.github.io/porymap/)
- [Porymap GitHub / downloads](https://github.com/huderlem/porymap)
- [YouTube: Using Porymap](https://www.youtube.com/watch?v=mHokDsp_Ysk)


---

# Part III — Logic and Behavior

## Chapter 4: Scripting with Poryscript

**Learning objectives.** By the end of this chapter you should be able to: explain why Poryscript exists and how it relates to the engine's native bytecode; set up and convert an existing project to use it; write scripts using full control flow instead of manual branching; work confidently with flags, variables, and buffered text; and assemble common event patterns from memory rather than looking each one up from scratch.

### 4.1 Why Poryscript Exists

The engine's native scripting format is a flat, assembly-like bytecode (`.inc` files) — entirely readable, but genuinely tedious once you need real branching logic, because the native format has no structured `if` or loop construct; conditional logic is built from manual `goto`-style jumps and comparison commands. Poryscript is a higher-level language that transpiles down to that exact same bytecode at build time, giving you real `if/elif/else`, `while`, `do-while`, and `switch` — the compiler handles turning your structured logic into the jump-based bytecode the engine actually reads.

This matters practically: nothing is lost by using Poryscript (it produces the same underlying commands you'd write by hand), and a great deal is gained in readability and in avoiding a class of bugs where a hand-written jump target silently points at the wrong label after an edit.

### 4.2 Installation and Editor Integration

```
pokeemerald-expansion/tools/poryscript/poryscript(.exe)
pokeemerald-expansion/tools/poryscript/command_config.json
pokeemerald-expansion/tools/poryscript/font_config.json
```

Add the Makefile hook described in the [Poryscript README](https://github.com/huderlem/poryscript), and add the compiled `poryscript` binary itself (not the two config files) to `.gitignore` — the binary is a build tool, not project source, but the configs define project-specific command signatures and should be tracked.

Editor support:
- **VS Code** — official Poryscript extension: syntax highlighting, autocomplete, and inline error diagnostics as you type.
- **JetBrains IDEs** (IntelliJ, CLion) — a community plugin is available.
- **Tree-sitter–based editors** (Neovim, Emacs, Zed, Helix, Lapce) — community-maintained Tree-sitter bindings exist for syntax highlighting.

> **📝 Note** — The autocomplete and diagnostics from the VS Code extension are worth the five minutes of setup on their own; a large fraction of Poryscript errors are typos in a flag/var/species constant name, and the extension catches most of these before you even attempt a build.

### 4.3 Converting Legacy Scripts

```bash
# Wraps existing scripts.inc content in `raw` blocks inside a new
# scripts.pory file, per map, without overwriting maps that are
# already converted.
bash convert_inc.sh
```

The generated `raw` blocks let you incrementally rewrite old `.inc` logic into proper structured Poryscript at your own pace — a converted map builds identically to its pre-conversion state until you actually start editing inside the raw block.

```poryscript
script Script_LegacyExample {
    raw `
    lock
    faceplayer
    goto Common_EventScript_ShowLegacyText
    `
}
```

### 4.4 Scripts, Text, and Map Script Types

A `.pory` file mixes two block kinds:

```poryscript
script Script_Adam {
    lock
    faceplayer
    msgbox(Text_Adam)
    release
}

text Text_Adam {
    "Hi!\n"
    "My name is Adam.\l"
    "What's your name?\p"
    "Nice to meet you, {PLAYER}!"
}
```

Beyond ordinary interaction scripts, every map supports **map scripts** — special script hooks the engine calls automatically at specific lifecycle moments rather than on player interaction:

| Map script type | Fires when |
|---|---|
| `on_load` | The map is loaded into memory, before it's actually displayed |
| `on_transition` | During the fade transition into the map |
| `on_frame` | Every frame the map is active — used sparingly, for continuous checks |
| `on_resume` | When control returns to the map after a script, menu, or battle ends |
| `on_warp_into` | Specifically when the player warps into this map (as opposed to walking in via a connection) |

```poryscript
mapscripts MapScripts_ExampleTown {
    MAP_SCRIPT_ON_TRANSITION {
        if (!flag(FLAG_SEEN_INTRO_CUTSCENE)) {
            call Script_IntroCutscene
        }
    }
    MAP_SCRIPT_ON_RESUME: Script_ExampleTown_OnResume
}
```

> **⚠ Pitfall** — `on_frame` scripts run continuously while the map is active. Anything expensive or anything that isn't carefully gated by a flag/var check can produce subtle performance issues or repeatedly re-triggering behavior you only meant to fire once. Prefer `on_transition` or `on_resume` for one-time checks, and reserve `on_frame` for genuinely continuous conditions.

### 4.5 Core Command Reference

| Command | Purpose |
|---|---|
| `lock` | Freezes the calling NPC's movement |
| `lockall` | Freezes every NPC on the current map |
| `faceplayer` | Turns the NPC to face the player |
| `applymovement(target, movements)` | Runs a movement sequence on an object event (see 4.9) |
| `waitmovement(target)` | Blocks script execution until the movement finishes |
| `msgbox(text)` | Basic dialogue box, default confirm-to-continue behavior |
| `msgbox(text, MSGBOX_YESNO)` | Dialogue with a yes/no prompt, result stored for a following `if` |
| `msgbox(text, MSGBOX_SIGN)` | Sign-style box (no NPC "talking" framing) |
| `msgbox(text, MSGBOX_AUTOCLOSE)` | Closes itself after a delay, no player input required |
| `giveitem(item, quantity)` | Adds an item to the player's bag |
| `givemon(species, level, item)` | Adds a Pokémon to the player's party/PC |
| `playse(sound)` / `playfanfare(fanfare)` | Sound effects and jingles |
| `fadescreen(type)` | Screen fade for cutscene transitions |
| `warp(map, warpId, x, y)` | Standard warp, with transition |
| `warpsilent(map, warpId, x, y)` | Warp with no transition effect |
| `setweather(type)` | Overrides the current map's weather at runtime |
| `dofieldeffect(effect)` | Triggers a field effect animation |
| `special(functionName)` | Calls a native C "special" function registered for script use (see 8.4) |
| `closemessage` | Closes an open message box without waiting for input |
| `release` / `releaseall` | Inverse of lock/lockall |
| `end` | Terminates the script |
| `return` | Returns from a `call`ed sub-script |
| `call(label)` | Jumps to another script and returns when it finishes |
| `goto(label)` | Jumps to another script permanently, no return |

### 4.6 Control Flow in Depth

```poryscript
script Script_Example {
    if (var(VAR_STORY_PROGRESS) >= 3) {
        msgbox(Text_Later)
    } elif (flag(FLAG_MET_RIVAL)) {
        msgbox(Text_MidGame)
    } else {
        msgbox(Text_Early)
    }

    while (var(VAR_COUNTER) < 5) {
        // repeated logic; remember to advance VAR_COUNTER inside the loop
        // or this will hang the script permanently at runtime
    }

    do {
        // runs at least once before the condition is checked
    } while (flag(FLAG_KEEP_GOING))

    switch (var(VAR_CHOICE)) {
        case 0:
            msgbox(Text_OptionA)
        case 1:
            msgbox(Text_OptionB)
        default:
            msgbox(Text_Fallback)
    }
}
```

Compound conditions combine with `&&` and `||`, and can be grouped with parentheses exactly as you'd expect from C:

```poryscript
if ((flag(FLAG_A) && flag(FLAG_B)) || var(VAR_OVERRIDE) == 1) {
    msgbox(Text_SpecialCase)
}
```

> **⚠ Pitfall** — A `while` loop with no condition-changing logic inside it is an infinite loop that will hang the game, not just the script. This is one of the few Poryscript mistakes that produces a hard freeze rather than a clean compiler or runtime error, so double check the loop's exit condition is actually reachable before you build.

### 4.7 Flags and Variables

```poryscript
if (flag(FLAG_RECEIVED_STARTER)) { ... }
setflag(FLAG_RECEIVED_STARTER)
clearflag(FLAG_RECEIVED_STARTER)

if (var(VAR_RIVAL_NAME) == 1) { ... }
setvar(VAR_RIVAL_NAME, 1)
addvar(VAR_STORY_PROGRESS, 1)
```

Two practical conventions worth adopting early:

- **Reserve a contiguous block of your own flags and vars** for project-specific use, separate from the engine's own reserved ranges (a handful of temp vars near the top of the variable space are used transiently by the engine itself and shouldn't be repurposed for persistent story state).
- **Name flags and vars descriptively and consistently** (`FLAG_RECEIVED_STARTER`, not `FLAG_0x900`) — with hundreds of story flags by the end of a project, self-documenting names are the only realistic way to avoid collisions and confusion months later.

### 4.8 The Text System in Depth

```
{PLAYER}          - inserts the player's name
{RIVAL}            - inserts the rival's name, if configured
{STR_VAR_1}         - inserts a buffered string (set via buffervar/bufferstring or C)
\n                  - line break within the same text box
\l                  - line break that waits for a player button press
\p                  - starts a new text box entirely (paragraph break)
```

**Buffering** lets a script insert dynamic content — a variable's value, an item name, a species name — into otherwise-static text:

```poryscript
script Script_BufferExample {
    lock
    faceplayer
    bufferitemname(STR_VAR_1, ITEM_POTION)
    msgbox(Text_YouReceivedBuffered)
    giveitem(ITEM_POTION)
    release
}

text Text_YouReceivedBuffered {
    "You received a {STR_VAR_1}!"
}
```

**Multiple choice** prompts use a dedicated command rather than a plain msgbox:

```poryscript
script Script_MultichoiceExample {
    lock
    faceplayer
    msgbox(Text_ChooseOne)
    multichoice(0, 0, MULTI_YESNO, FALSE)
    if (var(VAR_RESULT) == 0) {
        msgbox(Text_ChoseYes)
    } else {
        msgbox(Text_ChoseNo)
    }
    release
}
```

Color and highlight escape codes exist for stylized text (shop dialogue, emphasis on key story terms) — see the linked video tutorial below for the specific codes and hex values, since they're easier to demonstrate visually than to describe in a table.

> **📝 Note** — Text boxes have a finite visible character width per line before wrapping becomes ugly rather than automatic. Long, unbroken sentences without a manual `\n` in a sensible place will wrap wherever the engine happens to run out of room, which is rarely where you'd choose. Break your own lines deliberately rather than relying on auto-wrap for anything you care about the look of.

### 4.9 Movement Scripting

`applymovement` takes a target (an object event ID, or `OBJ_EVENT_ID_PLAYER`) and a named sequence of movement commands:

```poryscript
script Script_MovementExample {
    lock
    applymovement(OBJ_EVENT_ID_PLAYER, Movement_PlayerStepBack)
    waitmovement(0)
    applymovement(LOCALID_RIVAL, Movement_RivalWalkUp)
    waitmovement(0)
    msgbox(Text_RivalConfrontation)
    release
}

movement Movement_PlayerStepBack {
    walk_down
    face_up
}

movement Movement_RivalWalkUp {
    walk_up
    walk_up
    face_player
}
```

Common movement commands: `walk_up/down/left/right`, `run_up/down/left/right`, `face_up/down/left/right`, `face_player`, `jump_up/down/left/right` (for ledges), `delay` (a pause with no movement), `set_invisible` / `set_visible`, `lock_facing_direction` / `unlock_facing_direction`, and `walk_in_place_*` for a stationary animation (e.g. someone digging or fishing without moving).

> **⚠ Pitfall** — `applymovement` is asynchronous — the script continues immediately unless you explicitly `waitmovement`. Skipping the wait is a common cause of dialogue appearing before a character has finished visibly walking into position, since the two are actually racing rather than sequenced.

### 4.10 A Library of Common Patterns

**One-time trigger, gated by a flag:**
```poryscript
script Script_OneTimeEvent {
    if (flag(FLAG_EVENT_DONE)) {
        end
    }
    lock
    faceplayer
    msgbox(Text_FirstTime)
    setflag(FLAG_EVENT_DONE)
    release
}
```

**Give an item:**
```poryscript
script Script_GiveItem {
    lock
    faceplayer
    giveitem(ITEM_POTION)
    msgbox(Text_HereYouGo)
    release
}
```

**Give a Pokémon:**
```poryscript
script Script_GivePokemon {
    lock
    faceplayer
    givemon(SPECIES_RALTS, 5, ITEM_NONE)
    msgbox(Text_TakeThisPartner)
    release
}
```

**Warp-on-touch trigger (no dialogue):**
```poryscript
script Script_HiddenWarp {
    warp(MAP_SOME_DESTINATION, WARP_ID, 5, 5)
    waitstate
}
```

**Branching dialogue with a yes/no choice:**
```poryscript
script Script_YesNoBranch {
    lock
    faceplayer
    msgbox(Text_AskToBattle, MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {
        call Script_StartBattle
    } else {
        msgbox(Text_MaybeNextTime)
    }
    release
}
```

**NPC that gives an item once, then only talks:**
```poryscript
script Script_NPCOneTimeGift {
    lock
    faceplayer
    if (flag(FLAG_RECEIVED_GIFT)) {
        msgbox(Text_AlreadyGaveGift)
    } else {
        msgbox(Text_HereIsAGift)
        giveitem(ITEM_RARE_CANDY)
        setflag(FLAG_RECEIVED_GIFT)
    }
    release
}
```

**Checking whether the player's party contains a species:**
```poryscript
script Script_CheckForSpecies {
    lock
    faceplayer
    special(HasSpeciesInParty)   // hypothetical special; see Chapter 8.4
    if (var(VAR_RESULT) == TRUE) {
        msgbox(Text_YouHaveIt)
    } else {
        msgbox(Text_YouDoNotHaveIt)
    }
    release
}
```

**Short cutscene combining movement and dialogue:**
```poryscript
script Script_SmallCutscene {
    lockall
    applymovement(LOCALID_NPC, Movement_NPCApproach)
    waitmovement(0)
    msgbox(Text_NPCLine)
    applymovement(LOCALID_NPC, Movement_NPCLeave)
    waitmovement(0)
    releaseall
}

movement Movement_NPCApproach {
    walk_down
    walk_down
    face_player
}

movement Movement_NPCLeave {
    walk_up
    walk_up
}
```

### Chapter 4 Summary

- Poryscript transpiles to the same bytecode you'd write by hand; nothing is lost, structured control flow is gained.
- Map scripts (`on_load`, `on_transition`, `on_frame`, `on_resume`, `on_warp_into`) are automatic hooks, distinct from interaction scripts.
- `while` loops need a reachable exit condition — an unbounded loop hangs the whole game, not just the script.
- `applymovement` is asynchronous; pair it with `waitmovement` whenever the following dialogue depends on the movement finishing first.
- Reserve a dedicated flag/var range for your project and name them descriptively from the start.

### Try It Yourself

1. Convert one existing map's `.inc` scripts to `.pory` and rewrite at least one branch inside it as structured `if/elif/else` instead of a raw block.
2. Write an NPC that gives an item exactly once, using a flag check, and confirm both the "first visit" and "already received" paths in-emulator.
3. Write a short two-beat cutscene: an NPC walks toward the player, delivers a line, and walks away, with correct `waitmovement` calls at each step.

### Further Reading
- [Poryscript GitHub README](https://github.com/huderlem/poryscript)
- [Huderlem's blog: Poryscript design](https://www.huderlem.com/blog/posts/poryscript/)
- [YouTube: Intro to Poryscript](https://www.youtube.com/watch?v=IY3tpjyVm0Y)
- [YouTube: Poryscript Syntax and Giving Pokémon](https://www.youtube.com/watch?v=lWG-wJuclX4)
- [PokéCommunity Scripting Tutorial](https://www.pokecommunity.com/threads/scripting-tutorial.416800/)
- [YouTube: Text Formatting — Color and Buffering Strings](https://www.youtube.com/watch?v=avMM_cc6hHE)


## Chapter 5: NPCs, Object Events & Trainers

**Learning objectives.** By the end of this chapter you should be able to: explain how object events are represented and registered; choose the correct built-in movement type for a given NPC's intended behavior; configure a trainer battle with the right sight range and post-battle flow; read and modify trainer party data; and use the Task System for logic that needs to persist across multiple frames.

### 5.1 Object Event Architecture

Every placeable NPC, item, or decorative sprite in the overworld is an **object event**. Each one is backed by a graphics info entry that defines its visual identity — sprite sheet, dimensions, palette, shadow size, and which animation table drives its walking frames — separately from the *placement* data (position, movement type, script pointer) that Porymap manages per-map.

This separation matters practically: adding a brand new overworld sprite means registering a new graphics info entry once, in code; placing instances of that sprite around your world is then a Porymap-only operation with no further code changes needed.

Object events also carry an **elevation** value, used to disambiguate stacked geometry — a bridge over water, an upper floor visible below a gap — so the engine knows which layer of overlapping walkable space a given event belongs to.

### 5.2 Movement Types, Full Catalog

| Movement type | Behavior |
|---|---|
| Face direction (static) | Never moves; only ever faces one fixed direction |
| Look around | Idle in place, periodically glances in different directions |
| Walk in place | Animates a walking motion without changing position (useful layered under other logic) |
| Walk randomly | Wanders within a configured radius of its starting point, pausing between moves |
| Walk in a set pattern / follow a path | Repeats a fixed movement loop, useful for patrolling guards or predictable wildlife |
| Face player when approached | Static until the player enters its detection range, then turns to face them |
| Follow the player | Used for following-Pokémon-style behavior; tracks the player's recent path |
| Copy player | Mirrors the player's own movement input, offset by position (used for some puzzle/cutscene NPCs) |

Choosing the right one is mostly about matching player expectations: a shopkeeper should almost never wander (Face Direction or Look Around), a wild patrolling guard should use a fixed path, and background flavor NPCs (kids playing, birds in a park) read best with Walk Randomly.

### 5.3 Custom Movement and Paths

For behavior more specific than the built-in catalog — an NPC that walks a deliberate, non-repeating path as part of a cutscene rather than a passive idle loop — the correct tool is a **scripted movement**, not a movement-type setting. See Poryscript's `applymovement` (Chapter 4.9) for one-off scripted movement; for something that needs to repeat indefinitely as ambient behavior, a fixed-path movement type configured directly on the object event in Porymap is usually the better fit, since it doesn't require a running script to sustain it.

> **📝 Note** — A common design mistake is scripting an NPC's idle wandering with `applymovement` triggered from an `on_frame` map script. This works, but it's fighting the engine — the built-in "Walk Randomly" or fixed-path movement types are purpose-built for exactly this and cost nothing in script complexity or performance. Reach for scripted movement only when the behavior is genuinely one-time or story-triggered.

### 5.4 The Trainer Battle System

A trainer object event carries its own property set beyond the general object event fields: a **trainer type**, a **sight range**, and battle-specific flags.

```poryscript
script Script_TrainerBattle {
    trainerbattle_single(TRAINER_RIVAL_1, Text_BeforeBattle, Text_AfterBattle)
    msgbox(Text_PostBattleChat)
    release
}
```

Variants exist for the common cases:

- `trainerbattle_single` — standard 1v1 trainer.
- `trainerbattle_double` — a double battle, either against a single trainer running two Pokémon or (with `trainerbattle_rematch_double` and similar) two trainers together.
- `trainerbattle_rematch` — a trainer that can be re-fought, typically after a cooldown or story condition, generally paired with a second, stronger party configured for the rematch.

**Sight range** governs whether the trainer initiates battle automatically when the player walks into their forward-facing line of sight, versus only battling if the player talks to them directly. A trainer with sight range configured will call their "trainer sees you" behavior — usually an exclamation mark, a sound cue, and the trainer walking to close the distance — before the pre-battle text plays.

Trainer-level flags (exact names vary by version, but the concepts are consistent) commonly include:

- Whether the intro trainer-slide animation plays or is skipped.
- Whether the trainer can be battled again after losing to the player, versus becoming permanently defeated.
- Whether losing the battle sends the player to a Pokémon Center (mainline default) or has some custom consequence.

> **⚠ Pitfall** — A trainer's sight range interacting with tightly packed indoor spaces can produce battles triggering from angles that feel unfair to the player (spotted through what looks like a wall corner, or the instant they round it). Always test sight-range trainers by walking every plausible approach angle, not just the one you designed the room around.

### 5.5 Trainer Data Structure

Each trainer entry defines, at minimum:

- **Trainer class** — controls default battle music, intro animation style, and the class name shown in battle ("Youngster," "Ace Trainer," etc.).
- **AI flags** — a bitfield selecting which decision-making behaviors the trainer's AI uses in battle: whether it avoids obviously bad moves, tries to set up before attacking, switches out of unfavorable matchups, plays around status conditions, and so on. Weaker early-game trainers typically get few or no AI flags; late-game and postgame trainers get a fuller set to feel meaningfully sharper.
- **Party** — either a simple party (species and level only, with moves derived automatically from the species' learnset) or a fully custom party specifying exact moves, held items, and IVs per Pokémon. Custom parties require more entry work but are what any trainer meant to feel deliberately designed — a gym leader, a rival, a postgame boss — should use.
- **Items** — a trainer can carry a small pool of usable items (Full Restores, X Attacks, etc.) that its AI is allowed to use mid-battle if the relevant AI flag is set.
- **Double battle flag** — whether this trainer's encounter is a double battle.

> **📝 Note** — Custom movesets on trainer Pokémon are one of the highest-value, lowest-cost ways to make a trainer feel distinct. A generic "levels 1–4 learnset" Pikachu and a hand-tuned Pikachu carrying Thunderbolt, Iron Tail, Volt Switch, and Protect read as completely different opponents despite being the same species and level.

### 5.6 Following Pokémon

pokeemerald-expansion includes built-in support for an overworld-following partner Pokémon (in the style introduced by HeartGold/SoulSilver), including interaction dialogue and basic emotive reactions. Enabling it is primarily a `config.h` toggle plus a small amount of setup for which conditions summon/dismiss the follower — check `FEATURES.md` and the config file for the current toggle names, since this is exactly the kind of feature that used to require substantial custom C before it was folded into expansion as a standard, supported system.

### 5.7 The Task System in Depth

Tasks are the engine's mechanism for logic that must persist across multiple frames — anything that can't complete instantly within a single script call. Each running task gets a small block of persistent data (commonly referred to as `data[]`, a fixed-size array of working values) that survives between frames, plus a priority value controlling execution order relative to other simultaneously running tasks.

```c
// Illustrative pattern — field/function names are representative,
// not guaranteed literal in your checkout.
static void Task_ExampleDelayedAction(u8 taskId)
{
    if (gTasks[taskId].data[0]++ > 60) // roughly 1 second at 60fps
    {
        // do the thing the delay was waiting for
        DestroyTask(taskId);
    }
}

// Elsewhere, to start it:
CreateTask(Task_ExampleDelayedAction, 0); // 0 = priority
```

Common uses: a weather effect that needs to animate continuously, a cutscene beat that must wait a fixed duration before continuing, or a repeating background check (e.g. "has the player's party changed since last frame") that a single script call can't represent.

> **⚠ Pitfall** — Forgetting to `DestroyTask` when a task's job is done leaves it running indefinitely, silently consuming a task slot and continuing to execute its body every frame forever. This is a common source of "why is this sound effect looping forever" or "why did performance degrade the longer I played" bugs. Every `CreateTask` should have a clearly reachable `DestroyTask` somewhere in its own logic.

### 5.8 Field Effects and Special Functions

Beyond tasks, two more native-C hooks are commonly reached for from scripts:

- **Field effects** — visual/animation routines (dust clouds, splash effects, the sand-footprint trail) triggered via the `dofieldeffect` script command, backed by their own sprite templates and callback functions in C.
- **Special functions** — arbitrary native C functions explicitly registered to be callable by name from a script via the `special(...)` command. This is the standard bridge whenever a script needs to do something too complex or too stateful for Poryscript's own command set — checking complex party conditions, running custom math, or interacting with save data in ways no existing command exposes. See Chapter 8.4 for how to add a new one.

### Chapter 5 Summary

- Object events separate visual identity (graphics info, registered once) from placement (Porymap-managed, per instance).
- Choose movement types to match the *kind* of behavior wanted — static, idle, patrol, wander, or follow — rather than scripting ambient behavior that a built-in type already covers.
- Trainer battles are configured through sight range, trainer type, and dedicated `trainerbattle_*` script commands, layered under a full trainer data entry (class, AI flags, party, items).
- Custom trainer movesets are a high-value, low-cost way to differentiate trainers.
- Tasks handle any logic that needs to persist across frames; always ensure a `DestroyTask` is reachable to avoid a task leaking forever.
- `special()` functions are the standard bridge from scripts into native C for anything beyond Poryscript's built-in command set.

### Try It Yourself

1. Place three NPCs using three different movement types (static, walk randomly, fixed path) on one test map and confirm each behaves as expected.
2. Build a trainer battle with a sight-range trigger, a custom moveset on at least one party member, and a post-battle dialogue script.
3. Write a task that waits three seconds after being created, then triggers a message box, and confirm it correctly destroys itself afterward (check for it lingering by triggering it twice in a row).

### Further Reading
- [YouTube: The Task System](https://www.youtube.com/watch?v=-4lQeHUQXXU)


---

# Part IV — Content and Data

## Chapter 6: Gameplay Data Entry

**Learning objectives.** By the end of this chapter you should be able to: add a complete new species end to end, across every file it touches; configure learnsets, evolution, and Pokédex data correctly; build both simple and fully custom trainer parties; understand the probability math behind wild encounter tables well enough to design around it; and locate the right data table when adding or modifying a move, ability, or item.

> **📝 Note on specificity.** This chapter references struct fields and table names more specifically than earlier chapters, because gameplay data entry is inherently about specific fields. Treat field names as illustrative of the *shape* of each data structure — verify exact names against your own checkout's headers before relying on them literally.

### 6.1 The Species Pipeline in Depth

Order matters — the species constant must exist before anything else can reference it. A complete new species touches, at minimum:

1. **Species constant** — add `SPECIES_YOURMON` to the species constants file. This single line is the anchor every other file below hangs off of.
2. **Base stats table entry** — the core `gSpeciesInfo`-style struct, commonly including:
   - `baseHP`, `baseAttack`, `baseDefense`, `baseSpAttack`, `baseSpDefense`, `baseSpeed`
   - `type1`, `type2`
   - `catchRate`
   - `expYield`
   - `evYield_*` (which stats this species grants EVs in on defeat)
   - `itemCommon`, `itemRare` (wild held item chances)
   - `genderRatio`
   - `eggCycles`
   - `friendship` (base happiness)
   - `growthRate`
   - `eggGroup1`, `eggGroup2`
   - `abilities[3]` (two regular ability slots plus a hidden ability slot)
   - `safariZoneFleeRate`
   - `bodyColor`, `noFlip` (used by some Pokédex/UI display logic)
3. **Level-up learnset** — an ordered table of (level, move) pairs.
4. **TM/tutor compatibility** — which TMs and move tutors this species can use; expansion-era projects typically use a per-species list rather than the old fixed-width bitfield, but check your version.
5. **Egg moves** — a list of moves obtainable only through breeding.
6. **Evolution table** — method, condition parameter, and target species (see 6.3).
7. **Pokédex entry** — category name, flavor text, height, weight, and dex number/ordering (see 6.4).
8. **Graphics** — front sprite, back sprite, icon, footprint, cry, and normal + shiny palettes (see Chapter 7).

> **⚠ Pitfall** — The single most common early mistake is confusing **dex number** (the species' position in the Pokédex listing, which you control and which can be reordered) with **species ID** (the internal constant, which should never be reordered once other data references it). Renumbering species IDs after other tables already reference them is a self-inflicted wound that touches nearly every file above; get the constant right once, at the start, and only ever adjust dex *ordering* afterward.

This is genuinely one of the more tedious workflows in the whole project — there is no way around touching six-plus files per species — but expansion's data tables are consistently structured, so the second entry goes considerably faster than the first once the pattern is familiar.

### 6.2 Learnsets

Level-up learnsets are a straightforward ordered list:

```c
// Illustrative
static const struct LevelUpMove sYourmonLevelUpLearnset[] = {
    LEVEL_UP_MOVE( 1, MOVE_GROWL),
    LEVEL_UP_MOVE( 1, MOVE_TACKLE),
    LEVEL_UP_MOVE( 7, MOVE_CONFUSION),
    LEVEL_UP_MOVE(13, MOVE_TELEPORT),
    LEVEL_UP_MOVE_END
};
```

TM/tutor compatibility and egg moves follow similar list-based patterns in modern expansion versions — copy the closest comparable existing species (similar typing, similar role) as your starting template rather than building the list from a blank file; it's much faster to prune/add to a reasonable starting set than to reconstruct one from scratch.

### 6.3 Evolution Data

Evolution entries specify a method, a condition parameter (interpreted differently depending on the method), and a target species:

| Method | Condition parameter means |
|---|---|
| `EVO_LEVEL` | Minimum level |
| `EVO_ITEM` | Which evolution item is used |
| `EVO_TRADE` | Optionally, a specific held item required at time of trade |
| `EVO_FRIENDSHIP` | Minimum friendship value, optionally time-of-day gated |
| `EVO_MOVE_LEARNED` | Which move must be known |
| `EVO_LOCATION` | Which map/region the evolution can occur in |

```c
// Illustrative
static const struct Evolution sYourmonEvolutions[] = {
    {EVO_LEVEL, 16, SPECIES_YOURMON_EVO},
    EVOLUTIONS_END
};
```

A single species can have multiple valid evolution entries (branching evolutions — think Eevee), each independently evaluated whenever an evolution check runs.

### 6.4 Pokédex Entries

Pokédex data is mostly presentational but still required for a species to feel complete: category name ("the Seedling Pokémon"), flavor text, height and weight (used both for display and for a small number of move/ability interactions that key off height, like Skill Swap-adjacent effects or Powder-type weight interactions), and the species' position in dex ordering, which is a separate, safely-editable concern from its underlying species ID (see the Pitfall in 6.1).

### 6.5 Trainer Data Entry in Depth

Trainer entries commonly separate into a simple and a custom path:

```c
// Illustrative: simple party, moves derived from level-up learnset
static const struct TrainerMon sRivalParty_Simple[] = {
    { .species = SPECIES_YOURMON, .lvl = 12 },
};

// Illustrative: custom party with explicit moves, held item, and IVs
static const struct TrainerMon sRivalParty_Custom[] = {
    {
        .species = SPECIES_YOURMON_EVO,
        .lvl = 34,
        .moves = {MOVE_THUNDERBOLT, MOVE_IRON_TAIL, MOVE_VOLT_SWITCH, MOVE_PROTECT},
        .heldItem = ITEM_SITRUS_BERRY,
        .iv = 20,
    },
};
```

AI flags are a bitfield combined with `|`, commonly including concepts like: avoiding moves that would be resisted or immune, trying to set up stat boosts before attacking when safe, switching out of unfavorable type matchups, tracking and playing around status conditions, and using held/carried items when in danger. Weak early trainers typically ship with few or none of these; a gym leader or rival should carry enough to feel like they're making real decisions rather than attacking at random.

### 6.6 Wild Encounter Tables in Depth

Building on the Porymap-side configuration from Chapter 3.7, the underlying `wild_encounters.json` structure groups entries by map, with separate arrays for land, water, rock smash, and each fishing rod tier. Each array entry is a `{species, min_level, max_level}` triple, and — critically — **array position determines probability weight** via the fixed distribution shown in Chapter 3.7, not any value stored on the entry itself.

The direct design implication: reordering two entries in the array changes their relative rarity without changing anything else about them. This is worth deliberately exploiting — if a species needs to feel rare on a route without being absent entirely, put it in a low-weight slot rather than reducing the pool in some other way.

### 6.7 Moves and Move Effects

A move's data entry typically includes:

- `power`, `accuracy`, `pp`
- `type`, `category` (physical/special/status)
- `effect` — which effect routine the battle engine runs (many moves share effects and differ only in power/accuracy/flags; genuinely novel effects require new battle-script work, covered in Chapter 8.5)
- `target` — which battle-side/slot targeting rule applies
- `priority` — turn-order priority bracket
- `flags` — a bitfield covering things like `FLAG_MAKES_CONTACT` (relevant to contact-triggered abilities/items like Rough Skin or Rocky Helmet), `FLAG_PROTECT_AFFECTED`, `FLAG_MIRROR_MOVE_AFFECTED`, `FLAG_SNATCH_AFFECTED`, and similar

The overwhelming majority of "new move" requests are satisfied by reusing an existing effect with different power/accuracy/type/flags — expansion ships effects up through very recent generations, so check whether the mechanic you want already exists as an effect before assuming you need new battle-script work.

### 6.8 Abilities

Ability entries pair a description with an effect hook into the battle engine, triggered at specific well-defined moments: on switch-in, on taking damage, on a stat change, on weather change, on contact received, at end of turn, and several others. As with moves, most new-ability requests turn out to be a recombination of existing trigger points and effects rather than something requiring a genuinely new hook — check the existing ability list for the closest analog before writing new C.

### 6.9 Items

Item entries define price, description, which bag pocket they sort into, an item "type" (used for things like whether it's a key item, a TM, a berry), and function pointers for how it behaves — a `fieldUseFunc` for out-of-battle use (like a Repel or an Escape Rope) and separate battle-use handling for in-battle items (like a Potion or an X Attack). A `secondaryId` field is used by some item families (e.g. distinguishing which TM number a TM item corresponds to, or which specific berry).

### Chapter 6 Summary

- Species ID must be added first; every other data table hangs off it. Never confuse species ID (permanent, internal) with dex number (safely reorderable, presentational).
- A complete species touches base stats, learnset, TM/tutor compatibility, egg moves, evolution, Pokédex text, and a full graphics set.
- Evolution entries can branch — a species can have multiple valid evolution paths, each independently checked.
- Trainer parties range from simple (species + level) to fully custom (explicit moves, held item, IVs) — custom parties are worth the extra entry time for any trainer meant to feel deliberately designed.
- Wild encounter slot *position*, not any explicit probability field, determines weight — design encounter table order deliberately.
- Most "new move" and "new ability" requests are recombinations of existing effects and trigger points, not genuinely novel mechanics — check before writing custom battle-script logic.

### Try It Yourself

1. Add one complete new species from scratch — constant, base stats, a small learnset, one evolution, and Pokédex text — and confirm it's encounterable, battleable, and evolves correctly in-emulator.
2. Build both a simple and a fully custom trainer party for the same species and compare how differently they play in a test battle.
3. Take one existing map's wild encounter table and deliberately reorder two entries to swap their relative rarity, then confirm the change in-emulator across enough encounters to notice the shift.

### Further Reading
- [YouTube: Adding New Pokémon — Expanding the Pokédex](https://www.youtube.com/watch?v=T4tNu-MaYH4)


---

# Part V — Art and Presentation

## Chapter 7: Graphics & Sprites

**Learning objectives.** By the end of this chapter you should be able to: explain the GBA's indexed-color constraint well enough to avoid the most common import failures; set up a working indexed-art pipeline; add a complete overworld sprite and a complete battle sprite, correctly registered; manage palettes without collisions; and animate a tile or field effect.

### 7.1 GBA Graphics Fundamentals

The Game Boy Advance renders in **tile-based, indexed color** — this is the single fact that shapes every graphics workflow in this chapter. Rather than storing a full RGB value per pixel, each pixel stores an *index* into a small, separately-defined palette (commonly 16 colors per palette for most sprites and backgrounds, occasionally 256 for specific UI contexts). The hardware has a limited number of palette *slots* available simultaneously, shared across everything on screen — sprites, background layers, and UI — at once.

The practical consequence: a modern art tool exporting a naive full-color RGBA PNG will either fail to import cleanly or import with visibly wrong colors, because there's no indexed palette embedded in the file for the build pipeline to read. Every graphics asset in this project needs to be produced in, or converted into, genuine indexed-color form — not just visually limited to a small number of colors, but structurally saved as an indexed image with an explicit palette.

> **⚠ Pitfall** — "Looks like it only has 16 colors" is not the same thing as "is a properly indexed 16-color PNG." A full-color image that happens to only use 16 distinct RGB values will still fail to import correctly unless it was actually saved in indexed mode with those 16 values as its embedded palette. Always verify indexing mode in your art tool's export settings, not just by eyeballing the color count.

### 7.2 Tool Chain Setup

- **Pixelorama** (free, cross-platform, Mac-friendly) — set canvas/document color mode to **indexed** before drawing, not after; export as PNG with nearest-neighbor scaling if resizing, which preserves hard pixel edges instead of introducing blur/anti-aliasing artifacts that break indexing.
- **GraphicsGale** (Windows) — the tool assumed by most of the classic PokéCommunity tutorials; strong indexed-palette editing tools and a long history of decomp-specific workflow writeups built around it.
- **Porypal** — a free, open-source conversion utility specifically for turning full-color art into properly indexed, decomp-ready assets, useful if part of your pipeline (concept art, an AI-generated reference image, art from a collaborator using a different tool) produces RGBA output you need to convert rather than author natively in indexed mode.

Whichever tool you use, the practical checklist before importing anything is consistent: confirm indexed color mode, confirm the palette size fits the target budget (16 colors for the overwhelming majority of assets), and confirm dimensions match what the target system expects (see 7.3 and 7.4).

### 7.3 Overworld Sprite Pipeline in Depth

Overworld sprite sheets live in `graphics/object_events/pics/`, with their palettes in `graphics/object_events/palettes/`. A sheet is a strip of individual walking-animation frames — typically several frames per facing direction (down, up, left/right, often mirrored rather than drawn twice for left vs. right) — arranged in a fixed layout the build tooling expects.

Every sprite sheet is registered in the object event graphics info table, which defines (illustratively):

```c
// Illustrative
static const struct ObjectEventGraphicsInfo sYourmonFollowerGraphicsInfo = {
    .size = sizeof(sYourmonFollowerPicTable),
    .width = 16,
    .height = 32,
    .paletteTag = OBJ_EVENT_PAL_TAG_YOURMON,
    .shadowSize = SHADOW_SIZE_M,
    .tracks = TRACKS_FOOT,
    .oam = &sOamYourmon,
    .subspriteTables = sSubspriteTablesYourmon,
    .anims = sAnimTableYourmon,
    .images = sPicTableYourmon,
};
```

Once this registration exists, placing instances of the sprite is purely a Porymap operation — no further code changes are needed to use the same sprite for multiple object events across your world.

### 7.4 Battle Sprite Pipeline in Depth

Battle-context art is a separate asset family from overworld sprites, with its own conventions:

- **Front sprite** and **back sprite** — larger, more detailed art shown during battle, conventionally around 64×64 for most species (larger/legendary species commonly use bigger canvases within the engine's supported bounds).
- **Icon sprite** — the small (commonly 32×32-class) art used in menus, the party screen, and the Pokédex list.
- **Footprint** — a tiny 1-bit (not indexed-color, genuinely 1-bit) icon used in some Pokédex UI contexts.
- **Cry** — an audio asset, not visual, but conventionally added alongside the rest of a species' presentation set.

Both front and back sprites need **normal and shiny palette pairs** — two distinct palettes applied to the same underlying pixel/index data, so a shiny Pokémon shares its sprite's shape entirely and differs only in which palette is bound at render time.

Battle sprite **animation** (the idle bounce/breathing motion, and any special per-species animation) is driven by an `AnimCmd` table referencing frame data and timing, separate from the static front/back art itself.

### 7.5 Palette Management

Because palette slots are a shared, finite resource, every new sprite you register is implicitly competing for space with everything else that might be on screen simultaneously. Two practices keep this manageable:

- **Palette tags** — sprites are matched to their palette by a tag rather than a hard-coded index, letting the engine manage actual slot allocation dynamically as sprites load and unload. Always register a new sprite with a unique tag rather than reusing an existing one unless you specifically intend for two sprites to share a palette.
- **Reuse deliberately, not accidentally** — sharing a palette between two sprites that are genuinely meant to look color-coordinated is a valid, common technique (and saves palette budget). Two unrelated sprites accidentally sharing a palette because one was copy-pasted from the other without updating the tag is a bug, and usually shows up as one sprite's colors subtly shifting whenever the other is also loaded.

> **📝 Note** — If your project's design calls for very large numbers of simultaneously-visible custom overworld sprites (a crowded market scene, a large battle facility roster on screen at once), palette budget is worth thinking about at a design level, not just a technical one — it may be the actual limiting factor on how visually dense a scene can be, more than raw sprite count.

### 7.6 Tile and Tileset Art

Tilesets (Chapter 3.3) are built from individual tiles composited into metatiles across up to three layers (bottom, middle, top), with middle and top layers supporting transparency for overlap effects. The practical tile budget — how many distinct raw tiles a primary or secondary tileset can contain — is a genuine constraint worth respecting deliberately: an overly ambitious secondary tileset can leave no room for later additions to that same map cluster.

### 7.7 Animating Tiles and Field Effects

Two distinct animation systems exist, easy to conflate:

**Metatile (terrain) animation** — used for things like flowing water or swaying grass, implemented as tile *swapping* over time rather than sprite movement: the engine cycles through a small sequence of tile images assigned to the same metatile position, on a timer, rather than any object actually moving.

**Field effect (object) animation** — used for one-off or triggered visual effects (a splash when entering water, a dust cloud on a ledge jump, a footprint trail in sand), implemented as an actual animated sprite with its own frame strip, following the same 16×16-alignment and transparent-background-color conventions as other overworld art. Adding a new field effect means: creating the indexed frame-strip art, registering a sprite template and animation table for it, writing (or reusing) a callback function that drives its lifecycle, and adding an entry to the field effects table so it's callable via the `dofieldeffect` script command (Chapter 4.5).

### 7.8 UI and Menu Graphics

Title screen and other full-screen UI assets follow the same indexed `.png`/`.pal` pairing convention as gameplay art, with the added wrinkle that some UI elements are tied closely to their driving C logic (for the title screen specifically, `src/title_screen.c`) rather than being purely data-driven — meaningful title screen changes typically mean touching both the art and that source file together, not art alone.

> **⚠ Pitfall** — When editing an existing indexed PNG (rather than creating one from scratch), preserve the original indexing exactly — don't re-save it out of indexed mode and back in, and don't let your art tool "helpfully" re-optimize the palette order. A re-indexed image with the same visual appearance but a different underlying index-to-color mapping can still break rendering if any code references specific index values directly (a common pattern for things like a semi-transparent or "screen" blend index).

### Chapter 7 Summary

- The GBA renders in indexed color with a shared, limited palette budget — every asset needs genuine indexed export, not just a visually small color count.
- Overworld sprites separate registered graphics info (code, once) from placement (Porymap, per instance).
- Battle sprites need front, back, icon, and footprint art, each with normal and shiny palette pairs.
- Palette tags manage shared, finite palette slots — reuse deliberately, and watch for accidental sharing from careless copy-pasting.
- Metatile animation (tile swapping) and field effect animation (actual animated sprites) are two distinct systems serving different use cases.
- UI assets like the title screen often require touching both art and driving C code together.

### Try It Yourself

1. Set up your art tool in genuine indexed mode and export one test asset; confirm it imports without color corruption before doing any real art production.
2. Add one complete new overworld sprite — art, palette, registration — and place several instances of it across a test map.
3. Animate one metatile (e.g. simple flowing water) using tile swapping, and separately trigger one field effect via `dofieldeffect` from a script, to feel the difference between the two systems firsthand.

### Further Reading
- [PokéCommunity: Inserting Custom Sprites](https://www.pokecommunity.com/threads/inserting-custom-sprites.416167/)
- [PokéCommunity: Tile Inserting & Animating Tutorial](https://www.pokecommunity.com/threads/tile-inserting-animating-tutorial.422362/)
- [Editing the Title Screen — Gamer2020](https://gamer2020.net/pokeemeraldediting-the-title-screen/)


---

# Part VI — Advanced Topics

## Chapter 8: Custom C Code

**Learning objectives.** By the end of this chapter you should be able to: rigorously determine whether a given feature actually requires new C; navigate the codebase to find precedent before writing anything from scratch; explain the callback architecture well enough to know where new logic should hook in; distinguish battle scripts from Poryscript; and follow basic safety and debugging practices when you do write custom code.

### 8.1 When C Is Actually Necessary

Writing new C should be the last resort, not the first instinct — the overwhelming majority of what a hack needs is already exposed through config toggles, data tables, or Poryscript, and reaching for custom code before ruling those out is the single most common way early-project momentum gets bogged down in unnecessary complexity.

**The four-question check**, in order:

1. **Does a config.h toggle already do this?** Search `include/config.h` for anything adjacent to the behavior before assuming it needs custom logic.
2. **Does an existing feature branch do this?** Check the [Team Aqua's Asset Repo feature branch list](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo/wiki/Feature-Branches) — someone may have already built and shared exactly this.
3. **Can data-table or Poryscript edits achieve it without new C?** A surprising fraction of "custom mechanic" requests are actually just unusual combinations of existing systems — a move effect reused with different flags, a script pattern chained differently than usual.
4. **Is the change small, isolated, and well-precedented?** If the answer to the first three is genuinely no, look for the closest existing function doing something similar and pattern-match its structure rather than designing from a blank file.

> **📝 Note** — It's worth explicitly budgeting time to search before writing. Ten minutes grepping the codebase and checking FEATURES.md against a config toggle is reliably cheaper than an hour writing custom C for something that turns out to already exist.

### 8.2 Reading the Codebase Before Writing In It

Practical search strategies that consistently pay off:

- **Grep for the constant, not the concept.** If you're trying to understand how status conditions are checked, grep for `STATUS1_SLEEP` or a similar concrete constant rather than searching for "sleep" as a word, which will return comments, unrelated strings, and noise.
- **Follow one call chain all the way through, once, deliberately.** Pick a simple, well-understood feature (a basic item's field-use function is a good candidate) and trace it from the script command that invokes it, through the C function it calls, to wherever that function's effect actually lands. This single exercise teaches you more about the codebase's conventions than reading isolated files in the abstract.
- **Find the nearest existing analog before writing anything new.** If you're adding a new ability, find the three or four existing abilities that trigger at a similar moment (on switch-in, on contact, on weather change) and read all of them before writing your own — the pattern they share is almost always the pattern your new ability should also follow.

### 8.3 The Callback Architecture

Much of the engine's overworld and menu logic is organized around **callback functions** assigned to a small number of well-known global slots, most notably `gMain.callback1` and `gMain.callback2`, which the main loop invokes every frame. Switching between major game states — overworld, battle, a menu, a cutscene — is largely implemented as swapping which function is currently assigned to these callback slots, rather than any more elaborate state machine.

Functions with names prefixed `CB2_` (a strong, consistent codebase convention) are exactly these main-loop callbacks — `CB2_ReturnToField`, `CB2_InitBattle`, and similar. Recognizing this naming convention is a fast way to orient yourself when reading unfamiliar code: a `CB2_` function is a "what runs every frame while we're in this state" function, not a one-shot setup routine.

Sprites carry their own, smaller-scoped per-sprite callback (commonly `sprite->callback`), used for individual sprite animation and behavior logic independent of the overall game state.

### 8.4 Common Extension Points

| File (path/name varies by version) | What it governs |
|---|---|
| `src/event_object_movement.c` | Object event / NPC movement behavior implementation |
| `src/field_specials.c` | "Special" functions — native C routines registered to be callable by name from scripts via `special(...)` |
| `src/battle_script_commands.c` | The battle script command set (see 8.5) |
| `src/battle_util.c` | Ability and held-item effect hooks, many trigger-point implementations |
| `src/data/battle_moves.h` (and adjacent) | Move data definitions and effect assignments |

**Adding a new special function** is one of the more common, genuinely necessary reasons to touch C: writing the function itself (following the signature convention of existing specials), registering it in the specials table so the script compiler recognizes the name, and then calling it from Poryscript via `special(YourFunctionName)`. This is the standard bridge whenever a script needs to do something — complex party inspection, custom save-data interaction, arbitrary math — that no existing script command exposes.

### 8.5 Battle Scripts vs. Poryscript

These are easy to conflate by name and are genuinely different systems:

- **Poryscript** (Chapter 4) is for overworld events — NPC interactions, cutscenes, map logic.
- **Battle scripts** are a separate, older command language specifically for defining move and ability *effects* inside the battle engine — what animation plays, what damage formula applies, what secondary effect triggers, in what order. They are written directly against the native battle-script command set (not through Poryscript) and live alongside the move/ability data tables discussed in Chapter 6.7–6.8.

If you find yourself needing genuinely new move or ability behavior that no existing effect covers (rare, per 6.7–6.8, but it happens), this is the system you're extending — and it is a meaningfully steeper learning curve than Poryscript, both because the command set is lower-level and because battle mechanics carry more edge cases (interactions with other moves, abilities, and items) to get right.

### 8.6 Memory and Performance Considerations

The GBA is a genuinely memory-constrained embedded target, not a modern development environment with elastic resources. A few practical implications:

- **ROM space and banking** — the cartridge address space is finite, and very large data additions (a huge number of new species, extensive new graphics) can, in extreme cases, run into ROM size or banking constraints. This is rarely a concern for typical hack-sized content additions, but worth knowing exists if a project's scope is unusually large.
- **Avoid large stack allocations** — the working RAM available for function-local variables is small; a function that declares a large local array where a smaller one (or a heap/static allocation) would do is a real, not theoretical, risk on this hardware.
- **IWRAM vs. EWRAM vs. ROM placement** — some existing code uses placement attributes to control whether a given piece of data or a given function lives in faster, smaller internal RAM versus slower, larger external RAM versus ROM directly. You don't need to master this to write most custom features, but if you copy a placement attribute from existing code, understand generally why it's there rather than assuming it's decorative.

### 8.7 Safe Extension Practices

- **Gate new custom code behind its own `config.h` toggle**, even if you're the only person who will ever flip it. This keeps the change isolated, makes it trivially disableable if it turns out to be buggy, and makes future expansion version updates far less likely to silently conflict with it.
- **Isolate new code in its own file where reasonable**, rather than scattering small additions across many existing files, so future you (or a future merge) can see exactly what's custom at a glance.
- **Document non-obvious hooks with a comment explaining *why*, not just *what***. Code that looks like it does something unusual, with no explanation, is the code most likely to get "cleaned up" incorrectly by your future self during a later refactor.

### 8.8 Debugging Custom C

- **The built-in debug menu** (Chapter 9.1) is your first stop for verifying behavior interactively without needing print statements — Cheat Start, Warp to Map, and the Battle Debug Menu in particular can get you into the exact state you need to test a new feature quickly.
- **mGBA's built-in tools** — the emulator's memory viewer and logging console are the standard way to inspect actual runtime state and catch errors (invalid memory access, for instance) that a build success alone wouldn't reveal.
- **Deliberate, temporary debug output** — many decomp projects retain some existing convention for temporary debug text or logging; reuse whatever pattern the existing codebase already has rather than inventing a new one, both for consistency and because it's more likely to already be wired up correctly to a visible output.

### Chapter 8 Summary

- Run the four-question check before writing any new C: config toggle, feature branch, data/script solution, then — only then — custom code.
- Grep for concrete constants, follow one call chain deliberately, and find the nearest existing analog before writing anything new.
- The engine is organized around callback functions (`CB2_*` for main-loop state, per-sprite callbacks for individual behavior) rather than an elaborate explicit state machine.
- Battle scripts (move/ability effects) and Poryscript (overworld events) are different systems solving different problems — don't confuse them.
- The GBA is a real embedded target with real memory constraints; avoid large stack allocations and respect existing placement conventions.
- Gate custom code behind its own config toggle and document non-obvious hooks for your future self.

### Try It Yourself

1. Pick one existing item's field-use function and trace its full call chain from script command to final effect, writing down each function it passes through.
2. Add one small, genuinely necessary special function — even something trivial like returning a fixed value — and call it successfully from a test script, to build the full round-trip muscle memory before you need it for something that matters.
3. Find three existing abilities that trigger at the same moment (e.g. on switch-in) and compare their implementations side by side before you ever attempt to write a new one.


## Chapter 9: Troubleshooting & Debug Tools

**Learning objectives.** By the end of this chapter you should be able to: use the built-in debug menu effectively; diagnose the most common build failures without guesswork; recognize runtime crash patterns and map them to likely causes; debug graphics issues systematically; and use git as an active debugging tool, not just a backup system.

### 9.1 The Debug Menu, Full Tour

Access varies slightly by version — commonly **Select + Start**, sometimes **R + Start**, in the overworld. If neither works, check **Utilities → Expansion Version** is even reachable at all; older versions may use a different combination or require enabling the debug menu via a config toggle first.

| Tool | What it's for |
|---|---|
| Cheat Start | Jump straight into a fresh save for quick iterative testing, skipping the intro sequence |
| PC from Debug Menu | Access box storage from anywhere, without walking to a Pokémon Center |
| Warp to Map | Teleport to any map instantly, without scripting a temporary warp for testing purposes |
| Battle Debug Menu | Force a battle with specific, controllable parameters — accessed via Select on the Fight/Bag/Pokémon/Run menu during an active battle |
| Sprite Visualizer | Preview overworld and battle sprites directly, without needing to load them in an actual game context |
| Debug PC Fill | Rapidly populate boxes with test Pokémon, useful for testing UI and storage-related features at scale |
| Reroll Trainer ID | Useful for testing shiny-related or ID-dependent features without waiting on RNG |
| Expansion Version (under Utilities) | Confirms exactly which expansion version is running — critical when a tutorial's syntax doesn't match what's in front of you |

> **📝 Note** — Treat the debug menu as a first-class development tool, not a novelty. A huge amount of "does this actually work" verification that would otherwise require lengthy normal play to reach (a specific late-game trainer, a specific evolution condition, a rare encounter) is one Warp-to-Map or Cheat Start away.

### 9.2 Build System Troubleshooting

| Symptom | Likely cause | First step |
|---|---|---|
| Build fails immediately after a fresh `git pull` | Stale object files from the previous build state | `make clean`, then rebuild from scratch |
| "command not found" during build | A required tool binary (Poryscript, an image converter) isn't present in `tools/` yet | Re-check the relevant tool's install step; confirm the binary path matches what the Makefile expects |
| Build succeeds but the ROM doesn't reflect your change | Editing a generated/derived file instead of its source (e.g. hand-editing something Porymap owns) | Re-check you edited the actual source file, not a generated artifact |
| Long, unexplained build times after an unrelated change | A change touched a widely-included header, forcing a much larger recompile than expected | Not usually a bug — large headers are included broadly by design; consider whether the change could be isolated to a narrower file |

> **⚠ Pitfall** — When a build error's location doesn't make sense (an error reported in a file you didn't touch), check whether you edited a header that file includes, rather than assuming the compiler is confused. The reported location is almost always accurate; the actual cause is often one include away.

### 9.3 Runtime Crash Diagnosis

Crashes that occur after a successful build tend to fall into a small number of recognizable families:

- **Bad pointer in a data table** — a table entry referencing a constant, function, or asset pointer that doesn't actually exist or was mistyped. Commonly manifests as a crash specifically when the affected data is accessed (e.g. only when that one species is encountered, only when that one trainer is battled), which is itself a useful diagnostic clue — narrow down which specific entry is involved before searching further.
- **Missing null-terminator in an array** — many of this codebase's tables (learnsets, evolution lists, movement scripts) rely on an explicit end-marker rather than a separately tracked length. Forgetting the terminator causes the engine to keep reading past the intended end of the array into unrelated memory, which can produce bizarre, seemingly unrelated symptoms far from the actual mistake.
- **Uninitialized struct field** — a new data entry that's missing a field the existing pattern always sets, especially for fields with no obviously "safe" default. Comparing a new entry side-by-side against a known-working existing entry, field by field, is the most reliable way to catch this.

mGBA's built-in tools are the right instrument for all three: its memory viewer lets you inspect what a suspect pointer actually resolves to, and its logging console will often surface the specific address or context of a crash directly, saving significant guesswork versus black-box testing alone.

### 9.4 Graphics Debugging

- **Sprite Visualizer** (9.1) isolates whether a sprite's *art and registration* are correct independent of any gameplay context — if it renders correctly there but wrong in actual play, the bug is in placement/behavior logic, not the asset itself.
- **Palette collisions** (Chapter 7.5) typically present as one sprite's colors subtly shifting only when a specific other sprite is also loaded — if a graphics bug is intermittent and seems to depend on what else is on screen, suspect a palette tag collision before anything else.
- **Garbled or wrong colors on a freshly imported asset** almost always trace back to an indexing problem at export time (Chapter 7.1) rather than a bug in the game's rendering code — re-export the source asset in genuine indexed mode before debugging further on the code side.

### 9.5 Version Migration Troubleshooting

When jumping expansion versions, update one minor version at a time rather than skipping straight to the latest (Chapter 1.3), resolving any conflicts by hand at each individual step rather than batching several versions' worth of conflicts together. Cross-reference the changelog for each intermediate version against your own accumulated changes — if a changelog entry touches a file you've also customized, that's the specific spot to review carefully during the merge, rather than a general diff of the whole codebase.

Check **Utilities → Expansion Version** in the debug menu to confirm what you're actually running if changelog entries and your file state seem to disagree — it's a more reliable ground truth than assuming your last intentional update fully completed.

### 9.6 Git Workflow for Debugging

Git is an active debugging tool here, not just a backup mechanism:

- **`git bisect`** — when a regression is confirmed but its cause isn't obvious, and you have a reasonably granular commit history (see Chapter 1–2's emphasis on small, frequent commits), bisect will binary-search your history to the exact commit that introduced it far faster than manual inspection.
- **`git stash`** — useful for quickly reverting to a known-clean working state to confirm whether a bug is actually caused by your uncommitted changes, without losing that work.
- **Diffing against a clean checkout** — when something is behaving strangely and you suspect an accidental edit to a file you don't remember touching, diffing your working tree against a fresh clone of the same commit is a fast way to surface unintentional changes.

> **📝 Note** — This entire workflow depends on the commit discipline established in Chapters 1 and 2. `git bisect` is only as useful as your commit granularity — a project with five commits total gives bisect almost nothing to work with, while a project with frequent, small, isolated commits turns it into one of the most powerful debugging tools available for this kind of work.

### Chapter 9 Summary

- The debug menu is a first-class development tool — use Warp to Map, Cheat Start, and the Battle Debug Menu to reach test states instantly rather than playing to them normally.
- Most build failures resolve with `make clean` or by checking that a required tool binary is actually present.
- Runtime crashes cluster into a few recognizable families: bad data-table pointers, missing array terminators, and uninitialized struct fields — compare against a known-working entry when in doubt.
- Graphics bugs that depend on what else is loaded suggest a palette collision; garbled colors on import suggest an indexing problem, not a code bug.
- Migrate expansion versions incrementally and use the debug menu's Expansion Version display as ground truth.
- Git — especially `bisect`, `stash`, and diffing against a clean checkout — is an active debugging tool, and its usefulness scales directly with your commit discipline.

### Try It Yourself

1. Use Warp to Map and the Battle Debug Menu together to reach and test a specific late-game trainer battle without playing up to it normally.
2. Deliberately introduce one small bug (a missing array terminator, or a mistyped pointer in a data table) into a test branch, then practice diagnosing it using mGBA's memory viewer and logging console before reverting.
3. With a project that has at least five or six small commits, deliberately introduce a regression a few commits back, then use `git bisect` to find it, to build confidence in the tool before you need it under real pressure.

### Further Reading
- [pokeemerald-expansion documentation site](https://rh-hideout.github.io/pokeemerald-expansion/)


---

# Appendices

## Appendix A: Glossary

- **Decomp** — a full decompilation of a game's assembly into readable, rebuildable C source, as opposed to a binary patched after the fact.
- **ROM hack base** — a decomp fork (like expansion) meant to be built upon, not played as-is.
- **Feature branch** — a self-contained patch adding one feature, meant to be manually merged into your project rather than pulled as a version update.
- **Transpile** — converting one language into another at build time (Poryscript source into the engine's native bytecode).
- **Metatile** — a pre-assembled block of individually layered tiles, the actual unit you paint with in Porymap.
- **Metatile behavior** — a functional tag on a metatile (surfable, impassable, tall grass, etc.) independent of its visual appearance.
- **Object event** — the engine's term for any placed, potentially-moving map entity: NPCs, items, decorations, trainers.
- **Map script** — an automatic script hook tied to a map lifecycle moment (load, transition, frame, resume, warp-in), as opposed to a player-triggered interaction script.
- **Special (function)** — a native C function explicitly registered to be callable by name from a script via the `special(...)` command.
- **Task** — a unit of logic that persists across multiple frames, with its own small block of working data, managed via `CreateTask`/`DestroyTask`.
- **Battle script** — the separate, lower-level command language used to define move and ability effects inside the battle engine, distinct from Poryscript.
- **Indexed color** — a palette-based color system, required for GBA-compatible graphics, where each pixel stores a palette index rather than a direct color value.
- **Palette tag** — an identifier used to match a sprite to its palette, allowing the engine to manage shared, finite palette slots dynamically.
- **Config toggle** — a `#define` in `include/config.h` that switches a mechanic on/off or selects its generation-specific behavior.
- **Callback (CB2)** — a function assigned to one of a small number of well-known global slots (like `gMain.callback2`) that the main loop invokes every frame to drive the current game state.
- **AI flags** — a bitfield on a trainer defining which decision-making behaviors their battle AI uses.
- **Encounter slot weight** — the fixed, position-based probability distribution governing wild encounter rarity within a table.

## Appendix B: Quick Reference Tables

### B.1 File Location Lookup

| I want to change... | Look in... |
|---|---|
| A map's layout/terrain | Porymap → `data/maps/<Map>/map.json` |
| A map's interaction scripts | `data/maps/<Map>/scripts.pory` |
| A map's automatic lifecycle scripts | `mapscripts` block within `scripts.pory` |
| A map's dialogue text | `data/maps/<Map>/text.pory` |
| Whether a feature is on/off | `include/config.h` |
| A species' stats/moves/evolution | `src/data/pokemon/` |
| A trainer's party | `src/data/trainers.h` (path varies by version) |
| Wild encounter rates | Porymap Wild Pokémon tab, or `wild_encounters.json` |
| Overworld sprite art | `graphics/object_events/pics/` + `.../palettes/` |
| Overworld sprite registration | Object event graphics info table, `src/data/object_events/` (path varies) |
| Battle sprite art | `graphics/pokemon/<species>/` |
| Move data and effects | `src/data/battle_moves.h` and adjacent |
| Ability effect hooks | `src/battle_util.c` |
| Named IDs (species/items/moves/flags/vars) | `constants/` |
| A "special" script function | `src/field_specials.c` |

### B.2 Poryscript Command Quick Reference

| Command | Purpose |
|---|---|
| `lock` / `lockall` | Freeze the NPC / freeze all NPCs on the map |
| `release` / `releaseall` | Inverse of lock/lockall |
| `faceplayer` | Turn the NPC to face the player |
| `msgbox(text[, type])` | Dialogue box; types include default, `MSGBOX_YESNO`, `MSGBOX_SIGN`, `MSGBOX_AUTOCLOSE` |
| `multichoice(...)` | Multiple-choice prompt, result stored in a variable |
| `applymovement(target, list)` / `waitmovement(target)` | Run and (optionally) wait on a movement sequence |
| `giveitem(item[, qty])` / `givemon(species, level, item)` | Grant an item or a Pokémon |
| `playse(sound)` / `playfanfare(fanfare)` | Sound effects and jingles |
| `warp(...)` / `warpsilent(...)` | Warp with or without a transition effect |
| `setweather(type)` | Override current weather at runtime |
| `dofieldeffect(effect)` | Trigger a field effect animation |
| `special(name)` | Call a registered native C special function |
| `setflag` / `clearflag` / `flag(...)` | Set, clear, or check a flag |
| `setvar` / `addvar` / `var(...)` | Set, increment, or read a variable |
| `if / elif / else` | Conditional branching |
| `while` / `do...while` | Loops (ensure a reachable exit condition) |
| `switch / case / default` | Multi-branch selection |
| `call(label)` / `return` | Sub-script call and return |
| `goto(label)` | Permanent jump, no return |
| `end` | Terminate the script |

### B.3 Movement Command Quick Reference

| Command family | Examples |
|---|---|
| Directional walk | `walk_up`, `walk_down`, `walk_left`, `walk_right` |
| Directional run | `run_up`, `run_down`, `run_left`, `run_right` |
| Facing only | `face_up`, `face_down`, `face_left`, `face_right`, `face_player` |
| Ledge jumps | `jump_up`, `jump_down`, `jump_left`, `jump_right` |
| Timing/visibility | `delay`, `set_invisible`, `set_visible` |
| Facing lock | `lock_facing_direction`, `unlock_facing_direction` |
| Stationary animation | `walk_in_place_up/down/left/right` |

### B.4 Wild Encounter Slot Weights (Standard 12-Slot Land Table)

| Slot | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Weight | 20% | 20% | 10% | 10% | 10% | 10% | 5% | 5% | 4% | 4% | 1% | 1% |

Fishing rod tables are shorter and independently weighted per rod tier — check `wild_encounters.json` or Porymap's rod-specific tabs directly rather than assuming this same distribution applies.

## Appendix C: Full Source Index

**Setup & fundamentals**
- [INSTALL.md](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)
- [pokeemerald-expansion documentation site](https://rh-hideout.github.io/pokeemerald-expansion/)
- [pokeemerald-expansion FEATURES.md](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/FEATURES.md)
- [Team Aqua's Asset Repo: Basics of GitHub](https://github.com/Pawkkie/Team-Aquas-Asset-Repo/wiki/The-Basics-of-GitHub)
- [Team Aqua's Asset Repo: Feature Branches](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo/wiki/Feature-Branches)
- [Bivurnum's decomps-resources](https://github.com/Bivurnum/decomps-resources)
- [Team Aqua's Hideout — full YouTube tutorial playlist (60 videos)](https://www.youtube.com/playlist?list=PLLNv9Lq6kDmTIYfN5NvgQRvfOHTOXl0uU)

**Porymap**
- [Official Porymap guide](https://huderlem.github.io/porymap/)
- [Porymap GitHub / downloads](https://github.com/huderlem/porymap)
- [YouTube: Using Porymap](https://www.youtube.com/watch?v=mHokDsp_Ysk)

**Poryscript**
- [Poryscript GitHub README](https://github.com/huderlem/poryscript)
- [Huderlem's blog: Poryscript design](https://www.huderlem.com/blog/posts/poryscript/)
- [YouTube: Intro to Poryscript](https://www.youtube.com/watch?v=IY3tpjyVm0Y)
- [YouTube: Poryscript Syntax and Giving Pokémon](https://www.youtube.com/watch?v=lWG-wJuclX4)
- [PokéCommunity Scripting Tutorial](https://www.pokecommunity.com/threads/scripting-tutorial.416800/)
- [YouTube: Text Formatting — Color and Buffering Strings](https://www.youtube.com/watch?v=avMM_cc6hHE)

**NPCs, trainers, and tasks**
- [YouTube: The Task System](https://www.youtube.com/watch?v=-4lQeHUQXXU)

**Gameplay data**
- [YouTube: Adding New Pokémon — Expanding the Pokédex](https://www.youtube.com/watch?v=T4tNu-MaYH4)

**Graphics & sprites**
- [PokéCommunity: Inserting Custom Sprites](https://www.pokecommunity.com/threads/inserting-custom-sprites.416167/)
- [PokéCommunity: Tile Inserting & Animating Tutorial](https://www.pokecommunity.com/threads/tile-inserting-animating-tutorial.422362/)
- [Editing the Title Screen — Gamer2020](https://gamer2020.net/pokeemeraldediting-the-title-screen/)

**Community / ongoing support**
- [ROM Hacking Hideout Discord](https://discord.gg/6CzjAG6GZk)
- [PokéCommunity Decomp & Disassembly subforum](https://www.pokecommunity.com/forums/decomp-disassembly-tutorials.475/)
