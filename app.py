from flask import Flask, request, jsonify
import jwt
import datetime
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

JWT_SECRET = os.getenv("JWT_SECRET", "secret123")

# database user
users = {
    "dadar1@example.com": {
        "password": "dadar123",
        "name": "User Satu"
    }
}


# LOGIN 

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users.get(email)

    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "sub": email,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return jsonify({"access_token": token})



# ITEMS 

@app.route("/items", methods=["GET"])
def get_items():
    items = [
        {"id": 1, "name": "Laptop", "price": 35000000},
        {"id": 2, "name": "Mouse", "price": 100000},
        {"id": 3, "name": "Keyboard", "price": 500000}
    ]
    return jsonify({"items": items})



# PROFILE 

@app.route("/profile", methods=["PUT"])
def update_profile():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = decoded["email"]
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    # cek user di database
    user = users.get(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # data baru dari body
    data = request.get_json()
    name = data.get("name")
    new_email = data.get("email")

    if name:
        user["name"] = name
    if new_email:
        users[new_email] = users.pop(email)
        email = new_email

    return jsonify({
        "message": "Profile updated",
        "profile": {"name": user["name"], "email": email}
    })


if __name__ == "__main__":
    app.run(debug=True)
