
import requests

# Function to fetch Pokémon name and types from the PokeAPI
def get_pokemon_types(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract the Pokémon name and types from the response
        pokemon_data = {
            'name': data['name'],
            'types': [type_info['type']['name'] for type_info in data['types']],  # Pokémon types (e.g., electric, fire)
            'hp': next(stat['base_stat'] for stat in data['stats'] if stat['stat']['name'] == 'hp'),  # HP stat (e.g., 45)

        }
        
        return pokemon_data
    else:
        return None

# Test the function with an example Pokémon (e.g., "Pikachu")
pokemon_name = "Charizard"
pokemon_data = get_pokemon_types(pokemon_name)

if pokemon_data:
    print(f"Name: {pokemon_data['name']}")
    print(f"Types: {', '.join(pokemon_data['types'])}")
    print(f"HP: {pokemon_data['hp']}")  # Pokémon's HP

else:
    print("Pokémon data not found.")



# import requests

# # Define the URL for the Pokémon list API
# url = "https://pokeapi.co/api/v2/pokemon/"

# # Define parameters (limit for the number of results, you can change it to 100 max)
# params = {'limit': 20}  # This will fetch the first 20 Pokémon

# # Send a GET request to the API
# response = requests.get(url, params=params)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     data = response.json()
    
#     # Print the total number of Pokémon and the first 20 Pokémon names along with their image URLs
#     print(f"Total Pokémon: {data['count']}")
#     print("First 20 Pokémon:")
    
#     for pokemon in data['results']:
#         # Fetch detailed Pokémon information, including sprite images
#         pokemon_url = pokemon['url']
#         pokemon_data = requests.get(pokemon_url).json()

#         # Get the front sprite (default and shiny) from the sprites data
#         front_sprite = pokemon_data['sprites']['front_default']
#         shiny_sprite = pokemon_data['sprites']['front_shiny']


#         # Display Pokémon name and image URLs
#         print(f"Name: {pokemon['name']}")
#         print(f"Image URL: {front_sprite}")
#         print(f"Shiny Image URL: {shiny_sprite}")
#         print("-" * 50)

# else:
#     print("Error fetching data:", response.status_code)
