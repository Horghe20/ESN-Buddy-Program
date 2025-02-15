# Registration

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Controller](./index.md#controller) / Registration

> Auto-generated documentation for [controller.registration](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/registration.py) module.

#### Attributes

- `bp` - Create a blueprint for registration-related routes, with URL prefix '/registration': Blueprint('registration', __name__, url_prefix='/registration')


- [Registration](#registration)
  - [load_options](#load_options)
  - [register_buddy](#register_buddy)
  - [register_esners](#register_esners)

## load_options

[Show source in registration.py:28](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/registration.py#L28)

Loads registration form options from a JSON file.

#### Returns

- `dict` - Parsed JSON data containing form options.

#### Signature

```python
def load_options(): ...
```



## register_buddy

[Show source in registration.py:40](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/registration.py#L40)

Handles the registration of Erasmus students (Buddies).

GET:
    - Loads and displays the Buddy registration form.

POST:
    - Receives form data as JSON.
    - Validates email uniqueness.
    - Stores the new Buddy in the database.

#### Returns

- On success: JSON response with success message (HTTP 200).
- On failure: JSON response with an error message (HTTP 400 or 500).

#### Signature

```python
@bp.route("/buddy", methods=["GET", "POST"])
def register_buddy(): ...
```



## register_esners

[Show source in registration.py:103](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/registration.py#L103)

Handles the registration of ESN members (ESNers).

GET:
    - Loads and displays the ESNers registration form.

POST:
    - Receives form data as JSON.
    - Validates email and phone uniqueness.
    - Ensures the email is an official ESN Palermo email.
    - Stores the new ESNer in the database.

#### Returns

- On success: JSON response with success message (HTTP 200).
- On failure: JSON response with an error message (HTTP 400 or 500).

#### Signature

```python
@bp.route("/esners", methods=["GET", "POST"])
def register_esners(): ...
```