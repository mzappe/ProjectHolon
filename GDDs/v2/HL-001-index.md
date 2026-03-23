---
title: "Pokémon Holon Legends — GDD Index"
doc-id: HL-IDX-001
version: 1.0
status: In Progress
category: Meta
last-updated: 2026-03-22
author: Matt Zappe
---

# Pokémon Holon Legends — GDD Index

> **Status:** In Progress | **Version:** 1.0 | **Updated:** 2026-03-22

---

## Table of Contents

- [1. Project Summary](#1-project-summary)
- [2. Document Registry](#2-document-registry)
  - [2.1 Lore](#21-lore)
  - [2.2 Technical](#22-technical)
  - [2.3 Art](#23-art)
- [3. Suggested Reading Order](#3-suggested-reading-order)
- [4. Open Decisions Tracker](#4-open-decisions-tracker)
  - [4.1 Characters & Narrative](#41-characters--narrative)
  - [4.2 World & Locations](#42-world--locations)
  - [4.3 Gameplay & Mechanics](#43-gameplay--mechanics)
  - [4.4 Art & Design](#44-art--design)
  - [Changelog](#changelog)

---

## 1. Project Summary

**Pokémon Holon Legends** is a ROM hack built on [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion) (Pokémon Emerald decomp), set in the **Holon region** from the TCG Delta Species arc (EX Legend Maker through EX Dragon Frontiers).

The game tells the story of a scientific accident, an ancient mystery, and a living organism from space that has been dormant beneath a research tower for thousands of years. The Holon Research Tower has been broadcasting electromagnetic energy for years, slowly transforming local Pokémon into **Delta Species** — creatures with different elemental types than their species would normally carry. Then something went wrong.

The player travels outward from Mirage Forest through five locations that mirror the five TCG sets of the Delta Species arc, piecing together what happened, what is still happening, and how to stop it before the region's ecosystems collapse entirely.

| Detail | Value |
|--------|-------|
| **Base ROM** | pokeemerald-expansion (Pokémon Emerald decomp) |
| **Region** | Holon — from the TCG Delta Species arc |
| **TCG source** | EX Legend Maker · EX Delta Species · EX Holon Phantoms · EX Crystal Guardians · EX Dragon Frontiers |
| **Platform** | Game Boy Advance (GBA) |
| **Development** | Solo, AI-assisted, macOS |
| **Lore source** | Bulbapedia / TCG Delta Species arc; invented content marked in docs |

---

## 2. Document Registry

### 2.1 Lore

| ID | File | Title | Status | Version | Description |
|----|------|-------|--------|---------|-------------|
| HL-LOR-001 | [HL-100-story-bible.md](HL-100-story-bible.md) | Story & Lore Bible | Draft | 4.0 | Full narrative, world, characters, accident sequence, ending, postgame, themes, and open questions |
| HL-LOR-002 | [HL-101-delta-species-lore.md](HL-101-delta-species-lore.md) | Holon & Delta Species TCG Lore Reference | Stable | 1.0 | TCG card-sourced lore, Delta mechanics, Holon's Pokémon rules, and canonical type reference |

### 2.2 Technical

| ID | File | Title | Status | Version | Description |
|----|------|-------|--------|---------|-------------|
| HL-TEC-001 | [HL-200-technical-guide.md](HL-200-technical-guide.md) | Master Technical Guide | Stable | 1.0 | macOS dev environment, build pipeline, tool stack, branch strategy, production pipelines, roadmap |
| HL-TEC-002 | [HL-201-expansion-features.md](HL-201-expansion-features.md) | pokeemerald-expansion Features & Branch Guide | Stable | 1.0 | Expansion branch selection, key features, integration workflow, and feature flags |

### 2.3 Art

| ID | File | Title | Status | Version | Description |
|----|------|-------|--------|---------|-------------|
| HL-ART-001 | [HL-300-sprite-palette-guide.md](HL-300-sprite-palette-guide.md) | Delta Species Sprite Palette Swapping Guide | Stable | 1.0 | Step-by-step Pixelorama workflow for Delta recolors; palette conventions, export settings, verification |

---

## 3. Suggested Reading Order

For a new contributor or collaborator coming to the project cold:

| Step | Document | Why |
|------|----------|-----|
| 1 | **HL-100** — Story Bible (§1–§7) | Understand the setting, the accident, and the central conflict before anything else |
| 2 | **HL-101** — Delta Species Lore | Get grounded in the TCG source material the game is built on |
| 3 | **HL-100** — Story Bible (§8–§16) | Fragments, locations, characters, ending, postgame, and open questions |
| 4 | **HL-200** — Technical Guide (§1–§3) | Project model, mental framework, and environment setup |
| 5 | **HL-201** — Expansion Features | Understand the expansion branch before diving deeper into technical work |
| 6 | **HL-200** — Technical Guide (§4–§13) | Branch strategy, tool stack, pipelines, and working rules |
| 7 | **HL-300** — Sprite Palette Guide | Start producing Delta sprite assets |

---

## 4. Open Decisions Tracker

All items sourced from [HL-100 §16 — Open Questions](HL-100-story-bible.md#16-open-questions-pending-decisions). This tracker mirrors that section; update both when a decision is made.

### 4.1 Characters & Narrative

| Decision | Status | Notes |
|----------|--------|-------|
| **Starter Pokémon** — three Delta Species | ❌ Open | Specific choices not yet made |
| **Player character** — name, appearance, backstory | ❌ Open | Specific details not yet decided |
| **Rival** — identity, relationship to player, team | ❌ Open | Not yet designed |
| **Faction name and leadership** — group name; who leads and what drives them | ❌ Open | Character not yet designed |

### 4.2 World & Locations

| Decision | Status | Notes |
|----------|--------|-------|
| **The floating island surface** — what is up there; what the ancient civilization left | ❌ Open | TCG source material undefined; game to define |

### 4.3 Gameplay & Mechanics

| Decision | Status | Notes |
|----------|--------|-------|
| **Gym leader identities** — eight station chiefs; specialisms, teams, Delta connection | ❌ Open | Not yet designed |
| **Deoxys encounter design** — four-fragment battle beneath the Tower | ❌ Open | Mechanical approach not decided |
| **Postgame Delta legendary placement** — Rayquaza δ, Latias δ + Latios δ, Lugia δ | ❌ Open | Locations and encounter structures TBD |
| **Specific postgame details** — satellite islets secrets; faction researcher side content | ❌ Open | Full scope TBD |

### 4.4 Art & Design

| Decision | Status | Notes |
|----------|--------|-------|
| **Lugia δ typing and design** — invented form, not yet designed | ❌ Open | No TCG canon form exists; full design needed |

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 1.0 | 2026-03-22 | Initial index created; all five v2 docs registered; open decisions tracker seeded from HL-100 §16 |

---

*Pokémon Holon Legends — GDD Index | HL-IDX-001 v1.0 | Last updated 2026-03-22*
