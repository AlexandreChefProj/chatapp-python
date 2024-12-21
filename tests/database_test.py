import pytest
from app.database import (
    register_user, 
    get_user_by_email,  
    check_password, 
    save_message, 
    get_chat_history
)
from mongomock import MongoClient
from datetime import datetime

# Set up the mock database
@pytest.fixture
def mock_db():
    client = MongoClient()
    db = client.test_db
    return db

def test_register_user(mock_db, monkeypatch):
    # Patch the database
    monkeypatch.setattr("app.database.db", mock_db)
    
    # Register a new user
    result = register_user("testuser", "test@example.com", "password123")
    assert result['success'] is True
    assert result['message'] == "User registered successfully"
    
    # Test duplicate email
    result = register_user("testuser2", "test@example.com", "password123")
    assert result['success'] is False
    assert result['message'] == "Email already in use"

    # Test duplicate username
    result = register_user("testuser", "newemail@example.com", "password123")
    assert result['success'] is False
    assert result['message'] == "Username already in use"

def test_check_password(mock_db, monkeypatch):
    # Patch the database
    monkeypatch.setattr("app.database.db", mock_db)

    # Create a hashed password
    register_user("testuser", "test@example.com", "password123")
    user = get_user_by_email("test@example.com")
    assert check_password(user['password'], "password123") is True
    assert check_password(user['password'], "wrongpassword") is False

def test_save_and_get_chat_history(mock_db, monkeypatch):
    # Patch the database
    monkeypatch.setattr("app.database.db", mock_db)

    # Save chat messages
    save_message("testuser", "Hello, World!")
    save_message("testuser2", "Hi there!")

    # Fetch chat history
    chat_history = get_chat_history()

    # Debug output for inspection
    print("Chat history retrieved:", chat_history)

    # Verify messages are in the correct order
    assert len(chat_history) == 2, f"Unexpected number of messages: {len(chat_history)}"
    assert chat_history[0]['message'] == "Hello, World!", f"First message mismatch: {chat_history[0]}"
    assert chat_history[1]['message'] == "Hi there!", f"Second message mismatch: {chat_history[1]}"
