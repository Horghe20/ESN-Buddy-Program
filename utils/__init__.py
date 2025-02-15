"""
Utilities Package for ESN Matchmaking System

This package contains utility modules and configurations that support the core functionalities
of the ESN matchmaking system. These utilities provide essential services such as configuration
management, email notifications, database population with dummy data, and matchmaking logic.

Files:

1. populated_database.py:
   - Provides functionality to generate and insert random dummy data into the database.
   - Useful for testing and development purposes to populate the database with sample data.

2. config.py:
   - Contains configuration settings for the Flask application, including database connections,
     email server settings, and other application-specific configurations.
   - Ensures that the application is properly configured for different environments (development, production).

3. match.py:
   - Implements the matchmaking logic between Buddies and ESNers.
   - Provides functions to compute matching scores and perform the matchmaking process based on various attributes.

4. email_service.py:
   - Defines the `EmailService` class, which handles sending email notifications within the system.
   - Includes methods for sending match notifications, unmatch notifications, data elimination notifications, and password reset emails.

5. options.json:
   - A JSON file containing configuration options such as nationalities, languages, faculties, and interests.
   - Used by other modules to provide consistent and configurable options for data generation and matching.
"""