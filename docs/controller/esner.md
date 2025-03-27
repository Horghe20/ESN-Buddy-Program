# Esner

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Controller](./index.md#controller) / Esner

> Auto-generated documentation for [controller.esner](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/esner.py) module.

#### Attributes

- `bp` - Create a blueprint for ESNer-related routes, with URL prefix '/esner': Blueprint('esner', __name__, url_prefix='/esner')


- [Esner](#esner)
  - [profile](#profile)
  - [registration](#registration)
  - [update_profile](#update_profile)

## profile

[Show source in esner.py:81](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/esner.py#L81)

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



## registration

[Show source in esner.py:14](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/esner.py#L14)

Handles the registration process for ESN members (ESNers).

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
def registration(): ...
```



## update_profile

[Show source in esner.py:95](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/esner.py#L95)

Handles the updating of an ESNer's profile.

GET:
    - Renders the update profile form with current ESNer data.

POST:
    - Receives updated profile data in JSON format.
    - Updates only the provided fields in the ESNer’s record.
    - Commits changes to the database.

#### Returns

- On successful update (POST): JSON response with a success message and HTTP status 200.
- On failure (POST): JSON response with an error message and appropriate HTTP status.

#### Signature

```python
@bp.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile(): ...
```

#### See also

- [login_required](./auth.md#login_required)