"""
Authentication Module for ESN Buddy Program

This module provides authentication functionality, including login, logout, and user session management.

Blueprint:
    - auth: Handles authentication-related routes with the URL prefix `/auth`.

Functions:
    - load_logged_in_user(): Loads the logged-in admin user before each request.
    - login_required(view): Decorator that restricts access to logged-in users.
    - admin_required(view): Decorator that restricts access to admin users.
    - buddy_program_admin_required(view): Decorator that restricts access to Buddy Program Admin users.
    - buddy_program_manager_required(view): Decorator that restricts access to Buddy Program Manager users.
    - login(): Handles user login via a login form or API request.
    - logout(): Logs out the current user and clears the session.
"""

from datetime import datetime, timedelta, timezone
import functools
from operator import or_
import random
import string
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from sqlalchemy import and_
from werkzeug.security import check_password_hash, generate_password_hash
from database.tables import Esner, EsnerRole, PasswordResetToken, Role, db
from utils.email_service import email_service
import secrets


# Create a blueprint for authentication with the URL prefix '/auth'
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """
    Loads the logged-in admin user before processing each request.
    
    This function retrieves the `esner_id` from the session and loads the corresponding
    Esner object into the global `g` object for easy access throughout the request lifecycle.
    It also determines the user's roles and sets appropriate flags for admin, buddy program admin,
    and buddy program manager roles.
    """
    esner_id = session.get('esner_id')
    g.esner = Esner.query.get(esner_id) if esner_id else None
    if g.esner:
        g.esner.admin = False
        g.esner.buddy_program_admin = False
        g.esner.buddy_program_manager = False

        admin_role = Role.query.filter_by(name="Admin").first()
        esner = (
            Esner.query
            .join(Esner.roles)
            .join(Role)
            .filter(
                and_(
                    EsnerRole.role_id == admin_role.id,
                    EsnerRole.esner_id == g.esner.id
                )
            )
            .first()
        )
        if esner:
            g.esner.admin = True

        admin_buddy_program_role = Role.query.filter_by(name="Buddy Program Admin").first()
        esner = (
            Esner.query
            .join(Esner.roles)
            .join(Role)
            .filter(
                and_(
                    EsnerRole.role_id == admin_buddy_program_role.id,
                    EsnerRole.esner_id == g.esner.id
                )
            )
            .first()
        )

        if esner:
            g.esner.buddy_program_admin = True
            g.esner.buddy_program_manager = True
        else:
            manager_buddy_program_role = Role.query.filter_by(name="Buddy Program Manager").first()
            esner = (
                Esner.query
                .join(Esner.roles)
                .join(Role)
                .filter(
                    and_(
                        EsnerRole.role_id == manager_buddy_program_role.id,
                        EsnerRole.esner_id == g.esner.id
                    )
                )
                .first()
            )
            if esner:
                g.esner.buddy_program_manager = True  

def login_required(view):
    """
    Decorator function to restrict access to authenticated (logged-in) users.

    If a user is not logged in, they are redirected to the login page.

    Args:
        view (function): The view function to wrap.

    Returns:
        function: The wrapped view function.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.esner is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    """
    Decorator function to restrict access to admin users only.

    If a user is not an admin (or not logged in), they are redirected to the profile page.

    Args:
        view (function): The view function to wrap.

    Returns:
        function: The wrapped view function.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.esner.admin:
            return redirect(url_for('esner.profile'))
        return view(**kwargs)
    return wrapped_view

def buddy_program_admin_required(view):
    """
    Decorator function to restrict access to Buddy Program Admin users.

    If a user is not a Buddy Program Admin (or not logged in), they are redirected to the profile page.

    Args:
        view (function): The view function to wrap.

    Returns:
        function: The wrapped view function.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.esner.admin and not g.esner.buddy_program_admin:
            return redirect(url_for('esner.profile'))
        return view(**kwargs)
    return wrapped_view

def buddy_program_manager_required(view):
    """
    Decorator function to restrict access to Buddy Program Manager users.

    If a user is not a Buddy Program Manager (or not logged in), they are redirected to the profile page.

    Args:
        view (function): The view function to wrap.

    Returns:
        function: The wrapped view function.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.esner.admin and not g.esner.buddy_program_manager and not g.esner.buddy_program_admin:
            return redirect(url_for('esner.profile'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user authentication.

    GET: 
        - Renders the login page.

    POST:
        - Authenticates the user using email and password.
        - If authentication is successful, stores the user ID in the session.
        - If authentication fails, returns an error response.

    Returns:
        - On success: JSON response with redirect URL (HTTP 200).
        - On failure: JSON response with error message (HTTP 401 or 500).
    """
    if request.method == 'GET':
        if g.esner:
            return redirect(url_for('esner.profile')) 
        else:
            return render_template("auth/login.html")
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            esner = Esner.query.filter_by(email=email).first()
            
            if esner and check_password_hash(esner.password_hash, password):
                session.clear()
                session['esner_id'] = esner.id
                return jsonify({"redirect": url_for('esner.profile')}), 200
            
            return jsonify({"error": "Invalid credentials"}), 401
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal server error"}), 500

@bp.route('/logout')
@login_required
def logout():
    """
    Logs out the currently authenticated user.

    - Clears the session data.
    - Redirects the user to the login page.

    Returns:
        - Redirect response to the login page.
    """
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    try:
        if request.method == 'GET':
            return render_template('auth/forgot_password.html')
        else:
            data = request.get_json()
            email = data.get('email')
            esner = Esner.query.filter_by(email=email).first()
            if esner:
                # Check if there's an existing valid token
                existing_token = PasswordResetToken.query.filter_by(
                    esner_id=esner.id
                ).filter(
                    PasswordResetToken.expires_at > datetime.now(timezone.utc)
                ).first()
                
                # If there's an existing token, reuse it or invalidate it
                if existing_token:
                    # Option 1: Reuse the existing token
                    token = existing_token.token
                    
                    # Option 2: Invalidate existing token and create new one
                    # existing_token.mark_as_used()
                    # db.session.commit()
                    # token = secrets.token_urlsafe(32)
                else:
                    # Generate a new secure token
                    token = secrets.token_urlsafe(32)
                # Create a new token if not reusing
                if not existing_token:
                    reset_token = PasswordResetToken(
                        token=token,
                        esner_id=esner.id,
                        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
                        ip_address=request.remote_addr,
                        user_agent=request.user_agent.string
                    )
                    db.session.add(reset_token)
                    db.session.commit()
                reset_link = url_for('auth.reset_password', token=token, _external=True)
                email_service.send_reset_password_email(esner.email, reset_link)
            return jsonify({"message": "A password reset link has been sent to your email if it exists in our system."}), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    try:
        if request.method == 'GET':
            return render_template('auth/reset_password.html')
        if request.method == 'POST':
            # Find the token in the database
            data = request.get_json()
            token = data.get('token')
            reset_token = PasswordResetToken.query.filter_by(token=token).first()
            # Check if token exists and is valid
            if not reset_token or not reset_token.is_token_valid():
                return jsonify({"error": "A password reset link is expired. Get another one"}), 400
            
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            
            if password != confirm_password:
                return jsonify({"error": "Passwords don't matchy"}), 400

            
            # Get esner from token
            esner = Esner.query.get(reset_token.esner_id)
            
            if esner:
                # Update password
                esner.set_password(password)
                
                db.session.delete(reset_token)       
                db.session.commit()
                
                return jsonify({"message": "Password changed"}), 200            
            else:
                return jsonify({"error": "Esners not found"}), 404
                
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500