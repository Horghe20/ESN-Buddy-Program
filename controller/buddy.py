from flask import (
    Blueprint, g, jsonify, render_template, request
)
import json
from sqlalchemy import or_
from database.tables import Buddy, Esner
from database.db import db
from utils.email_service import email_service
from utils.utils import load_options

# Create a blueprint for registration-related routes, with URL prefix '/buddy'
bp = Blueprint('buddy', __name__, url_prefix='/buddy')

@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Handles the registration of Erasmus students (Buddies).

    This function supports both GET and POST requests:

    GET:
        - Renders the Buddy registration form.
        - Loads additional options from a JSON file to populate form fields.

    POST:
        - Receives registration data in JSON format.
        - Validates the uniqueness of the email and phone number.
        - Creates a new Buddy record in the database with the provided data.
        - Sends a registration confirmation email to the Buddy.
        - Commits the new Buddy to the database.

    Returns:
        - On successful registration (POST): JSON response with a success message and HTTP status 200.
        - On validation failure (POST): JSON response with an error message and HTTP status 400.
        - On server error (GET/POST): Renders an error page or returns a JSON error message with HTTP status 500.
    """
    if request.method == 'GET':
        try:
            # Render the registration form with options loaded from the JSON file.
            return render_template("buddy/registration.html", data=load_options())
        except Exception as e:
            print(e)
            return render_template("utils/errors.html", code=500), 500
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            phone_number = data.get('phone')
            
            # Check if a Buddy with the provided email already exists.
            if Buddy.query.filter_by(email=email).first():
                return jsonify({"error": "Email already registered!"}), 400
            
            # Check if a Buddy with the provided phone number already exists.
            if Buddy.query.filter_by(phone_number=phone_number).first():
                return jsonify({"error": "Phone number already registered!"}), 400
            
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
            email_service.send_registration_confirmation(new_buddy)
            db.session.commit()
            
            return jsonify({"message": "Form submitted successfully!"}), 200
        except Exception as e:
            # Rollback the transaction in case of any errors.
            print(e)
            db.session.rollback()
            return jsonify({"error": "Internal Server Error"}), 500