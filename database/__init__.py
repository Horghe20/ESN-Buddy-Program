"""
Database Package for ESN Matchmaking System

This package is responsible for setting up and managing the database interactions
for the ESN matchmaking system. It leverages SQLAlchemy to define models and perform
database operations in a structured and efficient manner.

Modules:

1. db.py:
   - Contains the setup for the SQLAlchemy instance (`db`).
   - Provides the `init_db(app)` function to initialize the database with a Flask application.
   - This setup is essential for binding the database to the Flask app, enabling ORM capabilities.

2. tables.py:
   - Defines the database models using SQLAlchemy ORM.
   - Models include `Buddy`, `Esners`, and `Admin`, representing the core entities in the system.
   - Each model includes fields and methods for managing data, such as JSON serialization and password hashing.
"""