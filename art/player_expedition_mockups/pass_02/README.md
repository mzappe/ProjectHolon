# Holon expeditionists — approved player sprites

Open **review.html** to view both characters, animate the sheets, and inspect individual frames. **overview.png** compares the original fronts with the approved designs.

## Direction

Both characters have white hair, blue eyes, deeper steel-blue clothing, orange side panels and waist/cuff trim, and small dark leather accents. Brendan's headband is dark neutral grey, clearly distinct from the white hair; May's original bandana and tied ends now use charcoal fabric, with neutral grey highlights on the larger trainer sprites, distinct from her white hair. The original poses, sprite dimensions, and silhouettes remain intact. May retains field trousers.

The iris pixels are handled separately from the shared hair and clothing indices, including the small eyes in the overworld frames. Pockets use simple paired rows rather than alternating colors. Larger packs remain blue fabric with leather edging and orange lower trim. This revision replaces the previous images in place; only the current mockup set is retained.

## Contents

Each character folder contains a 64×64 battle front, a 64×256 throwing back with four frames, and all ten Emerald player sheets: walking, running, Mach Bike, Acro Bike, surfing, fishing, watering, field move, underwater, and decorating. East-facing locomotion is mirrored in the viewer as in the game. Jumping and other movements that reuse these graphics inherit the same outfit. Underwater frames retain the existing submerged silhouette with lighter neutral head highlights and dark submerged body shading.

All 24 PNGs retain source dimensions, frame layout, a 16-entry indexed palette, and transparent index 0. These approved sprites are now installed in the game, with matching trainer, overworld, and shared underwater palettes. Palette changes alone account for some frames' changes. The full-scale fronts carry finer equipment details than the overworld sprites. Acro tricks, throws, fishing, and other action sheets can be reviewed in storage order; their viewer timing is illustrative, not a recreation of the complete runtime state machine. Credits, menu icons, alternate Ruby/Sapphire players, and FireRed/LeafGreen players are outside this Emerald avatar pass.

## Rebuild

From the repository root, with Pillow installed:

```sh
python3 art/player_expedition_mockups/pass_02/build_mockups.py
```

The script uses explicit palette maps, coordinate edits, and source-color masks. It has no random or generative step and writes only inside this mockup folder. It validates dimensions, 4-bit pixel indices, unchanged transparency masks, and unchanged source-file hashes. Original source PNGs are read from Git revision `1b7f9ee3c14128e4d34958017e35470544e96f88`, so rebuilding cannot accidentally recolor the already-integrated sprites. Rebuilding with the same Pillow version produces the same files. `review.html` is also the viewer template; its asset data is refreshed by the script.

The latest cleanup smooths May's hair into broad white areas and light-grey interior shadows, removes the isolated warm/dark pixels in her locks, and keeps a thin outer outline for readability. Her moving bandana is solid charcoal, and leftover skin-colored hair speckles are removed. Brendan’s four throwing frames now have lighter rear hair shading and a continuous dark headband. These edits are restricted to the hair and headwear: blue irises, outfits, palettes, and other approved sprites remain unchanged. Front hair boundaries are explicitly authored to preserve forehead gaps and eyes; moving/back hair regions are derived from the source hair material.

## Game integration

The 24 approved PNGs are copied into `graphics/trainers/{front_pics,back_pics}/` and `graphics/object_events/pics/people/{brendan,may}/`. The embedded palettes are exported to the two trainer PALs, two overworld PALs, and shared `player_underwater.pal`. The existing frame order, tile packing, animation tables, and collision geometry are retained. Reflections derive their colors from the active avatar palette at runtime. Link-room Brendan now uses his own palette rather than May's.

The generator rebuilds only this review/export folder; it does not install or overwrite game assets. After an approved future revision, copy the PNGs and export the matching 16-color palettes together, then build with `make -j8`.
