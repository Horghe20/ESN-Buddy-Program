

from io import BytesIO
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, send_file, session, url_for
)
from sqlalchemy import case, func
import json
import openpyxl
from werkzeug.security import check_password_hash, generate_password_hash

from database.tables import Admin, Buddy, Esners
from database.db import db
from controller.auth import admin_required, login_required
from utils.email_service import email_service

# Create a blueprint for admin-related routes with URL prefix '/admin'
bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    Render the profile page for the logged-in manager/admin.
    
    This route handles GET requests to '/manager/profile' and renders a template
    that displays the manager's profile information.
    
    :return: Rendered HTML template for the manager profile.
    """
    return render_template("admin/profile.html")

@bp.route('/index', methods=['GET'])
@admin_required
def index():
    """
    Render the admin index page displaying all registered admins.
    
    GET request:
      - Retrieves all Admin records from the database using the model's query attribute.
      - Renders the 'admin/index.html' template with the list of admins.
    
    :return: Rendered HTML template with admin data.
    """
    admins = Admin.query.all()
    return render_template("admin/index.html", admins=admins)


@bp.route('/add_admin', methods=['POST'])
@admin_required
def add_admin():
    """
    Add a new admin to the system.

    POST request:
      - Expects a JSON payload containing:
          - name: Admin's first name.
          - surname: Admin's surname.
          - phone_number: Admin's contact number.
          - email: Admin's email address.
          - password: Admin's password in plain text (will be hashed).
          - role: Role of the admin (typically an integer, e.g., 1 for admin privileges).
      - Checks if the email or phone number is already registered.
      - Ensures that the email domain contains 'esn'.
      - Creates a new Admin instance, sets its password using set_password(), and adds it to the database.
      - Returns a JSON response indicating success or an error if validation fails.

    :return: JSON response with a success message (HTTP 200) or error message.
    """
    try:
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        phone_number = data.get('phone_number')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Validate email format
        if "@" not in email or 'esn' not in email.split("@")[1]:
            return jsonify({"error": "Invalid email domain! Must contain 'esn'."}), 400

        # Check if email or phone number is already registered
        existing_admin = Admin.query.filter(
            (Admin.email == email) | (Admin.phone_number == phone_number)
        ).first()
        
        if existing_admin:
            return jsonify({"error": "An admin with this email or phone number already exists!"}), 400

        # Create and add new admin
        new_admin = Admin(
            name=name,
            surname=surname,
            phone_number=phone_number,
            email=email,
            role=int(role)
        )
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        return jsonify({"message": "Admin added successfully!"}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500



@bp.route('/remove_admin/<int:admin_id>', methods=['POST'])
@admin_required
def remove_admin(admin_id):
    """
    Remove an admin from the system.
    
    POST request:
      - The admin_id is provided as a URL parameter.
      - Checks if the admin exists. If the admin exists and is not the currently logged-in admin,
        the admin is deleted from the database.
      - If the logged-in admin attempts to remove themselves, an error is returned.
    
    :param admin_id: The ID of the admin to be removed.
    :return: JSON response indicating success (HTTP 200) or an error message.
    """
    try:
        admin = Admin.query.filter_by(id=admin_id).first()
        if not admin:
            return jsonify({"error": "Admin not found"}), 404

        # Prevent an admin from removing themselves.
        if admin.id != g.admin.id:
            db.session.delete(admin)
            db.session.commit()
        else:
            return jsonify({"error": "Can't remove yourself"}), 403

        return jsonify({"message": "Admin removed successfully!"}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/get_admin_info/<int:admin_id>', methods=['GET'])
@admin_required
def get_admin_info(admin_id):
    """
    Retrieve information about a specific admin (excluding sensitive password details).
    
    GET request:
      - The admin_id is provided as a URL parameter.
      - Retrieves the corresponding admin from the database.
      - Returns a JSON response with the admin's id, name, surname, phone number, email, and role.
    
    :param admin_id: The ID of the admin whose information is requested.
    :return: JSON response containing admin details or an error message if not found.
    """
    try:
        admin = Admin.query.filter_by(id=admin_id).first()
        if not admin:
            return jsonify({"error": "Admin not found"}), 404

        admin_info = {
            "id": admin.id,
            "name": admin.name,
            "surname": admin.surname,
            "phone_number": admin.phone_number,
            "email": admin.email,
            "role": admin.role
        }
        return jsonify(admin_info), 200
    except Exception as e:
        print(e)
        return render_template("errors/errors.html", code=500), 500


@bp.route('/update_admin/<int:admin_id>', methods=['PUT'])
@admin_required
def update_admin(admin_id):
    """
    Update information for a specific admin.
    
    PUT request:
      - Expects a JSON payload with any subset of the following fields:
          - name, surname, phone_number, email, role, password.
      - Retrieves the admin record by admin_id.
      - Updates the provided fields. If a password is provided, it is hashed using set_password().
      - Commits the changes to the database.
    
    :param admin_id: The ID of the admin to update.
    :return: JSON response indicating success (HTTP 200) or an error message.
    """
    data = request.get_json()
    admin = Admin.query.filter_by(id=admin_id).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    # Update fields if provided in the request data.
    if "name" in data:
        admin.name = data.get("name")
    if "surname" in data:
        admin.surname = data.get("surname")
    if "phone_number" in data:
        admin.phone_number = data.get("phone_number")
    if "email" in data:
        admin.email = data.get("email")
    if "role" in data:
        admin.role = int(data.get("role"))
    if "password" in data and data.get("password"):
        # Update the password by hashing the new value.
        admin.set_password(data.get("password"))

    try:
        db.session.commit()
        return jsonify({"message": "Admin updated successfully!"}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/update_password', methods=['POST'])
@login_required
def update_password():
    """
    Update the password for the logged-in manager/admin.
    
    This endpoint expects a JSON payload containing:
      - current_password: The current password provided by the user.
      - new_password: The new password to be set.
    
    The process is as follows:
      1. Ensure both current and new passwords are provided.
      2. Verify that the current password matches the stored hash.
         If the password is incorrect, return a 403 error.
      3. Retrieve the current admin from the database and update the password (hashed).
      4. Commit the changes, clear the session, and return a success message.
    
    In case of any error (missing fields, incorrect password, or database error),
    an error message with an appropriate HTTP status code is returned.
    
    :return: JSON response indicating success or error.
    """
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # Ensure both current and new passwords are provided.
        if not current_password or not new_password:
            return jsonify({"error": "Both current and new password are required"}), 400

        # Verify the current password using the stored password hash.
        if not check_password_hash(g.admin.password_hash, current_password):
            return jsonify({"error": "Incorrect password. If you forgot it, please contact IT."}), 403

        # Retrieve the currently logged-in admin and update the password.
        admin = Admin.query.get(g.admin.id)
        admin.password_hash = generate_password_hash(new_password)
        db.session.commit()
        session.clear()
        
        return jsonify({"message": "Password updated successfully!"}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/export_excel', methods=['GET'])
@admin_required
def export_excel():
    """
    Export Buddy and ESNers data into an Excel file.
    
    GET request:
      - Retrieves all Buddy and ESNers records from the database.
      - Calls create_exel() to generate an Excel workbook containing two sheets:
          1. Buddies sheet with details for each Buddy.
          2. ESNers sheet with details for each ESNer.
      - Returns the Excel file as a downloadable response.
    
    :return: Flask send_file response containing the Excel workbook.
    """
    try:
        # Retrieve all Buddy and ESNers records using the model's query interface.
        buddies = Buddy.query.all()
        esners = Esners.query.all()
    
        # Generate the Excel file and return it as an attachment.
        return send_file(
            create_exel(buddies, esners),
            as_attachment=True,
            download_name="export.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(e)
        return render_template("errors/errors.html", code=500), 500


@bp.route('/export_and_remove_all', methods=['GET'])
@admin_required
def remove_all():
    """
    Export all Buddy and ESNers data to an Excel file and then remove all records.
    
    GET request:
      - Retrieves all Buddy and ESNers records.
      - Generates an Excel file using create_exel().
      - Attempts to delete all records from both Buddy and ESNers tables.
      - Returns the Excel file as a downloadable response if deletion succeeds.
      - If an error occurs during deletion, the transaction is rolled back, and a 500 error is returned.
    
    :return: Flask send_file response containing the Excel workbook, or an error message.
    """
    # Retrieve all data from the Buddy and ESNers tables.
    buddies = Buddy.query.all()
    esners = Esners.query.all()
    file = create_exel(buddies, esners)
    
    try:
        # Delete all Buddy records.
        Buddy.query.delete()
        # Delete all ESNers records.
        Esners.query.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Optionally, log the exception or return an error response.
        return jsonify({"message": "Server Error"}), 500 

    # Return the Excel file as a downloadable response.
    return send_file(
        file,
        as_attachment=True,
        download_name="export.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ), 200


def create_exel(buddies, esners):
    """
    Create an Excel workbook with two worksheets containing Buddy and ESNers data.
    
    This function uses the openpyxl library to create an Excel workbook with the following structure:
    
      1. Buddies Sheet:
         - Title: "Buddies"
         - Columns (Headers): ID, Name, Surname, Email, Nationality, Languages Spoken, Faculty,
           Phone Number, Instagram, Telegram, Interests, Gender, Description, Semester, Year,
           Date of Insert, ESN Member ID.
         - Each Buddy record is appended as a row. Date formatting is applied to date_of_insert if available.
      
      2. ESNers Sheet:
         - Title: "ESNers"
         - Columns (Headers): ID, Name, Surname, Email, Phone Number, Languages Spoken, Nationality,
           Gender, Faculty, Interests, Description.
         - Each ESNer record is appended as a row.
    
    The workbook is then saved to a BytesIO stream, which is returned for use in a downloadable response.
    
    :param buddies: List of Buddy instances.
    :param esners: List of ESNers instances.
    :return: A BytesIO stream containing the Excel file.
    """
    # Create a new Excel workbook.
    wb = openpyxl.Workbook()
    
    # --- Create and populate the Buddies sheet ---
    ws_buddies = wb.active
    ws_buddies.title = "Buddies"

    # Define headers for the Buddy sheet.
    buddy_headers = [
        "ID", "Name", "Surname", "Email", "Nationality", "Languages Spoken", 
        "Faculty", "Phone Number", "Instagram", "Telegram", "Interests", 
        "Gender", "Description", "Semester", "Year", "Date of Insert", "ESN Member ID"
    ]
    ws_buddies.append(buddy_headers)

    # Append each Buddy record as a row.
    for buddy in buddies:
        # Format date_of_insert if available.
        date_str = buddy.date_of_insert.strftime('%Y-%m-%d %H:%M:%S') if buddy.date_of_insert else ''
        row = [
            buddy.id,
            buddy.name,
            buddy.surname,
            buddy.email,
            buddy.nationality,        # Consider converting JSON to a formatted string if needed.
            buddy.languages_spoken,   # May require conversion if stored as JSON.
            buddy.faculty,
            buddy.phone_number,
            buddy.instagram,
            buddy.telegram,
            buddy.interests,
            buddy.gender,
            buddy.description,
            buddy.semester,
            buddy.year,
            date_str,
            buddy.esn_member_id
        ]
        ws_buddies.append(row)

    # --- Create and populate the ESNers sheet ---
    ws_esners = wb.create_sheet(title="ESNers")
    esner_headers = [
        "ID", "Name", "Surname", "Email", "Phone Number", "Languages Spoken", 
        "Nationality", "Gender", "Faculty", "Interests", "Description"
    ]
    ws_esners.append(esner_headers)

    # Append each ESNer record as a row.
    for esner in esners:
        row = [
            esner.id,
            esner.name,
            esner.surname,
            esner.email,
            esner.phone_number,
            esner.languages_spoken,  # May require processing if stored as JSON.
            esner.nationality,
            esner.gender,
            esner.faculty,
            esner.interests,
            esner.description
        ]
        ws_esners.append(row)

    # Save the workbook to a BytesIO stream.
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output