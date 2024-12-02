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


# test if the given username and password match with the record in database
@pytest.mark.parametrize("username, password", [
    ("test_user", "hashed_password"),
    ("another_user", "another_password"),
    ("last_user", "last_password"),
], ids=["test_user", "another_user", "last_user"])
def test_if_username_password_match(username, password):
    response = supabase_client.table("users").select("*").eq("username", username).execute()
    user = response.data[0]
    assert user['password_hash'] == password


# test adding a new favorite pokemon to a user and remove that after the test
@pytest.mark.parametrize("user_id, pokemon_name", [
    ("03d6b91e-5e5a-4530-bbea-a4ea5472e707", "Pikachu")
], ids=["test_user"])
def test_adding_favorite_pokemon_check_if_stored_in_database(user_id, pokemon_name):
    # remove old favorites if exists
    (supabase_client.table("favorites")
     .delete().eq("user_id", user_id).eq("pokemon_name",pokemon_name).execute())

    # add new favorite pokemon to the test_user
    (supabase_client.table("favorites")
     .insert({"user_id": user_id, "pokemon_name": pokemon_name}).execute())

    # fetch the list of favorite pokemon for the given user
    response = (supabase_client.table("favorites")
                .select("pokemon_name").eq("user_id", user_id).execute())

    # check if the new favorite is in the list
    favorite_pokemon_names = [fav["pokemon_name"] for fav in response.data]
    assert pokemon_name in favorite_pokemon_names