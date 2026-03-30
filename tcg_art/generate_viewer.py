import csv
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'card-lists')
OUTPUT_DIR = os.path.join(BASE_DIR, 'viewers')

# Mapping CSV files to image directories
SET_MAPPING = {
    'Pokemon-Delta-Species.csv': 'ex_delta_species',
    'Pokemon-Crystal-Guardians.csv': 'ex_crystal_guardians',
    'Pokemon-Dragon-Frontiers.csv': 'ex-dragon_frontiers',
    'Pokemon-Holon-Phantoms.csv': 'ex_holon_phantoms',
    'Pokemon-Legend-Maker.csv': 'ex_legend_maker'
}

# CSS for a premium look
CSS = """
:root {
    --bg-color: #0d1117;
    --card-bg: #161b22;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;
    --accent: #58a6ff;
    --border: #30363d;
}

body {
    background-color: var(--bg-color);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 20px;
}

header {
    text-align: center;
    padding: 40px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
}

h1 {
    font-size: 2.5rem;
    color: var(--accent);
    margin: 0;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.card-item {
    background-color: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.card-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
}

.card-image-container {
    aspect-ratio: 5 / 7;
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.card-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.card-details {
    padding: 15px;
}

.card-name {
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 5px;
    display: block;
}

.card-meta {
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.card-number {
    float: right;
    color: var(--accent);
}
"""

def generate_html(csv_file, img_dir, set_name):
    csv_path = os.path.join(CSV_DIR, csv_file)
    cards = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Extract number for matching image, e.g., "1/113" -> "1"
            number_parts = row['Number'].split('/')
            card_num = number_parts[0]
            img_path = f"../{img_dir}/{card_num}_hires.png"
            
            cards.append({
                'name': row['Name'],
                'number': row['Number'],
                'rarity': row['Rarity'],
                'img_path': img_path
            })

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{set_name} - TCG Viewer</title>
    <style>{CSS}</style>
</head>
<body>
    <header>
        <h1>{set_name}</h1>
    </header>
    <div class="card-grid">
"""
    
    for card in cards:
        html_content += f"""
        <div class="card-item">
            <div class="card-image-container">
                <img src="{card['img_path']}" alt="{card['name']}" class="card-image" loading="lazy">
            </div>
            <div class="card-details">
                <span class="card-number">#{card['number']}</span>
                <span class="card-name">{card['name']}</span>
                <div class="card-meta">{card['rarity']}</div>
            </div>
        </div>
"""
        
    html_content += """
    </div>
</body>
</html>
"""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_filename = csv_file.replace('.csv', '.html')
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated {output_path}")

def generate_index(set_data):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TCG Art Viewer Index</title>
    <style>
        {CSS}
        .set-list {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            max-width: 600px;
            margin: 40px auto;
        }}
        .set-link {{
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            padding: 20px;
            border-radius: 12px;
            text-decoration: none;
            color: var(--text-primary);
            font-weight: 600;
            font-size: 1.2rem;
            transition: border-color 0.2s, background-color 0.2s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .set-link:hover {{
            border-color: var(--accent);
            background-color: #1c2128;
        }}
        .set-link::after {{
            content: '→';
            color: var(--accent);
        }}
    </style>
</head>
<body>
    <header>
        <h1>TCG Art Viewers</h1>
    </header>
    <div class="set-list">
"""
    for name, link in set_data:
        html_content += f'        <a href="{link}" class="set-link">{name}</a>\n'
        
    html_content += """
    </div>
</body>
</html>
"""
    output_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {output_path}")

def main():
    set_data = []
    for csv_file, img_dir in SET_MAPPING.items():
        set_name = csv_file.replace('Pokemon-', '').replace('.csv', '').replace('-', ' ')
        generate_html(csv_file, img_dir, set_name)
        link = csv_file.replace('.csv', '.html')
        set_data.append((set_name, link))
    
    generate_index(set_data)

if __name__ == "__main__":
    main()
