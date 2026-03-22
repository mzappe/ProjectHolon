# Pokemon Holon Legends
![59c53455-5679-4271-b1e0-aa6476b7e839](https://github.com/user-attachments/assets/cad60817-44ca-41f3-a7bc-1c8789deb525)

A Pokemon ROM hack set in the **Holon region** from the TCG Delta Species arc, built on [RHH's `pokeemerald-expansion`](https://github.com/rh-hideout/pokeemerald-expansion).

An ancient meteorite lies buried beneath the Holon Research Tower. For years, the Tower broadcast electromagnetic energy to track Mew sightings in Mirage Forest — unknowingly transforming the surrounding Pokemon into **Delta Species**, creatures carrying elemental types their species was never meant to have. Then something went wrong: the broadcast reached what was buried below, and a contained local phenomenon became a spreading ecological crisis. The player travels outward from Mirage Forest through five locations mirroring the five TCG sets of the Delta Species arc, piecing together what happened and how to stop it before the region's ecosystems collapse.

## Features

### The Holon Region
- **Three geographic zones** — the forested Mainland, the island Archipelago, and the endgame Dragon Frontiers
- **Five canonical TCG locations** — Mirage Forest (EX Legend Maker), Holon Village (EX Delta Species), Holon Lake (EX Holon Phantoms), the Unnamed Island (EX Crystal Guardians), and Dragon Frontiers (EX Dragon Frontiers)
- Connective towns, routes, and landmarks that make the region feel inhabited beyond its story anchors
- 8 Gyms + Pokemon League
- Gen 3 design philosophy — no quest markers, no mission menus, world-driven exploration

### Delta Species
- Pokemon transformed by electromagnetic radiation from the Holon Research Tower
- Non-standard elemental types, custom sprites and palettes
- Delta mutations spread outward from the Tower, growing more severe the closer you get
- Delta starter Pokemon

### Story
- A scientific accident, an ancient mystery, and a dormant extraterrestrial organism beneath the Tower
- Deoxys — fractured into four Delta formes, each locked into a single behavioral extreme
- Rayquaza — unable to identify what the fractured Delta Deoxys have become, responding with territorial aggression
- Steven Stone investigating the Holon Ruins and the ancient civilization that once protected the crash site
- A faction that appears to be part of the research effort but isn't what it seems

### Powered by pokeemerald-expansion
- Modern battle engine with Mega Evolution, Z-Moves, Dynamax, and Terastallization (configurable)
- Physical/Special split, Fairy type, all items/abilities/moves through Gen IX
- Improved AI, Level/EV caps, Sleep Clause, Type Indicators
- Quality-of-life: indoor running, follower Pokemon, day/night cycle, DexNav, HGSS-style Pokedex
- Full feature list in [`FEATURES.md`](FEATURES.md)

## Getting Started

### Prerequisites
- devkitARM (ARM GCC cross-compiler)
- libpng, pkg-config
- Python 3

Platform-specific setup instructions are in [`INSTALL.md`](INSTALL.md).

### Building

```bash
# Clone the repository (do not use GitHub's "Download Zip")
git clone https://github.com/mzappe/ProjectHolon.git
cd ProjectHolon

# Build the ROM
make -j$(nproc)
```

The output ROM will be `pokeemerald.gba`.

## Documentation

- [`FEATURES.md`](FEATURES.md) — Full pokeemerald-expansion feature list
- [`INSTALL.md`](INSTALL.md) — Platform-specific installation guides (Windows WSL, Linux, macOS, ChromeOS)
- [`GDDs/`](GDDs/) — Game design documents including story bible, gameplay guide, and technical reference

## Credits

This project is built on **[RHH's pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion)**, which is itself built on **[pret's pokeemerald](https://github.com/pret/pokeemerald)** decompilation.

```
Based on RHH's pokeemerald-expansion https://github.com/rh-hideout/pokeemerald-expansion/
```

Full contributor list for pokeemerald-expansion can be found in [`CREDITS.md`](CREDITS.md).

## Community

[![](https://dcbadge.limes.pink/api/server/6CzjAG6GZk)](https://discord.gg/6CzjAG6GZk)

Join the [ROM Hacking Hideout (RHH) Discord](https://discord.gg/6CzjAG6GZk) for pokeemerald-expansion support and discussion.

## Status

This project is in active development. Pokemon Holon Legends is not yet playable.
