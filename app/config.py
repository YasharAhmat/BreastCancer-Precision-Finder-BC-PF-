import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///app.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:')

class ProductionConfig(Config):
    def __init__(self):
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            self.SQLALCHEMY_DATABASE_URI = db_url.replace('postgres://', 'postgresql://', 1)
        else:
            raise RuntimeError("DATABASE_URL environment variable not set for production!")
