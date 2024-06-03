from collections import Counter

def calculate_usage(pokemons):
    species_counts = Counter(pokemon["species"] for pokemon in pokemons)
    total_pokemons = sum(species_counts.values())
    usage_rates = {species: count / total_pokemons * 100 for species, count in species_counts.items()}
    return usage_rates

usage_rates = calculate_usage(parsed_data)
print(usage_rates)
