from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
from collections import Counter

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

def normalize_species_name(name):
    return re.sub(r'\s*\(.*?\)$', '', name)

def parse_pokemon_data(data):
    pokemons = []
    pokemon_data = {}

    lines = data.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("Ability:"):
            pokemon_data["ability"] = line.split(": ")[1].strip()
        elif line.startswith("EVs:"):
            evs = line.split(": ")[1].strip()
            pokemon_data["evs"] = dict(re.findall(r'(\d+) (\w+)', evs))
        elif line.startswith("IVs:"):
            ivs = line.split(": ")[1].strip()
            pokemon_data["ivs"] = dict(re.findall(r'(\d+) (\w+)', ivs))
        elif line.startswith("-"):
            pokemon_data["moves"].append(line.strip().replace("-", "").strip())
        else:
            if "@ " in line:
                if pokemon_data:
                    pokemons.append(pokemon_data)
                    pokemon_data = {}
                parts = line.split("@")
                pokemon_data["species"] = normalize_species_name(parts[0].strip())
                pokemon_data["item"] = parts[1].strip()
                pokemon_data["moves"] = []
            elif line.endswith("Nature"):
                pokemon_data["nature"] = line.split()[0].strip()

    if pokemon_data:
        pokemons.append(pokemon_data)

    return pokemons

def calculate_usage(pokemons):
    species_counts = Counter(pokemon["species"] for pokemon in pokemons)
    total_pokemons = sum(species_counts.values())
    usage_rates = {species: count / total_pokemons * 100 for species, count in species_counts.items()}
    return usage_rates

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.json['data']
    parsed_data = parse_pokemon_data(data)
    usage_rates = calculate_usage(parsed_data)
    return jsonify(usage_rates)

if __name__ == '__main__':
    app.run(debug=True)
