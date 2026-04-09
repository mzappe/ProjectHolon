---
title: "Pokémon Holon Legends — GDD Index"
doc-id: HL-IDX-001
version: 1.2
status: In Progress
category: Meta
last-updated: 2026-04-08
author: Matt Zappe
---

# Pokémon Holon Legends — GDD Index

> **Status:** In Progress | **Version:** 1.2 | **Updated:** 2026-04-08

---

## Table of Contents

- [1. Project Summary](#1-project-summary)
- [2. Current Document Registry](#2-current-document-registry)
  - [2.1 Canon & Narrative](#21-canon--narrative)
  - [2.2 Technical](#22-technical)
  - [2.3 Art, World, and Postgame](#23-art-world-and-postgame)
  - [2.4 Data & Tracking Files](#24-data--tracking-files)
- [3. Suggested Reading Order](#3-suggested-reading-order)
- [4. Current Open Decisions](#4-current-open-decisions)
  - [4.1 Story & Character](#41-story--character)
  - [4.2 World Structure](#42-world-structure)
  - [4.3 Postgame & Encounter Design](#43-postgame--encounter-design)
- [Changelog](#changelog)

---

## 1. Project Summary

**Pokémon Holon Legends** is a ROM hack built on [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion), set in the **Holon region** from the TCG Delta Species arc.

The current documentation set is organized around a layered workflow:

- **HL-104** establishes the synthesized canonical lore and environmental reference.
- **HL-106 v1.8** is the active design bible and current primary narrative design document.
- **HL-200 through HL-203** define the technical baseline, expansion strategy, change tracking, and implementation order.
- **HL-300, HL-400, and HL-500** cover sprite workflow, location production, and postgame expansion planning.
- Supporting CSVs track implementation changes and the working Holon Pokédex dataset.

| Detail | Value |
|---|---|
| **Base ROM** | pokeemerald-expansion (Pokémon Emerald decomp) |
| **Setting** | Holon region / Delta Species arc |
| **Platform** | Game Boy Advance |
| **Development model** | Solo, AI-assisted |
| **Primary narrative design doc** | HL-106 Design Bible v1.8 |
| **Primary lore synthesis doc** | HL-104 Complete Canonical Lore Guide |

---

## 2. Current Document Registry

### 2.1 Canon & Narrative

| ID | File | Title | Status | Version | Purpose |
|---|---|---|---|---|---|
| HL-104 | [HL-104-complete-holon-lore-guide.md](HL-104-complete-holon-lore-guide.md) | Complete Canonical Lore Guide | Active reference | Not declared | Unified canon synthesis for Holon, Delta biology, geography, and TCG-grounded world logic |
| HL-106 | [HL-106-design-bible_v1-8.md](HL-106-design-bible_v1-8.md) | Design Bible | Working document | 1.8 | Current master narrative and game-structure document |

### 2.2 Technical

| ID | File | Title | Status | Version | Purpose |
|---|---|---|---|---|---|
| HL-TEC-001 | [HL-200-technical-guide.md](HL-200-technical-guide.md) | Master Technical Guide | Stable | 1.0 | Core environment setup, build workflow, tooling, and project operating model |
| HL-TEC-002 | [HL-201-expansion-features.md](HL-201-expansion-features.md) | pokeemerald-expansion Features & Branch Guide | Stable | 1.0 | Expansion config reference and community branch catalog |
| HL-TEC-003 | [HL-202-feature-config-log.csv](HL-202-feature-config-log.csv) | Feature & Config Change Log | In Progress | 1.0 | Running record of engine and config changes already made |
| HL-TEC-004 | [HL-203-feature-implementation-plan.md](HL-203-feature-implementation-plan.md) | Feature Implementation Master Plan | In Progress | 1.0 | Dependency-aware execution plan for feature rollout |

### 2.3 Art, World, and Postgame

| ID | File | Title | Status | Version | Purpose |
|---|---|---|---|---|---|
| HL-ART-001 | [HL-300-sprite-palette-guide.md](HL-300-sprite-palette-guide.md) | Delta Species Sprite Palette Swapping Guide | Stable | 1.0 | Pixelorama recolor workflow and palette rules for Delta placeholder sprites |
| HL-400 | [HL-400-location-build-guide.md](HL-400-location-build-guide.md) | Location Build Guide | Working Template | 1.0 | Production template and location registry for area-by-area content buildout |
| HL-500 | [HL-500-delta-horizon.md](HL-500-delta-horizon.md) | Delta Horizon | Draft | 0.1 | Battle-Frontier-style postgame island concept and facility plan |

### 2.4 Data & Tracking Files

| ID | File | Title | Status | Version | Purpose |
|---|---|---|---|---|---|
| DATA-001 | [holon_pokedex_v2.csv](holon_pokedex_v2.csv) | Holon Pokédex Dataset | Working data | v2 | Species/location/type dataset derived from TCG card coverage |
| DATA-002 | [HL-202-feature-config-log.csv](HL-202-feature-config-log.csv) | Feature Change Ledger | Active log | 1.0 | Lightweight implementation audit trail for engine changes |

---

## 3. Suggested Reading Order

For the current documentation set, this is the shortest path to full project context:

| Step | Document | Why |
|---|---|---|
| 1 | **HL-104** — Complete Canonical Lore Guide | Start with the TCG-grounded world, environmental logic, and Delta distribution rules |
| 2 | **HL-106 v1.8** — Design Bible | Read the active game interpretation of that lore: structure, cast, acts, climax, and postgame |
| 3 | **HL-400** — Location Build Guide | Translate narrative/world intent into actual production units and area planning |
| 4 | **HL-500** — Delta Horizon | Understand the current postgame frontier concept and where it sits relative to the main arc |
| 5 | **HL-200** — Master Technical Guide | Ground the project in its actual build environment and workflow |
| 6 | **HL-201** — Expansion Features & Branch Guide | Review the available engine capabilities before implementation decisions |
| 7 | **HL-203** — Feature Implementation Master Plan | Use the phased execution order when moving from planning into engine work |
| 8 | **HL-300** — Sprite Palette Guide | Use once art production or placeholder Delta sprite work begins |
| 9 | **holon_pokedex_v2.csv** | Reference species/location coverage when validating encounter plans and Delta distribution |

---

## 4. Current Open Decisions

These reflect the unresolved design questions and explicit `[TBD]` items in the current design bible, especially [HL-106-design-bible_v1-8.md](HL-106-design-bible_v1-8.md).

### 4.1 Story & Character

| Decision | Status | Notes |
|---|---|---|
| **Entrance town name** | Open | Opening town is defined structurally but still unnamed |
| **Professor Cozmo's defining moment / knowledge arc** | Open | Meteorite, Deoxys, and crystal network realization path still unresolved |
| **Steven's final scene** | Open | Emotional resolution is not fully locked |
| **Auren's full prior knowledge and motive for staying in Holon** | Open | Backstory implications remain important to late-game reveals |
| **Covert team lead identity, name, and personal drive** | Open | Function is defined; personal specifics remain intentionally unresolved |
| **Mr. Stone's final knowledge and response** | Open | Degree of awareness and consequence is still undecided |

### 4.2 World Structure

| Decision | Status | Notes |
|---|---|---|
| **Floating Island main-story function** | Open | Needs resolution before act structure is fully finalized |
| **How the player accesses and understands the civilization's deepest cosmic records** | Open | Tied to Dragon Frontiers, Steven's arc, and climax communication |

### 4.3 Postgame & Encounter Design

| Decision | Status | Notes |
|---|---|---|
| **Mew ☆ δ meaning at Dragon Frontiers** | Open | Underwater placement, Devon's knowledge, and mission framing are linked questions |
| **Rayquaza alliance mechanism at the climax** | Open | Outcome is locked; exact turn from hostility to alliance is not |
| **Jirachi δ postgame quest framing** | Open | Quest giver and exact mission structure remain undecided |
| **Floating Island surface content** | Open | Postgame destination is locked; specific reveal/content payload is not |
| **Shadow Lugia δ / XD001 mission design** | Open | Major postgame content is named but not yet fully designed |

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| 1.0 | 2026-03-22 | Initial index created around the earlier documentation set |
| 1.1 | 2026-04-05 | Registered HL-TEC-004 (Feature Implementation Master Plan) |
| 1.2 | 2026-04-08 | Rebuilt index for the current documentation set; removed dead HL-100/101 references; registered HL-104, HL-106 v1.8, HL-400, HL-500, and data files; updated reading order and open decisions to match active docs |

---

*Pokémon Holon Legends — GDD Index | HL-IDX-001 v1.2 | Last updated 2026-04-08*
