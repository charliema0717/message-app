import os

from flask import Flask, request, jsonify, json
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# File directory
FILE_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(FILE_DIR, exist_ok=True)

#File paths
USERS_FILE = os.path.join(FILE_DIR, "user.json")
MESSAGES_FILE = os.path.join(FILE_DIR, "messages.json")

# Hash passwords when initializing users
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([
            {"id": 1, "username": "admin", "password": generate_password_hash("admin123"), "role": "admin"},
            {"id": 2, "username": "user", "password": generate_password_hash("user123"), "role": "readonly"}
        ], f)

if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, "w") as f:
        json.dump([
            {"id": 1, "userId": 1, "message": "Welcome to the message board!"},
            {"id": 2, "userId": 1, "message": "This is a sample message."}
        ], f)

def get_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        return jsonify({"msg": f"Error reading users file: {str(e)}"}), 500

def get_messages():
    with open(MESSAGES_FILE, "r") as f:
        return json.load(f)
    
def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    users = get_users()
    user = next((u for u in users if u['username'] == username and check_password_hash(u['password'], password)), None)

    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity={
        "id": user["id"],
        "username": user["username"],
        "role": user["role"]
    })

    return jsonify({
        "token": access_token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    })

@app.route('/api/messages', methods=['GET'])
@jwt_required()
def get_all_messages():
    current_user = get_jwt_identity()
    if current_user["role"] not in ["admin", "readonly"]:
        return jsonify({"msg": "Permission denied"}), 403
    
    # Get all messages with pagination support
    messages = get_messages()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify(messages[start:end])

@app.route('/api/messages', methods=['POST'])
@jwt_required()
def create_message():
    # Get current user from JWT
    current_user = get_jwt_identity()

    # Verify user role
    if current_user["role"] != "admin":
        return jsonify({"msg": "Permission denied. Admin role required."}), 403
    
    # Get new message content from request
    message_content = request.json.get('message')
    if not message_content or not isinstance(message_content, str):
        return jsonify({"msg": "Message content must be a non-empty string"}), 400
    
    # Load existing messages
    messages = get_messages()

    # Add new message
    new_id = max([m["id"] for m in messages], default=0) + 1
    new_message = {
        "id": new_id,
        "userId": current_user["id"],
        "message": message_content
    }

    messages.append(new_message)
    save_messages(messages)
    
    return jsonify(new_message), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
