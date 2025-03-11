# Esner

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Controller](./index.md#controller) / Esner

> Auto-generated documentation for [controller.esner](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/esner.py) module.

#### Attributes

- `bp` - Create a blueprint for registration-related routes, with URL prefix '/registration': Blueprint('esner', __name__, url_prefix='/esner')


- [Esner](#esner)
  - [profile](#profile)
  - [register_esner](#register_esner)

## profile

[Show source in esner.py:87](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/esner.py#L87)

Renders the profile page for the logged-in ESNer.

This route is protected by a login requirement and handles GET requests to '/esner/profile'.
It displays the profile information of the currently logged-in ESNer.

#### Returns

- Rendered HTML template for the ESNer profile page.

#### Signature

```python
@bp.route("/profile", methods=["GET"])
@login_required
def profile(): ...
```

#### See also

- [login_required](./auth.md#login_required)



## register_esner

[Show source in esner.py:13](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/esner.py#L13)

Handles the registration process for ESN members (ESNers).

This function supports both GET and POST requests:

GET:
    - Renders the ESNer registration form.
    - Loads additional options from a JSON file to populate form fields.

POST:
    - Receives registration data in JSON format.
    - Validates the uniqueness of the email and phone number.
    - Ensures the email is an official ESN Palermo email.
    - Creates a new ESNer record in the database with the provided data.
    - Sets the password for the new ESNer.
    - Commits the new ESNer to the database.

#### Returns

- On successful registration (POST): JSON response with a success message and HTTP status 200.
- On validation failure (POST): JSON response with an error message and HTTP status 400.
- On server error (GET/POST): Renders an error page or returns a JSON error message with HTTP status 500.

#### Signature

```python
@bp.route("/registration", methods=["GET", "POST"])
def register_esner(): ...
```