import pytest

from src.app import get_pokemon_data


# Test the function with an example Pokémon (e.g., "Pikachu")
@pytest.mark.parametrize("pokemon_name, types, hp",[
    ("Charizard", ["fire", "flying"], 78),
    ("charmander", ["fire"], 39),
], ids=["Charizard", "charmander"])
def test_Pokemon_data_fetched_through_API(pokemon_name, types, hp):

    pokemon_data = get_pokemon_data(pokemon_name)

    assert pokemon_data['types'] == types
    assert pokemon_data['hp'] == hp

    # if pokemon_data:
    #     print(f"Name: {pokemon_data['name']}")
    #     print(f"Types: {', '.join(pokemon_data['types'])}")
    #     print(f"HP: {pokemon_data['hp']}")  # Pokémon's HP
    # else:
    #     print("Pokémon data not found.")

