import pytest
from supabase import create_client

from app import validate_password
from utility.getApiData import fetch_pokemons_with_details, get_pokemon_details_by_name

#Connect to supabase (HARDCODED CREDENTIALS)
SUPABASE_URL = "https://jsvmdeqisnnopuphusbl.supabase.co"
SUPABASE_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZ"
                "SIsInJlZiI6Impzdm1kZXFpc25ub3B1cGh1c2JsIiwicm9sZSI6ImFub24"
                "iLCJpYXQiOjE3MzI2NDk0NTUsImV4cCI6MjA0ODIyNTQ1NX0.UD5kGfPAlj"
                "LWgolwvY41Dq8fMkHiitDMX9nhQjkEYy4")

#Initialise Supabase client
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Test data fetch with get_pokemon_details_by_name(pokemon_name) function with example Pokémons
@pytest.mark.parametrize("pokemon_name, types, hp",[
    ("Charizard", ["fire", "flying"], 78),
    ("charmander", ["fire"], 39),
    ("bulbasaur", ['grass', 'poison'], 45),
], ids=["Charizard", "charmander", "bulbasaur"])
def test_getting_Pokemon_detail_by_name_through_API(pokemon_name, types, hp):
    pokemon_data = get_pokemon_details_by_name(pokemon_name)
    assert pokemon_data['types'] == types
    assert pokemon_data['hp'] == hp

# Test fetch_pokemons_with_details(limit) function with example Pokémons
# only test for limited but essential details
@pytest.mark.parametrize("limit, ids, hp",[
    (1, [1], [45]),
    (2, [1, 2], [45, 60]),
], ids=["first pokemon","first 2 pokemons"])
def test_fetching_pokemons_with_details(limit, ids, hp):
    detailed_data = fetch_pokemons_with_details(limit)
    API_ids = [pokemon['id'] for pokemon in detailed_data]
    API_hps = [pokemon['hp'] for pokemon in detailed_data]
    assert API_ids == ids
    assert API_hps == hp

# Test if the given username and password match with the record in database
@pytest.mark.parametrize("username, password", [
    ("test_user_for_pw_check", "hashed_password"),
], ids=["test_user"])
def test_validate_password_with_given_username_from_database(username, password):
    response = supabase_client.table("users").select("*").eq("username", username).execute()
    user = response.data[0]
    assert validate_password(password, user['password'])


# test adding a new favorite pokemon to a user and remove that after the test
@pytest.mark.parametrize("username, pokemon_name", [
    ("test_user", "Pikachu")
], ids=["test_user"])
def test_adding_favorite_pokemon_check_if_stored_in_database(username, pokemon_name):
    # remove old favorites if exists
    (supabase_client.table("favorites")
     .delete().eq("username", username).eq("pokemon_name",pokemon_name).execute())

    # add new favorite pokemon to the test_user
    (supabase_client.table("favorites")
     .insert({"username": username, "pokemon_name": pokemon_name}).execute())

    # fetch the list of favorite pokemon for the given user
    response = (supabase_client.table("favorites")
                .select("pokemon_name").eq("username", username).execute())

    # check if the new favorite is in the list
    favorite_pokemon_names = [fav["pokemon_name"] for fav in response.data]

    assert pokemon_name in favorite_pokemon_names


