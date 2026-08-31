# Pokemon Holon Legends

A Pokemon ROM hack set in the **Holon region** from the TCG Delta Species arc, built on [RHH's `pokeemerald-expansion`](https://github.com/rh-hideout/pokeemerald-expansion).

Deep in a lost primeval forest stands the **Holon Research Tower**, a spire the size of a mountain built to broadcast for Mew. It found something. It also started rewriting the wildlife around it, turning ordinary Pokemon into **Delta Species** that carry elemental types their kind was never born with. Now the change is spreading, and nobody who built the Tower will say why. You arrive as a fresh recruit with orders to catalog it, and follow the mutation outward across five regions, each one stranger than the last, until you learn what the Tower really woke up.

## Features

### The Holon Region

Five zones, each based on one set of the Delta Species arc, explored in story order as you work your way out from the epicenter.

- **Mirage Forest.** A dense, mist-drowned jungle of Jurassic-scale trees and hidden clearings. Fossil Pokemon roam it freely, Mew is rumored in it, and the healing power spot the whole region was founded on sits at its heart.
- **Holon Village and the Research Tower.** A research settlement laid out like a giant Poke Ball and ringed with farms, with the Tower firing tracking waves into a sky that never stops crackling.
- **Holon Lake.** A still highland lake with ancient stone domes half sunk in the shallows and a sprawl of active machinery running in the dark water underneath.
- **Crystal Isles.** A storm-battered volcanic archipelago where glowing crystals push up through the rock, the sand, and the reefs, taking their color from whatever ground they break through.
- **Dragon Frontiers.** Red sandstone cliffs at the edge of the map, with a second island floating above the clouds where the daytime sky fades to open starfield.

There are 8 gym leaders and a regional Champion, an Unbound-style quest system built into open world exploration, and a roster of Gen 1 through 3 species. Your starter is one of three rare Delta specimens: **Delta Dratini (Grass)**, **Delta Ralts (Fire)**, or **Delta Bagon (Water)**.

### Engine and configuration

Built on [RHH's `pokeemerald-expansion`](https://github.com/rh-hideout/pokeemerald-expansion). Configured so far:

- **Gen 6 mechanics baseline.** `GEN_LATEST` is set to `GEN_6`, covering learnsets, base stats, abilities, move data, and catch rates.
- **HGSS-style Pokedex** with dark mode and decapped names.
- **Follower Pokemon** enabled.
- **Reusable TMs.**
- **Shiny rate** doubled, from 1/8192 to 1/4096.

Full upstream feature list in [`FEATURES.md`](FEATURES.md).

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

- [`FEATURES.md`](FEATURES.md): full pokeemerald-expansion feature list
- [`INSTALL.md`](INSTALL.md): platform-specific installation guides (Windows WSL, Linux, macOS, ChromeOS)
- [`GDDs/`](GDDs/): game design documents (story bible, region and encounter tables, Pokedex build, engine configs, build log)

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
