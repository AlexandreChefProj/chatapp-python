from pymongo import MongoClient
import bcrypt
from app import db
from datetime import datetime


# --- User Management ---
def register_user(username, email, password):
    """Register a new user."""
    if db.users.find_one({"email": email}):
        return {"success": False, "message": "Email already in use"}
    if db.users.find_one({"username": username}):
        return {"success": False, "message": "Username already in use"}

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert new user (MongoDB will auto-generate the _id)
    db.users.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })

    return {"success": True, "message": "User registered successfully"}


def get_user_by_email(email):
    """Fetch a user by email."""
    return db.users.find_one({"email": email})


def get_user_by_username(username):
    """Fetch a user by username."""
    return db.users.find_one({"username": username})


def check_password(stored_password, provided_password):
    """Validate a password."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


# --- Chat Message Management ---

def save_message(username, message):
    print("saving a message.")
    """Save a chat message to the database."""
    db.messages.insert_one({
        "username": username,
        "message": message,
        "timestamp": datetime.utcnow()
    })


def get_chat_history(limit=50):
    print("retrieved last chat history")
    return list(db.messages.find().sort("timestamp", -1).limit(limit))[::-1]  # Reverse to show oldest first
