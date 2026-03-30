import os
import re
import logging

logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECIES_INFO_DIR = os.path.join(PROJECT_ROOT, 'src/data/pokemon/species_info')
LEARNSETS_FILE = os.path.join(PROJECT_ROOT, 'src/data/pokemon/level_up_learnsets/gen_6.h')
MOVES_INFO_FILE = os.path.join(PROJECT_ROOT, 'src/data/moves_info.h')


def _parse_constants(filename, pattern):
    """Extract constant definitions from header files. Returns dict: constant_name -> readable_string."""
    result = {}
    if not os.path.exists(filename):
        logger.warning(f"Constants file not found: {filename}")
        return result

    with open(filename, encoding='utf-8') as f:
        content = f.read()

    # Match lines like: .abilities = { ABILITY_OVERGROW, ABILITY_NONE, ABILITY_CHLOROPHYLL },
    # Or: .speciesName = _("Bulbasaur"),
    matches = re.findall(pattern, content, re.IGNORECASE)
    for match in matches:
        result[match[0]] = match[1]

    return result


def parse_abilities_map():
    """Parse ability constants from include/constants/abilities.h. Returns dict: ABILITY_NAME -> readable name."""
    ability_file = os.path.join(PROJECT_ROOT, 'include/constants/abilities.h')
    result = {}

    if not os.path.exists(ability_file):
        logger.warning(f"Ability constants file not found: {ability_file}")
        return result

    with open(ability_file, encoding='utf-8') as f:
        for line in f:
            # Match: ABILITY_OVERGROW = 65, (enum format)
            match = re.match(r'\s*(ABILITY_\w+)\s*=\s*\d+', line)
            if match:
                const_name = match.group(1)
                # Convert ABILITY_OVERGROW -> Overgrow
                readable = const_name.replace('ABILITY_', '').replace('_', ' ').title()
                result[const_name] = readable

    return result


def parse_species_map():
    """Parse species constants. Returns dict: SPECIES_NAME -> readable name."""
    species_file = os.path.join(PROJECT_ROOT, 'include/constants/species.h')
    result = {}

    if not os.path.exists(species_file):
        logger.warning(f"Species constants file not found: {species_file}")
        return result

    with open(species_file, encoding='utf-8') as f:
        for line in f:
            # Match: #define SPECIES_BULBASAUR 1
            match = re.match(r'#define\s+(SPECIES_\w+)\s+\d+', line)
            if match:
                const_name = match.group(1)
                # Convert SPECIES_BULBASAUR -> Bulbasaur
                readable = const_name.replace('SPECIES_', '').replace('_', ' ').title()
                result[const_name] = readable

    return result


def parse_moves_map():
    """Parse move constants. Returns dict: MOVE_NAME -> readable name."""
    moves_file = os.path.join(PROJECT_ROOT, 'include/constants/moves.h')
    result = {}

    if not os.path.exists(moves_file):
        logger.warning(f"Moves constants file not found: {moves_file}")
        return result

    with open(moves_file, encoding='utf-8') as f:
        for line in f:
            # Match: MOVE_TACKLE = 1, (enum format)
            match = re.match(r'\s*(MOVE_\w+)\s*=\s*\d+', line)
            if match:
                const_name = match.group(1)
                # Convert MOVE_TACKLE -> Tackle
                readable = const_name.replace('MOVE_', '').replace('_', ' ').title()
                result[const_name] = readable

    return result


def parse_moves_data():
    """Parse move metadata (type, power, accuracy) from moves_info.h.
    Returns dict: MOVE_NAME -> {type: 'Normal', power: 40, accuracy: 100}"""
    result = {}

    if not os.path.exists(MOVES_INFO_FILE):
        logger.warning(f"Moves info file not found: {MOVES_INFO_FILE}")
        return result

    with open(MOVES_INFO_FILE, encoding='utf-8') as f:
        content = f.read()

    # Split by move entries: [MOVE_TACKLE] = { ... },
    move_blocks = re.findall(r'\[MOVE_(\w+)\]\s*=\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', content, re.DOTALL)

    for move_const, move_body in move_blocks:
        move_name = f'MOVE_{move_const}'

        # Extract .type = TYPE_NORMAL,
        type_match = re.search(r'\.type\s*=\s*TYPE_(\w+)', move_body)
        move_type = type_match.group(1).replace('_', ' ').title() if type_match else 'Unknown'

        # Extract .power = 40, (handle conditional compilation)
        power_match = re.search(r'\.power\s*=\s*(\d+)', move_body)
        power = int(power_match.group(1)) if power_match else 0

        # Extract .accuracy (may be conditional)
        acc_match = re.search(r'\.accuracy\s*=\s*(\d+)', move_body)
        accuracy = int(acc_match.group(1)) if acc_match else 100

        result[move_name] = {
            'type': move_type,
            'power': power,
            'accuracy': accuracy,
        }

    logger.info(f"Parsed {len(result)} moves from moves_info.h")
    return result


