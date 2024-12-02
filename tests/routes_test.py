import pytest
from app import app
from app.database import register_user
from mongomock import MongoClient

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['LOGIN_DISABLED'] = False
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db(monkeypatch):
    client = MongoClient()
    mock_db = client.test_db
    monkeypatch.setattr("app.database.db", mock_db)
    return mock_db

def test_register_route(client, mock_db):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirects to home
    assert mock_db.users.find_one({"email": "test@example.com"}) is not None

def test_login_route(client, mock_db):
    register_user("testuser", "test@example.com", "password123")
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirects to home
