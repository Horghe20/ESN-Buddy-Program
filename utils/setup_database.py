import os
from flask import Flask

from database.db import db, init_db
from utils import config

def create_database():
    """
    Initialize the database, create tables, and add a test admin if no admin exists.
    """
    # Create a temporary Flask app context for database initialization
    app = Flask(__name__)
    app.config.from_object(config)  

    

if __name__ == "__main__":
    create_database()