def parse_gen3_species(pokemon_names):
    """Parse stats, abilities, categoryName, and evolutions for given Pokemon from all gen_*_families.h files.

    Args:
        pokemon_names: set of Pokemon names to look for (e.g. {'Bulbasaur', 'Eevee δ'})

    Returns:
        dict: {pokemon_name -> {stats: {...}, abilities: [...], categoryName: str, evolution: {...}}}
    """
    result = {}

    if not os.path.isdir(SPECIES_INFO_DIR):
        logger.warning(f"Species info dir not found: {SPECIES_INFO_DIR}")
        return result

    ability_map = parse_abilities_map()
    species_map = parse_species_map()

    # Parse all gen_*_families.h files
    gen_files = sorted([f for f in os.listdir(SPECIES_INFO_DIR) if f.startswith('gen_') and f.endswith('_families.h')])

    for gen_file in gen_files:
        gen_path = os.path.join(SPECIES_INFO_DIR, gen_file)
        logger.debug(f"Parsing {gen_file}")

        with open(gen_path, encoding='utf-8') as f:
            content = f.read()

        # Parse each species struct
        # Look for [SPECIES_BULBASAUR] = { ... },
        # Use a more lenient pattern that handles nested braces better
        species_blocks = re.findall(r'\[SPECIES_(\w+)\]\s*=\s*\{(.+?)\n\s*\},', content, re.DOTALL)

        for species_const, species_body in species_blocks:
            # Convert SPECIES_BULBASAUR -> Bulbasaur
            species_name = species_const.replace('_', ' ').title()

            # Only process if we're looking for this Pokemon
            if species_name not in pokemon_names:
                continue

            # Extract base stats
            hp_match = re.search(r'\.baseHP\s*=\s*(\d+)', species_body)
            atk_match = re.search(r'\.baseAttack\s*=\s*(\d+)', species_body)
            def_match = re.search(r'\.baseDefense\s*=\s*(\d+)', species_body)
            spa_match = re.search(r'\.baseSpAttack\s*=\s*(\d+)', species_body)
            spd_match = re.search(r'\.baseSpDefense\s*=\s*(\d+)', species_body)
            spe_match = re.search(r'\.baseSpeed\s*=\s*(\d+)', species_body)

            stats = {
                'HP': int(hp_match.group(1)) if hp_match else 0,
                'Attack': int(atk_match.group(1)) if atk_match else 0,
                'Defense': int(def_match.group(1)) if def_match else 0,
                'SpAtk': int(spa_match.group(1)) if spa_match else 0,
                'SpDef': int(spd_match.group(1)) if spd_match else 0,
                'Speed': int(spe_match.group(1)) if spe_match else 0,
            }

            # Extract abilities: .abilities = { ABILITY_OVERGROW, ABILITY_NONE, ABILITY_CHLOROPHYLL },
            abilities_match = re.search(r'\.abilities\s*=\s*\{\s*([A-Z_]+)\s*,\s*([A-Z_]+)\s*,\s*([A-Z_]+)\s*\}', species_body)
            abilities = []
            if abilities_match:
                ab1 = ability_map.get(abilities_match.group(1), abilities_match.group(1))
                ab2 = ability_map.get(abilities_match.group(2), abilities_match.group(2))
                ab3 = ability_map.get(abilities_match.group(3), abilities_match.group(3))
                # Only include non-None abilities
                abilities = [ab1 if 'None' not in ab1 else None,
                            ab2 if 'None' not in ab2 else None,
                            ab3 if 'None' not in ab3 else None]
                abilities = [ab for ab in abilities if ab is not None]

            # Extract categoryName: .categoryName = _("Seed"),
            cat_match = re.search(r'\.categoryName\s*=\s*_\("([^"]+)"\)', species_body)
            category_name = cat_match.group(1) if cat_match else None

            # Extract evolution: .evolutions = EVOLUTION({EVO_LEVEL, 16, SPECIES_IVYSAUR}),
            evo_match = re.search(r'\.evolutions\s*=\s*EVOLUTION\(\{([^}]+)\}\)', species_body)
            evolution = None
            if evo_match:
                evo_parts = [p.strip() for p in evo_match.group(1).split(',')]
                if len(evo_parts) >= 3:
                    evo_method = evo_parts[0]  # EVO_LEVEL, EVO_ITEM, etc.
                    evo_param = evo_parts[1]   # 16, ITEM_FIRE_STONE, etc.
                    evo_species = evo_parts[2] # SPECIES_IVYSAUR

                    # Convert species name
                    evo_species_name = species_map.get(evo_species, evo_species).replace('_', ' ').title()

                    # Build description
                    if 'LEVEL' in evo_method:
                        evolution = {
                            'method': 'level',
                            'param': int(evo_param),
                            'into': evo_species_name,
                            'description': f"Evolves at level {evo_param} into {evo_species_name}"
                        }
                    elif 'ITEM' in evo_method:
                        item_name = evo_param.replace('ITEM_', '').replace('_', ' ').title()
                        evolution = {
                            'method': 'item',
                            'param': evo_param,
                            'into': evo_species_name,
                            'description': f"Evolves with {item_name} into {evo_species_name}"
                        }
                    elif 'TRADE' in evo_method:
                        evolution = {
                            'method': 'trade',
                            'param': None,
                            'into': evo_species_name,
                            'description': f"Evolves when traded into {evo_species_name}"
                        }

            result[species_name] = {
                'stats': stats,
                'abilities': abilities,
                'categoryName': category_name,
                'evolution': evolution,
            }

    logger.info(f"Parsed {len(result)} Pokemon from all gen_*_families.h files")
    return result


