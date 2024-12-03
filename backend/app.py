from flask import Flask, jsonify, send_from_directory, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_cors import CORS
from utility.getApiData import fetch_pokemons_with_details
from utility.getApiData import get_pokemon_details_by_name

app = Flask(__name__, static_folder='frontend', static_url_path="")
CORS(app)  # Enable Cross-Origin Resource Sharing for React

app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Replace with a secure key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # Access token expires in 1 hour
jwt = JWTManager(app)

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
    
    if username:
        for user in users:
            if user["username"] == username and user["password"] == password:
                access_token = create_access_token(identity=username)
                return jsonify({"success": True, "message" : "user logged in successfully", "access_token": access_token})
        return jsonify({"success": False, "message" : "credentials are incorrect"})
    else:
        return jsonify({"success": False, "message" : "data was not received properly"})
    

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username:
        for user in users:
            if user["username"] == username:
                return jsonify({"success": False, "message" : "username already exists"})
        users.append({"username": username, "password": password})
        access_token = create_access_token(identity=username)
        return jsonify({"success": True, "message" : "user logged in successfully", "access_token": access_token})
    else:
        return jsonify({"success": False, "message" : "data was not received properly"})

@app.route('/favourite', methods=['GET'])
@jwt_required()
def favourite():
    # data = request.json
    # token = data.get("access_token")
    username = get_jwt_identity()
    pokemon = ''
    result = {}
    for user in favourites:
        if user["username"] == username:
            i = 0
            for pokemon in user["pokemon"]:
            # print(user["pokemon"])
                pokemons_details = get_pokemon_details_by_name(pokemon)
                result[i] = pokemons_details
                i += 1
            break
    print(result)
    return jsonify(result)

@app.route('/addFavourite', methods=['POST'])
@jwt_required()
def add_favourite():    
    username = get_jwt_identity()
    data = request.json
    pokemon_name = data.get("pokemon_name")

    for user in favourites:
        if user['username'] == username:
            if not pokemon_name in user["pokemon"]:
                user["pokemon"].append(pokemon_name)
            break
    
    return jsonify({"success": True})


@app.route('/removeFavourite', methods=['POST'])
@jwt_required()
def remove_favourite():    
    username = get_jwt_identity()
    data = request.json
    pokemon_name = data.get("pokemon_name")

    for user in favourites:
        if user['username'] == username:
            if pokemon_name in user['pokemon']:
                user['pokemon'].remove(pokemon_name)
            break
    
    return jsonify({"success": True})

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


if __name__ == '__main__':
    app.run(debug=True)




