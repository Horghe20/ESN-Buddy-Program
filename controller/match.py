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

import smtplib
from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import asc, case, func
from utils.email_service import email_service
from utils.match import match_making
from database.tables import Buddy, Esners
from database.db import db
from controller.auth import login_required

# Create a Blueprint for the match module with the URL prefix '/match'
bp = Blueprint('match', __name__, url_prefix='/match')


@bp.route('/automatic_match', methods=['GET'])
@login_required
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
    try:
        esners = (
            Esners.query
            .outerjoin(Buddy, Esners.id == Buddy.esn_member_id)
            .group_by(Esners.id)
            .having(func.count(Buddy.id) < Esners.max_number_of_buddy)
            .all()
        )      
        buddies = Buddy.query.filter_by(esn_member_id=None).all()

        if not esners or not buddies:
            return render_template("errors/errors.html", code=400, message="Not enough data for auto-matching"), 400
        
        data = match_making(buddies, esners)
        
        return render_template("match/automatic_match.html", data=data), 200
    except Exception as e:
        print(e)
        return render_template("errors/errors.html", code=500), 500


@bp.route('/manual_match', methods=['GET'])
@login_required
def manual_match():
    """
    Displays ESNers and Buddies for manual matching.

    - Orders ESNers by the number of Buddies they have.
    - Orders Buddies by whether they are matched and by their registration date.

    Returns:
        - Rendered template with ESNers and Buddies for matching.
    """
    try:
        esners = Esners.query.outerjoin(Buddy).group_by(Esners.id).order_by(func.count(Buddy.id)).all()
        
        buddies = Buddy.query.order_by(
            case(
                (Buddy.esn_member_id.isnot(None), 1),
                else_=0
            ),
            asc(Buddy.date_of_insert)
        ).all()    

        return render_template("match/manual_match.html", esners=esners, buddies=buddies)
    except Exception as e:
        print(e)
        return render_template("errors/errors.html", code=500), 500


@bp.route('/confirm_match', methods=['POST'])
@login_required
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
        esner = Esners.query.get(esner_id)

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

        esner = Esners.query.get(buddy.esn_member_id)

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
def remove_buddy(buddy_id):
    """
    Deletes a Buddy from the database.

    - Sends an email notification of data elimination.

    Returns:
        - Success message (HTTP 200).
        - Error messages (HTTP 404 or 500).
    """
    buddy = Buddy.query.get(buddy_id)
    
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


@bp.route('/remove/esner/<int:esner_id>', methods=['POST'])
@login_required
def remove_esner(esner_id):
    """
    Deletes an ESNer from the database.

    - Ensures the ESNer has no assigned Buddies before deletion.
    - Sends an email notification of data elimination.

    Returns:
        - Success message (HTTP 200).
        - Error messages (HTTP 400, 404, or 500).
    """
    esner = Esners.query.get(esner_id)
    
    if not esner:
        return jsonify({"error": "ESNer not found"}), 404
    
    if esner.buddies:
        return jsonify({"error": "Cannot remove ESNer with assigned buddies. Unassign buddies first."}), 400
    
    try:
        db.session.delete(esner)
        email_service.send_data_elimination_notification(esner.name, esner.email)
        db.session.commit()

        return jsonify({"message": "ESNer successfully removed"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Internal server error"}), 500
