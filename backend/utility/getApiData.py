import requests

# This function is used to process the pokemon details and return a dictionary with the required details
def processPokemon(pokemon_data):
    # Fetch Pokémon species details for description and evolution chain using the species url
    species_response = requests.get(pokemon_data['species']['url'])
    species_data = species_response.json()

    # Fetch evolution chain using the evolution chain url
    evolution_chain_response = requests.get(species_data['evolution_chain']['url'])
    evolution_chain_data = evolution_chain_response.json()

    # loop through the evolution chain and append the species names to a list
    evolution_chain = []
    current = evolution_chain_data['chain']
    while current:
        evolution_chain.append(current['species']['name'])
        current = current['evolves_to'][0] if current['evolves_to'] else None

    # Extract required details from the pokemon_data dictionary
    details = {
        "name": pokemon_data["name"],
        "id": pokemon_data["id"],
        "image": pokemon_data["sprites"]["front_default"],
        "hp": next(stat["base_stat"] for stat in pokemon_data["stats"] if stat["stat"]["name"] == "hp"),
        "attack": next(stat["base_stat"] for stat in pokemon_data["stats"] if stat["stat"]["name"] == "attack"),
        "defense": next(stat["base_stat"] for stat in pokemon_data["stats"] if stat["stat"]["name"] == "defense"),
        "speed": next(stat["base_stat"] for stat in pokemon_data["stats"] if stat["stat"]["name"] == "speed"),
        "weight": pokemon_data["weight"],
        "types": [ptype["type"]["name"] for ptype in pokemon_data["types"]],
        "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
        "moves": [move["move"]["name"] for move in pokemon_data["moves"]],
        "description": next(
            entry["flavor_text"] for entry in species_data["flavor_text_entries"]
            if entry["language"]["name"] == "en"
        ),
        "evolution_chain": evolution_chain
        
    }
    details["moves"] = details["moves"][:4] # limiting the number of moves to 4
    return details


# This function is used to fetch the details of a pokemon by its name
def get_pokemon_details_by_name(pokemon_name):    
    # This api endpoint returns directly a dictionary with the pokemon details
    pokemon_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if pokemon_response.status_code != 200:
        return {"error": f"Pokémon '{pokemon_name}' not found!"}
    pokemon_data = pokemon_response.json()
    # call the processPokemon function to process the pokemon details
    processed_data = processPokemon(pokemon_data)
    # returning the processed pokemon details
    return processed_data


# Used to fetch a certan number of pokemons with their details
# limit is the number of pokemons to be fetched
def fetch_pokemons_with_details(limit=5):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching data.")
        return []
    # this api endpoint returns a list of pokemons with a url to their details
    pokemon_list = response.json()["results"]
    result = []
    
    # looping through the list of pokemons and fetching their details using the url
    for pokemon in pokemon_list:
        pokemon_data = requests.get(pokemon["url"]).json()

        processed_data = processPokemon(pokemon_data)
        result.append(processed_data)

    # returning the list of pokemons with their details
    return result

