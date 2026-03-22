# Pokémon Holon Legends — Master Technical Guide

A comprehensive, concrete technical guide for building **Pokémon Holon** as a solo, AI-assisted ROM hack on **pokeemerald-expansion**, targeting **macOS** with **Antigravity** as the IDE.

> [!NOTE]
> This guide consolidates and ---

## Table of Contents

- [1. Project Model & Mental Framework](#1-project-model--mental-framework)
- [2. macOS Environment Setup](#2-macos-environment-setup)
  - [2.1 Prerequisites Checklist](#21-prerequisites-checklist)
  - [2.2 Xcode Command Line Tools](#22-xcode-command-line-tools)
  - [2.3 Homebrew, libpng & pkg-config](#23-homebrew-libpng--pkg-config)
  - [2.4 devkitARM Toolchain](#24-devkitarm-toolchain)
  - [2.5 Python](#25-python)
  - [2.6 Optional: Testing Dependencies](#26-optional-testing-dependencies)
  - [2.7 Shell Environment Verification](#27-shell-environment-verification)
- [3. Cloning, Building & Verifying](#3-cloning-building--verifying)
  - [3.1 Clone with Git (Never ZIP)](#31-clone-with-git-never-zip)
  - [3.2 First Build](#32-first-build)
  - [3.3 Parallel Builds on macOS](#33-parallel-builds-on-macos)
  - [3.4 Debug Build](#34-debug-build)
  - [3.5 Expected Output](#35-expected-output)
  - [3.6 Build Validation Checklist](#36-build-validation-checklist)
- [4. Branch Strategy & Upstream Tracking](#4-branch-strategy--upstream-tracking)
  - [4.1 Choosing an Expansion Branch](#41-choosing-an-expansion-branch)
  - [4.2 Adding the Upstream Remote](#42-adding-the-upstream-remote)
  - [4.3 Updating Your Fork](#43-updating-your-fork)
  - [4.4 Git Workflow Rules](#44-git-workflow-rules)
- [5. Workspace & Repo Structure](#5-workspace--repo-structure)
  - [5.1 Outer Workspace Layout](#51-outer-workspace-layout)
  - [5.2 Inner Repo Structure](#52-inner-repo-structure)
  - [5.3 Where to Put Custom Content](#53-where-to-put-custom-content)
- [6. Tool Stack](#6-tool-stack)
  - [6.1 IDE — Antigravity](#61-ide--antigravity)
  - [6.2 Emulator — mGBA](#62-emulator--mgba)
  - [6.3 Map Editor — Porymap](#63-map-editor--porymap)
  - [6.4 Scripting — Poryscript](#64-scripting--poryscript)
  - [6.5 Tileset Compiler — Porytiles](#65-tileset-compiler--porytiles)
  - [6.6 Tilemap Viewer — Tilemap Studio](#66-tilemap-viewer--tilemap-studio)
  - [6.7 Pixel Art — Aseprite](#67-pixel-art--aseprite)
  - [6.8 Community Assets — Team Aqua Asset Repo](#68-community-assets--team-aqua-asset-repo)
- [7. Config System & Engine Behavior](#7-config-system--engine-behavior)
  - [7.1 How Config Headers Work](#71-how-config-headers-work)
  - [7.2 Config File Quick Reference](#72-config-file-quick-reference)
  - [7.3 Priority Config Decisions for Holon](#73-priority-config-decisions-for-holon)
- [8. Core Production Pipelines](#8-core-production-pipelines)
  - [8.1 Maps — Building the World Graph](#81-maps--building-the-world-graph)
  - [8.2 Scripts & Events — Building Progression](#82-scripts--events--building-progression)
  - [8.3 Gameplay Data — Encounters, Trainers, Items](#83-gameplay-data--encounters-trainers-items)
  - [8.4 Graphics & Presentation](#84-graphics--presentation)
  - [8.5 Custom Systems — The Last Pipeline](#85-custom-systems--the-last-pipeline)
- [9. Transforming the Fork Into Pokémon Holon](#9-transforming-the-fork-into-pokémon-holon)
  - [9.1 The Five Replacement Layers](#91-the-five-replacement-layers)
  - [9.2 The Safe Customization Model](#92-the-safe-customization-model)
  - [9.3 What to Change First](#93-what-to-change-first)
  - [9.4 What NOT to Do First](#94-what-not-to-do-first)
- [10. Development Roadmap — Phased Build Order](#10-development-roadmap--phased-build-order)
- [11. Feature Branches — Integration Workflow](#11-feature-branches--integration-workflow)
- [12. Working Rules for Solo AI-Assisted Development](#12-working-rules-for-solo-ai-assisted-development)
- [13. Definition of "Successfully Started"](#13-definition-of-successfully-started)
- [Sources](#sources)

---

## 1. Project Model & Mental Framework

Pokémon Holon is a **decomp-based game development project**, not a traditional ROM-editing workflow. The engine base is `pokeemerald-expansion`, which RH-Hideout describes as a **"ROM hack base"** — a development platform derived from pret's `pokeemerald` decompilation, designed to be built from source rather than through binary patching.

> *"[pokeemerald-expansion] is a decompilation of Pokémon Emerald [and] a ROM hack base that includes many mechanics and quality-of-life features from across the Pokémon series."*
>
> — [pokeemerald-expansion README](https://github.com/rh-hideout/pokeemerald-expansion)

**Think in layers:**

| Layer | What It Is | Examples |
|---|---|---|
| **1. Engine base** | `pokeemerald-expansion` itself | Battle engine, rendering, save system, sound driver |
| **2. Project config** | Your config toggles and compile settings | `include/config/battle.h`, `include/config/save.h` |
| **3. Game shell** | Title, start flow, first area, branding | Custom title screen, new start town, Holon logo |
| **4. Game content** | Maps, scripts, encounters, trainers, text, graphics, music | Route 1, starter event, first gym leader roster |
| **5. Custom systems** | Engine extensions beyond what config/data/scripts can express | Unique mechanics, custom UI subsystems |

This layered model prevents the most common early mistake: treating the decomp as a ROM to "edit" rather than a codebase to build and maintain.

---

## 2. macOS Environment Setup

This section provides every command needed to go from a clean macOS install to a working build environment. If you've already completed any step, verify and skip ahead.

> [!IMPORTANT]
> All commands below assume **zsh** (the default shell since macOS 10.15 Catalina). If you're on an older bash setup, check with `echo $0`. The devkitARM instructions below include a bash fallback.

### 2.1 Prerequisites Checklist

Before building, you need all of the following installed:

| Dependency | Purpose | Installed? |
|---|---|---|
| Xcode Command Line Tools | Compiler, `make`, `git`, core UNIX tools | `xcode-select -p` to check |
| Homebrew | Package manager | `brew --version` to check |
| libpng | PNG image processing (used by build tools) | `brew list libpng` to check |
| pkg-config | Build-time library detection | `brew list pkg-config` to check |
| devkitARM | GBA cross-compiler toolchain | `$DEVKITARM/bin/arm-none-eabi-gcc --version` to check |
| Python 3 | Build scripts and data processing | `python3 --version` to check |

> Source: [MAC_OS.md](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/docs/install/mac/MAC_OS.md)

### 2.2 Xcode Command Line Tools

```bash
xcode-select --install
```

A dialog will appear; click **Install**. Alternatively, download from [Apple's Xcode Resources](https://developer.apple.com/xcode/resources/).

Verify:
```bash
xcode-select -p
# Expected: /Library/Developer/CommandLineTools  (or similar Xcode path)
gcc --version
make --version
git --version
```

### 2.3 Homebrew, libpng & pkg-config

**Install Homebrew** (if not already present):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Install libpng and pkg-config:**
```bash
brew install libpng
brew install pkg-config
```

Verify:
```bash
brew list libpng    # should show installed files
brew list pkg-config
```

> Source: [MAC_OS.md § Installing libpng, Installing pkg-config](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/docs/install/mac/MAC_OS.md)

### 2.4 devkitARM Toolchain

1. Download the `devkitpro-pacman-installer.pkg` from [devkitPro pacman releases](https://github.com/devkitPro/pacman/releases).
2. Open the `.pkg` to install devkitPro pacman.
3. Install the GBA development suite:

```bash
sudo dkp-pacman -Sy
sudo dkp-pacman -S gba-dev
sudo dkp-pacman -S devkitarm-rules
```

When prompted for package selection, press **Enter** to install all, then **Y** to confirm.

4. Add devkitARM to your shell environment (**zsh** — the default):

```bash
export DEVKITPRO=/opt/devkitpro
echo "export DEVKITPRO=$DEVKITPRO" >> ~/.zshrc
export DEVKITARM=$DEVKITPRO/devkitARM
echo "export DEVKITARM=$DEVKITARM" >> ~/.zshrc

echo "if [ -f ~/.zshrc ]; then . ~/.zshrc; fi" >> ~/.zprofile
```

<details>
<summary>If using bash instead of zsh…</summary>

```bash
export DEVKITPRO=/opt/devkitpro
echo "export DEVKITPRO=$DEVKITPRO" >> ~/.bashrc
export DEVKITARM=$DEVKITPRO/devkitARM
echo "export DEVKITARM=$DEVKITARM" >> ~/.bashrc

echo "if [ -f ~/.bashrc ]; then . ~/.bashrc; fi" >> ~/.bash_profile
```
</details>

5. **Restart your terminal** (or `source ~/.zshrc`), then verify:

```bash
echo $DEVKITPRO
# Expected: /opt/devkitpro

echo $DEVKITARM
# Expected: /opt/devkitpro/devkitARM

$DEVKITARM/bin/arm-none-eabi-gcc --version
# Expected: arm-none-eabi-gcc (devkitARM release XX) X.X.X
```

> Source: [MAC_OS.md § Installing devkitARM](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/docs/install/mac/MAC_OS.md)

### 2.5 Python

If Python 3 is not already installed (check with `python3 --version`):

- Download from [python.org/downloads](https://www.python.org/downloads/)
- Open the `.pkg` installer

Verify:
```bash
python3 --version
# Expected: Python 3.x.x
```

> Source: [MAC_OS.md § Installing Python](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/docs/install/mac/MAC_OS.md)

### 2.6 Optional: Testing Dependencies

To run the expansion's built-in test suite:

```bash
brew install coreutils
```

This provides GNU coreutils (the test runner uses `timeout` from GNU coreutils). On Apple Silicon, native Homebrew is recommended. Rosetta-based Intel Homebrew is possible but slower.

> Source: [MAC_OS.md § Optional: To run tests](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/docs/install/mac/MAC_OS.md)

### 2.7 Shell Environment Verification

Run this block to confirm everything is in place before your first build:

```bash
echo "=== Environment Check ==="
echo "Shell: $0"
echo "Xcode tools: $(xcode-select -p 2>/dev/null || echo 'NOT FOUND')"
echo "Make: $(make --version 2>/dev/null | head -1 || echo 'NOT FOUND')"
echo "Git: $(git --version 2>/dev/null || echo 'NOT FOUND')"
echo "Homebrew: $(brew --version 2>/dev/null | head -1 || echo 'NOT FOUND')"
echo "libpng: $(brew list libpng &>/dev/null && echo 'installed' || echo 'NOT FOUND')"
echo "pkg-config: $(brew list pkg-config &>/dev/null && echo 'installed' || echo 'NOT FOUND')"
echo "DEVKITPRO: ${DEVKITPRO:-NOT SET}"
echo "DEVKITARM: ${DEVKITARM:-NOT SET}"
echo "arm-none-eabi-gcc: $($DEVKITARM/bin/arm-none-eabi-gcc --version 2>/dev/null | head -1 || echo 'NOT FOUND')"
echo "Python: $(python3 --version 2>/dev/null || echo 'NOT FOUND')"
echo "==========================="
```

Every line should show a valid result, not `NOT FOUND` or `NOT SET`.

---

## 3. Cloning, Building & Verifying

### 3.1 Clone with Git (Never ZIP)

Always clone with Git — never download as ZIP. Commit history is required for future updating and merging with upstream.

```bash
cd ~/Documents/Decomps
git clone https://github.com/<your-username>/pokeemerald-expansion PokemonHolon
cd PokemonHolon
```

> [!WARNING]
> If you already cloned your fork, skip this step. Your repo is at `~/Documents/Decomps/PokemonHolon/`.

> Source: [INSTALL.md § Building pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)

### 3.2 First Build

```bash
cd ~/Documents/Decomps/PokemonHolon
make
```

A successful build produces `pokeemerald.gba` in the project root directory.

### 3.3 Parallel Builds on macOS

The standard `nproc` command is **not available on macOS**. Use:

```bash
sysctl -n hw.ncpu
# Example output: 10
```

Then build with that many parallel jobs:

```bash
make -j$(sysctl -n hw.ncpu)
```

This dramatically speeds up compilation. On a modern Mac, expect 1–3 minutes for a full build. As your Delta species count grows, build times will increase — parallel builds will matter more over time.

> Source: [INSTALL.md § Parallel builds](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md) — *"`nproc` is not available on macOS. The alternative is `sysctl -n hw.ncpu`."*

### 3.4 Debug Build

To produce `pokeemerald.elf` with debug symbols and debug-compatible optimization:

```bash
make debug
```

This is useful when you need to trace crashes or unexpected behavior. The debug menu (R+START in the overworld, SELECT in battle) is already included by default and auto-disabled in release builds via the `DISABLED_ON_RELEASE` pattern.

> Source: [INSTALL.md § Building with debug info](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)

### 3.5 Expected Output

A successful build ends with output similar to:

```
arm-none-eabi-ld: warning: ../../pokeemerald.elf has a LOAD segment with RWX permissions
Memory region         Used Size  Region Size  %age Used
           EWRAM:      243354 B       256 KB     92.83%
           IWRAM:       30492 B        32 KB     93.05%
             ROM:    26072244 B        32 MB     77.70%
...
arm-none-eabi-objcopy -O binary pokeemerald.elf pokeemerald.gba
```

The key file is **`pokeemerald.gba`** in the project root.

> Source: [INSTALL.md § Building pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)

### 3.6 Build Validation Checklist

Do **not** move past this point until every box is checked:

- [ ] `make` completes without errors
- [ ] `make debug` completes without errors
- [ ] `pokeemerald.gba` exists in the project root
- [ ] The ROM boots in your emulator (mGBA or equivalent)
- [ ] You can make a trivial change (e.g., edit a text string in `src/`), rebuild, and see the change in-game
- [ ] You have committed this known-good state: `git add -A && git commit -m "Baseline: verified clean build"`

This is your **real "environment complete"** state.

---

## 4. Branch Strategy & Upstream Tracking

### 4.1 Choosing an Expansion Branch

pokeemerald-expansion has three branch tiers:

| Branch | What It Contains | Best For |
|---|---|---|
| **Latest Patch** (e.g., `expansion/1.11.0`) | Last official release; all released features and bugfixes | Maximum stability |
| **`master`** | Latest Patch + any bugfixes discovered since | Stability with recent fixes |
| **`upcoming`** | Latest Patch + new features added since release | Access to newest features (less stable) |

> *"The `master` branch has all of the functionality from 'Latest Patch', as well as any bugfixes that have been discovered since that release."*
>
> — [INSTALL.md § Choosing a branch](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)

For Pokémon Holon, **`master`** is the recommended starting branch — stable enough for active development, with recent bugfixes included.

### 4.2 Adding the Upstream Remote

Add the official expansion repo so you can pull future updates:

```bash
cd ~/Documents/Decomps/PokemonHolon
git remote add RHH https://github.com/rh-hideout/pokeemerald-expansion
```

Verify your remotes:
```bash
git remote -v
# Expected:
# origin    https://github.com/<your-username>/pokeemerald-expansion (fetch/push)
# RHH       https://github.com/rh-hideout/pokeemerald-expansion (fetch/push)
```

> Source: [INSTALL.md § Migrating from pokeemerald](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)

### 4.3 Updating Your Fork

When you want to pull in upstream updates:

```bash
# 1. Check your current version
cat docs/CHANGELOG.md | head -20

# 2. Fetch the latest from upstream
git fetch RHH

# 3. Pull the target version (incremental updates recommended)
# For a specific patch:
git pull RHH expansion/1.11.0

# For the latest master:
git pull RHH master

# For the latest upcoming:
git pull RHH upcoming
```

> [!IMPORTANT]
> RH-Hideout recommends **incremental updates** through version tags rather than jumping multiple versions at once. The recommended update path (if starting from an older version) is:
> `1.6.2 → 1.7.4 → 1.8.3 → 1.9.4 → 1.10.3 → latest`

Expect merge conflicts during updates. Resolve them carefully, rebuild, and test.

> Source: [INSTALL.md § Updating pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)

### 4.4 Git Workflow Rules

| Rule | Example |
|---|---|
| **Always keep `main` buildable** | Never push broken code to your primary branch |
| **Commit small, coherent changes** | `"Create first test map"`, not `"Did a bunch of stuff"` |
| **Use feature branches for experiments** | `git checkout -b feature/custom-starters` |
| **Tag milestones** | `git tag v0.1-baseline` after your first clean build |
| **Never force-push to main** | Use merge or rebase workflows for integration |

---

## 5. Workspace & Repo Structure

### 5.1 Outer Workspace Layout

Keep the **game repo** separate from **project support files**. This is your actual setup:

```text
~/Documents/Decomps/                    ← workspace root
├── PokemonHolon/                        ← actual forked decomp repo (Git-tracked)
└── Documentation/                      ← planning docs, reference, guides
    ├── Technical Starter Guide v2.md   ← this document
    ├── Pokeemerald Expansion Features & Branch Guide.md
    ├── Region.md
    └── Story & Lore.md
```

As the project grows, consider adding sibling directories:

```text
~/Documents/Decomps/
├── PokemonHolon/
├── Documentation/
├── Assets-Source/              ← raw art files, tilesets, sprite source
│   ├── Tilesets/
│   ├── Sprites/
│   └── Audio/
├── Exports/                    ← playtest ROMs, screenshots, build notes
└── Scratch/                    ← experiments, one-offs, AI drafts
```

**Why:** The repo stays clean enough to build, diff, and update. Your support files stay accessible to AI tools without bloating the build.

### 5.2 Inner Repo Structure

Do **not** reorganize the engine directory layout. The repo already has a known structure with build rules, documentation, and community tooling that depends on these paths:

```text
PokemonHolon/
├── src/                        ← C source code (engine + game logic)
├── include/                    ← header files
│   └── config/                 ← feature config headers (20 files)
├── data/                       ← maps, scripts, encounters, event data
│   └── maps/                   ← individual map directories
├── graphics/                   ← sprites, tilesets, UI art, palettes
├── sound/                      ← music and sound effects
├── constants/                  ← game constant definitions
├── docs/                       ← internal documentation + install guides
├── tools/                      ← build tools (gbafix, mapjson, etc.)
├── migration_scripts/          ← upgrade helpers between versions
├── Makefile                    ← primary build entry point
├── config.mk                   ← build configuration
└── pokeemerald.gba             ← built ROM output
```

### 5.3 Where to Put Custom Content

Rather than scattering project-specific files across the engine tree, create namespaced subdirectories:

```text
graphics/
└── holon/                       ← all Holon-specific graphics
    ├── title/
    ├── ui/
    ├── trainers/
    ├── pokemon/
    └── overworld/

sound/
└── holon/                       ← Holon-specific music/SFX

data/
└── maps/
    ├── HolonMirageForest/          ← new maps use clear project-specific names
    ├── HolonRoute1/
    └── TestMap_Dev/            ← internal development maps
```

**Principle:** Organize your additions intentionally. The engine tree is a known quantity — your content should be easy to identify within it.

---

## 6. Tool Stack

### 6.1 IDE — Antigravity

**Status:** Already chosen and in use.

The decomp does not require a special IDE. What matters is: search, shell access, Git integration, multi-file navigation, and AI context-awareness. Antigravity provides all of these.

### 6.2 Emulator — mGBA

**Recommended:** [mGBA](https://mgba.io/)

- Most commonly used development emulator for GBA projects
- Supports GDB debugging when built with debug symbols (`make debug`)
- Suitable for rapid build→test iteration

**Alternative:** RetroArch with mGBA core for controller/input flexibility.

### 6.3 Map Editor — Porymap

**Required:** [Porymap](https://github.com/huderlem/porymap) — the standard cross-platform map editor for Gen 3 decomp projects.

Porymap handles:
- Map creation (tiles, dimensions, layout IDs, map groups)
- Collision editing
- Event placement (NPCs, warps, triggers, signposts)
- Map header/property editing
- Map connections
- Wild encounter tables
- Region map editing
- Tileset editing

**Files Porymap interacts with:**

| File Path | Purpose |
|---|---|
| `data/maps/` | Individual map directories (layout, events, headers) |
| `data/maps/map_groups.json` | Map group definitions |
| `src/data/wild_encounters.json` | Wild Pokémon encounter tables |
| `src/data/heal_locations.json` | Heal/fly points |
| `src/data/region_map/region_map_sections.json` | Region map section definitions |

> Sources:
> - [Porymap Manual — Introduction](https://huderlem.github.io/porymap/manual/introduction.html)
> - [Porymap Manual — Creating New Maps](https://huderlem.github.io/porymap/manual/creating-new-maps.html)
> - [Porymap Manual — Project Files](https://huderlem.github.io/porymap/manual/project-files.html)

### 6.4 Scripting — Poryscript

**Recommended:** [Poryscript](https://github.com/huderlem/poryscript) — a high-level scripting language that compiles to the lower-level `.inc` format used by the engine.

**Advantages over raw `.inc` scripting:**
- Structured control flow (`if`, `elif`, `else`, `while`, `do...while`, `switch`)
- Inline text with auto-formatting to fit message boxes
- Cleaner script organization
- Can be installed as a standalone binary or Git submodule

**Example — Poryscript vs. raw script:**

```c
// Poryscript
script MyNpc_Interact {
    lock
    faceplayer
    if (flag(FLAG_RECEIVED_STARTER)) {
        msgbox("Good luck on your journey!")
    } else {
        msgbox("Are you ready to choose your first partner Pokémon?")
    }
    release
}
```

vs.

```asm
@ Raw .inc script
MyNpc_Interact::
    lock
    faceplayer
    checkflag FLAG_RECEIVED_STARTER
    goto_if_set MyNpc_Interact_AlreadyGot
    msgbox MyNpc_Interact_Text1, MSGBOX_DEFAULT
    release
    end

MyNpc_Interact_AlreadyGot::
    msgbox MyNpc_Interact_Text2, MSGBOX_DEFAULT
    release
    end
```

**Recommendation:** Use Poryscript for all new script content. Only use raw `.inc` scripting when interfacing with systems that require it.

> Source: [Poryscript README](https://github.com/huderlem/poryscript)

### 6.5 Tileset Compiler — Porytiles

**Recommended for custom tilesets:** [Porytiles](https://github.com/grunt-lucas/porytiles) — an overworld tileset compiler that generates the assets required by both the game engine and Porymap.

**Outputs:**
- `metatiles.bin`
- `metatile_attributes.bin`
- Indexed `tiles.png`
- Palette files
- Animation folders/assets

Use this when creating entirely new tilesets from source pixel art. For minor edits to existing tilesets, Porymap's built-in tileset editor may suffice.

> Source: [Porytiles README](https://github.com/grunt-lucas/porytiles)

### 6.6 Tilemap Viewer — Tilemap Studio

**Supplementary tool:** [Tilemap Studio](https://github.com/Rangi42/tilemap-studio) — a tilemap viewer and editor, listed by the expansion docs as a useful additional tool.

> Source: [INSTALL.md § Useful additional tools](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md)

### 6.7 Pixel Art — Aseprite

**Recommended for sprite/pixel art:** [Aseprite](https://www.aseprite.org/)

The most practical editor for indexed-color pixel art. Porytiles references an Aseprite-compatible workflow in its documentation.

**Alternatives:** LibreSprite (free Aseprite fork), GIMP, Photoshop (with disciplined indexed-color export).

### 6.8 Community Assets — Team Aqua Asset Repo

**Primary community hub:** [Team Aqua's Asset Repo](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo)

> *"A collection of free-to-use assets for Generation 3 Pokémon decomp hacking."*

Categories include: feature branches, music, sound effects, sprites, tilesets, UI elements, and other hacking resources. Use this as your placeholder and prototyping asset source.

> Source: [Team Aqua Asset Repo README](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo)

---

## 7. Config System & Engine Behavior

### 7.1 How Config Headers Work

Expansion exposes most feature toggles as C `#define` directives in header files under `include/config/`. You change a value, rebuild, and the feature is enabled/disabled. No engine source code editing required.

**Key patterns:**

| Pattern | Meaning | Example |
|---|---|---|
| `TRUE` / `FALSE` | Simple on/off toggle | `#define B_SHOW_MOVE_DESCRIPTION TRUE` |
| `GEN_LATEST` | Use the most modern behavior (currently Gen 9) | `#define B_CRITICAL_CAPTURE GEN_LATEST` |
| `GEN_X` | Lock behavior to a specific generation | `#define B_EXP_SHARE GEN_6` |
| `0` | Disabled (for flag/var features, assign a real ID to enable) | `#define B_FLAG_MEGA_RING 0` |
| `DISABLED_ON_RELEASE` | Active in dev builds, stripped from release builds | `#define OW_FLAG_NO_COLLISION DISABLED_ON_RELEASE` |

### 7.2 Config File Quick Reference

Your project has **20 config header files** in `include/config/`:

| Config File | Purpose |
|---|---|
| `ai.h` | AI switching, prediction, smart battle behavior |
| `battle.h` | Battle mechanics, gen toggles, gimmicks, difficulty flags/vars |
| `caps.h` | Level caps, EV caps, experience scaling |
| `contest.h` | Contest mechanics |
| `debug.h` | Debug menus, sprite visualizer, AI timer |
| `dexnav.h` | DexNav feature toggle and parameters |
| `fishing.h` | Fishing mechanics configuration |
| `follower_npc.h` | NPC follower system (DPP-style partners) |
| `general.h` | RNG quality, expansion intro, units, compiler flags, bugfixes |
| `item.h` | TM reusability, Exp Share, Repels/Lures, VS Seeker, Dowsing Machine |
| `name_box.h` | Speaker name box display in dialogue |
| `overworld.h` | DNS, followers, map popups, field mechanics, wild encounter modifiers |
| `pokedex_plus_hgss.h` | HGSS-style Pokédex options |
| `pokemon.h` | Learnsets, breeding, evolution, species graphics, shiny flags |
| `pokerus.h` | Pokérus behavior |
| `save.h` | Freeing saveblock space from unused legacy features |
| `species_enabled.h` | Toggle entire generations/form groups of Pokémon |
| `summary_screen.h` | Summary screen stats, IV/EV display, move relearner |
| `test.h` | Testing framework configuration |
| `text.h` | Text system configuration |

### 7.3 Priority Config Decisions for Holon

These are the **highest-impact configuration changes** to make before starting content work:

**1. Disable ALL battle gimmicks** (`include/config/battle.h`):
```c
// Disable everything — Delta Species is the game's sole transformation identity
#define B_FLAG_MEGA_RING        0   // Mega Evolution disabled
#define B_FLAG_Z_RING           0   // Z-Moves disabled
#define B_FLAG_DYNAMAX_BAND     0   // Dynamax disabled
#define B_FLAG_TERA_ORB         0   // Tera disabled
```

**2. Free saveblock space** (`include/config/save.h`):
```c
// Enable ALL of these — Delta species flags and fragment tracking need the room
#define FREE_MYSTERY_EVENT_BUFFERS      TRUE    // +1104 bytes
#define FREE_MYSTERY_GIFT               TRUE    // +876 bytes
#define FREE_RECORD_MIXING_HALL_RECORDS TRUE    // +1032 bytes
#define FREE_UNION_ROOM_CHAT            TRUE    // +212 bytes
#define FREE_LINK_BATTLE_RECORDS        TRUE    // +88 bytes
#define FREE_ENIGMA_BERRY               TRUE    // +52 bytes
#define FREE_BATTLE_TOWER_E_READER      TRUE    // +188 bytes
#define FREE_POKEMON_JUMP               TRUE    // +16 bytes
#define FREE_TRAINER_HILL               TRUE    // +28 bytes
#define FREE_MATCH_CALL                 TRUE    // +104 bytes
```

**3. Disable the expansion intro** (`include/config/general.h`):
```c
#define EXPANSION_INTRO FALSE
```

**4. Configure species** (`include/config/species_enabled.h`):
```c
// Enable Gens 1–4 (the Delta Species arc's era)
#define P_GEN_1_POKEMON TRUE
#define P_GEN_2_POKEMON TRUE
#define P_GEN_3_POKEMON TRUE
#define P_GEN_4_POKEMON TRUE
// Disable Gens 7–9 initially; evaluate 5–6 selectively
#define P_GEN_7_POKEMON FALSE
#define P_GEN_8_POKEMON FALSE
#define P_GEN_9_POKEMON FALSE
// Disable form groups that conflict with Delta Species identity
#define P_MEGA_EVOLUTIONS   FALSE
#define P_REGIONAL_FORMS    FALSE
#define P_FUSION_FORMS      FALSE
// Keep cross-gen evolutions for roster diversity
#define P_CROSS_GENERATION_EVOS TRUE
```

**5. Enable Follower Pokémon and Day/Night** (`include/config/overworld.h`):
- Both are built-in and should be active for Holon

> [!TIP]
> For a complete feature-by-feature breakdown with Holon-specific recommendations, see the companion document: **`EXPANSION_GUIDE.md`** in your Documentation folder.

---

## 8. Core Production Pipelines

Early development in a decomp project is **not** heavy C programming. It is data authoring across four pipelines, plus a fifth for engine-level work when necessary.

### 8.1 Maps — Building the World Graph

**Primary tool:** Porymap

**Workflow — Creating a new map:**

1. Open Porymap and load your `PokemonHolon` project
2. Create a new map (File → New Map):
   - Assign a unique name (e.g., `HolonMirageForest`)
   - Choose a map group
   - Set dimensions (width × height in metatiles)
   - Select primary and secondary tilesets
3. Paint tiles on the map canvas
4. Set collision (walkability, ledges, water, etc.)
5. Place events:
   - **NPCs**: object events with associated scripts
   - **Warps**: connections between interior/exterior maps
   - **Triggers**: script triggers on tile entry
   - **Signposts**: interactable signs and hidden items
6. Define wild encounters (if applicable)
7. Set map connections to adjacent maps
8. Save → rebuild → test in emulator

**Files created/modified per map:**

```text
data/maps/HolonMirageForest/
├── map.json           ← map layout, dimensions, tilesets
├── scripts.inc        ← (or .pory if using Poryscript)
└── text.inc           ← NPC dialogue text
```

Plus entries added to `data/maps/map_groups.json`.

> [!TIP]
> **Start with a single test map**, not your final region. Create one internal development map (`TestMap_Dev`) to prove you can: place tiles, set collision, place warps, attach scripts, add an NPC, add a trainer, and test it all in-game. Once that loop works, your mapping pipeline is real.

> Sources:
> - [Porymap — Creating New Maps](https://huderlem.github.io/porymap/manual/creating-new-maps.html)
> - [Porymap — Project Files](https://huderlem.github.io/porymap/manual/project-files.html)

### 8.2 Scripts & Events — Building Progression

**Primary tools:** Poryscript (authoring) + Porymap (event placement)

Event scripting is the core of game progression — it's what makes maps playable. This is where you define:

| Script Type | Examples |
|---|---|
| NPC dialogue | Researcher field notes, townspeople reacting to Delta spread |
| Progression gates | Fragment discovery flags, ancient record unlocks, Deoxys encounter conditions |
| Cutscenes | First Delta Deoxys encounter, Rayquaza descent, Tower accident exposition |
| Item/gift logic | Starter selection (Delta species), research tools as key items |
| Battle triggers | Researcher battles, Delta Deoxys fragment encounters, Rayquaza |
| Ancient record reveals | Reading diamond carvings, stone dome inscriptions, Holon Legacy text |
| Warps/conditions | Tower floors, ancient ruin interiors, floating island access |


**Example — Complete NPC script (Poryscript):**

```c
script HolonProfessor_FirstMeet {
    lock
    faceplayer
    if (flag(FLAG_MET_RESEARCHER)) {
        msgbox("Good to see you again.\n"
               "Have you checked the old ruins yet?")
    } else {
        msgbox("Ah, you must be the new research\n"
               "assistant. Welcome to Holon!\p"
               "I'm lead researcher. I study the\n"
               "Delta phenomenon spreading from the Tower.")
        setflag(FLAG_MET_RESEARCHER)
    }
    release
}
```

**Mindset:** Early on, you are not "programming the whole game in C." You are building progression through event placement, script writing, flag/variable usage, warp logic, and battle triggers. That is the real core of building a Pokémon game in a decomp.

> Sources:
> - [Poryscript README](https://github.com/huderlem/poryscript)
> - [Porymap — Editing Map Events](https://huderlem.github.io/porymap/manual/editing-map-events.html)

### 8.3 Gameplay Data — Encounters, Trainers, Items

Expansion provides extensive built-in support for trainer customization and modern mechanics. Most data work is **definition and balancing**, not engine programming.

**Key data domains:**

| Domain | Where It Lives | How to Edit |
|---|---|---|
| Wild encounters | `src/data/wild_encounters.json` | Porymap or direct JSON — Delta encounter rates differ per location |
| Trainer rosters | `src/data/trainers.h` (or `.party` files) | Showdown syntax supported natively — paste from teambuilder |
| Species/forms | `src/data/pokemon/` | **Primary Delta work happens here** — stats, types, learnsets, sprites per Delta species |
| Items | `src/data/items.h` | Research tools, key items, Delta-specific held items |
| Moves | `src/data/moves_info.h` | Edit move data, power, type, effects |
| Maps | `data/maps/` | Porymap + map JSON files |

**Trainer authoring example (Showdown syntax):**
```
Charizard @ Charcoal
Ability: Blaze
Level: 38
- Flamethrower
- Dragon Rage
- Slash
- Scary Face
```

This is natively supported by expansion's trainer system — a huge time-saver versus manually defining every field.

**Workflow:**
1. Change one data domain at a time
2. Rebuild
3. Test the affected content in isolation
4. Commit the coherent change

Do **not** attempt giant all-at-once data overhauls before completing a working vertical slice.

### 8.4 Graphics & Presentation

**Asset categories you will gradually work with:**

| Category | Early Stage | Mid/Late Stage |
|---|---|---|
| Title/logo | Placeholder | Final Holon branding |
| UI | Expansion defaults | Custom menus, frames |
| Pokémon sprites | DS-style defaults | **Delta species custom sprites** — front, back, icon per Delta Pokémon |
| Trainer sprites | Defaults | Custom art for key characters |
| Overworld sprites | Defaults | Holon-specific NPCs and player |
| Tilesets | Existing + Team Aqua repo assets | Custom tilesets via Porytiles |
| Region map | Emerald defaults | Custom Holon region map |
| Music/SFX | Emerald defaults | Custom or community audio (BW2 music as atmospheric placeholder) |

**Use placeholders aggressively.** A working temporary asset is infinitely more valuable than no asset and a blocked pipeline.

**Pipeline order:**
1. Placeholder asset → 2. Working implementation → 3. In-game validation → 4. Replace with final art

> Source: [Team Aqua Asset Repo](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo) for community placeholder assets.

### 8.5 Custom Systems — The Last Pipeline

Before writing custom C code, always ask — in this order:

1. **Is this already built into expansion?** (Check FEATURES.md and config headers)
2. **Can I enable or tune it through config?** (Check `include/config/*.h`)
3. **Can I represent it through scripts/data?** (Poryscript, JSON data, flags/vars)
4. **Is there a stable feature branch for it?** (Check Team Aqua wiki, pret wiki)

Only if all answers are "no" should you move to custom engine work. Expansion already includes hundreds of features from the core series plus community QoL additions.

> Source: [pokeemerald-expansion README](https://github.com/rh-hideout/pokeemerald-expansion)

---

## 9. Transforming the Fork Into Pokémon Holon

### 9.1 The Five Replacement Layers

Building a new game on expansion means replacing the player-facing game in layers:

| Layer | What to Replace | Key Files/Domains |
|---|---|---|
| **World** | Maps, towns, routes, caves, warps, region map, heal points | `data/maps/`, `map_groups.json`, `heal_locations.json`, `region_map_sections.json` |
| **Progression** | Event flow, NPC logic, story gates, rival battles, gym sequence | Map scripts (`.pory` / `.inc`), flags, vars |
| **Gameplay data** | Encounters, trainers, items, moves, species tuning | `wild_encounters.json`, trainer data, species data |
| **Presentation** | Title, UI, tilesets, sprites, palettes, music/SFX | `graphics/`, `sound/`, UI source files |
| **Custom systems** | Mechanics expansion can't express via config/data/scripting | New C source files in `src/` |

### 9.2 The Safe Customization Model

Work through layers in order:

| Layer | Phase | Work |
|---|---|---|
| Layer 1 — Engine baseline | Keep intact | Don't modify expansion internals until you know what needs to change |
| Layer 2 — Project config | Configure | Branch choice, compile settings, config toggles, tool integration |
| Layer 3 — Game shell | Build first | Start flow, first area, initial NPCs, branding |
| Layer 4 — Broad content | Build second | Maps, trainers, encounters, assets, text, audio |
| Layer 5 — Custom systems | Build last | Only where config/data/scripts are insufficient |

### 9.3 What to Change First

Target the **game shell** — these changes structurally separate your game from Emerald:

- [ ] Title screen graphics → replace with Holon placeholder
- [ ] Expansion intro → disable (`EXPANSION_INTRO FALSE`)
- [ ] Create one custom starting area
- [ ] Create one connected route or interior
- [ ] Add one NPC with dialogue
- [ ] Add one trainer battle
- [ ] Add your own encounter table for that area
- [ ] Add version/project labels where visible

### 9.4 What NOT to Do First

> [!CAUTION]
> These actions cause the most damage in early development:
> - Building all five locations before the map pipeline is proven
> - Implementing all Delta species at once before testing one end-to-end
> - Writing the complete ancient record discovery system before a single record works
> - Merging multiple feature branches simultaneously
> - Replacing huge portions of the asset base before your pipeline works
> - Trying to "solve the full Delta Deoxys encounter system" before you have a playable shell

The repo structure and build flow already exist for a reason. Preserve them.

---

## 10. Development Roadmap — Phased Build Order

| Phase | Goal | Deliverable | Done? |
|---|---|---|---|
| **1. Stable engine baseline** | Prove the fork builds and runs | Clean build + debug build + ROM boots in emulator | ☐ |
| **2. Toolchain proof** | Prove content tools work | Porymap opens project, one test map created, Poryscript decision made | ☐ |
| **3. New game shell** | Stop being "Emerald with tweaks" | Title/branding, new start flow, one custom area, one researcher NPC, one trainer, one Delta encounter table | ☐ |
| **4. First Delta species** | Prove the Delta pipeline end-to-end | One Delta Pokémon: custom typing, placeholder sprite, correct encounter placement, correct summary screen display | ☐ |
| **5. Vertical slice** | Prove the full production loop | Mirage Forest entry → Holon outskirts → researcher NPCs → first ancient record → Delta encounter → trainer battle → heal loop | ☐ |
| **6. Production standards lock-in** | Stop improvising | Documented naming/folder/script/map/asset/testing conventions; Delta species authoring template established | ☐ |
| **7. Broad content** | Build all five locations | Mirage Forest, Holon, Holon Lake, Unnamed Island, Dragon Frontiers — maps, encounters, trainers, ancient records | ☐ |
| **8. Delta Deoxys encounters** | Implement all four fragments | Each Delta Deoxys fragment at its correct location with correct encounter conditions | ☐ |
| **9. Custom systems** | Add what scripting/data can't express | Fragment tracking, any Delta type UI work, anything that genuinely requires C | ☐ |
| **10. Polish & release prep** | Convert playable → shippable | QA, balance tuning, consistency pass, credits, packaging | ☐ |

**The correct build order in one sentence:**

> **Prove the engine → prove the tools → replace the game shell → prove one Delta species end-to-end → complete a vertical slice → lock production standards → scale all five locations → implement Deoxys encounters → add custom systems only where needed.**

> [!WARNING]
> **Do not jump into broad content production while you are still inventing the workflow.** If you're still uncertain about how maps are created, scripts are written, encounters are edited, or configs are changed — you're in pipeline proof, not production.

---

## 11. Feature Branches — Integration Workflow

Feature branches are community-maintained Git branches that add specific features not (yet) in expansion. They are **not guaranteed plug-ins** — some are version-specific, some have compatibility concerns, and some require adaptation from base `pokeemerald` to `pokeemerald-expansion`.

**Safe integration process:**

```bash
# 1. Always start on a dedicated branch
git checkout -b feature/decapitalized

# 2. Add the developer's repo as a remote
git remote add prof-harpe https://github.com/prof-harpe/pokeemerald-expansion

# 3. Pull the feature branch
git pull prof-harpe Decapitalized

# 4. Resolve any merge conflicts
# 5. Rebuild and test thoroughly
make -j$(sysctl -n hw.ncpu)

# 6. If it works: merge into your working branch
git checkout main
git merge feature/decapitalized

# 7. If it doesn't work: delete the branch and move on
git checkout main
git branch -D feature/decapitalized
```

> [!IMPORTANT]
> **Never pull a feature branch directly into your main working branch.** Always test on a disposable integration branch first.

For the full feature branch catalog with Holon-specific recommendations by tier, see: **`EXPANSION_GUIDE.md`** in your Documentation folder.

> Source: [Team Aqua Asset Repo Wiki — Feature Branches](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo/wiki/Feature-Branches)

---

## 12. Working Rules for Solo AI-Assisted Development

### Rule 1 — Always keep the main branch buildable
Never let your primary branch become a broken experiment pile. Use feature branches for risky work.

### Rule 2 — Commit small, coherent changes
Good: `"Set up Poryscript integration"` · `"Create first internal test map"` · `"Replace title graphics with Holon placeholders"`
Bad: `"Updated stuff"` · `"WIP everything"` · `"Changes"`

### Rule 3 — Use placeholders aggressively
A working temporary asset is more valuable than a blocked pipeline waiting for final art.

### Rule 4 — Test one pipeline at a time
Don't invent maps, scripts, assets, and custom engine code all at once. Prove each pipeline individually.

### Rule 5 — Use AI in bounded scopes

| ✅ Good AI use | ❌ Bad AI use |
|---|---|
| Explain a file or subsystem | "Refactor the whole project" |
| Draft a small script | "Rename everything" |
| Propose a localized code diff | "Merge five feature branches at once" |
| Review a set of changed files | "Rewrite all systems simultaneously" |
| Build a checklist or test plan | "Make the whole game" |

### Rule 6 — Prefer built-in expansion support before custom systems
Check config headers and FEATURES.md before writing custom C. The answer is usually "already built in."

### Rule 7 — Finish a real vertical slice before broad content production
A small complete loop teaches you more than a huge amount of unfinished content.

### Rule 8 — Don't break what you haven't explored
Before modifying any engine subsystem, read the relevant source files and understand how other files depend on it.

---

## 13. Definition of "Successfully Started"

The technical project is **properly started** when every item below is true:

- [ ] The repo builds and boots reliably (`make`, `make debug`, ROM runs)
- [ ] Your upstream remote strategy is in place (`RHH` remote added)
- [ ] Your map workflow works (Porymap → edit → rebuild → test)
- [ ] Your script workflow works (Poryscript or `.inc` → rebuild → test)
- [ ] Your placeholder asset workflow works (insert asset → rebuild → see in game)
- [ ] Key config decisions are made and applied (all gimmicks disabled, saveblock freed, species configured, DexNav enabled)
- [ ] **At least one Delta species is in the game with correct typing and a working placeholder sprite**
- [ ] You have one small playable internal slice that includes a Delta encounter table
- [ ] You understand where each type of future work goes (maps, scripts, data, graphics, config, custom code)

At that point, you are **no longer "setting things up."** You are actively developing Pokémon Holon.

---

## Sources

| Source | URL |
|---|---|
| pokeemerald-expansion GitHub | https://github.com/rh-hideout/pokeemerald-expansion |
| INSTALL.md | https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md |
| macOS Install Guide | https://github.com/rh-hideout/pokeemerald-expansion/blob/master/docs/install/mac/MAC_OS.md |
| Expansion Documentation | https://rh-hideout.github.io/pokeemerald-expansion/index.html |
| Team Aqua Asset Repo | https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo |
| Team Aqua Wiki | https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo/wiki |
| Porymap | https://huderlem.github.io/porymap/ |
| Porymap Manual — Introduction | https://huderlem.github.io/porymap/manual/introduction.html |
| Porymap Manual — Creating Maps | https://huderlem.github.io/porymap/manual/creating-new-maps.html |
| Porymap Manual — Project Files | https://huderlem.github.io/porymap/manual/project-files.html |
| Porymap Manual — Editing Events | https://huderlem.github.io/porymap/manual/editing-map-events.html |
| Poryscript | https://github.com/huderlem/poryscript |
| Porytiles | https://github.com/grunt-lucas/porytiles |
| Tilemap Studio | https://github.com/Rangi42/tilemap-studio |
| devkitPro Pacman Releases | https://github.com/devkitPro/pacman/releases |
| Python Downloads | https://www.python.org/downloads/ |
| Homebrew | https://brew.sh |
| Config files | `include/config/*.h` in the expansion repo |
