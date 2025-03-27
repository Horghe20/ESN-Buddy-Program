from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, send_file, session, url_for
)
from sqlalchemy import case, func, or_
from sqlalchemy.orm import joinedload
import json
from werkzeug.security import check_password_hash, generate_password_hash
from controller.buddy_program.match import create_exel

from database.tables import Buddy, Esner, EsnerRole, Role
from database.db import db
from controller.auth import admin_required, buddy_program_admin_required, login_required
from utils.email_service import email_service

# Create a blueprint for admin-related routes with URL prefix '/admin'
bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/index', methods=['GET'])
@login_required
@admin_required
def index():
    """
    Render the admin index page displaying all registered ESNers.

    GET request:
      - Retrieves all ESNer records from the database, including their roles.
      - Renders the 'admin/index.html' template with the list of ESNers.

    :return: Rendered HTML template with ESNer data.
    """
    esners = Esner.query.outerjoin(Esner.roles).outerjoin(Role).options(joinedload(Esner.roles)).all()    
    return render_template("admin/index.html", esners=esners)

@bp.route('/esner/<int:esner_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
@admin_required
def esner_info(esner_id):
    """
    Manage ESNer information, including viewing, updating, and deleting ESNers.

    GET request:
      - Retrieves the ESNer by ID and renders their profile page with roles.

    PUT request:
      - Updates the ESNer's details based on provided JSON data.

    DELETE request:
      - Deletes the ESNer if they have no associated Buddies and are not the current user.

    :param esner_id: ID of the ESNer to manage.
    :return: Rendered HTML template, JSON response, or error message.
    """
    try:
        esner = Esner.query.get(esner_id)
        if esner:
            if request.method == "GET":
                roles = Role.query.all()
                return render_template("admin/esner_profile.html", esner=esner, roles=roles)
            
            if request.method == "PUT":
                data = request.get_json()
                if "name" in data:
                    esner.name = data.get("name")
                if "surname" in data:
                    esner.surname = data.get("surname")
                if "phone_number" in data:
                    esner.phone_number = data.get("phone_number")
                if "email" in data:
                    esner.email = data.get("email")
                if "password" in data and data.get("password"):
                    esner.set_password(data.get("password"))
                db.session.commit()
                return jsonify({"message": "Update successfully!"}), 200

            if request.method == "DELETE":
                if esner.id != g.esner.id:
                    if len(esner.buddies) == 0:
                        db.session.delete(esner)
                        email_service.send_data_elimination_notification(esner.name, esner.email)
                        db.session.commit()
                    else:
                        return jsonify({"error": "The Esner has some Buddies, remove before"}), 403
                else:
                    return jsonify({"error": "Can't remove yourself"}), 403

                return jsonify({"message": "Admin removed successfully!"}), 200
        
        return render_template("utils/errors.html", code=404)
    except Exception as e: 
        return jsonify({"error": "Internal Server Error"}), 403

@bp.route('/esner/<int:esner_id>/role', methods=['POST', 'DELETE'])
@login_required
@admin_required
def manage_esner_role(esner_id):
    """
    Manage roles for a specific ESNer, including adding and removing roles.

    POST request:
      - Adds a role to the ESNer if not already assigned.

    DELETE request:
      - Removes a role from the ESNer, ensuring at least one admin remains.

    :param esner_id: ID of the ESNer to manage roles for.
    :return: JSON response indicating success or error.
    """
    try:
        esner = Esner.query.get(esner_id)
        if esner:
            data = request.get_json()
            role_id = data.get('role_id')
            role = Role.query.get(role_id)
            if role:
                if request.method == "POST":
                    if not EsnerRole.query.filter_by(esner_id=esner_id, role_id=role_id).first():
                        esner_role = EsnerRole(esner_id=esner_id, role_id=role_id)
                        db.session.add(esner_role)
                        db.session.commit()
                        return jsonify({"message": "Role added successfully!"}), 200
                else:
                    esner_role = EsnerRole.query.filter_by(esner_id=esner_id, role_id=role_id).first()
                    if not esner_role:
                        return jsonify({"error": "Role not assigned to this Esner"}), 404

                    admin_role = Role.query.filter_by(name='Admin').first()
                    if not admin_role:
                        return jsonify({"error": "Admin role not found"}), 404

                    other_admin = EsnerRole.query.filter(EsnerRole.role_id == admin_role.id, EsnerRole.esner_id != esner_id).first()
                    if admin_role.id == role.id and not other_admin:
                        return jsonify({"error": "Cannot delete the only admin"}), 400

                    db.session.delete(esner_role)
                    db.session.commit()
                    return jsonify({"message": "Role removed successfully!"}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    return render_template("utils/errors.html", code=404)

@bp.route('/export_and_remove_all', methods=['GET'])
@login_required
@buddy_program_admin_required
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
    try:
        # Retrieve all Buddy and ESNers records using the model's query interface.
        buddies = Buddy.query.all()
        esners = Esner.query.all()

        Buddy.query.delete()
        Esner.query.filter(~Esner.roles.any()).delete()
        db.session.commit()
    
        # Generate the Excel file and return it as an attachment.
        return send_file(
            create_exel(buddies, esners),
            as_attachment=True,
            download_name="export.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Server Error"}), 500 