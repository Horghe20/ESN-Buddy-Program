"""
Match Module for ESN Buddy Program

This module handles the matching process between Erasmus students (Buddies) and ESN members (ESNers).
It includes automatic and manual matching functionalities, match confirmation, and the ability to remove matches.

Blueprint:
    - match: Manages match-related routes with the URL prefix `/match`.

Functions:
    - automatic_match(): Automatically assigns Buddies to ESNers based on available slots.
    - manual_match(): Displays ESNers and Buddies for manual matching.
    - confirm_match(): Confirms a match between a Buddy and an ESNer.
    - remove_match(): Removes an existing match.
    - remove_buddy(): Deletes a Buddy from the database.
    - remove_esner(): Deletes an ESNer from the database (only if they have no assigned Buddies).
"""

from io import BytesIO
import smtplib
from flask import Blueprint, g, jsonify, render_template, request, send_file
import openpyxl
from sqlalchemy import asc, case, func
from utils.email_service import email_service
from utils.match import match_making
from database.tables import Buddy, Esner
from database.db import db
from controller.auth import buddy_program_admin_required, buddy_program_manager_required, login_required

# Create a Blueprint for the match module with the URL prefix '/match'
bp = Blueprint('match', __name__, url_prefix='/match')


@bp.route('/automatic_match', methods=['GET'])
@login_required
@buddy_program_manager_required
def automatic_match():
    """
    Automatically assigns Buddies to ESNers based on availability.

    - Retrieves ESNers with open buddy slots.
    - Retrieves unmatched Buddies.
    - Uses match_making utility to create matches.
    - Returns the match results in an HTML template.

    Returns:
        - On success: Rendered template with match data (HTTP 200).
        - On failure: Error message template (HTTP 400 or 500).
    """
    # try:
    esners = (
        Esner.query
        .outerjoin(Buddy, Esner.id == Buddy.esn_member_id)
        .group_by(Esner.id)
        .having(func.count(Buddy.id) < Esner.max_number_of_buddy)
        .all()
    )      
    buddies = Buddy.query.filter_by(esn_member_id=None).all()

    if not esners or not buddies:
        return render_template("utils/errors.html", code=400, message="Not enough data for auto-matching"), 400
    

    data = match_making(buddies, esners)
    
    return render_template("match/automatic_match.html", data=data), 200
    # except Exception as e:
    #     print(e)
    #     return render_template("utils/errors.html", code=500), 500


@bp.route('/manual_match', methods=['GET'])
@login_required
@buddy_program_manager_required
def manual_match():
    """
    Displays ESNers and Buddies for manual matching.

    - Orders ESNers by the number of Buddies they have.
    - Orders Buddies by whether they are matched and by their registration date.

    Returns:
        - Rendered template with ESNers and Buddies for matching.
    """
    # try:
    esners = Esner.query.outerjoin(Buddy).group_by(Esner.id).order_by(func.count(Buddy.id)).all()
    
    buddies = Buddy.query.order_by(
        case(
            (Buddy.esn_member_id.isnot(None), 1),
            else_=0
        ),
        asc(Buddy.date_of_insert)
    ).all()    

    return render_template("match/manual_match.html", esners=esners, buddies=buddies)
    # except Exception as e:
    #     print(e)
    #     return render_template("utils/errors.html", code=500), 500


@bp.route('/confirm_match', methods=['POST'])
@login_required
@buddy_program_manager_required
def confirm_match():
    """
    Confirms a match between a Buddy and an ESNer.

    - Updates the Buddy's `esn_member_id`.
    - Sends match confirmation emails.
    - Handles various SMTP errors for email notifications.

    Returns:
        - Success message (HTTP 200).
        - Error messages (HTTP 400, 404, or 500).
    """
    try:
        data = request.get_json()
        buddy_id = data.get('buddy_id')
        esner_id = data.get('esner_id')
        buddy = Buddy.query.get(buddy_id)
        esner = Esner.query.get(esner_id)

        if not buddy or not esner:
            return jsonify({"error": "Buddy or ESNer not found"}), 404

        buddy.esn_member_id = esner.id

        email_service.send_match_notification_buddy(buddy, esner)
        email_service.send_match_notification_esner(buddy, esner)
        
        db.session.commit()
        return jsonify({"message": "Match confirmed successfully!"}), 200
    except smtplib.SMTPException as e:
        return jsonify({"error": f"SMTP error occurred: {e}"}), 500
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.session.rollback()


@bp.route('/remove_match', methods=['POST'])
@login_required
@buddy_program_manager_required
def remove_match():
    """
    Removes an existing match.

    - Sets the Buddy's `esn_member_id` to None.
    - Sends unmatch notification emails.

    Returns:
        - Success message (HTTP 200).
        - Error messages (HTTP 400, 404, or 500).
    """
    try:
        data = request.get_json()
        buddy_id = data.get('buddy_id')

        buddy = Buddy.query.get(buddy_id)
        if not buddy or buddy.esn_member_id is None:
            return jsonify({"error": "Buddy is not matched or does not exist"}), 400

        esner = Esner.query.get(buddy.esn_member_id)

        buddy.esn_member_id = None

        email_service.send_unmatch_notification_buddy(buddy)
        email_service.send_unmatch_notification_esner(buddy, esner)
        
        db.session.commit()
        return jsonify({"message": "Unmatch confirmed successfully!"}), 200
    except smtplib.SMTPException as e:
        return jsonify({"error": f"SMTP error occurred: {e}"}), 500
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.session.rollback()


@bp.route('/remove/buddy/<int:buddy_id>', methods=['POST'])
@login_required
@buddy_program_admin_required
def remove_buddy(buddy_id):
    """
    Deletes a Buddy from the database.

    - Sends an email notification of data elimination.

    Returns:
        - Success message (HTTP 200).
        - Error messages (HTTP 404 or 500).
    """
    buddy = Buddy.query.get(buddy_id)
    print(buddy.id)
    if not buddy:
        return jsonify({"error": "Buddy not found"}), 404
    
    try:
        db.session.delete(buddy)
        email_service.send_data_elimination_notification(buddy.name, buddy.email)
        db.session.commit()

        return jsonify({"message": "Buddy successfully removed and notified"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/export_excel', methods=['GET'])
@login_required
@buddy_program_admin_required
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
        esners = Esner.query.all()
    
        # Generate the Excel file and return it as an attachment.
        return send_file(
            create_exel(buddies, esners),
            as_attachment=True,
            download_name="export.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(e)
        return render_template("utils/errors.html", code=500), 500


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
         - Columns (Headers): ID, Name, Surname, Type, Email, Phone Number, Languages Spoken, Nationality,
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
        "ID", "Name", "Surname", "Type", "Email", "Phone Number", "Languages Spoken", 
        "Nationality", "Gender", "Faculty", "Interests", "Description"
    ]
    ws_esners.append(esner_headers)

    # Append each ESNer record as a row.
    for esner in esners:
        row = [
            esner.id,
            esner.name,
            esner.surname,
            esner.type,
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