from flask import (
    Blueprint, g, jsonify, render_template, request
)
import json
from sqlalchemy import or_
from controller.auth import login_required
from database.tables import Buddy, Esner
from database.db import db
from utils.utils import load_options

# Create a blueprint for ESNer-related routes, with URL prefix '/esner'
bp = Blueprint('esner', __name__, url_prefix='/esner')

@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Handles the registration process for ESN members (ESNers).

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
            return render_template("esner/registration.html", data=load_options())
        except Exception as e:
            print(e)
            return render_template("utils/errors.html", code=500), 500
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            
            if '@' not in email or 'esn' not in email.split("@")[1].lower():
                return jsonify({"error": "Email must be the official one"}), 400
            
            if Esner.query.filter(
                or_(Esner.email == email, Esner.phone_number == data.get('phone'))
            ).first():
                return jsonify({"error": "Email or Phone already registered!"}), 400
            
            new_esner = Esner(
                name=data.get('name'),
                surname=data.get('surname'),
                type=data.get('type'),
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
            
            db.session.add(new_esner)
            db.session.commit()
            
            return jsonify({"message": "Form submitted successfully!"}), 200
        except Exception as e:
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

@bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    """
    Handles the updating of an ESNer's profile.
    
    GET:
        - Renders the update profile form with current ESNer data.
    
    POST:
        - Receives updated profile data in JSON format.
        - Updates only the provided fields in the ESNer’s record.
        - Commits changes to the database.
    
    Returns:
        - On successful update (POST): JSON response with a success message and HTTP status 200.
        - On failure (POST): JSON response with an error message and appropriate HTTP status.
    """
    if request.method == 'GET':
        return render_template("esner/update_profile.html", data=load_options())
    
    if request.method == 'POST':
        try:
            esner = Esner.query.get(g.esner.id)
            if esner:
                data = request.get_json()
                
                if "name" in data:
                    esner.name = data.get("name")
                if "surname" in data:
                    esner.surname = data.get("surname")
                if "phone" in data:
                    esner.phone_number = data.get("phone")
                if "type" in data:
                    esner.type = data.get('type')
                if "email" in data:
                    esner.email = data.get("email")
                if "gender" in data:
                    esner.gender = data.get("gender")
                if "nationality" in data:
                    esner.set_nationality(data.get("nationality"))
                if "languages" in data:
                    esner.set_languages_spoken(data.get("languages"))
                if "faculty" in data:
                    esner.set_faculty(data.get("faculty"))
                if "interests" in data:
                    esner.set_interests(data.get("interests"))
                if "description" in data:
                    esner.description = data.get("description")
                if "max_number_of_buddy" in data:
                    esner.max_number_of_buddy = data.get("max_number_of_buddy")
                if "password" in data and data.get("password"):
                    esner.set_password(data.get("password"))
                
                db.session.commit()
                return jsonify({"message": "Profile updated successfully!"}), 200
            else:
                return jsonify({"error": "ESNer not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
