from app.models import User

def test_user_initialization():
    user = User("test@example.com", "testuser", "hashedpassword", "12345")
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password == "hashedpassword"
    assert user.id == "12345"

def test_user_from_dict():
    user_data = {
        "_id": "12345",
        "email": "test@example.com",
        "username": "testuser",
        "password": "hashedpassword",
    }
    user = User.from_dict(user_data)
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password == "hashedpassword"
    assert user.id == "12345"

def test_get_id():
    user = User("test@example.com", "testuser", "hashedpassword", "12345")
    assert user.get_id() == "12345"
