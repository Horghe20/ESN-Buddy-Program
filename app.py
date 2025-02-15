"""
Application Entry Point for ESN Buddy Program Matching System

This module initializes and configures the Flask web application. 
It sets up the database, error handling, and routes while also registering blueprints 
for different parts of the application.

Modules:
    - os: Provides functions to interact with the operating system.
    - flask: The Flask framework for building web applications.
    - database.db: Handles database connections and initialization.
    - utils.config: Application configuration settings.
    - utils.email_service: Handles email functionalities.
    - controller (auth, registration, match, admin): Defines routes and logic for user authentication, 
      registration, matching, and admin functionalities.

Functions:
    - create_app(test_config=None): Initializes and configures the Flask application.
"""

import os
from flask import Flask, redirect, url_for, render_template
from database.db import db, init_db  # Import the SQLAlchemy instance and initialization function
from utils import config  # Import configuration settings

def create_app(test_config=None):
    """
    Factory function to create and configure the Flask application.

    Args:
        test_config (dict, optional): Configuration settings for testing. Defaults to None.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)  
    app.config.from_object("utils.config")  

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """
        Ensures that the database session is properly closed after each request.

        Args:
            exception (Exception, optional): The exception that occurred, if any. Defaults to None.
        """
        db.session.remove()

    @app.route('/')
    def home():
        """
        Root route that redirects users to the manual match page.

        Returns:
            Response: A redirect response to the match manual match page.
        """
        return redirect(url_for('match.manual_match'))

    @app.errorhandler(404)
    def page_not_found(e):
        """
        Handles 404 errors by rendering a custom error page.

        Args:
            e (Exception): The error instance.

        Returns:
            Tuple[Response, int]: A tuple containing the rendered error page and HTTP status code.
        """
        return render_template('errors/errors.html', code=404), 200

    with app.app_context():
        init_db(app)  
        from database.tables import Admin, Esners, Buddy  

        db.create_all()  

        # Ensure there is at least one admin user
        if not Admin.query.first():
            print("No admin found. Creating a test admin...")
            new_admin = Admin(
                name="test",
                surname="test",
                phone_number="+391111111111",
                email="test@esnpalermo.com",
                role=1  
            )
            new_admin.set_password("test")  
            db.session.add(new_admin)
            db.session.commit()
            print("Test admin created successfully.")
        else:
            print("Admin already exists. No new admin created.")

    # Initialize email service
    from utils.email_service import email_service
    email_service.mail.init_app(app)

    # Register application blueprints
    import controller.auth, controller.registration, controller.match, controller.admin
    app.register_blueprint(controller.auth.bp)
    app.register_blueprint(controller.registration.bp)
    app.register_blueprint(controller.match.bp)
    app.register_blueprint(controller.admin.bp)

    return app  

# Create application instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  
