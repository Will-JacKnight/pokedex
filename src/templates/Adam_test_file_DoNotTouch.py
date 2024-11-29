import requests
import re
import string  # For generating all letters of the alphabet

# Step 1: Fetch Pokémon names from the Pokémon API
def fetch_first_gen_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"  # Fetch the first 151 Pokémon
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_names = [pokemon['name'] for pokemon in data['results']]
        return pokemon_names
    else:
        raise Exception("Failed to fetch Pokémon data")

# Step 2: Filter Pokémon names using regex for all letters of the alphabet
def search_pokemon_by_all_letters(pokemon_names):
    pokemon_by_letter = {}
    for letter in string.ascii_lowercase:  # Iterate over all letters (a-z)
        # Create a regex pattern for names starting with the current letter
        pattern = re.compile(f"^{letter}", re.IGNORECASE)
        # Filter Pokémon names matching the pattern
        filtered_pokemon = [name for name in pokemon_names if pattern.match(name)]
        # Add to the dictionary
        pokemon_by_letter[letter] = filtered_pokemon
    return pokemon_by_letter

# Step 3: Test the function
try:
    # Fetch Pokémon names
    pokemon_names = fetch_first_gen_pokemon()

    # Get Pokémon grouped by starting letter
    pokemon_by_letter = search_pokemon_by_all_letters(pokemon_names)

    # Print Pokémon grouped by letters
    for letter, pokemon_list in pokemon_by_letter.items():
        print(f"Pokémon starting with '{letter.upper()}': {pokemon_list}")

except Exception as e:
    print("Error:", e)





# import requests
# import re
#
# # Step 1: Fetch Pokémon names from the Pokémon API
# def fetch_first_gen_pokemon():
#     url = "https://pokeapi.co/api/v2/pokemon?limit=151"  # Fetch the first 151 Pokémon
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         pokemon_names = [pokemon['name'] for pokemon in data['results']]
#         return pokemon_names
#     else:
#         raise Exception("Failed to fetch Pokémon data")
#
# # Step 2: Filter Pokémon names using regex
# def search_pokemon_by_letter(letter, pokemon_names):
#     # Create a regex pattern for names starting with the input letter (case-insensitive)
#     pattern = re.compile(f"^{letter}", re.IGNORECASE)
#     filtered_pokemon = [name for name in pokemon_names if pattern.match(name)]
#     return filtered_pokemon
#
# # Step 3: Test the function for letter "A"
# try:
#     # Fetch Pokémon names
#     pokemon_names = fetch_first_gen_pokemon()
#     print("All Pokémon fetched:", pokemon_names)
#
#     # Test search for Pokémon starting with "A"
#     search_letter = "a"
#     results = search_pokemon_by_letter(search_letter, pokemon_names)
#     print(f"Pokémon starting with '{search_letter}':", results)
#
# except Exception as e:
#     print("Error:", e)
