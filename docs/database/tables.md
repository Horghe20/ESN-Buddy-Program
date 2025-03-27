# Tables

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Database](./index.md#database) / Tables

> Auto-generated documentation for [database.tables](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py) module.

- [Tables](#tables)
  - [Buddy](#buddy)
    - [Buddy().get_faculty](#buddy()get_faculty)
    - [Buddy().get_interests](#buddy()get_interests)
    - [Buddy().get_languages_spoken](#buddy()get_languages_spoken)
    - [Buddy().get_nationality](#buddy()get_nationality)
    - [Buddy().set_faculty](#buddy()set_faculty)
    - [Buddy().set_interests](#buddy()set_interests)
    - [Buddy().set_languages_spoken](#buddy()set_languages_spoken)
    - [Buddy().set_nationality](#buddy()set_nationality)
  - [Esner](#esner)
    - [Esner().check_password](#esner()check_password)
    - [Esner().get_faculty](#esner()get_faculty)
    - [Esner().get_interests](#esner()get_interests)
    - [Esner().get_languages_spoken](#esner()get_languages_spoken)
    - [Esner().get_nationality](#esner()get_nationality)
    - [Esner().set_faculty](#esner()set_faculty)
    - [Esner().set_interests](#esner()set_interests)
    - [Esner().set_languages_spoken](#esner()set_languages_spoken)
    - [Esner().set_nationality](#esner()set_nationality)
    - [Esner().set_password](#esner()set_password)
  - [EsnerRole](#esnerrole)
  - [EsnerType](#esnertype)
  - [PasswordResetToken](#passwordresettoken)
    - [PasswordResetToken().create_token](#passwordresettoken()create_token)
    - [PasswordResetToken().is_token_valid](#passwordresettoken()is_token_valid)
  - [Role](#role)

## Buddy

[Show source in tables.py:11](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L11)

Represents an Erasmus student (Buddy) in the ESN Buddy Program.

#### Attributes

- `id` *int* - Primary key.
- `name` *str* - First name of the student.
- `surname` *str* - Last name of the student.
- `email` *str* - Unique email address.
- `nationality` *str* - JSON-encoded nationality information.
- `languages_spoken` *str* - JSON-encoded list of languages spoken.
- `faculty` *str* - JSON-encoded list of faculties.
- `phone_number` *str* - Unique contact number.
- `instagram` *str* - Instagram handle.
- `telegram` *str* - Telegram handle.
- `interests` *str* - JSON-encoded list of interests.
- `gender` *str* - Gender of the student.
- `description` *str* - Additional information.
- `semester` *str* - Semester of exchange (e.g., "Fall", "Spring").
- `year` *int* - Year of exchange.
- `date_of_insert` *datetime* - Timestamp of record creation.
- `esn_member_id` *int* - Foreign key referencing the Esners model.

#### Signature

```python
class Buddy(db.Model): ...
```

### Buddy().get_faculty

[Show source in tables.py:74](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L74)

Retrieves faculty information from a JSON string.

#### Signature

```python
def get_faculty(self): ...
```

### Buddy().get_interests

[Show source in tables.py:82](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L82)

Retrieves interests from a JSON string.

#### Signature

```python
def get_interests(self): ...
```

### Buddy().get_languages_spoken

[Show source in tables.py:58](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L58)

Retrieves the list of languages from a JSON string.

#### Signature

```python
def get_languages_spoken(self): ...
```

### Buddy().get_nationality

[Show source in tables.py:66](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L66)

Retrieves nationality information from a JSON string.

#### Signature

```python
def get_nationality(self): ...
```

### Buddy().set_faculty

[Show source in tables.py:70](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L70)

Stores faculty information as a JSON string.

#### Signature

```python
def set_faculty(self, faculties): ...
```

### Buddy().set_interests

[Show source in tables.py:78](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L78)

Stores interests as a JSON string.

#### Signature

```python
def set_interests(self, interests): ...
```

### Buddy().set_languages_spoken

[Show source in tables.py:54](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L54)

Stores a list of languages as a JSON string.

#### Signature

```python
def set_languages_spoken(self, languages): ...
```

### Buddy().set_nationality

[Show source in tables.py:62](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L62)

Stores nationality information as a JSON string.

#### Signature

```python
def set_nationality(self, nationalities): ...
```



## Esner

[Show source in tables.py:93](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L93)

Represents an ESN member who assists Erasmus students.

#### Attributes

- `id` *int* - Primary key.
- `name` *str* - First name of the ESN member.
- `surname` *str* - Last name of the ESN member.
- `type` *str* - type of esner, Volounteer, Honorarium, Alumnus
- `email` *str* - Unique email address.
- `phone_number` *str* - Contact number.
- `languages_spoken` *str* - JSON-encoded list of languages spoken.
- `nationality` *str* - JSON-encoded nationality information.
- `gender` *str* - Gender of the ESN member.
- `faculty` *str* - JSON-encoded list of faculties.
- `interests` *str* - JSON-encoded list of interests.
- `max_number_of_buddy` *int* - Maximum number of Buddies they can manage.
- `description` *str* - Additional information.
- `password_hash` *str* - Hashed password for authentication.
- `buddies` *relationship* - One-to-many relationship with Buddy model.
- `roles` *relationship* - Many-to-many relationship with Role model.

#### Signature

```python
class Esner(db.Model): ...
```

### Esner().check_password

[Show source in tables.py:171](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L171)

Checks if the given password matches the stored hash.

#### Signature

```python
def check_password(self, password): ...
```

### Esner().get_faculty

[Show source in tables.py:154](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L154)

Retrieves faculty information from a JSON string.

#### Signature

```python
def get_faculty(self): ...
```

### Esner().get_interests

[Show source in tables.py:162](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L162)

Retrieves interests from a JSON string.

#### Signature

```python
def get_interests(self): ...
```

### Esner().get_languages_spoken

[Show source in tables.py:138](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L138)

Retrieves the list of languages from a JSON string.

#### Signature

```python
def get_languages_spoken(self): ...
```

### Esner().get_nationality

[Show source in tables.py:146](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L146)

Retrieves nationality information from a JSON string.

#### Signature

```python
def get_nationality(self): ...
```

### Esner().set_faculty

[Show source in tables.py:150](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L150)

Stores faculty information as a JSON string.

#### Signature

```python
def set_faculty(self, faculties): ...
```

### Esner().set_interests

[Show source in tables.py:158](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L158)

Stores interests as a JSON string.

#### Signature

```python
def set_interests(self, interests): ...
```

### Esner().set_languages_spoken

[Show source in tables.py:134](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L134)

Stores a list of languages as a JSON string.

#### Signature

```python
def set_languages_spoken(self, languages): ...
```

### Esner().set_nationality

[Show source in tables.py:142](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L142)

Stores nationality information as a JSON string.

#### Signature

```python
def set_nationality(self, nationalities): ...
```

### Esner().set_password

[Show source in tables.py:167](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L167)

Hashes and stores the given password.

#### Signature

```python
def set_password(self, password): ...
```



## EsnerRole

[Show source in tables.py:196](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L196)

#### Attributes

- `esner` - Relationships: db.relationship('Esner', back_populates='roles')


Represents the association between an esner and a role.

This table creates a many-to-many relationship between Esners and Roles.

#### Attributes

- `esner_id` *int* - Foreign key referring to the Esner.
- `role_id` *int* - Foreign key referring to the Role.

Relationships:
    - `esner` *Esner* - The esner associated with the role.
    - `role` *Role* - The role associated with the esner.

#### Signature

```python
class EsnerRole(db.Model): ...
```



## EsnerType

[Show source in tables.py:87](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L87)

#### Signature

```python
class EsnerType(str, Enum): ...
```



## PasswordResetToken

[Show source in tables.py:218](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L218)

#### Attributes

- `id` - Primary Key: db.Column(db.Integer, primary_key=True)

- `token` - Token and Esner Information: db.Column(db.String(255), nullable=False, unique=True)

- `created_at` - Timestamp Tracking: db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

- `ip_address` - Request Metadata: db.Column(db.String(45), nullable=True)

- `esner` - Relationship with Esner model: db.relationship('Esner', backref='password_reset_tokens')


Represents a password reset token for Esner authentication and password recovery.

This model stores temporary tokens used for securely resetting Esner passwords.
Each token is associated with a specific Esner and has a limited validity period.

#### Attributes

- `id` *int* - Unique identifier for the password reset token.
- `token` *str* - Unique cryptographic token for password reset.
- `esner_id` *int* - Foreign key referencing the Esner requesting the password reset.
- `email` *str* - Email address associated with the password reset request.
- `created_at` *datetime* - Timestamp of token creation.
- `expires_at` *datetime* - Timestamp when the token becomes invalid.
- `used` *bool* - Indicates whether the token has been used to reset the password.
- `used_at` *datetime, optional* - Timestamp when the token was used.
- `ip_address` *str, optional* - IP address of the password reset request.
- `user_agent` *str, optional* - User agent information of the request.

Relationships:
    - `esner` *relationship* - Relationship with the Esner model.

#### Signature

```python
class PasswordResetToken(db.Model): ...
```

### PasswordResetToken().create_token

[Show source in tables.py:260](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L260)

Creates a new password reset token for an Esner.

#### Arguments

- [esner_id](#passwordresettoken) *int* - ID of the Esner requesting password reset.
- [token](#passwordresettoken) *str* - Cryptographic token for password reset.
- `expiration_hours` *int, optional* - Hours until token expires. Defaults to 1.
- [ip_address](#passwordresettoken) *str, optional* - IP address of the request. Defaults to None.
- [user_agent](#passwordresettoken) *str, optional* - User agent of the request. Defaults to None.

#### Returns

- [PasswordResetToken](#passwordresettoken) - A new password reset token instance.

#### Signature

```python
def create_token(
    self, esner_id, token, expiration_hours=24, ip_address=None, user_agent=None
): ...
```

### PasswordResetToken().is_token_valid

[Show source in tables.py:284](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L284)

Checks if a password reset token is valid and not expired.

#### Returns

- `bool` - True if the token is valid and not used, False otherwise.

#### Signature

```python
def is_token_valid(self): ...
```



## Role

[Show source in tables.py:176](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L176)

#### Attributes

- `esner` - Relationship with UserRole: db.relationship('EsnerRole', back_populates='role', cascade='all, delete-orphan')


Represents a role in the system.

#### Attributes

- `id` *int* - Unique identifier for the role.
- `name` *str* - The name of the role (e.g., "Admin", "Editor").

Relationships:
    - `esner` *list* - List of EsnerRole associations linking this role to esners.

#### Signature

```python
class Role(db.Model): ...
```