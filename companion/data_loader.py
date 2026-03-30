import csv
import os
import logging

from name_mapper import name_to_sprite_dir, validate_sprite_dirs

logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITE_ROOT  = os.path.join(PROJECT_ROOT, 'graphics', 'pokemon')
TCG_ROOT     = os.path.join(PROJECT_ROOT, 'tcg_art')
POKEDEX_CSV  = os.path.join(PROJECT_ROOT, 'GDDs', 'holon_pokedex_v2.csv')
CARD_CSV_DIR = os.path.join(TCG_ROOT, 'card-lists')

# Maps the ex-number shorthand in pokedex CSV to actual image directory names
EX_NUM_TO_DIR = {
    'ex11': 'ex_delta_species',
    'ex12': 'ex_legend_maker',
    'ex13': 'ex_holon_phantoms',
    'ex14': 'ex_crystal_guardians',
    'ex15': 'ex-dragon_frontiers',
}

# Maps CSV filenames to (directory name, display name)
TCG_SETS = [
    ('Pokemon-Delta-Species.csv',    'ex_delta_species',    'EX Delta Species'),
    ('Pokemon-Legend-Maker.csv',     'ex_legend_maker',     'EX Legend Maker'),
    ('Pokemon-Holon-Phantoms.csv',   'ex_holon_phantoms',   'EX Holon Phantoms'),
    ('Pokemon-Crystal-Guardians.csv','ex_crystal_guardians','EX Crystal Guardians'),
    ('Pokemon-Dragon-Frontiers.csv', 'ex-dragon_frontiers', 'EX Dragon Frontiers'),
]

# GBA sprite filenames (normal palette — shiny variants generated server-side)
SPRITE_FILES = {
    'main':      'anim_front_gba.png',   # animated, used as hero sprite in grid + modal
    'front':     'anim_front_gba.png',   # same image, rendered static (no CSS animation)
    'back':      'back_gba.png',         # back battle sprite (normal palette ✓)
    'icon':      'icon_gba.png',         # small menu icon
    'overworld': 'overworld.png',        # no GBA variant exists
}


def _card_img_url(card_image: str) -> str:
    """Convert a card_image CSV value like 'ex12/8_hires.png' to a /cards/ URL."""
    if not card_image or card_image == 'placeholder':
        return None
    parts = card_image.split('/', 1)
    if len(parts) != 2:
        return None
    ex_num, filename = parts
    img_dir = EX_NUM_TO_DIR.get(ex_num)
    if not img_dir:
        return None
    return f'/cards/{img_dir}/{filename}'


def load_pokedex() -> list:
    entries = []
    with open(POKEDEX_CSV, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            name = row['name'].strip()
            sprite_dir = name_to_sprite_dir(name)
            sprites = {
                key: f'/sprites/{sprite_dir}/{fname}'
                for key, fname in SPRITE_FILES.items()
            }
            # Shiny variants generated server-side via palette swap
            sprites['shiny_front'] = f'/sprites/{sprite_dir}/shiny/anim_front_gba.png'
            sprites['shiny_back']  = f'/sprites/{sprite_dir}/shiny/back_gba.png'
            entries.append({
                'dex_number':  int(row['dex_number']),
                'name':        name,
                'category':    row['category'].strip(),
                'type_1':      row['type_1'].strip(),
                'type_2':      row['type_2'].strip(),
                'tcg_type_1':  row['tcg_type_1'].strip(),
                'tcg_type_2':  row['tcg_type_2'].strip(),
                'tcg_set':     row['tcg_set'].strip(),
                'location':    row['location'].strip(),
                'card_number': row['card_number'].strip(),
                'evolves_from':row['evolves_from'].strip(),
                'needs_review':row['needs_review'].strip().lower() == 'yes',
                'card_img_url':_card_img_url(row['card_image'].strip()),
                'sprite_dir':  sprite_dir,
                'sprites':     sprites,
            })

    validate_sprite_dirs(SPRITE_ROOT, entries)
    logger.info("Loaded %d Pokédex entries.", len(entries))
    return entries


def load_tcg() -> list:
    cards = []
    for csv_file, img_dir, set_name in TCG_SETS:
        path = os.path.join(CARD_CSV_DIR, csv_file)
        if not os.path.exists(path):
            logger.warning("TCG CSV not found: %s", path)
            continue
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                card_num = row['Number'].split('/')[0]
                cards.append({
                    'name':    row['Name'].strip(),
                    'number':  row['Number'].strip(),
                    'rarity':  row['Rarity'].strip(),
                    'set':     set_name,
                    'img_url': f'/cards/{img_dir}/{card_num}_hires.png',
                })
    logger.info("Loaded %d TCG cards across %d sets.", len(cards), len(TCG_SETS))
    return cards
