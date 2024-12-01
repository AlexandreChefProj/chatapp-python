import os

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')  # Imthe45678383920029lordofthese993993393993;;;soils
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/chatapp')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')  # Optional: Flask environment setting


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/chatapp_dev'


class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = os.getenv('MONGO_URI', 'your_production_mongo_uri')


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/chatapp_test'
