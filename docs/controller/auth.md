# Auth

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Controller](./index.md#controller) / Auth

> Auto-generated documentation for [controller.auth](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py) module.

#### Attributes

- `bp` - Create a blueprint for authentication with the URL prefix '/auth': Blueprint('auth', __name__, url_prefix='/auth')


- [Auth](#auth)
  - [admin_required](#admin_required)
  - [buddy_program_admin_required](#buddy_program_admin_required)
  - [buddy_program_manager_required](#buddy_program_manager_required)
  - [forgot_password](#forgot_password)
  - [load_logged_in_user](#load_logged_in_user)
  - [login](#login)
  - [login_required](#login_required)
  - [logout](#logout)
  - [reset_password](#reset_password)

## admin_required

[Show source in auth.py:123](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L123)

Decorator function to restrict access to admin users only.

If a user is not an admin (or not logged in), they are redirected to the profile page.

#### Arguments

- `view` *function* - The view function to wrap.

#### Returns

- `function` - The wrapped view function.

#### Signature

```python
def admin_required(view): ...
```



## buddy_program_admin_required

[Show source in auth.py:142](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L142)

Decorator function to restrict access to Buddy Program Admin users.

If a user is not a Buddy Program Admin (or not logged in), they are redirected to the profile page.

#### Arguments

- `view` *function* - The view function to wrap.

#### Returns

- `function` - The wrapped view function.

#### Signature

```python
def buddy_program_admin_required(view): ...
```



## buddy_program_manager_required

[Show source in auth.py:161](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L161)

Decorator function to restrict access to Buddy Program Manager users.

If a user is not a Buddy Program Manager (or not logged in), they are redirected to the profile page.

#### Arguments

- `view` *function* - The view function to wrap.

#### Returns

- `function` - The wrapped view function.

#### Signature

```python
def buddy_program_manager_required(view): ...
```



## forgot_password

[Show source in auth.py:236](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L236)

#### Signature

```python
@bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password(): ...
```



## load_logged_in_user

[Show source in auth.py:37](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L37)

Loads the logged-in admin user before processing each request.

This function retrieves the `esner_id` from the session and loads the corresponding
Esner object into the global `g` object for easy access throughout the request lifecycle.
It also determines the user's roles and sets appropriate flags for admin, buddy program admin,
and buddy program manager roles.

#### Signature

```python
@bp.before_app_request
def load_logged_in_user(): ...
```



## login

[Show source in auth.py:180](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L180)

Handles user authentication.

GET:
    - Renders the login page.

POST:
    - Authenticates the user using email and password.
    - If authentication is successful, stores the user ID in the session.
    - If authentication fails, returns an error response.

#### Returns

- On success: JSON response with redirect URL (HTTP 200).
- On failure: JSON response with error message (HTTP 401 or 500).

#### Signature

```python
@bp.route("/login", methods=["GET", "POST"])
def login(): ...
```



## login_required

[Show source in auth.py:104](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L104)

Decorator function to restrict access to authenticated (logged-in) users.

If a user is not logged in, they are redirected to the login page.

#### Arguments

- `view` *function* - The view function to wrap.

#### Returns

- `function` - The wrapped view function.

#### Signature

```python
def login_required(view): ...
```



## logout

[Show source in auth.py:221](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L221)

Logs out the currently authenticated user.

- Clears the session data.
- Redirects the user to the login page.

#### Returns

- Redirect response to the login page.

#### Signature

```python
@bp.route("/logout")
@login_required
def logout(): ...
```

#### See also

- [login_required](#login_required)



## reset_password

[Show source in auth.py:283](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/auth.py#L283)

#### Signature

```python
@bp.route("/reset_password", methods=["GET", "POST"])
def reset_password(): ...
```