def parse_gen6_learnsets(pokemon_names):
    """Parse level-up movesets for given Pokemon from gen_6.h.

    Args:
        pokemon_names: set of Pokemon names to look for

    Returns:
        dict: {pokemon_name -> [(level, move_name), ...]}
    """
    result = {}

    if not os.path.exists(LEARNSETS_FILE):
        logger.warning(f"Learnsets file not found: {LEARNSETS_FILE}")
        return result

    moves_data = parse_moves_data()
    moves_map = parse_moves_map()

    with open(LEARNSETS_FILE, encoding='utf-8') as f:
        content = f.read()

    # Find all learnset arrays: static const struct LevelUpMove sBulbasaurLevelUpLearnset[] = { ... }
    learnset_blocks = re.findall(
        r'static\s+const\s+struct\s+LevelUpMove\s+s(\w+)LevelUpLearnset\[\]\s*=\s*\{([^}]*LEVEL_UP_END[^}]*)\}',
        content,
        re.DOTALL
    )

    for species_const, moves_body in learnset_blocks:
        # Convert sBulbasaurLevelUpLearnset -> Bulbasaur
        species_name = species_const.replace('_', ' ').title()

        if species_name not in pokemon_names:
            continue

        # Extract all LEVEL_UP_MOVE( level, MOVE_NAME) entries
        moves = []
        move_matches = re.findall(r'LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*(MOVE_\w+)\)', moves_body)

        for level, move_const in move_matches:
            move_name = moves_map.get(move_const, move_const)
            move_info = moves_data.get(move_const, {})

            moves.append({
                'level': int(level),
                'name': move_name,
                'type': move_info.get('type', 'Unknown'),
                'power': move_info.get('power', 0),
                'accuracy': move_info.get('accuracy', 100),
            })

        result[species_name] = sorted(moves, key=lambda m: m['level'])

    logger.info(f"Parsed learnsets for {len(result)} Pokemon from gen_6.h")
    return result
