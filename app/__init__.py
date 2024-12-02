import os
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from pymongo import MongoClient
from dotenv import load_dotenv
from app.config import DevelopmentConfig, DockerConfig, TestingConfig

# Load environment variables from .env file if it exists
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Configure the application based on the environment
env = os.getenv('FLASK_ENV', 'development')
if env == 'docker':
    app.config.from_object(DockerConfig)
    print("We used DockerConfig!")
elif env == 'testing':
    app.config.from_object(TestingConfig)
    print("We used TestingConfig!")
else:
    app.config.from_object(DevelopmentConfig)
    print("We used DevelopmentConfig!")

# Set the secret key for Flask session management (using environment variable or generate one)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'Imthe45678383920029lordofthese993993393993;;;soils')  # You can set this in .env

# Initialize MongoDB (using pymongo)

client = MongoClient(app.config['MONGO_URI'])
print("we show client now bro check this out heck yeah dude look over here")
print(app.config['MONGO_URI'])
print(client)
db = client.get_database()
print(db)

# Initialize Flask-Login for user session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect here for unauthorized access

# Initialize Flask-SocketIO for real-time messaging
socketio = SocketIO(app)

# Import routes and sockets after initializing the app to avoid circular imports
from app import routes, sockets
