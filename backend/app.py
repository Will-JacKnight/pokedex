from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from utility.getApiData import fetch_pokemons_with_details
from utility.getApiData import get_pokemon_details_by_name

app = Flask(__name__, static_folder='frontend', static_url_path="")
CORS(app)  # Enable Cross-Origin Resource Sharing for React

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    # Serve React static files or fallback to index.html
    if path and (path.startswith("static") or path.endswith((".js", ".css", ".ico"))):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

# Test API endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    # return "hello world"
    return jsonify({"message": "Hello from Flask!"})

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




