"""
Registration Module for ESN Buddy Program

This module handles the registration of Erasmus students (Buddies) and ESN members (ESNers).
It provides routes for form rendering and data submission.

Blueprint:
    - registration: Handles buddy and ESNer registration with the URL prefix `/registration`.

Functions:
    - load_options(): Loads form options from a JSON file.
    - register_buddy(): Handles Buddy registration via GET (form display) and POST (form submission).
    - register_esners(): Handles ESNer registration via GET (form display) and POST (form submission).
"""

from flask import (
    Blueprint, g, jsonify, render_template, request
)
import json
from sqlalchemy import or_
from database.tables import Buddy, Esners
from database.db import db

# Create a blueprint for registration-related routes, with URL prefix '/registration'
bp = Blueprint('registration', __name__, url_prefix='/registration')


def load_options():
    """
    Loads registration form options from a JSON file.

    Returns:
        dict: Parsed JSON data containing form options.
    """
    with open('./utils/options.json', 'r') as file:
        data = json.load(file)
    return data


@bp.route('/buddy', methods=['GET', 'POST'])
def register_buddy():
    """
    Handles the registration of Erasmus students (Buddies).

    GET:
        - Loads and displays the Buddy registration form.

    POST:
        - Receives form data as JSON.
        - Validates email uniqueness.
        - Stores the new Buddy in the database.

    Returns:
        - On success: JSON response with success message (HTTP 200).
        - On failure: JSON response with an error message (HTTP 400 or 500).
    """
    if request.method == 'GET':
        try:
            # Render the registration form with options loaded from the JSON file.
            return render_template("registration/buddy.html", data=load_options())
        except Exception as e:
            print(e)
            return render_template("errors/errors.html", code=500), 500
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            
            # Check if a Buddy with the provided email already exists.
            if Buddy.query.filter_by(email=email).first():
                return jsonify({"error": "Email already registered!"}), 400
            
            # Create a new Buddy instance with data from the JSON payload.
            new_buddy = Buddy(
                name=data.get('name'),
                surname=data.get('surname'),
                email=email,
                nationality=json.dumps(data.get('nationality')),
                languages_spoken=json.dumps(data.get('languages')),
                faculty=json.dumps(data.get('faculty')),
                phone_number=data.get('phone'),
                instagram=data.get('instagram'),
                telegram=data.get('telegram'),
                interests=json.dumps(data.get('interests')),
                gender=data.get('gender'),
                description=data.get('description'),
                semester=data.get('semester'),
                year=data.get('year')
            )
            
            # Add the new Buddy to the database and commit the transaction.
            db.session.add(new_buddy)
            db.session.commit()
            
            return jsonify({"message": "Form submitted successfully!"}), 200
        except Exception as e:
            # Rollback the transaction in case of any errors.
            db.session.rollback()
            return jsonify({"error": "Internal Server Error"}), 500
    

@bp.route('/esners', methods=['GET', 'POST'])
def register_esners():
    """
    Handles the registration of ESN members (ESNers).

    GET:
        - Loads and displays the ESNers registration form.

    POST:
        - Receives form data as JSON.
        - Validates email and phone uniqueness.
        - Ensures the email is an official ESN Palermo email.
        - Stores the new ESNer in the database.

    Returns:
        - On success: JSON response with success message (HTTP 200).
        - On failure: JSON response with an error message (HTTP 400 or 500).
    """
    if request.method == 'GET':
        try:
            # Render the ESNers registration form with options loaded from the JSON file.
            return render_template("registration/esners.html", data=load_options())
        except Exception as e:
            print(e)
            return render_template("errors/errors.html", code=500), 500
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            
            # Validate that the email is an ESN Palermo email.
            if '@' not in email or 'esn' not in email.split("@")[1].lower():
                return jsonify({"error": "Email must be the official one"}), 400
            
            # Check if an ESNer with the provided email or phone number already exists.
            if Esners.query.filter(
                or_(Esners.email == email, Esners.phone_number == data.get('phone'))
            ).first():
                return jsonify({"error": "Email or Phone already registered!"}), 400
            
            # Create a new ESNers instance with data from the JSON payload.
            new_esner = Esners(
                name=data.get('name'),
                surname=data.get('surname'),
                email=email,
                phone_number=data.get('phone'),
                languages_spoken=json.dumps(data.get('languages')),
                nationality=json.dumps(data.get('nationality')),
                gender=data.get('gender'),
                faculty=json.dumps(data.get('faculty')),
                interests=json.dumps(data.get('interests')),
                max_number_of_buddy=data.get('max_number_of_buddy'),
                description=data.get('description')
            )
            
            # Add the new ESNer to the database and commit the transaction.
            db.session.add(new_esner)
            db.session.commit()
            
            return jsonify({"message": "Form submitted successfully!"}), 200
        except Exception as e:
            # Rollback the transaction in case of any errors.
            print(e)
            db.session.rollback()
            return jsonify({"error": "Internal Server Error"}), 500
