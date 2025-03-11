"""
Database Configuration Module

This module initializes and configures the SQLAlchemy database instance for the Flask application.

Modules:
    - flask_sqlalchemy: Provides SQLAlchemy ORM integration for Flask.

Attributes:
    db (SQLAlchemy): The SQLAlchemy database instance used for handling database operations.

Functions:
    - init_db(app): Initializes the database with the given Flask application instance.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()

def init_db(app):
    """
    Initializes the database with the given Flask application instance.

    This function binds the SQLAlchemy database instance to the Flask application,
    enabling database operations.

    Args:
        app (Flask): The Flask application instance to associate with the database.

    Returns:
        None
    """
    db.init_app(app)
