from flask import (
    Blueprint, g, jsonify, render_template, request
)
import json
from sqlalchemy import or_
from controller.auth import login_required
from database.tables import Buddy, Esner
from database.db import db
from utils.utils import load_options

# Create a blueprint for registration-related routes, with URL prefix '/registration'
bp = Blueprint('esner', __name__, url_prefix='/esner')
@bp.route('/registration', methods=['GET', 'POST'])
def register_esner():
    """
    Handles the registration process for ESN members (ESNers).

    This function supports both GET and POST requests:

    GET:
        - Renders the ESNer registration form.
        - Loads additional options from a JSON file to populate form fields.

    POST:
        - Receives registration data in JSON format.
        - Validates the uniqueness of the email and phone number.
        - Ensures the email is an official ESN Palermo email.
        - Creates a new ESNer record in the database with the provided data.
        - Sets the password for the new ESNer.
        - Commits the new ESNer to the database.

    Returns:
        - On successful registration (POST): JSON response with a success message and HTTP status 200.
        - On validation failure (POST): JSON response with an error message and HTTP status 400.
        - On server error (GET/POST): Renders an error page or returns a JSON error message with HTTP status 500.
    """
    if request.method == 'GET':
        try:
            # Render the ESNer registration form with options loaded from the JSON file.
            return render_template("registration/esner.html", data=load_options())
        except Exception as e:
            print(e)
            return render_template("utils/errors.html", code=500), 500
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            
            # Validate that the email is an ESN Palermo email.
            if '@' not in email or 'esn' not in email.split("@")[1].lower():
                return jsonify({"error": "Email must be the official one"}), 400
            
            # Check if an ESNer with the provided email or phone number already exists.
            if Esner.query.filter(
                or_(Esner.email == email, Esner.phone_number == data.get('phone'))
            ).first():
                return jsonify({"error": "Email or Phone already registered!"}), 400
            
            # Create a new ESNer instance with data from the JSON payload.
            new_esner = Esner(
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
                description=data.get('description'),
            )
            new_esner.set_password(data.get('password'))
            
            # Add the new ESNer to the database and commit the transaction.
            db.session.add(new_esner)
            db.session.commit()
            
            return jsonify({"message": "Form submitted successfully!"}), 200
        except Exception as e:
            # Rollback the transaction in case of any errors.
            print(e)
            db.session.rollback()
            return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    Renders the profile page for the logged-in ESNer.

    This route is protected by a login requirement and handles GET requests to '/esner/profile'.
    It displays the profile information of the currently logged-in ESNer.

    Returns:
        - Rendered HTML template for the ESNer profile page.
    """
    return render_template("esner/profile.html")