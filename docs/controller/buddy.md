# Buddy

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Controller](./index.md#controller) / Buddy

> Auto-generated documentation for [controller.buddy](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy.py) module.

#### Attributes

- `bp` - Create a blueprint for registration-related routes, with URL prefix '/buddy': Blueprint('buddy', __name__, url_prefix='/buddy')


- [Buddy](#buddy)
  - [registration](#registration)

## registration

[Show source in buddy.py:14](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy.py#L14)

Handles the registration of Erasmus students (Buddies).

This function supports both GET and POST requests:

GET:
    - Renders the Buddy registration form.
    - Loads additional options from a JSON file to populate form fields.

POST:
    - Receives registration data in JSON format.
    - Validates the uniqueness of the email and phone number.
    - Creates a new Buddy record in the database with the provided data.
    - Sends a registration confirmation email to the Buddy.
    - Commits the new Buddy to the database.

#### Returns

- On successful registration (POST): JSON response with a success message and HTTP status 200.
- On validation failure (POST): JSON response with an error message and HTTP status 400.
- On server error (GET/POST): Renders an error page or returns a JSON error message with HTTP status 500.

#### Signature

```python
@bp.route("/registration", methods=["GET", "POST"])
def registration(): ...
```