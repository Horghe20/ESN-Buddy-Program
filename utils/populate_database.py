"""
Data Generation Script for ESN Matchmaking System

This script generates random dummy data for the ESN matchmaking system using the Faker library.
It creates instances of Buddy and Esners with random attributes and inserts them into the database.
The script is useful for testing and development purposes, allowing developers to populate the database
with sample data.

Modules and Libraries:
- random: Used for random selections and sampling.
- json: Used for handling JSON data.
- datetime: Used for generating timestamps.
- Faker: A library for generating fake data.
- Flask: A micro web framework for Python.
- SQLAlchemy: An ORM for database interactions.

Functions:
- load_options(): Loads options (nationalities, languages, faculties, interests) from a JSON file.
- generate_buddy(fake, options): Generates a Buddy instance with random dummy data.
- generate_esner(fake, options): Generates an Esners instance with random dummy data.
- main(): The main function that sets up the Flask app, initializes the database, and inserts dummy data.

Usage:
- Run this script to populate the database with 50 Buddy records and 10 Esners records.
- Ensure that the database is properly configured and accessible before running the script.
"""

import random
import json
from datetime import datetime

from faker import Faker
from flask import Flask
from database.db import db, init_db

# Import your database and models
from database.tables import Buddy, Esner, EsnerType

# Path to the options file
OPTIONS_FILE = './utils/options.json'

def load_options():
    """Load options (nationalities, languages, faculties, interests) from a JSON file.

    Returns:
        dict: A dictionary containing lists of options for nationalities, languages, faculties, and interests.
    """
    with open(OPTIONS_FILE, 'r') as f:
        options = json.load(f)
    return options

def generate_buddy(fake, options):
    """Generate a Buddy instance with random dummy data.

    Args:
        fake (Faker): An instance of the Faker class for generating fake data.
        options (dict): A dictionary of options for generating random attributes.

    Returns:
        Buddy: A Buddy instance populated with random data.
    """
    # Generate basic fields
    name = fake.first_name()
    surname = fake.last_name()
    # Ensure unique email using Faker’s unique generator
    email = fake.unique.email()
    phone = fake.phone_number()[0:15]
    
    # Random selections from options (pick one or more items)
    nationality = random.sample(options['nationalities'], k=1)
    languages = random.sample(options['languages'], k=1)
    # Here you might assume one faculty per buddy. You can also select more if needed.
    faculty = random.sample(options['faculties'], k=1)
    interests = random.sample(options['interests'], k=random.randint(5, 15))
    
    # Other fields
    instagram = f"@{fake.user_name()}"
    telegram = fake.user_name()
    gender = random.choice(["Male", "Female", "Other"])
    description = fake.text(max_nb_chars=200)
    semester = random.choice(["Fall", "Spring"])
    # For example, the year could be an integer between 1 and 4 (or actual years)
    year = random.randint(1, 4)
    
    # Create and return the Buddy instance
    buddy = Buddy(
        name=name,
        surname=surname,
        email=email,
        nationality=json.dumps(nationality),
        languages_spoken=json.dumps(languages),
        faculty=json.dumps(faculty),
        phone_number=phone,
        instagram=instagram,
        telegram=telegram,
        interests=json.dumps(interests),
        gender=gender,
        description=description,
        semester=semester,
        year=year,
        date_of_insert=datetime.utcnow()
    )
    return buddy

def generate_esner(fake, options):
    """Generate an Esners instance with random dummy data.

    Args:
        fake (Faker): An instance of the Faker class for generating fake data.
        options (dict): A dictionary of options for generating random attributes.

    Returns:
        Esners: An Esners instance populated with random data.
    """
    name = fake.first_name()
    surname = fake.last_name()
    
    # Create an email with the required domain
    email = f"{fake.user_name()}@esnpalermo.com"
    
    phone = fake.phone_number()[0:15]
    
    languages = random.sample(options['languages'], k=random.randint(1, 3))
    nationality = random.sample(options['nationalities'], k=random.randint(1, 3))
    faculties = random.sample(options['faculties'], k=random.randint(1, 2))
    interests = random.sample(options['interests'], k=random.randint(5, 15))
    
    gender = random.choice(["Male", "Female", "Other"])
    description = fake.text(max_nb_chars=200)
    
    # Randomly select the type of Esner (Volunteer, Honorarium, Alumnus)
    esner_type = random.choice([EsnerType.VOLUNTEER, EsnerType.HONORARIUM, EsnerType.ALUMNUS])
    
    # Randomly set the maximum number of buddies (you could adjust this as per your needs)
    max_number_of_buddy = random.randint(1, 5)

    # Create the Esner instance with all generated data
    esner = Esner(
        name=name,
        surname=surname,
        email=email,
        phone_number=phone,
        languages_spoken=json.dumps(languages),
        nationality=json.dumps(nationality),
        gender=gender,
        faculty=json.dumps(faculties),
        interests=json.dumps(interests),
        type=esner_type,
        description=description,
        max_number_of_buddy=max_number_of_buddy
    )
    
    # Set a dummy password
    esner.set_password("test")
    
    return esner

def main():
    """Main function to set up the Flask app, initialize the database, and insert dummy data."""
    # Create a Flask app instance (adjust configuration as needed)
    app = Flask(__name__)
    # Make sure your app config includes the correct SQLALCHEMY_DATABASE_URI etc.
    app.config.from_object("config")  

    # Create all tables (if not created already)
    with app.app_context():
        init_db(app)
        from database.tables import Esner, Buddy

        db.create_all()
        options = load_options()
        fake = Faker()
        
        # Insert 50 Buddy entries
        for _ in range(12):
            buddy = generate_buddy(fake, options)
            db.session.add(buddy)
        
        # Insert 10 Esners entries
        for _ in range(5):
            esner = generate_esner(fake, options)
            db.session.add(esner)
        
        try:
            db.session.commit()
            print("Successfully inserted 50 Buddy records and 10 Esners records.")
        except Exception as e:
            db.session.rollback()
            print("An error occurred while inserting records:", e)

if __name__ == '__main__':
    main()