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

import functools
from operator import or_
import random
import string
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from sqlalchemy import and_
from werkzeug.security import check_password_hash, generate_password_hash
from database.tables import Esner, EsnerRole, Role, db
from utils.email_service import email_service

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