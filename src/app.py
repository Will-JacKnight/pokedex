from flask import Flask, render_template, request, jsonify
import requests, bcrypt
from supabase import create_client

#Connect to supabase (HARDCODED CREDENTIALS)
SUPABASE_URL = "https://jsvmdeqisnnopuphusbl.supabase.co"
SUPABASE_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZ"
                "SIsInJlZiI6Impzdm1kZXFpc25ub3B1cGh1c2JsIiwicm9sZSI6ImFub24"
                "iLCJpYXQiOjE3MzI2NDk0NTUsImV4cCI6MjA0ODIyNTQ1NX0.UD5kGfPAlj"
                "LWgolwvY41Dq8fMkHiitDMX9nhQjkEYy4")

#Initialise Supabase client
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# Home page
@app.route("/")
def home_page():
    return render_template("login.html")


@app.route('/register', methods=["GET"])
def show_signup_page():
    return render_template("signup_test.html")


@app.route('/login', methods=["GET"])
def show_login_page():
    return  render_template("login_test.html")


@app.route('/register', methods=['POST'])
def register_user():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password: 
        return jsonify({"error": "Username and password are required"}), 400

    response = supabase_client.table("users").select("*").eq("username", username).execute()
    if response.data:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        supabase_client.table("users").insert({"username": username, "password": hashed_password}).execute()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e: 
        return jsonify({"error": str(e)}), 500 


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    # Query the database for the user
    response = supabase_client.table("users").select("*").eq("username", username).execute()
    user = response.data[0] if response.data else None

    # If user does not exist
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

  # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({"error": "Invalid username or password"}), 401


    # Successful login
    return jsonify({"message": "Login successful", "user": {"id": user['id'], "username": user['username']}}), 200


@app.route('/favorite', methods=['POST'])
def favorite_pokemon():
    data = request.json
    user_id = data.get('user_id')
    pokemon_name = data.get('pokemon_name')

    if not user_id or not pokemon_name:
        return jsonify({"error": "User ID and Pokemon name are required"}), 400

    # Check if the Pokémon is already a favorite
    response = supabase_client.table("favorites").select("*").eq("user_id", user_id).eq("pokemon_name", pokemon_name).execute()
    if response.data:
        return jsonify({"error": "This Pokemon is already in your favorites"}), 400

    # Add to favorites
    response = supabase_client.table("favorites").insert({"user_id": user_id, "pokemon_name": pokemon_name}).execute()
    return jsonify({"message": f"{pokemon_name} added to favorites"}), 200


@app.route('/favorites/<user_id>', methods=['GET'])
def list_favorites(user_id):
    try:
        #Query the favorites table for the user's Pokémon
        response = supabase_client.table("favorites").select("pokemon_name").eq("user_id", user_id).execute()

        if response.data:
                #Return the list of Pokémon names
                #fav is a temporary variable which represents one favorite Pokemon at a time from response.data, and allows us to list them one by one
                return jsonify({"favorites": [fav['pokemon_name'] for fav in response.data]}), 200
        else:
                #No favorites found for the user
                return jsonify({"favorites": []}), 200
    except Exception as e:
        #Handle unexpected errors
        return jsonify({"error": str(e)}), 500


@app.route('/favorite', methods=['DELETE'])
def remove_favorite():
    data = request.json
    user_id = data.get('user_id')
    pokemon_name = data.get('pokemon_name')

    #Validate input
    if not user_id or not pokemon_name:
        return jsonify({"error": "User ID and Pokémon name are required"}), 400

    try:
        #Delete the favorite from the table
        response = supabase_client.table("favorites").delete().eq("user_id", user_id).eq("pokemon_name", pokemon_name).execute()

        if response.data:
                #Matching favorite exists so successful deletion
                return jsonify({"message": f"{pokemon_name} removed from favorites"}), 200
        else:
                #No matching favorite found so no deletion
                return jsonify({"error": "Favorite not found"}), 404
    except Exception as e:
            #Handle unexpected errors
            return jsonify({"error": str(e)}), 500


# Function to fetch Pokémon name and types from the PokeAPI
def get_pokemon_data(pokemon_name):
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

def fetch_data_from_users_table():
    try:
        # Test fetching data from the "users" table
        response = supabase_client.table("users").select("*").execute()
        return {"data": response.data}, 200
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True)
