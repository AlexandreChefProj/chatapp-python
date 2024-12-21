import pytest
from app.database import (
    register_user, 
    get_user_by_email,  
    check_password, 
    save_message, 
    get_chat_history
)
from mongomock import MongoClient

# Fixture pour configurer une base de données mockée
@pytest.fixture
def mock_db():
    client = MongoClient()
    db = client.test_db
    yield db
    # Nettoyer la base de données après chaque test
    client.drop_database("test_db")

def test_register_user(mock_db, monkeypatch):
    # Patcher la base de données
    monkeypatch.setattr("app.database.db", mock_db)
    
    # Tester l'enregistrement d'un nouvel utilisateur
    result = register_user("testuser", "test@example.com", "password123")
    assert result['success'] is True
    assert result['message'] == "User registered successfully"
    
    # Vérifier que l'utilisateur est bien dans la base
    user = get_user_by_email("test@example.com")
    assert user is not None
    assert user['username'] == "testuser"

    # Tester l'utilisation d'un email déjà existant
    result = register_user("testuser2", "test@example.com", "password123")
    assert result['success'] is False
    assert result['message'] == "Email already in use"

    # Tester l'utilisation d'un nom d'utilisateur déjà existant
    result = register_user("testuser", "newemail@example.com", "password123")
    assert result['success'] is False
    assert result['message'] == "Username already in use"

def test_check_password(mock_db, monkeypatch):
    # Patcher la base de données
    monkeypatch.setattr("app.database.db", mock_db)

    # Créer un utilisateur pour le test
    register_user("testuser", "test@example.com", "password123")
    user = get_user_by_email("test@example.com")

    # Vérifier les mots de passe
    assert user is not None
    assert check_password(user['password'], "password123") is True
    assert check_password(user['password'], "wrongpassword") is False

def test_save_and_get_chat_history(mock_db, monkeypatch):
    # Patcher la base de données
    monkeypatch.setattr("app.database.db", mock_db)

    # Sauvegarder des messages
    save_message("testuser", "Hello, World!")
    save_message("testuser2", "Hi there!")

    # Récupérer l'historique des messages
    chat_history = get_chat_history()

    # Vérifier les messages dans l'historique
    assert len(chat_history) == 2
    assert chat_history[0]['message'] == "Hello, World!"
    assert chat_history[0]['author'] == "testuser"
    assert chat_history[1]['message'] == "Hi there!"
    assert chat_history[1]['author'] == "testuser2"

    # Vérifier l'état de la base de données
    messages_in_db = list(mock_db.chat.find())
    assert len(messages_in_db) == 2
    assert messages_in_db[0]['message'] == "Hello, World!"
    assert messages_in_db[1]['message'] == "Hi there!"
