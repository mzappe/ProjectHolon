#!/usr/bin/env bash
# Convert a 256x256 indexed master -> a title-screen 4bpp tile sheet + tilemap.
#   build_title_bg.sh [master.png] [stem]
#   stem "rayquaza" (default) = BG0 Deoxys layer, also (re)writes the shared palette.
#   stem "clouds"             = BG1 overlay layer, palette left untouched.
# Run from repo root.
set -euo pipefail
GRIT=/opt/devkitpro/tools/bin/grit
GBAGFX=tools/gbagfx/gbagfx
MASTER=${1:-art/title_screen_masters/deoxys_bg.png}
STEM=${2:-rayquaza}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

"$GRIT" "$MASTER" -gB4 -mRtpf -mLs -mp14 -pT0 -pn16 -ftb -fh! -o "$work/gen"

img=$(( $(wc -c < "$work/gen.img.bin") ))
map=$(( $(wc -c < "$work/gen.map.bin") ))
echo "$STEM  tiles: $(( img / 32 )) / 512   img: $img   map: $map"
[ "$map" -eq 2048 ] || { echo "ERROR map != 2048 bytes"; exit 1; }
[ "$img" -le 16384 ] || { echo "ERROR over 512 tiles"; exit 1; }

cp "$work/gen.img.bin" "$work/gen.4bpp"
cp "$work/gen.pal.bin" "$work/gen.gbapal"
"$GBAGFX" "$work/gen.4bpp" "graphics/title_screen/$STEM.png" -palette "$work/gen.gbapal" -width 1
cp "$work/gen.map.bin" "graphics/title_screen/$STEM.bin"
if [ "$STEM" = "rayquaza" ]; then
    "$GBAGFX" "$work/gen.gbapal" graphics/title_screen/rayquaza_and_clouds.pal
    echo "  + rewrote rayquaza_and_clouds.pal"
fi
echo "installed $STEM.png / $STEM.bin"
