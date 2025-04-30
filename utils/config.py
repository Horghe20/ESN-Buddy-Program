
import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")  # NEVER use default in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOP_AUTOMATIC_MATCH = 3
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "")

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///matchmaking.db"

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")



def get_config():
    env = os.getenv("FLASK_ENV").lower()
    print(env)

    if env == "development":
        return DevelopmentConfig
    else:
        return ProductionConfig
