from flask import Flask, request, jsonify
from supabase import create_client

#Connect to supabase (HARDCODED CREDENTIALS) 
SUPABASE_URL = "https://jsvmdeqisnnopuphusbl.supabase.co"
SUPABASE_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
				"Impzdm1kZXFpc25ub3B1cGh1c2JsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI2NDk0NT"
				"UsImV4cCI6MjA0ODIyNTQ1NX0.UD5kGfPAljLWgolwvY41Dq8fMkHiitDMX9nhQjkEYy4")

#Initialise Supabase client 
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#Initialise Flask app 
app = Flask(__name__)

@app.route('/')
def home():
	    return "Hello, Pokedex!"


@app.route('/test-supabase')
def test_supabase():
    try:
        # Test fetching data from the "users" table
        response = supabase.table("users").select("*").execute()
        return {"data": response.data}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/login', methods=['POST'])
def login():
	data = request.json
	email = data.get('email')
	password = data.get('password')
	
	#Check if email and password are provided
	if not email or not password: 
			return jsonify({"error": "Email and password are required"}), 400

	#Query the database for the user
	response = supabase.table("users").select("*").eq("username", email).execute()
	user = response.data[0] if response.data else None

	#If user does not exist 
	if not user:
			return jsonify({"error": "Invalid email or password"}), 401

	#Verify the password 
	if password != user['password_hash']:
			return jsonify({"error": "Invalid email or password"}), 401

	#Successful login 
	return jsonify({"message": "Login successful", "user": {"id": user['id'], "username": user['username']}}), 200 


if __name__ == "__main__":
    app.run(debug=True)
