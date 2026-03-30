import os
import re
import logging

logger = logging.getLogger(__name__)

# Explicit overrides for names that don't auto-convert cleanly
OVERRIDES = {
    'nidoran_f': 'nidoran_f',
    'nidoran_m': 'nidoran_m',
    'mr_mime': 'mr_mime',
    'mime_jr': 'mime_jr',
    'ho_oh': 'ho_oh',
    'porygon_z': 'porygon_z',
    'jangmo_o': 'jangmo_o',
    'hakamo_o': 'hakamo_o',
    'kommo_o': 'kommo_o',
}


def name_to_sprite_dir(name: str) -> str:
    """Convert a Pokémon name from the Holon Pokédex CSV to a sprite directory name.

    Handles delta variants (δ), ex variants, golden stars (★), Holon's prefix,
    form prefixes (Rain/Sunny/Snow-cloud), gender symbols, and punctuation.
    """
    # 1. Strip variant suffixes — longest combinations first
    name = re.sub(r'\s+(ex\s+δ|★\s+δ|ex δ|★ δ|ex|★|δ)$', '', name.strip())
    # 2. Strip "Holon's " prefix
    name = re.sub(r"^Holon's\s+", '', name)
    # 3. Strip form prefixes
    name = re.sub(r'^(Rain|Sunny|Snow-cloud)\s+', '', name)
    # 4. Lowercase
    name = name.lower()
    # 5. Gender symbols (before space→underscore to avoid double underscores)
    name = name.replace(' ♀', '_f').replace(' ♂', '_m')
    name = name.replace('♀', '_f').replace('♂', '_m')
    # 6. Strip apostrophes and periods
    name = name.replace("'", '').replace('.', '')
    # 7. Spaces and hyphens → underscores
    name = name.replace(' ', '_').replace('-', '_')
    # 8. Collapse any double underscores from prior steps
    name = re.sub(r'_+', '_', name).strip('_')

    return OVERRIDES.get(name, name)


def validate_sprite_dirs(sprite_root: str, pokedex_entries: list) -> None:
    """Log warnings for any Pokédex entry whose sprite directory doesn't exist."""
    seen = set()
    missing = []
    for entry in pokedex_entries:
        d = entry.get('sprite_dir', '')
        if d and d not in seen:
            seen.add(d)
            if not os.path.isdir(os.path.join(sprite_root, d)):
                missing.append((entry.get('name', ''), d))

    if missing:
        logger.warning("Missing sprite directories for %d Pokémon:", len(missing))
        for name, d in missing:
            logger.warning("  '%s' → graphics/pokemon/%s/ (not found)", name, d)
    else:
        logger.info("All %d unique sprite directories found.", len(seen))
