import json
from database.db import db
from database.tables import Role, Esner, EsnerRole  # Assuming 'EsnerRole' is the table linking roles to esners

def add_test_esner_and_admin_role():
    # Step 1: Check if "Buddy Program Admin" role exists, if not, create it.
    admin_role = Role.query.filter_by(name="Admin").first()
    if admin_role is None:
        # Create the Buddy Program Admin role if it doesn't exist
        admin_role = Role(name="Admin")
        db.session.add(admin_role)
        print("added Admin to Role")
    # Step 1: Check if "Buddy Program Admin" role exists, if not, create it.
    admin_buddy_role = Role.query.filter_by(name="Buddy Program Admin").first()
    if admin_buddy_role is None:
        # Create the Buddy Program Admin role if it doesn't exist
        admin_buddy_role = Role(name="Buddy Program Admin")
        db.session.add(admin_buddy_role)
        print("added Buddy Program Admin to Role")


    # Check for "Buddy Program Manager" role
    manager_buddy_role = Role.query.filter_by(name="Buddy Program Manager").first()
    if manager_buddy_role is None:
        # Create and add the "Buddy Program Manager" role
        manager_buddy_role = Role(name="Buddy Program Manager")
        db.session.add(manager_buddy_role)
        print("added Buddy Program Manager to Role")


    

    # Step 2: Check if the test ESN member exists (based on email or name)
    existing_admin = EsnerRole.query.filter_by(role_id=admin_role.id).first()  # Check for an existing admin role
    if existing_admin is None:
        # Create a new test ESN member if they don't exist
        test_esner = Esner(
            name="Test",
            surname="ESN",
            email="test@esnpalermo.com",
            phone_number="1234567890",
            languages_spoken='["English", "Spanish"]',
            nationality='["American"]',
            gender="Male",
            faculty='["Computer Science"]',
            interests='["Buddy Program", "Erasmus"]',
            max_number_of_buddy=5,
            description='Test ESN Member',
        )
        test_esner.set_password("test")  # Set a test password
        db.session.add(test_esner)
        print(f"added Esn Admin {test_esner.email} : test")

        
        # Step 3: Create a link (EsnerRole) between the test ESN member and the Buddy Program Admin role
        # First, check if the test ESN member already has the "Buddy Program Admin" role
        esner_role = EsnerRole.query.filter_by(esner_id=test_esner.id, role_id=admin_role.id).first()
        
        if esner_role is None:
            # Create a new relationship between the test ESN member and the "Buddy Program Admin" role
            esner_role = EsnerRole(esner_id=test_esner.id, role_id=admin_role.id)
            db.session.add(esner_role)
            esner_role = EsnerRole(esner_id=test_esner.id, role_id=admin_buddy_role.id)
            db.session.add(esner_role)

            print("Added test to admin role")

        # Commit all changes to the database
        db.session.commit()

def load_options():
    """
    Loads registration form options from a JSON file.

    Returns:
        dict: Parsed JSON data containing form options.
    """
    with open('./utils/options.json', 'r') as file:
        data = json.load(file)
    return data