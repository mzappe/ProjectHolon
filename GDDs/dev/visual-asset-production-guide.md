---
title: "Pokémon Holon Legends — Visual Asset and Animation Production Guide"
doc-id: HL-ART-002
version: 1.0
status: Living Document
category: Art
last-updated: 2026-08-31
author: Matt Zappe
---

# Pokémon Holon Legends — Visual Asset and Animation Production Guide

> **Status:** Living Document | **Version:** 1.0 | **Updated:** 2026-08-31

This is the creative-production hub for Project Holon's visual identity. It describes what can be designed with Codex and image-generation assistance, which assets can become production-ready game content, how artwork moves from an idea into the ROM, and which visual projects should be tackled first.

It is intentionally broader than a drawing guide. The goal is to connect concept development, pixel-art production, GBA constraints, animation programming, repository integration, and in-game validation into one repeatable workflow.

Related technical references:

- [Customizing the Emerald Title Screen](title-screen-customization-tutorial.md)
- [Delta Species Sprite Palette Swapping Guide](sprite-palette-guide.md)
- [Complete Canonical Lore Guide](../story/complete-holon-lore-guide.md)
- [Delta Horizon](../story/delta-horizon.md)
- [Project Build Log](../BUILD-LOG.md)

---

## Table of Contents

- [1. Purpose and Scope](#1-purpose-and-scope)
- [2. What Codex Can Contribute](#2-what-codex-can-contribute)
- [3. Production Levels](#3-production-levels)
- [4. Core Production Workflow](#4-core-production-workflow)
- [5. Technical Art Standards](#5-technical-art-standards)
- [6. Title Screen Art and Animation](#6-title-screen-art-and-animation)
- [7. Intro Sequences and Cutscenes](#7-intro-sequences-and-cutscenes)
- [8. Battle Backgrounds and Transitions](#8-battle-backgrounds-and-transitions)
- [9. Delta Species and Custom Pokémon](#9-delta-species-and-custom-pokémon)
- [10. Trainers and Character Presentation](#10-trainers-and-character-presentation)
- [11. Overworld Environments and Maps](#11-overworld-environments-and-maps)
- [12. Interface, Icons, and Collectible Art](#12-interface-icons-and-collectible-art)
- [13. Effects and Ambient Animation](#13-effects-and-ambient-animation)
- [14. Holon Visual Idea Bank](#14-holon-visual-idea-bank)
- [15. Recommended Production Roadmap](#15-recommended-production-roadmap)
- [16. Repository Integration Map](#16-repository-integration-map)
- [17. Reusable Creative Briefs](#17-reusable-creative-briefs)
- [18. Review and Definition of Done](#18-review-and-definition-of-done)
- [19. Limitations and Risk Management](#19-limitations-and-risk-management)
- [20. Working Agreements](#20-working-agreements)
- [21. Immediate Next Projects](#21-immediate-next-projects)
- [Changelog](#changelog)

---

## 1. Purpose and Scope

This guide covers visual work in four connected disciplines:

1. **Creative direction** — themes, silhouettes, motifs, palettes, composition, and visual storytelling.
2. **Raster and pixel-art production** — mockups, illustrations, sprites, tiles, backgrounds, effects, and animation frames.
3. **Technical art** — indexed palettes, transparency, tile reuse, sprite-sheet layout, GBA conversion, memory awareness, and build compatibility.
4. **Implementation** — loading assets, programming motion and effects, connecting species data, building the ROM, and validating the result in-game.

The scope includes both adaptations of existing Pokémon material and original material created for Project Holon:

- Delta Species forms
- Fully custom Pokémon and evolutionary families
- Title-screen key art
- Cutscene stills and limited animation
- Battle environments and encounter transitions
- Trainer and overworld sprites
- Tilesets and environmental set dressing
- UI artwork and icons
- Particle, palette, scanline, and affine effects
- Concept sheets and visual-development documents

The guide does not assume every generated image is a shippable asset. It establishes a process for turning strong visual ideas into deterministic, hardware-compatible game assets.

---

## 2. What Codex Can Contribute

Codex can operate across the full path from a rough idea to a tested implementation. The amount of human direction required depends on how canon-sensitive and visually specific the asset is.

### 2.1 Capability matrix

| Area | Capabilities | Typical deliverables | Integration potential |
|---|---|---|---|
| Art direction | Develop motifs, palettes, silhouette rules, faction identities, and regional style | Art bible, mood boards, palette plans, design briefs | Documentation and production reference |
| Concept art | Generate or edit visual explorations from text and references | Composition studies, creature concepts, environment concepts, pose sheets | Reference for final pixel work |
| Pixel art | Create, edit, clean, resize, index, and validate raster assets | Sprites, icons, backgrounds, stills, tiles, effects | Directly usable after technical validation |
| Animation design | Plan timing, loops, layers, transitions, and frame economy | Storyboards, frame lists, sprite sheets, timing charts | Can be implemented in C and event scripts |
| Technical art | Enforce dimensions, transparency, palette count, tile alignment, and format | Indexed PNGs, palettes, tilemaps, optimized sheets | Build-pipeline-ready assets |
| Programming | Wire assets into existing systems or implement new presentation logic | C changes, data-table changes, scripts, configuration | Compiled and tested in the ROM |
| QA | Inspect assets, compile, run targeted tests, and diagnose visual corruption | Checklists, screenshots, build results, correction passes | Production verification |
| Documentation | Record conventions and make future work repeatable | Tutorials, specifications, asset manifests, build-log entries | Long-term project knowledge |

### 2.2 Strongest use cases

The most efficient assignments combine creative work with a bounded technical target:

- “Create three title-screen compositions that preserve the approved logo area.”
- “Design a Lightning/Metal Delta form for this species, then finish its front and back sprites.”
- “Create an animated research-tower battle background using the existing battle-environment format.”
- “Turn this cutscene description into four stills with a pan, lightning flash, and dialogue timing.”
- “Create a visual language for Holon energy and reuse it across maps, battles, menus, and cutscenes.”

### 2.3 Work that remains deliberately controlled

Generated imagery is best treated as visual-development material until it passes a production pass. Final assets require deliberate control over:

- Anatomy and identity across multiple views
- Pixel clusters and outline quality
- Palette indices and transparency
- Frame-to-frame consistency
- Sprite anchors and battle positioning
- Tile boundaries and repeated-tile budgets
- Text spelling and logo fidelity
- Copyright and provenance decisions for reference materials
- The distinction between established canon and new Project Holon interpretation

---

## 3. Production Levels

Every visual request should identify its intended production level. This prevents a mockup from being mistaken for a finished game asset.

### 3.1 Level A — Exploration

Purpose: discover what the asset should be.

Deliverables may include:

- Mood boards
- Silhouette sheets
- Palette studies
- Composition thumbnails
- Loose character or environment concepts
- Written visual directions

Exploration assets are not constrained to GBA dimensions or palettes. Their value is speed and range.

### 3.2 Level B — Approved concept

Purpose: establish the design that production will follow.

An approved concept should lock:

- Subject and silhouette
- Major colors and material language
- Pose or composition
- Required layers
- Narrative purpose
- Elements that must remain invariant

It may still be larger and more detailed than the final game asset.

### 3.3 Level C — Game-resolution prototype

Purpose: prove that the concept survives the actual display scale.

The prototype should use the correct canvas and approximate palette budget. It should answer:

- Is the silhouette readable?
- Do the focal points survive at native resolution?
- Does the sprite fit its box?
- Does the background leave room for UI and battlers?
- Can the image be divided into practical layers or tiles?

It does not need final animation or perfect optimization.

### 3.4 Level D — ROM-ready asset

Purpose: produce a deterministic source asset accepted by the build pipeline.

Requirements include:

- Correct dimensions and sheet layout
- Correct color mode and palette count
- Valid transparency index
- Clean pixel clusters without accidental anti-aliasing
- Consistent frames and views
- Source PNG/PAL/BIN files stored in the repository
- No dependence on an external preview-only file

### 3.5 Level E — Integrated and verified

Purpose: finish the feature as players will experience it.

Requirements include:

- Code or data integration
- Successful build
- In-game inspection
- Correct timing, layering, positioning, and palette behavior
- No regression to adjacent screens or forms
- Documentation of important implementation decisions

Unless a request explicitly stops at an earlier level, production work should aim for Level E.

---

## 4. Core Production Workflow

### 4.1 Phase 1 — Define the brief

Before generating or editing artwork, define:

- Asset type and intended screen
- Narrative purpose
- Required subject, text, and recognizable features
- Target dimensions and format
- Art-style reference
- Palette or atmosphere
- Animation requirements
- Elements to preserve
- Elements to avoid
- Whether the output is exploratory or intended for the ROM

If the asset depicts established canon, identify the lore source and which details are mandatory. If the asset introduces new interpretation, label that interpretation as a proposal until approved.

### 4.2 Phase 2 — Inspect the target system

Before committing to a design, inspect the current assets and code that will consume it. Questions include:

- What does the existing loader expect?
- Is the image a sprite, tiled background, affine background, or full-screen bitmap?
- Which dimensions are hardcoded?
- Does it share a palette with another layer?
- Which files are true sources and which files are generated?
- What animation facilities already exist?
- Is there a proven neighboring asset to use as the structural template?

### 4.3 Phase 3 — Explore compositions or designs

Create distinct concepts rather than minor color variants. Exploration should compare meaningful alternatives such as:

- Different silhouettes
- Different camera angles
- Different focal points
- Different degrees of transformation
- Different layer structures
- Different emotional tones

Each concept should be named and briefly described so feedback can be precise.

### 4.4 Phase 4 — Lock the visual contract

Once a direction is selected, record the invariants. Example:

> Preserve the base Pokémon's head shape, eye placement, and tail silhouette. Replace its organic armor with crystalline plates. Keep the chest marking visible in front and back views. Do not add wings or change the number of limbs.

The visual contract is repeated during edits so refinements do not cause design drift.

### 4.5 Phase 5 — Produce the native-resolution asset

Rebuild the chosen design at the actual target size. This is usually not a simple automatic downscale. It requires:

- Simplifying small details
- Replacing gradients with intentional clusters or bands
- Strengthening silhouette breaks
- Correcting tangents and one-pixel noise
- Reserving colors for readable highlights
- Positioning the asset on the engine's expected anchor

### 4.6 Phase 6 — Apply technical constraints

Convert and validate:

- Indexed color mode
- Palette size and order
- Transparent palette index
- GBA-safe RGB conversion
- Correct sheet dimensions
- Correct tile or map data
- Compression and loader compatibility

Generated binary formats should be produced through the repository's toolchain. Source PNG, PAL, and BIN files remain the editable truth.

### 4.7 Phase 7 — Implement animation and behavior

Animation can combine authored frames with inexpensive engine effects:

- Frame swaps
- Sprite translation
- Affine scale and rotation
- Background scrolling
- Palette cycling
- Alpha blending
- Brightness fades
- Scanline distortion
- Window masks
- Particles and secondary sprites

Engine effects are often more memory-efficient and consistent than storing many full frames.

### 4.8 Phase 8 — Build and validate

Validation should occur on the intended screen, not only in an image editor. Review:

- Native 240×160 output
- Hardware-like color and scaling
- Layer priorities
- Transparency and palette ownership
- Sprite anchors
- UI overlap
- Animation loop seams
- Timing with music, dialogue, or battle flow
- Behavior during fades and scene transitions

### 4.9 Phase 9 — Preserve the result

For finished work:

- Store final project assets inside the repository.
- Preserve larger masters or concept sources in an appropriate art-source folder if they are needed later.
- Do not leave a game-referenced image only in an external generation directory.
- Record non-obvious code and pipeline decisions in the build log.
- Update this guide when a new reusable convention is established.

---

## 5. Technical Art Standards

### 5.1 GBA display and color fundamentals

- Native display: **240×160 pixels**.
- Most background and object graphics are organized in **8×8 tiles**.
- 4bpp graphics use **16 palette entries**, normally with index 0 reserved for transparency where applicable.
- GBA color uses **5 bits per RGB channel**; desktop colors can shift after conversion.
- Pixel art must be resized with nearest-neighbor sampling.
- Anti-aliased edges and partially transparent pixels are generally unsuitable for native sprite assets.
- An image that visually contains few colors is not necessarily an indexed PNG. Color mode must be verified.

### 5.2 Pixel-art quality rules

Final pixel art should use:

- Intentional clusters instead of scattered single pixels
- Consistent outline treatment
- Readable value separation before hue separation
- Controlled use of highlights
- Limited dithering, reserved for surfaces that benefit from texture
- Clean diagonals and curves
- No automatic smoothing
- No accidental subpixel or semi-transparent edge colors

### 5.3 Palette rules

Every palette should have a purpose. A typical sprite palette allocates colors among:

- Transparency
- Outline and deepest shadow
- Primary material ramp
- Secondary material ramp
- Highlight or energy accent
- Eye, mouth, or identifying feature

Normal and shiny palettes must preserve value structure. A shiny palette should look intentional and remain readable; it is not enough to rotate hues indiscriminately.

### 5.4 Layering strategy

Complex scenes should be decomposed by motion and palette needs:

- Static far background
- Scrolling atmosphere
- Main subject or silhouette
- Foreground framing
- UI and text
- Additive or flashing effects
- Sprite-based particles

The right layer split makes animation cheaper and prevents a single effect from forcing the entire scene to be redrawn.

### 5.5 Asset safety

- Never overwrite an approved asset during exploration; use versioned siblings or a working source folder.
- Do not hand-edit generated `.4bpp`, `.8bpp`, `.gbapal`, `.smol`, or `.smolTM` files.
- Keep transparent index behavior stable.
- Inspect neighboring assets before assuming a format is universal.
- Preserve unrelated user changes in the working tree.

---

## 6. Title Screen Art and Animation

The title screen is the recommended first complete visual-production project because it concentrates art direction, layering, animation, audio timing, and GBA technical work into one highly visible feature.

### 6.1 Existing structure

The Emerald title screen currently combines:

- `graphics/title_screen/pokemon_logo.png`
- `graphics/title_screen/emerald_version.png`
- `graphics/title_screen/rayquaza.png` and its tilemap
- `graphics/title_screen/clouds.png` and its tilemap
- `graphics/title_screen/logo_shine.png`
- `graphics/title_screen/press_start.png`
- Shared and element-specific palettes
- Behavior implemented primarily in `src/title_screen.c`

The approved new subtitle can be treated as a locked element while the rest of the composition is redesigned around it.

### 6.2 Possible visual directions

These are proposals, not automatic canon:

#### A. Research Tower Signal

The Holon Research Tower rises through a dark forest canopy while energy rings sweep outward. A Delta silhouette emerges in the cloud layer as the logo resolves.

#### B. Delta Storm

A legendary subject is backlit by a magnetic storm. Clouds and energy move at different speeds, with brief palette flashes revealing details.

#### C. Mirage Forest Discovery

The screen begins almost black. Firefly-like energy traces reveal ancient stonework, crystalline growth, and finally the main subject behind the logo.

#### D. Dual World

The composition contrasts natural Holon with the technological broadcast network. The divide is animated through scanning bands or a palette transition rather than a hard split.

### 6.3 Recommended animation structure

A practical title sequence can have three phases:

1. **Reveal, 2–4 seconds**
   - Fade from black
   - Establish atmospheric layer
   - Introduce energy or silhouette
   - Resolve the logo and subtitle

2. **Impact, 0.5–1.5 seconds**
   - Legendary movement, lightning flash, signal pulse, or camera-like shake
   - Logo shine synchronized to a musical accent

3. **Ambient loop**
   - Slow cloud or fog movement
   - Palette cycling in crystals or energy
   - Sparse particles
   - Stable readability for `PRESS START`

### 6.4 Title-screen deliverables

- Approved composition mockup
- Layer separation plan
- Native-resolution master
- Indexed source layers
- Tile sheets and tilemaps
- Animation timing chart
- Updated title-screen code
- Successful ROM build
- Native-resolution capture for review

For exact replacement and conversion steps, use [Customizing the Emerald Title Screen](title-screen-customization-tutorial.md).

---

## 7. Intro Sequences and Cutscenes

Cutscenes can range from economical illustrated stills to fully animated sprite sequences. The most effective GBA approach often combines detailed still art with restrained motion.

### 7.1 Supported cutscene formats

#### Illustrated still sequence

- One or more 240×160 compositions
- Fades or cuts between images
- Dialogue or narration overlays
- Strong for history, dreams, legends, and distant events

#### Layered limited animation

- Separate subject, background, and atmosphere
- Blinks, mouth changes, cloth or hair motion
- Rain, dust, spores, sparks, fog, or energy
- Camera pans and subtle affine zoom
- Strong for emotional close-ups and important reveals

#### Comic-panel presentation

- Multiple panels introduced in sequence
- Masked reveals and dramatic typography
- Efficient when several story beats must fit in limited memory

#### Overworld cinematic

- Existing map and object-event sprites
- Custom character poses where necessary
- Camera movement, screen effects, and scripted timing
- Strong for events the player should understand spatially

#### Battle-engine cinematic

- Battlers, battle backgrounds, particles, and battle-animation commands
- Strong for transformations, awakenings, captures, and boss phase changes

### 7.2 Cutscene production package

Each cutscene should have:

- Narrative objective
- Beat-by-beat storyboard
- Shot list and approximate duration
- Dialogue or narration lock
- Asset list per shot
- Transition and effect list
- Audio or music cues
- Skip and replay behavior, if applicable
- Memory/load strategy
- Event-script integration plan

### 7.3 Animation economy

High perceived motion does not require many frames. A still can feel alive through:

- Two-frame eye or light animation
- Independent fog scroll
- Palette shimmer
- One-pixel breathing motion
- Slow pan across a larger image
- Foreground particles moving faster than the background
- Brightness flashes that briefly reveal hidden detail
- Sound cues synchronized to a small visual change

### 7.4 Candidate Holon cutscenes

- The original expedition entering Mirage Forest
- The first Research Tower signal activation
- The Delta incident spreading across the region
- A first-person glimpse of Mew through distorted energy
- The player approaching the tower during a storm
- A legendary Delta awakening
- The postgame voyage beyond the horizon

These should be checked against the canonical lore guide before story details are locked.

---

## 8. Battle Backgrounds and Transitions

Battle environments are a high-impact way to make Holon feel distinct because players see them repeatedly and immediately associate them with location and story state.

### 8.1 Existing structure

Current environments live under `graphics/battle_environment/` and commonly include:

- `tiles.png`
- `map.bin`
- `palette.pal`
- Optional `anim_tiles.png`
- Optional `anim_map.bin`
- Environment-specific palette variants

Loading and scene behavior are centered around `src/battle_bg.c` and battle-environment data tables.

### 8.2 Background categories

#### Regional biome backgrounds

- Mirage Forest
- Holon settlement outskirts
- Lake wilds
- Crystal caves
- Research facilities
- Dragon Frontiers
- Delta Horizon coast or jungle

#### Landmark backgrounds

- Research Tower interior
- Tower rooftop or transmitter deck
- Ancient stone circle
- Crystal Guardian chamber
- Delta Preserve arena
- Delta Colosseum

#### Story-state variants

- Normal
- Signal-active
- Storm or crisis
- Postgame recovery
- Night and day
- Corrupted or stabilized Delta energy

#### Boss arenas

- Custom platform silhouettes
- Multi-phase palettes
- Animated environmental hazards
- Background transformations synchronized to HP or form changes

### 8.3 Animation opportunities

- Moving water or reflections
- Wind through grass or canopy
- Pulsing tower lights
- Scrolling data or signal bands
- Crystal refraction through palette cycling
- Lightning illumination
- Machinery indicators
- Drifting ash, snow, spores, or dust
- Slow cloud parallax

### 8.4 Composition rules

Battle backgrounds must support gameplay first:

- Keep player and opponent silhouettes readable.
- Avoid high-contrast detail directly behind battlers.
- Preserve the visual ground plane.
- Test both large and small Pokémon.
- Leave the message and action UI legible.
- Ensure animated elements do not compete with attack effects.

### 8.5 Battle-background deliverables

- Native battle mockup with representative battlers and UI
- Indexed tile source
- Tilemap and palette
- Animated-tile sheet and timing, if used
- Environment-selection rule
- Day/night or story variants, if required
- Battle test against multiple sprite sizes

---

## 9. Delta Species and Custom Pokémon

Custom Pokémon production is one of the most valuable uses of this workflow. Delta forms benefit from an existing identity anchor; fully custom species provide greater freedom but require a stronger design-development phase.

### 9.1 Delta Species design goals

A successful Delta should be recognizable as its base species at a glance while visibly communicating that something fundamental has changed.

Preserve at least several identity anchors:

- Core silhouette
- Face and eye placement
- Limb count and body plan
- Signature feature such as ears, tail, wings, shell, or crest
- Characteristic posture or expression

Transform features that communicate the new adaptation:

- Material: organic, metal, crystal, bark, fungus, stone, plasma
- Surface pattern
- Secondary structures such as fins, vents, plates, or growths
- Energy color and effect language
- Posture or weight distribution
- Environmental wear or symbiosis

### 9.2 Degrees of Delta transformation

#### Palette Delta

The silhouette and pixel structure remain unchanged; only normal and shiny palettes change. This is fast and useful for placeholders, but has the weakest visual differentiation.

#### Marking Delta

The original sprite is edited with new markings, highlights, eyes, or small structural changes. This preserves animation efficiently.

#### Structural Delta

The species receives a redesigned front and back sprite while retaining recognizable anatomy. This is the recommended standard for important Delta encounters.

#### Radical Delta

The adaptation substantially changes anatomy or material language. This requires the same design rigor as a custom species and should have strong lore justification.

### 9.3 Fully custom Pokémon design goals

A custom species should begin with a design brief, not a sprite box. Define:

- Biological or mythological basis
- Gameplay role
- Type combination
- Habitat and behavior
- Personality
- Scale
- Evolution relationship
- Signature visual feature
- Signature move or ability, if relevant
- Connection to Holon's ecosystem or story

The design should be judged in silhouette before surface detail is finalized.

### 9.4 Complete Pokémon asset package

The exact files vary by species and project configuration, so a neighboring species should always be inspected. A typical complete package includes:

| Asset | Typical source | Typical role |
|---|---|---|
| Animated front sprite | `anim_front.png` | Front battle display and idle frames |
| Static front sprite | `front.png`, where used | Forms or configurations without a frame sheet |
| Back sprite | `back.png` | Player-side battle display |
| Normal palette | `normal.pal` | Standard battle colors |
| Shiny palette | `shiny.pal` | Shiny battle colors |
| Party icon | `icon.png` | Party, storage, and menus |
| Overworld sprite | `overworld.png` | Followers or scripted map appearances |
| Overworld palettes | `overworld_normal.pal`, `overworld_shiny.pal` | Follower palette variants |
| Footprint | `footprint.png` | Pokédex presentation |
| Optional variants | Female, form, Mega, G-Max, or story-state subfolders | Alternate appearances |

For the current Sableye package, representative dimensions are:

- `anim_front.png`: **64×128**, two 64×64 frames
- `back.png`: **64×64**
- `icon.png`: **32×64**, two 32×32 frames
- `overworld.png`: **192×32**, a row of 32×32 frames
- `footprint.png`: **16×16**

Do not assume these examples override the conventions of the target species or form. Inspect the exact neighboring implementation before creating files.

### 9.5 Front-sprite requirements

- Readable silhouette at 64×64
- Clear face and focal feature
- Grounding or flight height appropriate to the species
- Enough margin for animation without clipping
- Two frames that preserve anatomy and volume
- Motion that reinforces personality rather than merely shifting pixels

Good two-frame motions include breathing, a tail or ear reaction, wing settling, energy pulsing, or a subtle stance change.

### 9.6 Back-sprite requirements

The back sprite must be designed as a genuine rear three-quarter view. It should not be a mirrored or crudely rotated front sprite.

It must preserve:

- Head-to-body scale
- Limb count and joint structure
- Placement of markings
- Material and lighting logic
- Signature feature visibility
- Color-ramp use from the front sprite

The back view may exaggerate a recognizable feature because it occupies a large part of the player's battle view.

### 9.7 Icon requirements

The party icon should prioritize identity over anatomical completeness:

- Simplify aggressively.
- Keep the face or signature feature recognizable.
- Use clean animation between its two frames.
- Confirm palette-index requirements against the icon system.
- Test on party, summary, storage, and other menu backgrounds.

### 9.8 Overworld requirements

The overworld sprite should communicate the same species at 32×32 through:

- Silhouette
- Dominant colors
- Head/body proportion
- Signature appendage
- Consistent direction and foot placement

Follower and scripted-encounter use may require different animation expectations. Verify the intended runtime system before finalizing the sheet.

### 9.9 Shiny design rules

A strong shiny palette should:

- Preserve light-to-dark ordering
- Remain distinct from the normal palette
- Reinforce the species concept
- Avoid merging neighboring materials into one value
- Keep eyes and focal accents readable
- Avoid accidental resemblance to an unrelated form when that would confuse players

### 9.10 Gameplay integration package

For a new form or species, art may be accompanied by:

- Species constant or form entry
- Species name and category
- Typing
- Base stats
- Abilities
- Gender ratio and growth rate
- Catch rate and experience yield
- Height and weight
- Pokédex text
- Level-up, teachable, and egg learnsets
- Evolution or form-change logic
- Encounter or gift placement
- Cry assignment or custom audio plan
- Sprite scale, elevation, and animation metadata

Form tables already used by the expansion provide a natural foundation for Delta variants. The correct choice between a new form and a fully independent species should be made before data integration.

### 9.11 Recommended first sprite pilot

Start with one important Delta form and complete the entire package rather than producing many disconnected front sprites. The pilot should validate:

- The approved Delta design language
- Front/back consistency
- Palette and shiny conventions
- Icon and overworld simplification
- Folder and naming conventions
- Species/form integration
- Battle and menu positioning
- The review process for future roster work

The existing palette-swapping guide remains useful for placeholder Deltas. Structural Deltas and fully custom species require the fuller workflow defined here.

---

## 10. Trainers and Character Presentation

### 10.1 Supported trainer assets

- Battle front sprites
- Player back sprites
- Overworld walk cycles
- Running, cycling, surfing, fishing, and field-action variants
- VS portraits and splashes
- Cutscene close-ups
- Expression sets
- Uniform and story-state variants
- Silhouettes and holographic projections

### 10.2 Character design system

Important characters should have a small design sheet recording:

- Role and affiliation
- Silhouette
- Color hierarchy
- Signature accessory
- Age and physical bearing
- Research, wilderness, or combat function
- Relationship to Holon technology
- How the design changes across the story

### 10.3 Faction differentiation

Factions should be identifiable without relying on text. Differentiate them using:

- Silhouette and garment structure
- Material vocabulary
- Palette
- Emblems and equipment
- Animation posture
- Technology condition: pristine, improvised, ancient, damaged, or organic

### 10.4 Trainer production package

- Approved full-body concept
- Battle pose
- Indexed trainer sprite and palette
- Overworld sheet and palette
- Optional VS portrait
- Optional expression or cutscene art
- Trainer-class or character data integration
- Battle and map validation

---

## 11. Overworld Environments and Maps

### 11.1 Supported environment work

- Primary and secondary tilesets
- Animated water, lights, foliage, machinery, and crystals
- Environmental props
- Architecture kits
- Signs, emblems, and doors
- Map-specific foreground overlays
- Large vistas or panorama layers
- Weather and ambience
- Region-map art and location icons
- Story-state map transformations

### 11.2 Tileset development workflow

1. Define the biome and navigation needs.
2. Identify reusable terrain families.
3. Establish palette ownership.
4. Draw base tiles and transitions.
5. Build metatiles and collision behavior.
6. Add animated tiles sparingly.
7. Construct a test map that exercises every transition.
8. Review repetition, readability, and collision in-game.

### 11.3 Environmental storytelling

Holon maps can communicate history through repeated visual clues:

- Signal equipment overtaken by vegetation
- Crystals aligned with ancient foundations
- Wildlife paths around unstable energy zones
- Research structures built over older ruins
- Material changes as the player approaches a broadcast source
- Settlements that reuse expedition hardware differently

### 11.4 Story-state variants

Rather than building entirely new maps for every story beat, selected tiles, palettes, object events, and overlays can represent:

- Power restored or lost
- Signal active or dormant
- Flooding, fire, storm, or regrowth
- Crystal activation
- Faction occupation
- Postgame stabilization

---

## 12. Interface, Icons, and Collectible Art

### 12.1 Supported UI work

- Window frames and menu backgrounds
- Cursors and selectors
- Type, category, and status icons
- Pokédex page decoration
- Quest and chapter markers
- Key-item and inventory icons
- Badges, medals, facility symbols, and achievements
- Region maps and location cards
- Save-select artwork
- Chapter recap cards
- Custom title cards and interstitials

### 12.2 UI principles

- Readability outranks decoration.
- Reuse visual motifs instead of inventing a new style per screen.
- Test against the darkest and lightest expected backgrounds.
- Keep text contrast and selection states unmistakable.
- Treat color-blind accessibility as a reason to combine color with shape.
- Avoid spending palette colors on detail that disappears at native resolution.

### 12.3 Holon UI motif candidates

- Concentric signal rings
- Crystal facets
- Tower-grid geometry
- Ancient circle markings
- Field-research labels and specimen tags
- Split natural/technological borders
- Delta glyph accents

These motifs should be consolidated into an art bible before broad UI replacement begins.

---

## 13. Effects and Ambient Animation

Effects are small assets with disproportionate impact. They can unify otherwise separate screens under one visual identity.

### 13.1 Supported effects

- Delta energy particles
- Signal waves and scanning bands
- Crystal glints
- Fog, dust, ash, rain, spores, snow, and sparks
- Electrical arcs
- Holographic noise
- Impact flashes
- Transformation rings
- Environmental palette cycles
- Screen distortion and shake
- Masked reveals

### 13.2 Reusable Holon effect library

A long-term goal should be a shared effect vocabulary rather than one-off effects for every scene. Candidate families:

| Effect family | Visual language | Uses |
|---|---|---|
| Broadcast energy | Concentric rings, scanlines, narrow pulses | Tower scenes, Delta encounters, title screen |
| Stable Delta energy | Slow orbiting motes, controlled color cycle | Friendly Deltas, preserves, menus |
| Unstable Delta energy | Broken arcs, jitter, palette inversion | Crisis scenes, boss phases, corrupted zones |
| Crystal resonance | Faceted glints, refracted bands | Island, caves, guardians, items |
| Mirage phenomenon | Soft distortion, displaced silhouettes | Forest, Mew sightings, dreams |

### 13.3 Effect production package

- Effect purpose and trigger
- Sprite sheet or procedural plan
- Palette
- Timing curve
- Blend mode or layer requirements
- Lifetime and loop behavior
- Reuse rules
- Stress test with battle and UI palettes

---

## 14. Holon Visual Idea Bank

This section collects directions worth exploring. They are proposals until individually approved.

### 14.1 Title and intro ideas

- The Research Tower signal travels across a dark map of Holon, awakening Delta silhouettes in sequence.
- A quiet Mirage Forest view is disrupted by a single expanding pulse before the title appears.
- The title logo reflects in Holon Lake and distorts as energy passes beneath the surface.
- Ancient stone markings and modern tower geometry align for one moment during the title reveal.

### 14.2 Cutscene ideas

- Expedition photographs transition into living scenes.
- A tower monitor shows a signal pattern that matches ancient circle markings.
- The player's first Mew sighting uses foreground foliage, a one-frame glance, and lingering particles rather than a full reveal.
- The Delta incident is shown through several habitats instead of explained entirely through dialogue.
- A boss transformation temporarily drains color from the scene before rebuilding it in the Delta palette.

### 14.3 Battle-environment ideas

- Mirage Forest with subtly displaced background layers
- Tower laboratory with animated status lights and cable shadows
- Holon Lake with signal ripples traveling opposite the natural water motion
- Crystal chamber that changes palette as the battle progresses
- Dragon Frontier cliffs with high cloud parallax
- Delta Horizon Colosseum mixing natural rock with structures built by resident trainers

### 14.4 Delta design ideas

- Species adapted to broadcast energy through antenna-like growths
- Metal Deltas whose reflective areas visually echo tower construction
- Crystal Deltas that refract type-colored energy rather than simply becoming gem-covered
- Forest Deltas in symbiosis with spores, moss, or roots
- Lake Deltas with bioluminescent markings that resemble signal graphs
- Stable postgame Deltas with calmer poses and less fractured energy than crisis-era encounters

### 14.5 UI ideas

- Pokédex pages styled as evolving field-research records
- Delta entries that briefly scan or resolve when first opened
- Location cards using a small landscape silhouette and signal-strength motif
- Facility badges based on the four Delta Horizon activities

---

## 15. Recommended Production Roadmap

The roadmap prioritizes reusable systems and complete vertical slices over isolated assets.

### Phase 0 — Visual foundation

**Goal:** establish a common language before scaling production.

Deliverables:

- Holon palette families
- Material and effect vocabulary
- Delta transformation rules
- Outline and shading conventions
- UI motif selection
- Reference-resolution rules
- Folder and versioning conventions

Exit condition: new assets can be reviewed against a written standard rather than taste alone.

### Phase 1 — Title-screen vertical slice

**Goal:** finish one polished, integrated presentation feature.

Deliverables:

- Final composition
- New title artwork and layer assets
- Reveal sequence and ambient loop
- Subtitle integration
- Audio timing
- Build and emulator verification

Why first: it tests composition, pixel conversion, palettes, layering, animation code, and review at a manageable scope.

### Phase 2 — Signature Delta family

**Goal:** establish the complete Pokémon-production standard.

Deliverables:

- Family concept sheet
- Front, back, icon, overworld, normal, shiny, and footprint assets
- Species/form data
- Battle and menu integration
- A documented template for the rest of the Delta roster

Why second: it exposes the consistency challenges that will shape all future custom Pokémon work.

### Phase 3 — Signature battle environment

**Goal:** establish the Holon battle-background pipeline.

Deliverables:

- One important location background
- Animated environmental tiles
- Appropriate selection logic
- Story or time variant if useful
- Validation with several battler sizes

Why third: it creates a reusable standard before many regional environments are commissioned.

### Phase 4 — Cutscene toolkit

**Goal:** create reusable scene-loading, transition, and effect patterns.

Deliverables:

- One short story cutscene
- Still-image and layer-loading convention
- Pan, fade, flash, and particle helpers
- Storyboard and timing template
- Skip behavior

### Phase 5 — Character and UI identity

**Goal:** extend the established art direction across frequently seen screens.

Deliverables:

- Main-character and faction presentation pass
- VS or portrait standard
- Shared UI motif library
- Location-card or chapter-card system

### Phase 6 — Scaled asset production

**Goal:** produce the roster and environment backlog consistently.

Workstreams:

- Delta families
- Custom species
- Battle environments
- Map and tileset polish
- Cutscene chapters
- UI and collectible artwork
- Reusable effects

Scaling begins only after the pilot assets have resolved file formats, review standards, and visual identity.

---

## 16. Repository Integration Map

| Feature | Primary asset location | Primary code/data location | Existing guide or template |
|---|---|---|---|
| Emerald title screen | `graphics/title_screen/` | `src/title_screen.c`, `src/graphics.c` | [Title-screen tutorial](title-screen-customization-tutorial.md) |
| FRLG title screen | `graphics/title_screen_frlg/` | `src/title_screen_frlg.c` | Inspect separately; Emerald assumptions do not automatically apply |
| Pokémon sprites | `graphics/pokemon/<species>/` | `src/data/pokemon/species_info/` and graphics tables | Use a neighboring species/form |
| Delta placeholder palettes | Species graphics folders | Species/form data | [Sprite palette guide](sprite-palette-guide.md) |
| Battle environments | `graphics/battle_environment/` | `src/battle_bg.c`, `src/data/battle_environment.h` | Use a neighboring environment |
| Trainer battle sprites | `graphics/trainers/` | `src/data/graphics/trainers.h` and trainer data | Use a neighboring trainer class |
| Tilesets | `data/tilesets/` | Tileset data and animation code | Use the target primary/secondary set |
| Overworld effects | Relevant graphics folders | Field-effect and object-event systems | Inspect the target effect system |
| Intro/cutscene graphics | Feature-specific graphics folder | Intro/event/task implementation | Select the runtime approach per scene |
| UI graphics | Feature-specific `graphics/` folder | Screen implementation and graphics tables | Use the target screen's existing assets |

This map identifies starting points, not universal contracts. The consuming code remains the authority for exact dimensions, palette mode, and file layout.

---

## 17. Reusable Creative Briefs

These templates are designed to be copied into a task or chat and completed with project-specific information.

### 17.1 General visual-asset brief

```text
Asset type:
Production level: Exploration / Approved concept / Prototype / ROM-ready / Integrated
Screen or gameplay use:
Primary request:
Narrative purpose:
Required subject or elements:
Reference images and their roles:
Style and era:
Composition or pose:
Palette and mood:
Exact text, if any:
Animation or effects:
Technical target:
Must preserve:
Must avoid:
Destination in the project:
```

### 17.2 Title-screen brief

```text
Create a Project Holon title-screen direction.

Production level:
Primary subject:
Approved logo/subtitle assets:
Narrative idea:
Mood:
Reveal duration:
Ambient loop behavior:
Required layers:
Music or sound cues:
Must preserve:
Must avoid:
```

### 17.3 Delta Species brief

```text
Create a Delta form for:

Base species:
Delta typing:
Degree: Palette / Marking / Structural / Radical
Cause or habitat:
Behavioral change:
Identity anchors to preserve:
Features to transform:
Material language:
Normal palette direction:
Shiny palette direction:
Signature move or ability idea:
Required package: front / back / icon / overworld / footprint / data
Production level:
Must avoid:
```

### 17.4 Fully custom Pokémon brief

```text
Create a fully custom Pokémon for Project Holon.

Evolution stage:
Type:
Biological, mythological, or object basis:
Habitat:
Behavior and personality:
Gameplay role:
Approximate scale:
Signature silhouette feature:
Evolution relationship:
Connection to Holon:
Normal palette:
Shiny concept:
Required package:
Production level:
Must avoid:
```

### 17.5 Cutscene brief

```text
Create a Project Holon cutscene.

Story placement:
Narrative objective:
Characters or subjects:
Location:
Required story beats:
Dialogue or narration:
Format: stills / layered animation / panels / overworld / battle-engine
Approximate duration:
Music and sound cues:
Required effects:
Skip/replay behavior:
Canon references:
Must preserve:
Must avoid:
```

### 17.6 Battle-background brief

```text
Create a Project Holon battle environment.

Location:
Battle types that use it:
Time or story state:
Ground plane:
Far background:
Animated elements:
Palette and mood:
Representative battlers for testing:
Environment-selection rule:
Required variants:
Must preserve:
Must avoid:
```

### 17.7 Edit request with invariants

```text
Edit target:
Change only:
Keep unchanged:
Reason for the edit:
Technical constraints:
Output version name:
```

For edits, list every invariant that matters. “Keep everything else unchanged” is useful but should not replace explicit identity, composition, palette, and dimension constraints.

---

## 18. Review and Definition of Done

### 18.1 Concept review

- [ ] The asset has a clear narrative or gameplay purpose.
- [ ] Its silhouette or composition reads immediately.
- [ ] Required canon details are present.
- [ ] New interpretation is labeled and approved.
- [ ] The design is meaningfully distinct from rejected alternatives.
- [ ] The selected direction has recorded invariants.

### 18.2 Pixel-art review

- [ ] Canvas and sheet dimensions are correct.
- [ ] Pixel clusters are deliberate.
- [ ] There is no accidental anti-aliasing.
- [ ] Outline treatment is consistent.
- [ ] Values remain readable at native resolution.
- [ ] Transparent areas are clean.
- [ ] Multiple views and frames preserve anatomy and materials.

### 18.3 Palette review

- [ ] The image is genuinely indexed where required.
- [ ] Palette count is within budget.
- [ ] Index 0 behavior is correct.
- [ ] Normal and shiny value structures are coherent.
- [ ] Colors survive GBA conversion.
- [ ] Shared palette ownership is respected.

### 18.4 Animation review

- [ ] Motion supports character or atmosphere.
- [ ] Frame anchors are stable.
- [ ] No anatomy changes accidentally between frames.
- [ ] Loop seams are invisible or intentional.
- [ ] Timing works at the game's frame rate.
- [ ] Effects do not obscure UI or gameplay information.
- [ ] The scene has a stable resting state where needed.

### 18.5 Integration review

- [ ] Source assets are stored in the repository.
- [ ] Generated binaries are produced by the normal toolchain.
- [ ] The project builds successfully.
- [ ] The correct runtime system loads the asset.
- [ ] Position, scale, and layer priority are correct.
- [ ] Adjacent screens, forms, or environments are unaffected.
- [ ] The result has been inspected in-game at native scale.
- [ ] Important implementation decisions are documented.

### 18.6 Complete Pokémon review

- [ ] Front sprite
- [ ] Front animation
- [ ] Back sprite
- [ ] Normal palette
- [ ] Shiny palette
- [ ] Party icon and animation
- [ ] Overworld sprite and palettes, if required
- [ ] Footprint, if required
- [ ] Species/form data
- [ ] Battle position and elevation
- [ ] Summary, party, storage, Pokédex, and battle checks
- [ ] Encounter, gift, evolution, or form-change route

---

## 19. Limitations and Risk Management

### 19.1 Generated pixel art is not automatically production pixel art

Image generation can provide excellent composition, texture, atmosphere, and design exploration. It may also introduce:

- Too many colors
- Soft or semi-transparent edges
- Noisy single pixels
- Inconsistent outlines
- Details too small for the final canvas
- Anatomy changes between views or frames
- Fake sprite-sheet spacing
- Incorrect text

The remedy is a deliberate native-resolution and technical-art pass, followed by in-game validation.

### 19.2 Multi-view consistency is a separate task

A strong front sprite does not guarantee a correct back sprite, icon, or overworld version. Each view should inherit a written design contract and be reviewed against the others.

### 19.3 Animation consistency requires controlled iteration

Generating many frames independently often causes drift. Prefer:

- One approved key frame
- One targeted motion at a time
- Explicit invariants
- Minimal frame count
- Engine transforms and particles for secondary motion

### 19.4 GBA constraints can change the design

Palette, tile, sprite, and memory restrictions are not merely export concerns. They can require changes to composition and detail. Technical inspection should happen before a design is treated as final.

### 19.5 Canon and provenance require conscious decisions

Project Holon draws from established Pokémon and TCG material while adding original interpretation. For every major asset:

- Identify which details come from canonical references.
- Identify which details are original Project Holon proposals.
- Avoid tracing or copying an unrelated artist's work without authorization.
- Track references used for identity, pose, composition, or style.
- Prefer original compositions and project-specific visual language.

### 19.6 Large batches should follow successful pilots

Producing a large sprite or background batch before standards are settled multiplies inconsistency and rework. Complete one representative asset package, document what worked, and then scale.

---

## 20. Working Agreements

### 20.1 What to provide when requesting art

The minimum useful request identifies:

- What the asset is
- Where it will appear
- Whether it is exploratory or intended for the ROM
- What must remain recognizable
- Any required lore, text, type, or palette

References are helpful but not mandatory. When supplied, label each reference as one of:

- **Edit target** — the image whose pixels or content should change
- **Identity reference** — establishes the subject's required appearance
- **Style reference** — establishes rendering language
- **Composition reference** — establishes framing or layout
- **Supporting insert** — material to be composited into the result

### 20.2 What Codex should report

For project-bound assets, the handoff should report:

- Final saved paths
- Production level reached
- The final brief or generation prompt
- Which elements were generated, hand-cleaned, converted, or coded
- Build and test results
- Remaining decisions or known limitations

### 20.3 Iteration rule

After a direction is approved, each revision should target one clear change when possible. Examples:

- Increase silhouette separation around the tail.
- Reduce background contrast behind the opponent battler.
- Change only the crystal glow from green to cyan.
- Slow the cloud layer while preserving all other title timing.

Single-purpose revisions reduce drift and make approval history understandable.

### 20.4 File-handling rule

- Preview-only concepts may remain outside the game asset tree.
- Any asset referenced by the project must be copied into the workspace.
- Approved files should not be silently overwritten by new variants.
- Existing source assets should be preserved unless replacement is explicitly requested.

---

## 21. Immediate Next Projects

The following sequence offers the highest learning and visual return.

### 21.1 Project One — Final title-screen package

**Target:** integrated and verified.

Decisions needed:

- Primary subject
- Chosen composition direction
- Relationship between nature, tower technology, and Delta energy
- Reveal duration and ambient loop
- Whether the existing Pokémon logo remains unchanged

Expected result: a polished title sequence that establishes the game's visual identity within seconds.

### 21.2 Project Two — Signature Delta pilot

**Target:** one complete form or family.

Decisions needed:

- Base species
- Delta typing
- Degree of transformation
- Habitat or cause
- Whether it is encountered during the main story, postgame, or both

Expected result: front, back, icon, overworld, footprint, normal/shiny palettes, data integration, and a reusable roster standard.

### 21.3 Project Three — Research Tower battle environment

**Target:** one landmark background with restrained animation.

Decisions needed:

- Tower room or exterior location
- Signal-active and inactive states
- Main material palette
- Animated machinery or energy element

Expected result: a battle backdrop unmistakably specific to Project Holon.

### 21.4 Project Four — Short Delta incident cutscene

**Target:** a 10–20 second integrated cinematic.

Decisions needed:

- Exact story beat
- Viewpoint character
- Dialogue or narration
- Illustrated-still or layered-animation approach

Expected result: a reusable cutscene pipeline for later story chapters.

### 21.5 Project Five — Holon art bible

**Target:** a concise, stable reference derived from the completed pilot assets.

Contents:

- Approved palette families
- Pixel-art conventions
- Delta material and effect language
- Faction motifs
- Environment keys
- UI motifs
- Examples of approved and rejected approaches

Expected result: a reference that allows future assets to remain coherent even when created months apart.

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| 1.0 | 2026-08-31 | Initial complete guide covering visual capabilities, production levels, technical standards, title screens, cutscenes, battle backgrounds, Delta and custom Pokémon, environments, UI, effects, roadmap, reusable briefs, and review criteria. |

---

*Pokémon Holon Legends — Visual Asset and Animation Production Guide | HL-ART-002 v1.0 | Last updated 2026-08-31*
