# Holon tileset research catalog

## Follow-up: GBC-style sets already in Emerald format (2026-09-22)

The strongest new donor candidate found is [jschoeny/TARC2](https://github.com/jschoeny/TARC2), an Emerald-expansion project. Its [hack credits](https://github.com/jschoeny/TARC2/blob/main/HACK_CREDITS.md) name Morlock-Liam for Gen 2 Kanto assets. Direct file-tree inspection verified these three related sets:

| Set | Verified supplied files | Assessment |
| --- | --- | --- |
| [olden_times primary](https://github.com/jschoeny/TARC2/tree/main/data/tilesets/primary/olden_times) | tiles.png, palettes, metatiles.bin, metatile_attributes.bin, bottom/middle/top PNGs, palette primers | GBC-inspired outdoor donor; includes more detailed terrain alongside retro vegetation, so it is a hybrid rather than strict Crystal graphics. |
| [olden_times_town secondary](https://github.com/jschoeny/TARC2/tree/main/data/tilesets/secondary/olden_times_town) | tiles.png, palettes, metatiles.bin, attributes and bottom/middle/top PNGs | Small town/building supplement, not a complete regional architecture library. |
| [olden_times_mountain secondary](https://github.com/jschoeny/TARC2/tree/main/data/tilesets/secondary/olden_times_mountain) | tiles.png, palettes, metatiles.bin, attributes, bottom/middle/top PNGs and overcast animation frames | Mountain supplement with atmospheric animation assets. |

Visually inspected each set's middle.png. These are materially closer to an Emerald import than a raw commercial tilesheet. Layer source images are present, but a working Porytiles invocation/configuration was not verified, and no Holon compilation or import was performed. Graphics-specific reuse permission remains unverified; the credits establish provenance, not blanket permission.

No standalone, explicitly reusable, fully verified GBC-style Porytiles pack was located in this follow-up. Seaglass's creator confirms Emerald-expansion/Porymap usage in a [development post](https://www.reddit.com/r/PokemonROMhacks/comments/1e798we/), but that does not establish a public reusable asset release. Heart & Soul and CrystalDust should be treated as Johto/GBA directions, not automatically classified as GBC-style tileset packs. Zaebucca's packs and pokecrystal/pokezelda source graphics still require conversion.

Research date: 2026-09-21. Brief: nostalgic Pokémon environments that feel distinct from ordinary Gen 3, with a viable path to Hoenn as postgame.

This is a broad, source-checked catalog, not a claim to list every tileset ever posted online. It covers every **32-entry Full Tilesets directory** in the inspected Great Tileset Exchange snapshot, plus public artist libraries, decomp projects, specialist packs, paid alternatives, and further discovery sources. Variants and paired primaries/secondaries are counted separately in that directory; they are not 32 independent art styles.

**Recommendation:** retain LeoB ORAS as the leading shared foundation. Compare it against Ekat-based Gen 3 environments and Heart & Soul’s Johto direction. Build Holon’s identity with selected forest, ruins, reef, laboratory and industrial additions. Zaebucca is the strongest substantially different retro direction to audition, but would call for a broader visual overhaul.

Holon suitability and relative effort below are editorial judgments. Technical dependencies and permission descriptions come from the linked sources. No candidate has been imported or tested in Holon during this research. A public repository alone does not establish permission to reuse every contributed graphic.

## Start with these candidates

| Candidate | Why it deserves a comparison | Likely role | Relative work |
| --- | --- | --- | --- |
| LeoB ORAS | Shared visual foundation with Hoenn-oriented coverage | Primary + town secondaries | Lower than a new style; still requires integration |
| Ekat’s public Gen 3 library | Broad environmental variety while retaining Pokémon familiarity | Sources for multiple primary/secondary sets | Medium; raw sheets need assembly |
| Shady Forest + Autumn Ruins | Strong match for Mirage Forest and ancient sites | Specialized secondaries | Medium; layer/dependency conversion |
| Small town with lab | Research settlement and rail-related pieces | Town secondary | Medium; greenery dependency |
| Underwater + Underwater Reef | Much more varied submerged environments | Underwater primary and secondaries | Medium |
| Sewer variants | Pipes and industrial structures for Holon infrastructure | Facility secondaries / prop sources | Medium |
| Heart & Soul | Johto nostalgia with a GBA implementation to study | Alternative foundation / regional donors | Medium–high; extract selected data and track credits |
| J-Treecko252 | Strong Gen 3 supplemental tile source | Paths, rocks, buildings, details | Medium |
| Magiscarf | An alternative broader art direction | Foundation artwork / selective props | Higher; style and palette adaptation |
| Roger Wrightshoe | Safari, dripstone cave, XY-inspired terrain and greenery | Wilderness supplements | Medium–high; raw sheets |
| Sacred Phoenix / Alienor | Woodland, ruins and rustic environment vocabulary | Selective forest / ruins donors | Higher; mixed permissions and format |
| Zaebucca Adventure Begins | A deliberate GBC-like visual identity | Alternative whole-game direction | High; new integration and sprite cohesion |

Source and reuse details for each are in the tables below.

## A. All 32 packaged Great Tileset Exchange entries

The repository describes Exchange material as intended for easy Emerald insertion, but says most sets assume triple-layer metatiles. This is **not** a promise of immediate compatibility with Holon or LeoB’s primary. Its separate Other Tilesets directory may require indexing, palette changes, resizing and reformatting. [Tileset directory guidance](https://github.com/monhacks/teamaquas-assets/blob/main/Tilesets/README.md)

The asset repository allows use and editing by default, subject to asset-specific exceptions. Follow each pack’s README and credits.md, including port/assembly credits. [Repository reuse policy](https://github.com/monhacks/teamaquas-assets#readme)

Each name below opens the source folder, including its previews, files and credits. “Primary” and “secondary” in this table are the actual package designations.

| Pack / source | Format | Suggested Holon use | What makes it useful | Dependencies / credit notes |
| --- | --- | --- | --- | --- |
| [Alternative Pokecenter Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Alternative%20Pokecenter%20Secondary) | Secondary | Town services | Alternative Pokémon Center interiors; useful supporting set. | Credit Ekat, Vurtax, Heartlessdragoon, and Rahtak. |
| [Autumn Ruins Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Autumn%20Ruins%20Secondary) | Secondary | Holon Ruins / ancient sites | Weathered masonry, columns, vegetation and subdued terrain. Strong thematic fit. | Yumekua assembly, Rahtak port; preserve the full credits.md. |
| [Beach Cave Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Beach%20Cave%20Secondary) | Secondary | Coastal caves / island approaches | Coastal cave environment; good transition between the shore and underground areas. | Ekat and other credited artists; Rahtak port. |
| [Caves Alt Primary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Caves%20Alt%20Primary) | Primary | Large cave systems | Alternative cave foundation, paired with Caves Alt Secondary. | Explicitly requires expanded metatile limits. Reborn Victory Road source; preserve listed credits. |
| [Caves Alt Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Caves%20Alt%20Secondary) | Secondary | Large cave systems | Companion to Caves Alt Primary; evaluate the pair together. | Explicitly requires expanded metatile limits. Reborn Victory Road source; preserve listed credits. |
| [Desert Primary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Desert%20Primary) | Primary | Arid Dragon Frontiers terrain | A dedicated desert foundation instead of recoloring ordinary routes. | KingTapir, Ekat, TheDeadHeroAlistair, Skillmen; Rahtak port. |
| [Desert Pyramid Exterior Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Desert%20Pyramid%20Exterior%20Secondary) | Secondary | Ancient desert landmarks | Pyramid exteriors for an archaeological area; optional architectural direction. | KingTapir, Ekat, TheDeadHeroAlistair, Skillmen; Rahtak port. |
| [Desert Village Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Desert%20Village%20Secondary) | Secondary | Remote arid settlements | Desert settlement architecture to accompany the desert primary. | KingTapir, Ekat, TheDeadHeroAlistair, Skillmen; Rahtak port. |
| [Distortion World Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Distortion%20World%20Secondary) | Secondary | Floating island / anomalous areas | Floating rock platforms and unnatural terrain. Adapt the motifs and palette for Holon. | Phyromatical, spaceemotion; Rahtak port. Artwork does not provide gravity mechanics. |
| [Dojo Exterior Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Dojo%20Exterior%20Secondary) | Secondary | Traditional settlements | Traditional building exterior; useful if the region includes a mentor community. | TheDeadHeroAlistair building, Yumekua assembly, Rahtak port; full credits.md applies. |
| [Dojo Interior Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Dojo%20Interior%20Secondary) | Secondary | Training halls / ceremonial rooms | A specialized interior option for a dojo or sanctuary. | Rejuvenation-associated credits; preserve the full list and Rahtak port credit. |
| [Emerald Slide](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Emerald%20Slide) | Primary recolor | Glacial coast / snow routes | Winter variant of Emerald general; a conservative snow environment option. | Ryu winter theme, Archie project, Pawkkie edits. Includes instructions for copying general and replacing palettes. |
| [Gate Platinum Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Gate%20Platinum%20Secondary) | Secondary | Transit checkpoints | Platinum-style gate building environment, redrawn from gameplay references. | Credit blloop. Explicitly requires expanded and triple-layer metatiles. |
| [Gatehouse Secondary Alt](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Gatehouse%20Secondary%20Alt) | Secondary | Research checkpoints / route transitions | Alternative gatehouse interior. | Credit princess-phoenix and Rahtak. Explicitly requires expanded and triple-layer metatiles. |
| [Gatehouse Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Gatehouse%20Secondary) | Secondary | Research checkpoints / route transitions | General gatehouse interior. | Credit Ekat, Vurtax, Heartlessdragoon, Rahtak. Explicitly requires expanded and triple-layer metatiles. |
| [Gen 4 Cave Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Gen%204%20Cave%20Secondary) | Secondary | Mountain caves | Gen 4-style cave details; useful alternative to stock Emerald cave shapes. | Kyledove, Ghoulslash, Rahtak. Graphics for rock climbing do not implement the mechanic. |
| [Gen 4 Interior Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Gen%204%20Interior%20Secondary) | Secondary | Homes / general interiors | Gen 4-style indoor set sourced from Glazed. | Preserve credits.md, including Glazed contributors; this release does not authorize all Glazed assets. |
| [Legend of Zelda House Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Legend%20of%20Zelda%20House%20Secondary) | Secondary | Hermit cabins / rustic outposts | Zelda-inspired house architecture for an isolated settlement. | Hek-el-grande buildings, Yumekua assembly, Rahtak port; full credits.md applies. |
| [LeoB ORAS](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/LeoB%20ORAS) | Primary + regional secondaries | Shared Holon / Hoenn foundation | Our baseline: ORAS-inspired colors and updated outdoor/building artwork. | Credit leob0505 and listed inspirations. Include matching door animations; large-tree palette limitations affect Mauville / Battle Frontier. |
| [Lugia Movie Altar Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Lugia%20Movie%20Altar%20Secondary) | Secondary | Island shrine / legendary site | Movie-inspired altar pieces; good landmark vocabulary for coastal ruins. | jinxchan6306 movie assets, Yumekua assembly, Rahtak port; full credits.md applies. |
| [Pyramid Interior Primary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Pyramid%20Interior%20Primary) | Primary | Ancient temple interiors | Dedicated temple foundation for a separate ruins environment. | Princess-phoenix, Pokémon Rejuvenation team, Rahtak. |
| [Pyramid Interior Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Pyramid%20Interior%20Secondary) | Secondary; WIP | Ancient temple interiors | Companion temple details; the source explicitly labels this set WIP. | Princess-phoenix, Pokémon Rejuvenation team, Rahtak. Inspect completeness before mapping. |
| [Sewer (Clear water) Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Sewer%20%28Clear%20water%29%20Secondary) | Secondary | Waterworks / research infrastructure | Pipes, platforms and clear-water sewer variants; strong Holon infrastructure donor. | Magiscarf, Kyle Dove, Kane89, Aveontrainer, Rahtak. |
| [Sewer Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Sewer%20Secondary) | Secondary | Abandoned industrial infrastructure | Sewer platform, barrel and pipe vocabulary for utility areas. | Magiscarf, Kyle Dove, Kane89, Aveontrainer; credit Rahtak for the port. |
| [Shady Forest Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Shady%20Forest%20Secondary) | Secondary | Mirage Forest / abandoned outposts | Cool-toned trees, dead trunks, logs and overgrown buildings. Strong starting point for a mysterious forest. | Yumekua assembly, Rahtak port; preserve the full credits.md. |
| [Small town with lab Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Small%20town%20with%20lab%20Secondary) | Secondary | Research settlement / expedition base | Town and lab pieces plus parts of a train station; particularly relevant to Holon. | Uses Rahtak greenery grass; replace or supply that dependency. Includes Porytiles layer images. Preserve credits.md and Rahtak credit. |
| [Space Meteor Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Space%20Meteor%20Secondary) | Secondary | High-altitude / cosmic encounters | Space and meteor environment with sample star animations. | Includes Porytiles layer images. Credit Rahtak and all artists in credits.md. |
| [Underwater Primary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Underwater%20Primary) | Primary | Holon Lake depths / ocean floor | Dedicated underwater foundation. | Ekat, Vurtax, Heartlessdragoon; Rahtak port. |
| [Underwater Reef Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Underwater%20Reef%20Secondary) | Secondary | Crystal Island reefs | Coral, sea plants and layered underwater cliffs. One of the strongest regional additions. | Ekat, Vurtax, Heartlessdragoon; Rahtak port. |
| [Underwater Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Underwater%20Secondary) | Secondary | Lake depths / submerged areas | An alternative underwater detail set; compare with Reef for different underwater biomes. | Hek, Ekat, Vurtax, Heartlessdragoon; Rahtak port. |
| [Valencia Island](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Valencia%20Island) | FRLG-format set | Tropical island towns | Kalarie’s Orange Islands GBA tiles, included with permission. | Uses primary palette 7; explicitly NOT triple-layer. README links FRLG-to-Emerald adaptations and original credits. |
| [Volcano Secondary](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Volcano%20Secondary) | Secondary | Volcanic fringes / Dragon Frontiers | Lava, rocky platforms and shrine-like structures; strong biome addition. | Yumekua assembly, Rahtak port; preserve full credits.md. |

### Six source previews worth opening first

These are original source previews, not proposed Holon maps. Credit follows each linked pack’s README/credits.md: Shady Forest, Autumn Ruins and Volcano include Yumekua’s assembly and Rahtak’s port; Reef is credited to Ekat, Vurtax and Heartlessdragoon with Rahtak’s port; the lab set has its own eight-artist list plus port credit; Distortion World credits Phyromatical, spaceemotion and Rahtak.

**Shady Forest Secondary** — [source and full credits](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Shady%20Forest%20Secondary)

![Shady Forest Secondary source preview](https://raw.githubusercontent.com/monhacks/teamaquas-assets/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Shady%20Forest%20Secondary/example.png)

**Autumn Ruins Secondary** — [source and full credits](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Autumn%20Ruins%20Secondary)

![Autumn Ruins Secondary source preview](https://raw.githubusercontent.com/monhacks/teamaquas-assets/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Autumn%20Ruins%20Secondary/example.png)

**Underwater Reef Secondary** — [source and full credits](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Underwater%20Reef%20Secondary)

![Underwater Reef Secondary source preview](https://raw.githubusercontent.com/monhacks/teamaquas-assets/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Underwater%20Reef%20Secondary/example.png)

**Small town with lab Secondary** — [source and full credits](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Small%20town%20with%20lab%20Secondary)

![Small town with lab Secondary source preview](https://raw.githubusercontent.com/monhacks/teamaquas-assets/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Small%20town%20with%20lab%20Secondary/example.png)

**Volcano Secondary** — [source and full credits](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Volcano%20Secondary)

![Volcano Secondary source preview](https://raw.githubusercontent.com/monhacks/teamaquas-assets/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Volcano%20Secondary/example.png)

**Distortion World Secondary** — [source and full credits](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Distortion%20World%20Secondary)

![Distortion World Secondary source preview](https://raw.githubusercontent.com/monhacks/teamaquas-assets/main/Tilesets/The%20Great%20Tileset%20Exchange/Full%20Tilesets/Distortion%20World%20Secondary/example.png)

## B. Public art libraries and specialist sheets

These are artwork sources. A proposed primary/secondary role here is a recommendation, not a claim that the download already contains Emerald tiles, palettes, metatiles or attributes.

| Source | Coverage / suggested role | Reuse evidence and adaptation notes |
| --- | --- | --- |
| [Ekat’s Public Gen 3 Tilesets](https://eeveeexpo.com/resources/621/) | Broad Gen 3 environment library; foundation artwork and biome secondaries | Author lists 81 sets at 1× size and a per-set credits file. Public resource; preserve all relevant contributors. Build/index selected sheets for Emerald. **Top priority.** |
| [J-Treecko252 Gen 3 gallery](https://www.deviantart.com/j-treecko252/gallery/79196109/pokemon-gen-3-tiles) | Supplemental terrain, buildings and environment details | Verify each sheet; the individually checked releases below explicitly permit use/editing with credit. **Top priority.** |
| [J-Treecko252 Dark City Tiles 01](https://www.deviantart.com/j-treecko252/art/Dark-City-Tiles-01-898234017) | City buildings; candidate research-town architecture | Author explicitly allows use and edits with credit, including outside Essentials. |
| [J-Treecko252 Rock Tiles Ver.06](https://www.deviantart.com/j-treecko252/art/Rock-Tiles-Ver-06-884759182) | Terrain variety for cliffs and routes | Author explicitly allows use and edits with credit. |
| [J-Treecko252 Path Tiles EX Add-Ons](https://www.deviantart.com/j-treecko252/art/Path-Tiles-EX-Add-Ons-01-884690320) | Less rigid path shapes and route detail | Author explicitly allows use and edits with credit. Useful without changing the entire art direction. |
| [Magiscarf Revamped Tiles](https://www.deviantart.com/magiscarf/art/Revamped-Tiles-829482346) | Broad nature, exterior and interior artwork | Creator permits noncommercial use and editing; page labels CC BY-NC-SA 3.0. Needs palette/scale/style review before GBA conversion. **Strong alternate art direction.** |
| [Dawn Bronze / Pokémon Umber](https://eeveeexpo.com/resources/26/) | Scrubland, caves and ocean; especially useful for arid environments | Public release with multi-artist credits. Raw/Essentials-oriented graphics, not an Emerald package. |
| [Foxowl23 Coastal City](https://www.deviantart.com/foxowl23/art/Gen-3-Coastal-City-Tileset-877455638) | Port town buildings, beach details and coastal architecture | Explicitly free with credit; preserve the listed contributors for edited components. Good Crystal Island settlement source. |
| [AnonAlpaca Big Tree Pack](https://eeveeexpo.com/resources/602/) | Giant and unusual trees, bamboo, dead trees, seasonal variants | Use with credit and editing allowed. Creator says perspective best suits B/W; evaluate scale and perspective against LeoB. Good Mirage Forest landmark source. |
| [AnonAlpaca Big Flora Pack](https://eeveeexpo.com/resources/607/) | Plant detail to accompany the tree pack | Public resource; follow its credit notice. Treat as supplemental flora requiring conversion. |
| [KingTapir collection](https://eeveeexpo.com/threads/3728/) | An additional coherent artist library to audition | Public collection compiled by NocTurn/Turner; credit original art. Compilation notes shadow transparency still needs work. Desert Exchange ports already contain some KingTapir material. |
| [ChaoticCherryCake Public Indoor Tileset](https://www.deviantart.com/chaoticcherrycake/art/Public-Indoor-Tileset-From-Public-Tiles-483814875) | Interior furnishings and room details | Public compilation; credits Kyle-Dove, Newtiteuf and Thegreatblaid. Preserve contributor permissions and build GBA data. |
| [PhantomFae Gen 3 Sinnoh maps](https://eeveeexpo.com/resources/1661/) | Sinnoh exteriors/caves and associated tilesets; mountain/settlement donors | Explicit public resource, with full contributor list. Essentials map data is not Porymap data. Useful assembled material, partly overlaps Ekat. |

### Additional coherent styles in Aki’s collection

The [Ready to use Tilesets collection](https://eeveeexpo.com/resources/15/) groups public work by artist. “Ready” refers to Essentials image formatting, not GBA/decomp compatibility. Its credit instructions name the original artists; compilation alone does not warrant crediting Aki for another artist’s artwork.

| Style / artist | Available direction |
| --- | --- |
| Akizakura16 | HGSS-inspired exterior/interior sets and door sheets |
| LotusKing / Aigue--marine | Outlined and lineless alternatives |
| Kaliser | Public collection; compiler explicitly notes past private/public ambiguity—recheck selected pieces |
| JesusCarrasco / Thegreatblaid | Green/red exterior variants and interiors |
| WilsonScarloxy | Matching outdoor and indoor sets |
| SailorVicious / Heavy-Metal-Lover | Hoenn Project artwork in outlined/lineless forms |
| Kyle-Dove | Public collection; DS-style direction |
| UltimoSpriter | Gen 5 exterior set |
| Akizakura16 + Shiney570 + UltimoSpriter | Gen 5 interior compilation |
| Magiscarf | Compiled versions; overlaps the direct creator source above |

For Kyle-Dove, also see the [creator’s original public resource release](https://www.deviantart.com/kyle-dove/art/Kyledove-s-Public-Resources-103892943). Restrict selection to public releases; this is not permission for every image in an artist’s gallery.

### TAAR raw-sheet collections and individual additions

| Source | Suggested Holon role | Reuse / format notes |
| --- | --- | --- |
| [Roger Wrightshoe / gray ninja](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/Other%20Tilesets/Roger%20Wrightshoe) | Safari greenery, dripstone caves, XY-style Route 120 terrain, stairs | README requests Roger Wrightshoe credit. Raw-sheet conversion. **Strong wilderness donor.** |
| [Sacred Phoenix / Alienor v2](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/Other%20Tilesets/Sacred%20Phoenix) | Forests, rustic settlement detail, ruins | Mixed per-contributor terms. Semi-opaque red masking denotes private material; exclude it. Opaque red marks obsolete free tiles. Requires careful selection and conversion. |
| [Droid779 Snow Tiles](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/Other%20Tilesets/Droid779) | Glacial coast and snowy environments | Repository policy applies; credit Droid779. Raw-sheet conversion. |
| [Ewraz / Erawz Collected Tilesets](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/Other%20Tilesets/Ewraz%20Collected%20Tilesets) | FRLG-style alternate terrain/props | README says free to use and lists Alistair, Serg!o, Remy, Fangking Omega and Kyledove. |
| [Voluptua’s Collected Tilesets](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/Other%20Tilesets/Voluptuas%20Collected%20Tilesets) | Broad donor library for individual props and alternate styles | Numbered sheets have separate contributor lists. Some credit mapping is incomplete; track selected assets individually. |
| [Rahtak greenery](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Individual%20Tiles/Rahtak) | Grass/greenery; dependency of the lab-town set | Credit FM and Zeikaro for art and Rahtak for porting. |
| [Oomer individual tiles](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Individual%20Tiles/Oomer) | Aquarium, palms, flowers, cactus, small props | Folder inspected; repository-wide policy, no local README found. Keep provenance when selecting. |
| [KyuZee fence](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Individual%20Tiles/KyuZee) | Small town detail | Designed for general palette 5, replacing the default fence. |
| [yoshord decorations](https://github.com/monhacks/teamaquas-assets/tree/main/Tilesets/The%20Great%20Tileset%20Exchange/Individual%20Tiles/yoshord) | Cabins, homes, secret bases | Includes furniture and Pokémon-themed decor using SecretBase palettes. Useful supplements, not a world style. |

## C. Public decomp projects worth inspecting

These are candidate source projects, not standalone asset-pack guarantees. Extract selected environments after checking their credits and format; importing another game wholesale is unnecessary for this art decision.

| Project | Why it is relevant | Reuse evidence / practical status |
| --- | --- | --- |
| [Pokémon Heart & Soul](https://github.com/PokemonHnS-Development/pokemonHnS) / [expansion repository](https://github.com/PokemonHnS-Development/pokehns-expansion) | Johto/HGSS demake direction already implemented on GBA | Original README invites derivative projects and lists tileset sources including Crystal Advance, Ekat99, TheDeadHeroAlistair and Johto Redrawn. Preserve asset-level attribution; invitation is not a blanket license for all third-party art. **Strong alternative to audition.** |
| [LiderMorti00 Sinnoh base](https://github.com/LiderMorti00/Sinnoh-pokeemerald-expansion) | Sinnoh town/mountain environments in an Emerald-expansion project | [Creator’s public base release](https://whackahack.com/foro/threads/sinnoh-gba-en-pokeemerald-expansion.68853/). A useful decomp donor candidate; asset-specific reuse terms were not established in this pass. |
| [sinnoh-remakes / pokeemerald-platinum](https://github.com/sinnoh-remakes/pokeemerald-platinum) | Another public Platinum demake effort | Investigate current map/art coverage. Public code and project description verified; completeness and blanket graphic permissions not verified. |
| [CrystalDust](https://github.com/Deokishisu/CrystalDust) | Crystal-to-GBA approach to Johto nostalgia | Public Emerald hack source. Useful historical/technical comparison; check graphic-specific permissions before extracting assets. |
| [LeoB Modern Emerald ORAS](https://github.com/lbsbezerra/pokeemerald-modern-oras) | Working implementation of the shared-foundation candidate | Companion to LeoB’s public asset release; good integration reference, not a separate independent art style. |
| [LeoB Emerald Rogue improved graphics](https://github.com/lbsbezerra/pokeemerald-rogue-improved-graphics) | Further LeoB graphics work on a different map/game structure | Public fork verified. Treat newer artwork as a candidate to inspect; do not assume the earlier ORAS release terms cover every new graphic. |
| [Pokémon Emerald Rogue](https://github.com/Pokabbie/pokeemerald-rogue) | Multi-environment implementation reference | Public source verified. Better as a source for studying environment organization until individual graphic permissions are checked. |
| [LeoB Minish Quest / pokezelda](https://github.com/lbsbezerra/pokeemerald-pokezelda) | Zelda-inspired environments in an Emerald-derived project | Interesting larger style departure. Public repository verified; individual artwork permissions and completeness not verified. |

## D. Paid and broader retro alternatives

These are publicly purchasable sources, not free asset releases. Prices below are the displayed prices observed during research and may change. None was purchased. Artwork needs GBA conversion, and a paid pack should not be uploaded as raw assets into a public source repository without permission.

| Pack | Holon fit | Observed availability / effort |
| --- | --- | --- |
| [Zaebucca Adventure Begins](https://zaebucca.itch.io/adventure-begins) | Strong GBC-like alternate foundation: wilderness, villages, desert and interiors | Listed $14.99 with demo; Adventure Inside and character expansion included on the page. High adaptation effort; evaluate matching trainers/Pokémon too. |
| [Zaebucca The Nest](https://zaebucca.itch.io/) | Fungal forest dungeon vocabulary for strange wilderness | Listed $4.99 on creator storefront. Specialist art donor; review pack terms before acquisition. |
| [Zaebucca Tar Pit](https://zaebucca.itch.io/) | Lava, fossils and obsidian cliffs for prehistoric volcanic areas | Listed $4.99 on creator storefront. Strong thematic option if choosing this retro direction. |
| [Zaebucca Candle Cathedral](https://zaebucca.itch.io/) | Gothic ruins/ossuary; narrower fit than the forest and volcano packs | Listed $7.99 on creator storefront. Optional architectural departure. |
| [LimeZu Modern Interiors](https://limezu.itch.io/moderninteriors) | Control rooms, hospitals, museum and research-facility furnishings | Free sample; full-version license threshold shown as $1.50. Edits/project use allowed with credit; redistribution restricted. Useful prop donor, but art style and proportions need adaptation. |

Zaebucca’s purchasable packs are an asset route to explore for a retro aesthetic. This does **not** identify them as an exact public release of Emerald Seaglass’s custom tiles.

## E. Wider discovery sources and references

| Source | How to use it |
| --- | --- |
| [Team Aqua / monhacks asset repository](https://github.com/monhacks/teamaquas-assets) | First stop for GBA-oriented assets and explicit pack credits. Catalog A covers the inspected Full Tilesets directory completely. |
| [Eevee Expo graphics resources](https://eeveeexpo.com/resources/categories/6/) | Browse new artist packs and public game-jam releases. Many are Essentials-oriented. |
| [Aki’s organized public collections](https://eeveeexpo.com/resources/15/) | Efficient comparison of coherent artist styles; options are listed in section B. |
| [Gen 3 Ultimate Tileset Collection 3.0.0 announcement](https://www.reddit.com/r/PokemonROMhacks/comments/1l3j8el/) | Additional discovery lead. Announcement found, but full current download contents and all permissions were not independently audited. |
| [Cham3leon’s graphics collection announcement/link](https://www.pokecommunity.com/threads/looking-for-more-gen-3-sprites.538433/) | Search-indexed creator reply points to an Ultra Mega Graphics Collection. Direct forum access failed here; treat as an unverified directory lead, not a cleared asset pack. |
| [Johto Redrawn](https://retroredrawn.com/johto/index.html) | Art-direction reference for nostalgic but different environments. Collaborative gallery, not a blanket reusable tileset library. |
| [Ikarus FireRed tileset patch](https://www.reddit.com/r/PokemonROMhacks/comments/1td8vp3/ikarus_tileset_patch_v32_fixed_version_gen_4/) | Gen 4-style binary patch comparison. Lower priority than decomp packages: extraction, credit tracking and conversion add work. |

## F. Recommended environment plan for Holon

This is a proposed selection strategy, not an assertion that these sets already interoperate.

| Holon environment | First sources to audition | Likely bespoke work |
| --- | --- | --- |
| Ordinary settlements and routes; future Hoenn | LeoB ORAS | Shared palette tuning, Holon signs and architecture |
| Mirage Forest | Shady Forest, Ekat, Roger Wrightshoe; selected AnonAlpaca trees | Giant trunks, vines, mist, consistent canopy shapes |
| Research settlement / railway remains | Lab-town set, J-Treecko buildings, sewer props | Tower silhouette, radar dishes, rail remnants, industrial structures |
| Ancient Holon Ruins | Autumn Ruins, Lugia altar; selected Sacred Phoenix pieces | Holon symbols and recurring architecture tied to the tower site |
| Holon Lake depths | Underwater Primary plus underwater secondaries | Submerged machinery and pipelines; no ready-made complete Holon facility was verified |
| Crystal Island | Reef, Beach Cave, Valencia Island, Foxowl coastal buildings | A consistent custom crystal family; animated glow if desired |
| Volcanic fringes / arid frontiers | Volcano, Desert Primary, Dawn Bronze | Red-cliff palette, monoliths and biome transitions |
| Glacial coast | Emerald Slide, Droid779 Snow | Ice floes and shoreline combinations |
| Floating island / upper atmosphere | Distortion World, Space Meteor | Rework recognizable Sinnoh imagery; sky/void presentation and Holon landmarks |

## G. Integration findings specific to this checkout

At research time, [include/fieldmap.h](../../include/fieldmap.h) defines 512 primary metatiles, 1,024 total metatiles and eight 8×8 tiles per metatile. [src/field_camera.c](../../src/field_camera.c) renders that existing two-layer data. Therefore packs that require triple-layer or expanded metatile support need a project change or a conversion before import.

For candidate selection:

1. **Choose a visual foundation before assembling every biome.** Keep comparable grass, water, cliff, tree and building samples in one test scene.
2. **Check each secondary with its intended primary.** Shared palette and tile references can prevent arbitrary mixing even when both packages import individually.
3. **Treat Essentials sheets as artwork.** Reconstruct palettes, GBA tiles/metatiles, behaviors, collisions and animation data. A doubled 16-pixel sheet can be reduced cleanly; genuinely larger art needs redrawing or selective adaptation.
4. **Preserve Hoenn map semantics.** Replacement metatile IDs, behaviors, scripted tiles, doors and animations determine whether existing maps survive unchanged.
5. **Test three representative scenes:** a Holon town, a forest/ruins route and an existing Hoenn town. Add one lab or underwater room before making a final commitment.

Relevant technical references: [Porytiles’ GBA/decomp tileset explanation](https://grunt-lucas.github.io/porytiles-user-docs/gba-decomp-tileset-system.html), [triple-layer metatiles](https://github.com/pret/pokeemerald/wiki/Triple-layer-metatiles), [expanded metatile counts](https://github.com/pret/pokeemerald/wiki/Expanding-The-Metatile-Count).

## Research coverage

- Read the Holon lore guide to prioritize forest, ruins, research infrastructure, underwater, volcanic, crystal and floating-island environments.
- Inspected the public repository file tree and fetched 71 tileset metadata/credit files.
- Enumerated all 32 packaged Exchange entries and read available READMEs and credits.
- Visually inspected the six source previews embedded above.
- Checked creator/resource pages for wider libraries, project descriptions and explicit reuse statements where available.
- Did not download every external asset archive, audit every contributor license, or validate in-game compatibility. Unknowns are marked in the tables.

Inspected asset repository tree: `16ceb3d7ab418b9801b99b65c30221c59ffd4a1d`. Source links track the current main branch and may evolve.
