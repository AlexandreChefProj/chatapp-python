import pytest
from app.models import User

def test_user_initialization():
    # Tester l'initialisation d'un utilisateur
    user = User("test@example.com", "testuser", "hashedpassword", "12345")
    
    # Vérifier les attributs de l'utilisateur
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password == "hashedpassword"
    assert user.id == "12345"

def test_user_from_dict():
    # Données utilisateur simulées
    user_data = {
        "_id": "12345",
        "email": "test@example.com",
        "username": "testuser",
        "password": "hashedpassword",
    }
    
    # Tester la création d'un utilisateur à partir d'un dictionnaire
    user = User.from_dict(user_data)
    
    # Vérifier les attributs de l'utilisateur
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password == "hashedpassword"
    assert user.id == "12345"

def test_user_from_dict_missing_field():
    # Tester avec un champ manquant
    user_data_incomplete = {
        "_id": "12345",
        "email": "test@example.com",
        "username": "testuser",
    }
    
    # Vérifier que l'erreur est levée pour les champs manquants
    with pytest.raises(KeyError):
        User.from_dict(user_data_incomplete)

def test_get_id():
    # Tester la méthode `get_id`
    user = User("test@example.com", "testuser", "hashedpassword", "12345")
    assert user.get_id() == "12345"

def test_user_equality():
    # Vérifier si deux utilisateurs avec les mêmes données sont égaux
    user1 = User("test@example.com", "testuser", "hashedpassword", "12345")
    user2 = User("test@example.com", "testuser", "hashedpassword", "12345")
    
    assert user1 == user2

def test_user_inequality():
    # Vérifier si deux utilisateurs différents ne sont pas égaux
    user1 = User("test@example.com", "testuser", "hashedpassword", "12345")
    user2 = User("other@example.com", "otheruser", "otherpassword", "67890")
    
    assert user1 != user2
