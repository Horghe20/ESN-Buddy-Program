"""
API package for ESN Buddy Program

This package is a core component of the ESN (Erasmus Student Network) buddy program system,
designed to facilitate the pairing of Erasmus students (Buddies) with ESN members (ESNers).
The package is built using Flask and SQLAlchemy, providing an API interface for managing
user authentication, registration, administration, and matchmaking processes.

Modules:

1. auth.py:
   - Manages user authentication for admin users.
   - Provides routes for login and logout.
   - Includes decorators for protecting routes that require authentication and admin privileges.

2. admin.py:
   - Provides administrative functionalities for managing admin users.
   - Includes routes for viewing, adding, removing, and updating admin details.
   - Supports exporting Buddy and ESNers data to Excel and performing bulk deletions.

3. registration.py:
   - Manages the registration process for Buddies and ESNers.
   - Provides routes for rendering registration forms and processing form submissions.
   - Validates input data and stores it in the database.

4. match.py:
   - Implements the matchmaking logic between Buddies and ESNers.
   - Provides routes for automatic and manual matching.
   - Includes functionalities for confirming and removing matches, as well as removing Buddies and ESNers.
"""