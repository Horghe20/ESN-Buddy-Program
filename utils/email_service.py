"""
Email Service Module

This module defines the `EmailService` class, which provides methods for sending various types
of email notifications within the ESN matchmaking system. It utilizes the Flask-Mail extension
to handle email sending operations, allowing the application to communicate with users via email.

Components:

- EmailService Class: Manages the setup and sending of emails using Flask-Mail.
  - Methods:
    - `send_email(to_email, subject, template)`: Sends a generic email with the specified recipient, subject, and HTML template.
    - `send_match_notification_buddy(buddy, esner)`: Sends a notification email to a Buddy when they are matched with an ESNer.
    - `send_match_notification_esner(buddy, esner)`: Sends a notification email to an ESNer when a Buddy is assigned to them.
    - `send_unmatch_notification_buddy(buddy)`: Sends a notification email to a Buddy when their match is removed.
    - `send_unmatch_notification_esner(buddy, esner)`: Sends a notification email to an ESNer when a Buddy is removed from their match list.
    - `send_data_elimination_notification(name, email)`: Sends a notification email to a user when their data is removed from the system.
    - `send_reset_password_email(email, password)`: Sends a password reset email to the specified email address with a new password.

Usage:

- Create an instance of `EmailService` to use its methods for sending emails.
- Ensure that the Flask application is configured with the necessary email server settings.

Example:

```python
from flask import Flask
from email_service import email_service

app = Flask(__name__)
# Configure your app with email server settings
email_service.send_match_notification_buddy(buddy, esner)
Security Note: Ensure that sensitive information such as email credentials is kept secure and not exposed in version control systems.
"""

from flask_mail import Message, Mail
from flask import current_app

class EmailService:
    """
    A service class for handling email notifications within the ESN system.
    This class is responsible for sending various types of emails, such as:
    - Matching notifications between Buddies and ESNers.
    - Unmatch notifications when a match is removed.
    - Notifications for data elimination and password resets.
    """

    def __init__(self):
        """
        Initializes the EmailService class and sets up the Flask Mail instance.
        """
        self.mail = Mail()

    def send_email(self, to_email, subject, template):
        """
        Sends an email with the specified subject and HTML template to the given recipient.
        
        :param to_email: The email address of the recipient.
        :param subject: The subject of the email.
        :param template: The HTML content of the email.
        """
        msg = Message(
            subject=subject,
            recipients=[to_email],
            html=template,
            sender=current_app.config["MAIL_USERNAME"]
        )
        self.mail.send(msg)

    def send_match_notification_buddy(self, buddy, esner):
        """
        Sends a match notification to a Buddy when they are matched with an ESNer.
        
        :param buddy: The Buddy instance who is matched.
        :param esner: The ESNer instance with whom the Buddy is matched.
        """
        subject = "🎉 You've been matched with an ESNer!"
        template = f"""
        <h2>Hi {buddy.name},</h2>
        <p>We are excited to inform you that you have been matched with an ESNer!</p>
        <p><b>Your ESNer:</b> {esner.name} {esner.surname}</p>
        <p>Contact them at:</p>
        <ul>
            <li>Email: {esner.email}</li>
            <li>Phone: {esner.phone_number}</li>
        </ul>
        <p>We hope you enjoy this experience and build a great connection!</p>
        """
        self.send_email(buddy.email, subject, template)

    def send_match_notification_esner(self, buddy, esner):
        """
        Sends a match notification to an ESNer when they are assigned a Buddy.
        
        :param buddy: The Buddy instance assigned to the ESNer.
        :param esner: The ESNer instance who is assigned a Buddy.
        """
        subject = "🎉 A Buddy has been assigned to you!"
        template = f"""
        <h2>Hi {esner.name},</h2>
        <p>Great news! A Buddy has been assigned to you in the ESN Buddy Program.</p>
        <p><b>Your Buddy:</b> {buddy.name} {buddy.surname}</p>
        <p>Contact them at:</p>
        <ul>
            <li>Email: {buddy.email}</li>
            <li>Phone: {buddy.phone_number}</li>
        </ul>
        <p>Thank you for being part of the ESN community!</p>
        """
        self.send_email(esner.email, subject, template)

    def send_unmatch_notification_buddy(self, buddy):
        """
        Sends a notification to a Buddy when their match with an ESNer is removed.
        
        :param buddy: The Buddy instance whose match has been removed.
        """
        subject = "⚠️ Your ESN Buddy Match Has Been Removed"
        template = f"""
        <h2>Hi {buddy.name},</h2>
        <p>Unfortunately, your ESNer match has been removed.</p>
        <p>If you have any concerns, feel free to reach out to the ESN team.</p>
        """
        self.send_email(buddy.email, subject, template)

    def send_unmatch_notification_esner(self, buddy, esner):
        """
        Sends a notification to an ESNer when their match with a Buddy is removed.
        
        :param buddy: The Buddy instance whose match with the ESNer has been removed.
        :param esner: The ESNer instance whose match with the Buddy has been removed.
        """
        subject = "⚠️ Your Buddy has been removed from your match list"
        template = f"""
        <h2>Hi {esner.name},</h2>
        <p>Your Buddy, <b>{buddy.name} {buddy.surname}</b>, is no longer assigned to you.</p>
        <p>You will be assigned a new Buddy soon!</p>
        <p>If you need further assistance, feel free to contact the ESN team.</p>
        """
        self.send_email(esner.email, subject, template)

    def send_data_elimination_notification(self, name, email):
        """
        Sends a notification email to inform a user that their data has been removed from the system.
        
        :param name: The name of the user whose data has been removed.
        :param email: The email address of the user to send the notification to.
        """
        subject = "Your Data Has Been Removed"
        message = f"Dear {name},\n\nYour personal data has been completely removed from our system.\n\nBest regards,\nYour ESN Team"
        self.send_email(email, subject, message)

    def send_reset_password_email(self, email, password):
        """
        Sends an email with a new password when a user requests a password reset.
        
        :param email: The email address of the user to send the password reset email to.
        :param password: The new password to be provided to the user.
        """
        subject = "Reset Your Password"
        body = f"You requested a password reset. The following is your new password, use it for access and change the password:{password} If you did not request this, please ignore this email."
        self.send_email(email, subject, body)

email_service = EmailService()

