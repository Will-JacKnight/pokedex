import pytest
from supabase import create_client

from app import get_pokemon_data

#Connect to supabase (HARDCODED CREDENTIALS)
SUPABASE_URL = "https://jsvmdeqisnnopuphusbl.supabase.co"
SUPABASE_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZ"
                "SIsInJlZiI6Impzdm1kZXFpc25ub3B1cGh1c2JsIiwicm9sZSI6ImFub24"
                "iLCJpYXQiOjE3MzI2NDk0NTUsImV4cCI6MjA0ODIyNTQ1NX0.UD5kGfPAlj"
                "LWgolwvY41Dq8fMkHiitDMX9nhQjkEYy4")

#Initialise Supabase client
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)


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


# test if username and password match with the record in database
@pytest.mark.parametrize("username, password", [
    ("test_user", "test_<PASSWORD>"),
    ("pokemaster", "pokepoke123")
], ids=["test_user"])
def test_if_username_password_match(username, password):
    pass