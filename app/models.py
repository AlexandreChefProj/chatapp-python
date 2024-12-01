from flask_login import UserMixin
from bson import ObjectId  # Import ObjectId from bson module

class User(UserMixin):
    def __init__(self, email, username, password, user_id=None):
        self.id = user_id  # MongoDB _id is used for Flask-Login's user identification
        self.email = email
        self.username = username
        self.password = password  # Store the password (hashed) directly here
        # If needed, add other attributes like 'created_at' or 'updated_at'

    def __repr__(self):
        return f'<User(username={self.username}, email={self.email}, user_id={self.id})>'


    @classmethod
    def from_dict(cls, data):
        # Ensure _id is converted to string in case it's an ObjectId
        user_id = str(data['_id']) if isinstance(data['_id'], ObjectId) else data['_id']
        return User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            user_id=user_id  # Convert _id to string for Flask-Login
        )

    def get_id(self):
        """This is required by Flask-Login to identify the user."""
        return str(self.id)
