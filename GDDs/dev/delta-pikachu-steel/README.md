# Pikachu δ — Steel Front Sprite Test

This folder contains the first production-oriented art test for `SPECIES_PIKACHU_DELTA_STEEL`.

## Design direction

- Canonical type: pure Steel / Metal
- Identity: preserve Pikachu's established Generation III silhouette and animation
- Body: pale electrum and cool steel rather than normal saturated yellow
- Highlights: ivory-silver specular pixels
- Shadows and ear tips: cooler graphite
- Cheeks: retained red for immediate Pikachu readability
- Overall goal: living metallic adaptation, not a robot or armor costume

## Files

| File | Purpose |
|---|---|
| `front.png` | First 64×64 front battle frame |
| `anim_front.png` | Two-frame 64×128 front battle animation sheet |
| `normal.pal` | 16-entry indexed Steel Delta palette |

The pixel layout derives from the current `graphics/pokemon/pikachu/anim_front.png` source so anatomy, anchors, and animation remain build-safe. The new palette is original to this test.

This is an art test and is not yet connected to a species entry or graphics table.

## Image-generation record

Three built-in image-generation attempts were made for a more structural Steel Delta redesign. All three were rejected by the image safety system during output. The finished test therefore uses the repository's deterministic indexed-pixel pipeline rather than an API/CLI fallback.
