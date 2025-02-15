# Admin

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Controller](./index.md#controller) / Admin

> Auto-generated documentation for [controller.admin](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py) module.

#### Attributes

- `bp` - Create a blueprint for admin-related routes with URL prefix '/admin': Blueprint('admin', __name__, url_prefix='/admin')


- [Admin](#admin)
  - [add_admin](#add_admin)
  - [create_exel](#create_exel)
  - [export_excel](#export_excel)
  - [get_admin_info](#get_admin_info)
  - [index](#index)
  - [profile](#profile)
  - [remove_admin](#remove_admin)
  - [remove_all](#remove_all)
  - [update_admin](#update_admin)
  - [update_password](#update_password)

## add_admin

[Show source in admin.py:49](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L49)

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

#### Returns

JSON response with a success message (HTTP 200) or error message.

#### Signature

```python
@bp.route("/add_admin", methods=["POST"])
@admin_required
def add_admin(): ...
```

#### See also

- [admin_required](./auth.md#admin_required)



## create_exel

[Show source in admin.py:346](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L346)

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

#### Arguments

- `buddies` - List of Buddy instances.
- `esners` - List of ESNers instances.

#### Returns

A BytesIO stream containing the Excel file.

#### Signature

```python
def create_exel(buddies, esners): ...
```



## export_excel

[Show source in admin.py:274](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L274)

Export Buddy and ESNers data into an Excel file.

GET request:
  - Retrieves all Buddy and ESNers records from the database.
  - Calls create_exel() to generate an Excel workbook containing two sheets:
      1. Buddies sheet with details for each Buddy.
      2. ESNers sheet with details for each ESNer.
  - Returns the Excel file as a downloadable response.

#### Returns

Flask send_file response containing the Excel workbook.

#### Signature

```python
@bp.route("/export_excel", methods=["GET"])
@admin_required
def export_excel(): ...
```

#### See also

- [admin_required](./auth.md#admin_required)



## get_admin_info

[Show source in admin.py:147](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L147)

Retrieve information about a specific admin (excluding sensitive password details).

GET request:
  - The admin_id is provided as a URL parameter.
  - Retrieves the corresponding admin from the database.
  - Returns a JSON response with the admin's id, name, surname, phone number, email, and role.

#### Arguments

- `admin_id` - The ID of the admin whose information is requested.

#### Returns

JSON response containing admin details or an error message if not found.

#### Signature

```python
@bp.route("/get_admin_info/<int:admin_id>", methods=["GET"])
@admin_required
def get_admin_info(admin_id): ...
```

#### See also

- [admin_required](./auth.md#admin_required)



## index

[Show source in admin.py:33](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L33)

Render the admin index page displaying all registered admins.

GET request:
  - Retrieves all Admin records from the database using the model's query attribute.
  - Renders the 'admin/index.html' template with the list of admins.

#### Returns

Rendered HTML template with admin data.

#### Signature

```python
@bp.route("/index", methods=["GET"])
@admin_required
def index(): ...
```

#### See also

- [admin_required](./auth.md#admin_required)



## profile

[Show source in admin.py:20](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L20)

Render the profile page for the logged-in manager/admin.

This route handles GET requests to '/manager/profile' and renders a template
that displays the manager's profile information.

#### Returns

Rendered HTML template for the manager profile.

#### Signature

```python
@bp.route("/profile", methods=["GET"])
@login_required
def profile(): ...
```

#### See also

- [login_required](./auth.md#login_required)



## remove_admin

[Show source in admin.py:112](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L112)

Remove an admin from the system.

POST request:
  - The admin_id is provided as a URL parameter.
  - Checks if the admin exists. If the admin exists and is not the currently logged-in admin,
    the admin is deleted from the database.
  - If the logged-in admin attempts to remove themselves, an error is returned.

#### Arguments

- `admin_id` - The ID of the admin to be removed.

#### Returns

JSON response indicating success (HTTP 200) or an error message.

#### Signature

```python
@bp.route("/remove_admin/<int:admin_id>", methods=["POST"])
@admin_required
def remove_admin(admin_id): ...
```

#### See also

- [admin_required](./auth.md#admin_required)



## remove_all

[Show source in admin.py:306](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L306)

Export all Buddy and ESNers data to an Excel file and then remove all records.

GET request:
  - Retrieves all Buddy and ESNers records.
  - Generates an Excel file using create_exel().
  - Attempts to delete all records from both Buddy and ESNers tables.
  - Returns the Excel file as a downloadable response if deletion succeeds.
  - If an error occurs during deletion, the transaction is rolled back, and a 500 error is returned.

#### Returns

Flask send_file response containing the Excel workbook, or an error message.

#### Signature

```python
@bp.route("/export_and_remove_all", methods=["GET"])
@admin_required
def remove_all(): ...
```

#### See also

- [admin_required](./auth.md#admin_required)



## update_admin

[Show source in admin.py:180](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L180)

Update information for a specific admin.

PUT request:
  - Expects a JSON payload with any subset of the following fields:
      - name, surname, phone_number, email, role, password.
  - Retrieves the admin record by admin_id.
  - Updates the provided fields. If a password is provided, it is hashed using set_password().
  - Commits the changes to the database.

#### Arguments

- `admin_id` - The ID of the admin to update.

#### Returns

JSON response indicating success (HTTP 200) or an error message.

#### Signature

```python
@bp.route("/update_admin/<int:admin_id>", methods=["PUT"])
@admin_required
def update_admin(admin_id): ...
```

#### See also

- [admin_required](./auth.md#admin_required)



## update_password

[Show source in admin.py:225](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/admin.py#L225)

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

#### Returns

JSON response indicating success or error.

#### Signature

```python
@bp.route("/update_password", methods=["POST"])
@login_required
def update_password(): ...
```

#### See also

- [login_required](./auth.md#login_required)