import io
import logging
import os

from flask import Flask, jsonify, render_template, send_from_directory, send_file
from PIL import Image

import data_loader

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITE_ROOT  = os.path.join(PROJECT_ROOT, 'graphics', 'pokemon')
TCG_ROOT     = os.path.join(PROJECT_ROOT, 'tcg_art')

# Load all data at startup
POKEDEX = data_loader.load_pokedex()
TCG     = data_loader.load_tcg()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/pokedex')
def api_pokedex():
    return jsonify(POKEDEX)


@app.route('/api/tcg')
def api_tcg():
    return jsonify(TCG)


# Cache of palette-swapped shiny sprites: (pokemon_name, sprite_file) → PNG bytes
_shiny_cache: dict = {}

def _parse_jasc_pal(pal_path: str) -> list:
    """Parse a JASC-PAL file and return a flat [R,G,B, R,G,B, ...] palette list."""
    with open(pal_path) as f:
        lines = f.readlines()
    # Format: JASC-PAL / 0100 / <count> / R G B per line
    colors = []
    for line in lines[3:]:
        line = line.strip()
        if not line:
            continue
        r, g, b = (int(x) for x in line.split())
        colors.extend([r, g, b])
    # Pad to 256 colors (768 values) as required by Pillow
    colors.extend([0] * (768 - len(colors)))
    return colors

def _make_shiny(pokemon_name: str, sprite_file: str) -> bytes:
    """Apply shiny_gba.pal to a GBA sprite PNG and return the PNG bytes."""
    cache_key = (pokemon_name, sprite_file)
    if cache_key in _shiny_cache:
        return _shiny_cache[cache_key]

    sprite_dir = os.path.join(SPRITE_ROOT, pokemon_name)
    sprite_path = os.path.join(sprite_dir, sprite_file)
    pal_path    = os.path.join(sprite_dir, 'shiny_gba.pal')

    img = Image.open(sprite_path).copy()  # palette-mode PNG
    shiny_pal = _parse_jasc_pal(pal_path)
    img.putpalette(shiny_pal)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    result = buf.read()
    _shiny_cache[cache_key] = result
    return result


@app.route('/sprites/<pokemon_name>/<filename>')
def serve_sprite(pokemon_name, filename):
    return send_from_directory(os.path.join(SPRITE_ROOT, pokemon_name), filename)


@app.route('/sprites/<pokemon_name>/shiny/<filename>')
def serve_shiny_sprite(pokemon_name, filename):
    """Serve a palette-swapped shiny version of a GBA sprite."""
    png_bytes = _make_shiny(pokemon_name, filename)
    return send_file(io.BytesIO(png_bytes), mimetype='image/png')


@app.route('/cards/<path:filepath>')
def serve_card(filepath):
    return send_from_directory(TCG_ROOT, filepath)


if __name__ == '__main__':
    logger.info("Starting Holon Companion at http://localhost:8080")
    # use_reloader=False prevents Flask from watching the large graphics/ tree
    app.run(debug=True, use_reloader=False, port=8080)
