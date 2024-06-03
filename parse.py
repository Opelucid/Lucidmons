import re

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
                pokemon_data["species"] = parts[0].strip()
                pokemon_data["item"] = parts[1].strip()
                pokemon_data["moves"] = []
            elif line.endswith("Nature"):
                pokemon_data["nature"] = line.split()[0].strip()
    
    if pokemon_data:
        pokemons.append(pokemon_data)
    
    return pokemons

def read_data_from_file(file_path):
    with open(file_path, "r") as file:
        data = file.read()
    return data

file_path = "pokemon_data.txt"
data = read_data_from_file(file_path)
parsed_data = parse_pokemon_data(data)
print(parsed_data)
