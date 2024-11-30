import requests

def processPokemon(pokemon_data):
    # Fetch Pokémon species details for description and evolution chain
    species_response = requests.get(pokemon_data['species']['url'])
    species_data = species_response.json()

    # Fetch evolution chain
    evolution_chain_response = requests.get(species_data['evolution_chain']['url'])
    evolution_chain_data = evolution_chain_response.json()

    # Traverse evolution chain
    evolution_chain = []
    current = evolution_chain_data['chain']
    while current:
        evolution_chain.append(current['species']['name'])
        current = current['evolves_to'][0] if current['evolves_to'] else None

    # Extract required details
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



def get_pokemon_details_by_name(pokemon_name):    
    # Fetch Pokémon details
    pokemon_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if pokemon_response.status_code != 200:
        return {"error": f"Pokémon '{pokemon_name}' not found!"}
    pokemon_data = pokemon_response.json()
    # print(pokemon_data)
    processed_data = processPokemon(pokemon_data)
    return processed_data



def fetch_pokemons_with_details(limit=5):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching data.")
        return []
    
    pokemon_list = response.json()["results"]
    result = []
    # print(pokemon_list[0:3])
    
    for pokemon in pokemon_list:
        pokemon_data = requests.get(pokemon["url"]).json()

        processed_data = processPokemon(pokemon_data)
        result.append(processed_data)

    return result



# # funciton to fetch pokemon data from api
# def fetch_pokemons_with_details(limit=3):
#     url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         print("Error fetching data.")
#         return []
    
#     pokemon_list = response.json()["results"]
#     result = []
    
#     for pokemon in pokemon_list:
#         pokemon_data = requests.get(pokemon["url"]).json()
        
#         # Extract basic fields
#         name = pokemon_data["name"]
#         image = pokemon_data["sprites"]["front_default"]
#         hp = next(stat["base_stat"] for stat in pokemon_data["stats"] if stat["stat"]["name"] == "hp")
#         attack = next(stat["base_stat"] for stat in pokemon_data["stats"] if stat["stat"]["name"] == "attack")
#         defense = next(stat["base_stat"] for stat in pokemon_data["stats"] if stat["stat"]["name"] == "defense")
#         speed = next(stat["base_stat"] for stat in pokemon_data["stats"] if stat["stat"]["name"] == "speed")
#         weight = pokemon_data["weight"]  # Weight in hectograms (hgs)
#         types = [t["type"]["name"] for t in pokemon_data["types"]]
#         abilities = [a["ability"]["name"] for a in pokemon_data["abilities"]]
#         moves = [m["move"]["name"] for m in pokemon_data["moves"]]
        
#         # Fetch description from species endpoint
#         species_url = pokemon_data["species"]["url"]
#         species_data = requests.get(species_url).json()

#         evolution_chain_url = species_data["evolution_chain"]["url"]
#         evolution_chain_data = requests.get(evolution_chain_url).json()

#         evolution_chain = []
#         current = evolution_chain_data['chain']
#         while current:
#             evolution_chain.append(current['species']['name'])
#             if current['evolves_to']:
#                 current = current['evolves_to'][0]
#             else:
#                 current = None

#         descriptions = [
#             entry["flavor_text"] for entry in species_data["flavor_text_entries"] 
#             if entry["language"]["name"] == "en"
#         ]
#         description = descriptions[0].replace("\n", " ").replace("\f", " ") if descriptions else "No description available."
        
#         # Add to results
#         result.append({
#             "name": name,
#             "image": image,
#             "hp": hp,
#             "attack": attack,
#             "defense": defense,
#             "speed": speed,
#             "weight": weight,
#             "types": types,
#             "abilities": abilities,
#             "moves": moves,
#             "description": description, 
#              "evolution_chain": evolution_chain
#         })
    
#     return result