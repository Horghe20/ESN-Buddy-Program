from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from .db import db  # Import the SQLAlchemy database instance

# Define the Buddy model representing Erasmus students.
class Buddy(db.Model):
    """
    Represents an Erasmus student (Buddy) in the ESN Buddy Program.

    Attributes:
        id (int): Primary key.
        name (str): First name of the student.
        surname (str): Last name of the student.
        email (str): Unique email address.
        nationality (str): JSON-encoded nationality information.
        languages_spoken (str): JSON-encoded list of languages spoken.
        faculty (str): JSON-encoded list of faculties.
        phone_number (str): Unique contact number.
        instagram (str): Instagram handle.
        telegram (str): Telegram handle.
        interests (str): JSON-encoded list of interests.
        gender (str): Gender of the student.
        description (str): Additional information.
        semester (str): Semester of exchange (e.g., "Fall", "Spring").
        year (int): Year of exchange.
        date_of_insert (datetime): Timestamp of record creation.
        esn_member_id (int): Foreign key referencing the Esners model.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nationality = db.Column(db.Text, nullable=True)  # Stored as JSON
    languages_spoken = db.Column(db.Text, nullable=True)  # Stored as JSON
    faculty = db.Column(db.Text, nullable=True)  # Stored as JSON
    phone_number = db.Column(db.String(20), unique=True)
    instagram = db.Column(db.String(100))
    telegram = db.Column(db.String(100))
    interests = db.Column(db.Text)  # Stored as JSON or comma-separated values
    gender = db.Column(db.String(50))
    description = db.Column(db.Text)
    semester = db.Column(db.String(20))  # E.g., "Fall", "Spring"
    year = db.Column(db.Integer)
    date_of_insert = db.Column(db.DateTime, default=datetime.utcnow)  # Date of insertion
    esn_member_id = db.Column(db.Integer, db.ForeignKey('esner.id'), nullable=True)

    # Methods for handling JSON data
    def set_languages_spoken(self, languages):
        """Stores a list of languages as a JSON string."""
        self.languages_spoken = json.dumps(languages)
    
    def get_languages_spoken(self):
        """Retrieves the list of languages from a JSON string."""
        return json.loads(self.languages_spoken)
    
    def set_nationality(self, nationalities):
        """Stores nationality information as a JSON string."""
        self.nationality = json.dumps(nationalities)
    
    def get_nationality(self):
        """Retrieves nationality information from a JSON string."""
        return json.loads(self.nationality)
    
    def set_faculty(self, faculties):
        """Stores faculty information as a JSON string."""
        self.faculty = json.dumps(faculties)
    
    def get_faculty(self):
        """Retrieves faculty information from a JSON string."""
        return json.loads(self.faculty)
    
    def set_interests(self, interests):
        """Stores interests as a JSON string."""
        self.interests = json.dumps(interests)
    
    def get_interests(self):
        """Retrieves interests from a JSON string."""
        return json.loads(self.interests)


# Define the Esners model representing ESN members.
class Esner(db.Model):
    """
    Represents an ESN member who assists Erasmus students.

    Attributes:
        id (int): Primary key.
        name (str): First name of the ESN member.
        surname (str): Last name of the ESN member.
        email (str): Unique email address.
        phone_number (str): Contact number.
        languages_spoken (str): JSON-encoded list of languages spoken.
        nationality (str): JSON-encoded nationality information.
        gender (str): Gender of the ESN member.
        faculty (str): JSON-encoded list of faculties.
        interests (str): JSON-encoded list of interests.
        max_number_of_buddy (int): Maximum number of Buddies they can manage.
        description (str): Additional information.
        password_hash (str): Hashed password for authentication.
        buddies (relationship): One-to-many relationship with Buddy model.
        roles (relationship): Many-to-many relationship with Role model.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    languages_spoken = db.Column(db.Text, nullable=True)  # Stored as JSON
    nationality = db.Column(db.Text, nullable=True)  # Stored as JSON
    gender = db.Column(db.String(50))
    faculty = db.Column(db.Text, nullable=True)  # Stored as JSON
    interests = db.Column(db.Text, nullable=True)  # Stored as JSON
    max_number_of_buddy = db.Column(db.Integer, nullable=False, default=3)
    description = db.Column(db.Text)
    password_hash = db.Column(db.String(255), nullable=False)
    buddies = db.relationship('Buddy', backref='esn_member', lazy=True)
    roles = db.relationship('EsnerRole', back_populates='esner', cascade="all, delete-orphan")

    # Methods for handling JSON data
    def set_languages_spoken(self, languages):
        """Stores a list of languages as a JSON string."""
        self.languages_spoken = json.dumps(languages)
    
    def get_languages_spoken(self):
        """Retrieves the list of languages from a JSON string."""
        return json.loads(self.languages_spoken)
    
    def set_nationality(self, nationalities):
        """Stores nationality information as a JSON string."""
        self.nationality = json.dumps(nationalities)
    
    def get_nationality(self):
        """Retrieves nationality information from a JSON string."""
        return json.loads(self.nationality)
    
    def set_faculty(self, faculties):
        """Stores faculty information as a JSON string."""
        self.faculty = json.dumps(faculties)
    
    def get_faculty(self):
        """Retrieves faculty information from a JSON string."""
        return json.loads(self.faculty)
    
    def set_interests(self, interests):
        """Stores interests as a JSON string."""
        self.interests = json.dumps(interests)
    
    def get_interests(self):
        """Retrieves interests from a JSON string."""
        return json.loads(self.interests)
    
    # Methods for password hashing and verification
    def set_password(self, password):
        """Hashes and stores the given password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Checks if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

# Role Table
class Role(db.Model):
    """
    Represents a role in the system.

    Attributes:
        id (int): Unique identifier for the role.
        name (str): The name of the role (e.g., "Admin", "Editor").
    
    Relationships:
        esner (list): List of EsnerRole associations linking this role to esners.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relationship with UserRole
    esner = db.relationship('EsnerRole', back_populates='role', cascade="all, delete-orphan")


# EsnerRole Table (Many-to-Many)
class EsnerRole(db.Model):
    """
    Represents the association between an esner and a role.

    This table creates a many-to-many relationship between Esners and Roles.

    Attributes:
        esner_id (int): Foreign key referring to the Esner.
        role_id (int): Foreign key referring to the Role.
    
    Relationships:
        esner (Esner): The esner associated with the role.
        role (Role): The role associated with the esner.
    """
    
    esner_id = db.Column(db.Integer, db.ForeignKey('esner.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

    # Relationships
    esner = db.relationship('Esner', back_populates='roles')
    role = db.relationship('Role', back_populates='esner')