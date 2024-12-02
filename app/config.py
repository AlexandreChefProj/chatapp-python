import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')  # Imthe45678383920029lordofthese993993393993;;;soils
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo-db:27017/chatapp')
    FLASK_ENV = os.getenv('FLASK_ENV', 'docker')  # change "docker" to not use the docker build, but well, that's what I try to do here lol


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/chatapp_dev'


class DockerConfig(Config):
    DEBUG = False
    MONGO_URI = "mongodb://mongo-db:27017/docker-database"



class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/chatapp_test'
