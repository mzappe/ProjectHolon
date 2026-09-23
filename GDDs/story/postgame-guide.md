---
title: "Pokémon Holon Legends — Postgame Guide"
doc-id: HL-600
version: 0.1
status: Draft
category: Postgame
last-updated: 2026-09-16
author: Matt Zappe
---

# Pokémon Holon Legends — Postgame Guide

> **Status:** Draft | **Version:** 0.1 | **Updated:** 2026-09-16

---

## Table of Contents

- [1. Postgame Structure Overview](#1-postgame-structure-overview)
- [2. Mission-Based Content](#2-mission-based-content)
  - [2.1 Mew ☆ δ — Traces of the Beginning](#21-mew--δ--traces-of-the-beginning)
  - [2.2 The Heroes of Alto Mare](#22-the-heroes-of-alto-mare)
  - [2.3 Jirachi δ — The Comet's Arrival](#23-jirachi-δ--the-comets-arrival)
  - [2.4 Shadow Lugia / XD001](#24-shadow-lugia--xd001)
- [3. Loose Legendaries & Catchables](#3-loose-legendaries--catchables)
- [4. Gold Star Pokémon — The Shiny Mystery Layer](#4-gold-star-pokémon--the-shiny-mystery-layer)
  - [4.1 Foundation (Confirmed)](#41-foundation-confirmed)
  - [4.2 The Three Delta Gold Stars — The Unaging Ones](#42-the-three-delta-gold-stars--the-unaging-ones)
  - [4.3 The Ten Non-Delta Gold Stars — Standalone Encounters](#43-the-ten-non-delta-gold-stars--standalone-encounters)
  - [4.4 Encounter Mechanics (Confirmed)](#44-encounter-mechanics-confirmed)
- [5. Delta Horizon](#5-delta-horizon)
- [6. NEW: The Hoenn Incursion](#6-new-the-hoenn-incursion)
  - [6.1 Premise](#61-premise)
  - [6.2 Structure](#62-structure)
  - [6.3 Why Hoenn, Why Now](#63-why-hoenn-why-now)
  - [6.4 Zones & Beats](#64-zones--beats)
  - [6.5 Character Threads Resolved Here](#65-character-threads-resolved-here)
  - [6.6 Technical Rationale](#66-technical-rationale)
- [7. Character Threads Still Open Postgame](#7-character-threads-still-open-postgame)
- [8. Open Questions](#8-open-questions)
- [Changelog](#changelog)

---

## 1. Postgame Structure Overview

Postgame content falls into five buckets:

1. **Mission-based content** — self-contained questlines tied to a specific legendary/mythical, triggered after the credits.
2. **Loose legendaries** — Pokémon left unresolved by the main story, now roaming and catchable.
3. **Gold Star Pokémon** — thirteen shiny individuals, three carrying a layered mystery and ten standing as self-contained encounters.
4. **Delta Horizon** — a standalone Battle Frontier–equivalent island, mechanically separate from the story postgame.
5. **The Hoenn Incursion** *(new)* — a longer-form narrative arc that sends the player back to the mainland, reusing Hoenn's existing map data.

None of these are mutually exclusive — they can unlock in parallel or be sequenced by the player's own priorities.

---

## 2. Mission-Based Content

### 2.1 Mew ☆ δ — Traces of the Beginning

Mew was permanently transformed by proximity to Deoxys when it woke — a Delta transformation that never reverted. Found during the main story at Dragon Frontiers as a Water-type Delta Species, the furthest possible point from where the expedition began its search in Mirage Forest.

Postgame, the player follows traces of Mew's passage across all five zones — evidence of its movement, ancient carvings that recorded it millennia ago, researchers who came close and missed it. The final encounter should land as the closing page of something the player has been reading the entire game, likely staged at Dragon Frontiers or back at Mirage Forest where the search started.

### 2.2 The Heroes of Alto Mare

Latias δ and Latios δ postgame mission. Placement is unresolved between Holon Village and Holon Lake.

### 2.3 Jirachi δ — The Comet's Arrival

Dark/Fire typing. Seeded by the comet the Castaway mentions offhand during the player's first Volcano Observatory visit in Act 4 — a slow, distant approach that means nothing at the time. The comet carries Jirachi toward Earth, woken eventually by the outward pulse of the Tower incident. Located at the Crystal Isles volcano. This is the primary postgame mission by current weighting.

### 2.4 Shadow Lugia / XD001

Name and concept only. No origin, location, or connection to the Epsilon/Deoxys plotline has been established. This is the least developed postgame thread and the most open-ended — it doesn't currently need to tie into Holon's core mythology at all.

---

## 3. Loose Legendaries & Catchables

| Legendary | Status | Notes |
|---|---|---|
| Regirock, Regice, Registeel | Sealed, Mirage Forest | Deliberately sealed by the ancient civilization; postgame unseal. |
| Rayquaza δ | Postgame catchable | Single-type Fire Delta, no Metal secondary. Same individual allied with the player at the climax, or a separate sighting — TBD. |
| Delta Mewtwo | Remains at Holon Lake | Permanently transformed by Epsilon's proof-of-concept; unremovable evidence. Type TBD. |
| Groudon ☆, Kyogre ☆ | Loose in Holon's deep wilderness | Resurrected and lost by Epsilon in the witnessed Act 4 event; drawn further out by the region's ongoing magnetic disruption. |
| Deoxys | Open question | Whether it's catchable after being restored at the climax hasn't been decided. |

---

## 4. Gold Star Pokémon — The Shiny Mystery Layer

The Holon TCG arc includes thirteen canonical Gold Star cards across its five sets. Cross-referencing the Pokédex data:

| Pokémon | Set | Location | Delta? |
|---|---|---|---|
| Regirock ★ | EX Legend Maker | Mirage Forest | No |
| Regice ★ | EX Legend Maker | Mirage Forest | No |
| Registeel ★ | EX Legend Maker | Mirage Forest | No |
| Groudon ★ | EX Delta Species | Holon Research Tower | No |
| Kyogre ★ | EX Delta Species | Holon Research Tower | No |
| Metagross ★ | EX Delta Species | Holon Research Tower | No |
| Mewtwo ★ | EX Holon Phantoms | Holon Lake | No |
| Pikachu ★ | EX Holon Phantoms | Holon Lake | No |
| Gyarados ★ δ | EX Holon Phantoms | Holon Lake | **Yes** |
| Alakazam ★ | EX Crystal Guardians | Unnamed Island (Crystal Isles) | No |
| Celebi ★ | EX Crystal Guardians | Unnamed Island (Crystal Isles) | No |
| Mew ★ δ | EX Dragon Frontiers | Dragon Frontiers | **Yes** |
| Charizard ★ δ | EX Dragon Frontiers | Dragon Frontiers | **Yes** |

Ten are non-Delta. Three are Delta. That split is the structural basis for how this layer is built.

### 4.1 Foundation (Confirmed)

- **Gold Star = shiny.** In-world, shininess stays natural, unexplained population variance — no mechanical cause is invented for *why* a given individual is shiny. The TCG "star" designation is simply the card treatment applied to a shiny individual.
- **Force-shiny via `P_FLAG_FORCE_SHINY`** on each scripted encounter. Never shiny-locked, never left to RNG — these are specific individuals, not a rare roll.
- **Regular (non-shiny) versions of the same species still exist** in normal wild tables where applicable, so a Gold Star reads as a contrast against something the player has already seen, not the only version available.
- **No on-screen explanation.** No NPC uses the word "shiny." The shimmer speaks for itself.
- **Postgame/late-game discoveries**, consistent with the game's no-quest-marker, organic-discovery philosophy.

### 4.2 The Three Delta Gold Stars — The Unaging Ones

Mew ★ δ, Gyarados ★ δ, and Charizard ★ δ carry a genuine layered mystery the other ten don't share.

**The hook:** these are the same specific individuals documented decades ago by the first researchers to reach Holon. Those original records were classified or suppressed, and the individuals in question don't appear to have aged. The mystery isn't "why are they shiny" — it's why they've persisted unaged, and what the original researchers found that got buried. This ties the mystery into the antagonist faction's pre-Delta-accident presence in Holon.

**Suppression source:** Epsilon fits better than a generic "old researchers" framing, since Epsilon already has an established pattern of quiet suppression — burying the Deoxys incident, hiding infrastructure. They found the Gold Stars during their crystal-network survey (Era 4) and sat on it because an organism that doesn't age didn't fit the energy-harvesting narrative they were selling the board. Finding the Gold Star records doubles as evidence of Epsilon's broader concealment pattern rather than sitting beside the main plot as an unrelated curiosity.

**How the player encounters the idea (diegetic, not explained):**
- A weathered field journal or torn photo showing an individual with the exact same marking pattern the player later finds in an encounter.
- An old researcher — the Island Hermit is the natural candidate, given he's already an isolated, pre-existing figure with no faction ties — who mentions having "said the same thing thirty years ago" without elaborating further.
- Local names or vague references ("the gold one") rather than any mechanical term.

**Resolution stays open**, consistent with the game's Crichton/Crouch commitment. The suppressed records can confirm *that* these individuals don't age without explaining *why* — matching how the main plot treats expertise and blind spots rather than resolving into a tidy unifying answer.

**Individual basis for each (per-location framing, not a shared cause):**
- **Gyarados ★ δ — Holon Lake.** The Lake of Rage parallel: a shining individual born from Holon Lake's already-anomalous field (the same field responsible for Meowth δ's pre-evolution Metal typing and Magikarp δ's inverted evolution line).
- **Charizard ★ δ — Dragon Frontiers.** The natural endpoint of the Delta phenomenon running its full course on a species with no Tower interference at all — paired with Mew ★ δ as the set's other headline Gold Star, and deserving the same narrative weight rather than being left as a simple postgame catch.
- **Mew ★ δ — Dragon Frontiers.** Already covered in full under [2.1](#21-mew--δ--traces-of-the-beginning). Its Gold Star mystery folds into and culminates the existing Mew mission rather than running as a separate track — it earns the ending's own treatment rather than following the same structure as the other two.

### 4.3 The Ten Non-Delta Gold Stars — Standalone Encounters

These ten share no unifying lore. Each is its own self-contained postgame encounter or mini-mission — the point is variety of encounter *type*, not a connected mystery:

| Pokémon | Location | Status |
|---|---|---|
| Regirock ★, Regice ★, Registeel ★ | Mirage Forest | Already covered — see [Section 3](#3-loose-legendaries--catchables). These are specifically the shiny individuals the ancient civilization sealed; the "exceptional ones" framing already fits without new design work. |
| Groudon ★, Kyogre ★ | Holon Research Tower (card) / loose in deep wilderness (story) | Already covered — see [Section 3](#3-loose-legendaries--catchables). The already-established Act 4 resurrection-and-loss event is the Gold Star origin for these two; no separate encounter needed. |
| Metagross ★ | Holon Research Tower | **Needs a new standalone encounter.** No design work done yet. |
| Mewtwo ★ | Holon Lake | **Needs a new standalone encounter**, distinct from Delta Mewtwo (a different individual with a different story). |
| Pikachu ★ | Holon Lake | **Needs a new standalone encounter.** |
| Alakazam ★ | Crystal Isles | **Needs a new standalone encounter.** Possible tie to the Holon Circle or the Castaway's own tracking, given his throughline already runs through this zone. |
| Celebi ★ | Crystal Isles | **Needs a new standalone encounter.** |

Encounter *type* variety floated for these five (not yet assigned to specific Pokémon): a casino-style event, a pure static encounter, a roaming encounter. Assignment is open.

### 4.4 Encounter Mechanics (Confirmed)

- **One-per-save, no respawn.** Gold Stars are individuals, not population spawns — unlike Gen 3's legendary respawn-on-reset precedent. Once an encounter triggers, save-resetting to retry a catch attempt is fine; fleeing or fainting the Pokémon *after* the event has triggered risks it being gone for that save.
- **Proposed, not locked:** a unique held item or custom move per individual, signaling in the Pokédex/summary screen that this isn't just a shiny — communicating that this specific Pokémon was somewhere and did something before the player found it. Floated in discussion, not yet confirmed as a design decision.

---

## 5. Delta Horizon

Full detail lives in HL-500. Summary for this guide:

A remote sea island, the game's Battle Frontier equivalent, reached by boat on first visit and Fly afterward. Inhabited by an independent community of trainers unaffiliated with the Holon research effort. Four facilities:

- **Delta Colosseum** (Battle Tower equivalent) — ranked singles/doubles win-streak battles.
- **Delta Preserve** (Battle Factory equivalent) — rentals drawn entirely from Delta Species.
- **Delta Labyrinth** (Battle Pyramid equivalent) — a dungeon crawl through crystal-embedded terrain.
- **Delta Passage** (Battle Pike equivalent) — a linear route of random-outcome rooms.

Its unlock condition and any connection to Auren, Ty, the Castaway, or the ancient civilization remain open. Whether its "outward pulse" framing is the same Tower incident pulse established in HL-110 also needs reconciling — see Open Questions.

---

## 6. NEW: The Hoenn Incursion

### 6.1 Premise

Months after Dragon Frontiers, reports start coming in from Hoenn: Pokémon behaving strangely near Rustboro, a species nobody can identify sighted near a familiar route, a Devon facility gone quiet. The outward pulse the Tower incident sent through the crystal network — established in HL-110 as having unresolved global effects — didn't stay contained to Holon. It reached the region the entire expedition launched from.

This is Holon's *Jurassic Park* → *The Lost World* turn: the wonder of the first game giving way to the wonder becoming a problem that follows you home. Delta Species are now loose on the Hoenn mainland, and the corporation that caused it also owns most of the infrastructure it's now spreading through.

### 6.2 Structure

The player travels back to Hoenn by boat — the same journey in reverse that opened the game. Rather than a new region, this arc **reuses Hoenn's existing map** with targeted overlays: quarantined zones, Delta encounter tables layered onto familiar routes, altered NPC dialogue and event scripts reflecting the outbreak, and a handful of new interior maps (a Devon containment site, an operations camp) rather than a full new tileset.

The player isn't exploring blind. They're returning to a place they already know, watching it get overwritten by what they caused.

### 6.3 Why Hoenn, Why Now

- **Devon is Hoenn's company.** Steven, now president, has to deal with the consequences of his own organization's covert program in his own backyard — the postgame test of what "his Devon" actually does differently.
- **It closes the loop on an existing open question.** HL-110 Era 5 flags the pulse's global-scale effect as unresolved. This arc is the answer.
- **It reframes familiar ground.** Routes, towns, and NPCs the player (if they know Hoenn) already associates with the base game now carry Delta Species and containment infrastructure — the same "wonder becomes threat" turn Crichton/Crouch structure calls for, now played out somewhere ordinary instead of somewhere exotic.

### 6.4 Zones & Beats

*Placeholder structure — exact routes and staging TBD once base-map scope is confirmed.*

- **Arrival:** The player disembarks to a Devon-controlled perimeter, not a warm welcome. Something is already being managed, and the player is here because Steven asked them to be — the same "outside, trusted" role they filled at the start of the game.
- **Containment zones:** Familiar Hoenn routes now host Delta encounter tables and visible quarantine measures — fencing, warning signage, evacuated towns or districts. Delta Species here would skew toward whichever families make narrative sense as "escaped and adapting" rather than the full regional dex.
- **The source point:** Tracing the outbreak back to whichever Devon facility or shipment carried the pulse's effect out of Holon — this is where Steven's institutional arc gets tested directly: contain quietly, or disclose.
- **Escalation:** A Lost World beat — something Delta-touched proves difficult to contain, forcing a choice between capture and letting it go. Mirrors the Groudon/Kyogre breakout from Act 4, but now on Devon's home ground with no Holon-side crystal network to explain or contain it.
- **Resolution:** Not a reversal — consistent with the game's refusal of restoration endings. Hoenn doesn't get "fixed." It gets a new, managed equilibrium, same as Holon did. Devon under Steven either becomes the institution that discloses and manages this honestly, or doesn't — this is the concrete test of his presidency the main story's ending only gestures at.

### 6.5 Character Threads Resolved Here

- **Steven as president** — this arc is the actual proving ground for "what does Steven's Devon do differently," rather than leaving it as an epilogue statement.
- **Ty's endpoint** — a plausible location for Ty to resurface, on Devon's home turf rather than in Holon, if reconciliation or a final confrontation is wanted without repeating Dragon Frontiers' stakes.
- **Mr. Stone** — an opportunity to show, rather than state, what he does or doesn't do with the knowledge he has by the game's end.

### 6.6 Technical Rationale

Because pokeemerald-expansion is built on Hoenn's own map data, this arc can be built primarily through:

- **Map overlays and recolors** on existing Hoenn tilesets rather than new tile art.
- **Encounter table edits** layering Delta Species onto existing routes.
- **Event script changes** — NPC dialogue swaps, new flags, quarantine barriers — reusing existing map objects and warps rather than authoring new maps wholesale.
- A small number of genuinely new interior maps (containment facility, operations camp) where reuse isn't sufficient.

This keeps the arc's scope proportional to solo-dev capacity while still delivering a full postgame region shift.

---

## 7. Character Threads Still Open Postgame

- **Ty's endpoint** — reconciliation, permanent distance, or a Hoenn Incursion appearance.
- **Steven as Devon's president** — what he does with the company, tested concretely by the Hoenn Incursion rather than left as a stated outcome.
- **Mr. Stone** — role and knowledge level by the time of any postgame confrontation.
- **Auren** — whether the Champion has any active postgame role beyond the title itself.

---

## 8. Open Questions

- Does the Hoenn Incursion's outbreak trace to a single shipment/facility, or is it framed as the pulse having reached Hoenn directly through some other mechanism?
- Which Hoenn routes/towns host the outbreak, and how much of the base map needs quarantine-state overlays vs. staying untouched?
- Does Ty appear in this arc, and if so, is it before or after any resolution reached at Dragon Frontiers?
- Does the Hoenn Incursion's pulse-reaches-Hoenn premise reconcile with, or replace, Delta Horizon's own "outward pulse" framing from HL-500?
- Is Delta Horizon's unlock gated behind the Hoenn Incursion, independent of it, or does completing one affect the other?
- What Delta Species families make sense as "escaped and adapted" for Hoenn specifically, versus families that should stay Holon-exclusive?
- What are the five specific standalone encounter designs for Metagross ★, Mewtwo ★, Pikachu ★, Alakazam ★, and Celebi ★ — which gets the casino event, which gets a static encounter, which roams?
- Is the held-item/custom-move-per-Gold-Star idea worth locking in, or staying with a plain shiny + no extra mechanical marker?

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 0.1 | 2026-09-16 | Initial compilation from HL-110 and HL-500; added The Hoenn Incursion as a new postgame arc |
| 0.2 | 2026-09-18 | Added Gold Star Pokémon section, cross-referenced against the full Pokédex CSV and prior Gold Star lore discussion; renumbered sections 4–8 |

---

*Pokémon Holon Legends — Postgame Guide | HL-600 v0.1 | Last updated 2026-09-16*
