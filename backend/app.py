from flask import Flask, jsonify, send_from_directory, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_cors import CORS
from utility.getApiData import fetch_pokemons_with_details
from utility.getApiData import get_pokemon_details_by_name
from supabase import create_client
import requests, bcrypt 

app = Flask(__name__, static_folder='frontend', static_url_path="")
CORS(app)  # Enable Cross-Origin Resource Sharing for React

app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Replace with a secure key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # Access token expires in 1 hour
jwt = JWTManager(app)

#Connect to supabase (HARDCODED CREDENTIALS)
SUPABASE_URL = "https://jsvmdeqisnnopuphusbl.supabase.co"
SUPABASE_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZ"
                "SIsInJlZiI6Impzdm1kZXFpc25ub3B1cGh1c2JsIiwicm9sZSI6ImFub24"
                "iLCJpYXQiOjE3MzI2NDk0NTUsImV4cCI6MjA0ODIyNTQ1NX0.UD5kGfPAlj"
                "LWgolwvY41Dq8fMkHiitDMX9nhQjkEYy4")

#Initialise Supabase client
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)


users = []
favourites = [{"username" : "yash", "pokemon" : ["pikachu", "charizard", "bulbasaur", "charmander"] }, {"username" : "riya", "pokemon" : "charmander"}, {"username" : "kevin", "pokemon" : ["bulbasaur"]}]

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    # Serve React static files or fallback to index.html
    if path and (path.startswith("static") or path.endswith((".js", ".css", ".ico"))):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    print(users)

    # finding user in the database
    response = supabase_client.table("users").select("*").eq("username", username).execute()
    user = response.data[0] if response.data else None

    # checking if password and user matches
    if not (user and validate_password(password, user["password"])):
        return jsonify({"success": False, "message" : "credentials are incorrect"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify({"success": True, "message" : "user logged in successfully", "access_token": access_token})


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    response = supabase_client.table("users").select("*").eq("username", username).execute()
    if response.data:
        return jsonify({"success": False, "message" : "username already exists"}), 400

   
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        supabase_client.table("users").insert({"username": username, "password": hashed_password}).execute()
        access_token = create_access_token(identity=username)

        return jsonify({"success": True, "message" : "user logged in successfully", "access_token": access_token}), 201
    except Exception as e: 
        return jsonify({"success": False, "message" : "data was not received properly"}), 500 
    
# returns all the favourites
@app.route('/favourite', methods=['GET'])
@jwt_required()
def favourite():
    # data = request.json
    # token = data.get("access_token")
    username = get_jwt_identity()

    try:
        #Query the favorites table for the user's Pokémon
        response = supabase_client.table("favorites").select("pokemon_name").eq("username", username).execute()

        if response.data:
            #Return the list of Pokémon names
            #fav is a temporary variable which represents one favorite Pokemon at a time from response.data, and allows us to list them one by one
            list1 = [fav['pokemon_name'] for fav in response.data]
            i = 0
            result = {}
            for pokemon_name in list1:
                pokemons_details = get_pokemon_details_by_name(pokemon_name)
                result[i] = pokemons_details
                i += 1
            return jsonify(result), 200
        
        else:
                #No favorites found for the user
                return jsonify({"favorites": []}), 200
    except Exception as e:
        #Handle unexpected errors
        return jsonify({"error": str(e)}), 500

    # # pokemon = ''
    # result = {}
    # for user in favourites:
    #     if user["username"] == username:
    #         i = 0
    #         for pokemon in user["pokemon"]:
    #         # print(user["pokemon"])
    #             pokemons_details = get_pokemon_details_by_name(pokemon)
    #             result[i] = pokemons_details
    #             i += 1
    #         break
    # print(result)
    # return jsonify(result)

# add favourite
@app.route('/addFavourite', methods=['POST'])
@jwt_required()
def add_favourite():    
    username = get_jwt_identity()
    data = request.json
    pokemon_name = data.get("pokemon_name")

    # check if pokemon not already favourite
    response = supabase_client.table("favorites").select("*").eq("username", username).eq("pokemon_name", pokemon_name).execute()
    if response.data:
        return jsonify({"success": True}), 200 # send message that pokemon is already favourite
    
    response = supabase_client.table("favorites").insert({"username": username, "pokemon_name": pokemon_name}).execute()
    return jsonify({"success": True}), 200 # send message that pokemon was made favourite

    # for user in favourites:
    #     if user['username'] == username:
    #         if not pokemon_name in user["pokemon"]:
    #             user["pokemon"].append(pokemon_name)
    #         break
    
    # return jsonify()

# remove favourite
@app.route('/removeFavourite', methods=['POST'])
@jwt_required()
def remove_favourite():    
    username = get_jwt_identity()
    data = request.json
    pokemon_name = data.get("pokemon_name")

    try:
        #Delete the favorite from the table
        response = supabase_client.table("favorites").delete().eq("username", username).eq("pokemon_name", pokemon_name).execute()

        if response.data:
                #Matching favorite exists so successful deletion
                return jsonify({"success": True}), 200
        else:
                #No matching favorite found so no deletion
                return jsonify({"error": "Favorite not found"}), 404
    except Exception as e:
            #Handle unexpected errors
            return jsonify({"error": str(e)}), 500

    # for user in favourites:
    #     if user['username'] == username:
    #         if pokemon_name in user['pokemon']:
    #             user['pokemon'].remove(pokemon_name)
    #         break
    
    # return jsonify({"success": True})

@app.route('/api/pokemons', methods=['GET'])
def pokemons():
    # Fetch and display Pokémon data
    pokemons = fetch_pokemons_with_details(44)
    pokemons_obj = {}
    i = 0
    pokemons_obj[i] = pokemons[0]
    i += 1
    for i in range(1, len(pokemons)):
        if pokemons[i]["name"] not in pokemons[i-1]["evolution_chain"]:
            pokemons_obj[i] = pokemons[i]
        i += 1

    return jsonify(pokemons_obj)


@app.route('/api/pokemon/<name>', methods=['GET'])
def pokemon(name):
    result = {}
    pokemon = get_pokemon_details_by_name(name)
    i = 0
    if pokemon.get("evolution_chain"):
        for name in pokemon["evolution_chain"]:
            details = get_pokemon_details_by_name(name)
            if details.get("id") < 152:
                result[i] = details
                result[i]["level"] = i+1
                i += 1
    return jsonify(result)

def validate_password(input_password: str, stored_password: str) -> bool:
    """
        Verify the input password against the stored hashed password.

        :param input_password: The password provided by the user.
        :param stored_password: The hashed password stored in the database.
        :return: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8'))


if __name__ == '__main__':
    app.run(debug=True)




