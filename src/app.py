from flask import Flask, render_template, request, jsonify
import requests
from supabase import create_client

#Connect to supabase (HARDCODED CREDENTIALS)
SUPABASE_URL = "https://jsvmdeqisnnopuphusbl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impzdm1kZXFpc25ub3B1cGh1c2JsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI2NDk0NTUsImV4cCI6MjA0ODIyNTQ1NX0.UD5kGfPAljLWgolwvY41Dq8fMkHiitDMX9nhQjkEYy4"

#Initialise Supabase client
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# Home page
@app.route("/")
def home_page():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login_page():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if email and password are provided
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Query the database for the user
    response = supabase_client.table("users").select("*").eq("username", email).execute()
    user = response.data[0] if response.data else None

    # If user does not exist
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Verify the password
    if password != user['password_hash']:
        return jsonify({"error": "Invalid email or password"}), 401

    # Successful login
    return jsonify({"message": "Login successful", "user": {"id": user['id'], "username": user['username']}}), 200


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