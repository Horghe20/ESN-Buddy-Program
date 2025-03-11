# Admin

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Controller](./index.md#controller) / Admin

> Auto-generated documentation for [controller.admin](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/admin.py) module.

#### Attributes

- `bp` - Create a blueprint for admin-related routes with URL prefix '/admin': Blueprint('admin', __name__, url_prefix='/admin')


- [Admin](#admin)
  - [esner_info](#esner_info)
  - [index](#index)
  - [manage_esner_role](#manage_esner_role)
  - [remove_all](#remove_all)

## esner_info

[Show source in admin.py:34](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/admin.py#L34)

Manage ESNer information, including viewing, updating, and deleting ESNers.

GET request:
  - Retrieves the ESNer by ID and renders their profile page with roles.

PUT request:
  - Updates the ESNer's details based on provided JSON data.

DELETE request:
  - Deletes the ESNer if they have no associated Buddies and are not the current user.

#### Arguments

- `esner_id` - ID of the ESNer to manage.

#### Returns

Rendered HTML template, JSON response, or error message.

#### Signature

```python
@bp.route("/esner/<int:esner_id>", methods=["GET", "PUT", "DELETE"])
@login_required
@admin_required
def esner_info(esner_id): ...
```

#### See also

- [admin_required](./auth.md#admin_required)
- [login_required](./auth.md#login_required)



## index

[Show source in admin.py:18](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/admin.py#L18)

Render the admin index page displaying all registered ESNers.

GET request:
  - Retrieves all ESNer records from the database, including their roles.
  - Renders the 'admin/index.html' template with the list of ESNers.

#### Returns

Rendered HTML template with ESNer data.

#### Signature

```python
@bp.route("/index", methods=["GET"])
@login_required
@admin_required
def index(): ...
```

#### See also

- [admin_required](./auth.md#admin_required)
- [login_required](./auth.md#login_required)



## manage_esner_role

[Show source in admin.py:92](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/admin.py#L92)

Manage roles for a specific ESNer, including adding and removing roles.

POST request:
  - Adds a role to the ESNer if not already assigned.

DELETE request:
  - Removes a role from the ESNer, ensuring at least one admin remains.

#### Arguments

- `esner_id` - ID of the ESNer to manage roles for.

#### Returns

JSON response indicating success or error.

#### Signature

```python
@bp.route("/esner/<int:esner_id>/role", methods=["POST", "DELETE"])
@login_required
@admin_required
def manage_esner_role(esner_id): ...
```

#### See also

- [admin_required](./auth.md#admin_required)
- [login_required](./auth.md#login_required)



## remove_all

[Show source in admin.py:144](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/admin.py#L144)

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
@login_required
@buddy_program_admin_required
def remove_all(): ...
```

#### See also

- [buddy_program_admin_required](./auth.md#buddy_program_admin_required)
- [login_required](./auth.md#login_required)