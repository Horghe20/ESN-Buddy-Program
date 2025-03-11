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
  - [Role](#role)

## Buddy

[Show source in tables.py:10](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L10)

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

[Show source in tables.py:73](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L73)

Retrieves faculty information from a JSON string.

#### Signature

```python
def get_faculty(self): ...
```

### Buddy().get_interests

[Show source in tables.py:81](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L81)

Retrieves interests from a JSON string.

#### Signature

```python
def get_interests(self): ...
```

### Buddy().get_languages_spoken

[Show source in tables.py:57](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L57)

Retrieves the list of languages from a JSON string.

#### Signature

```python
def get_languages_spoken(self): ...
```

### Buddy().get_nationality

[Show source in tables.py:65](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L65)

Retrieves nationality information from a JSON string.

#### Signature

```python
def get_nationality(self): ...
```

### Buddy().set_faculty

[Show source in tables.py:69](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L69)

Stores faculty information as a JSON string.

#### Signature

```python
def set_faculty(self, faculties): ...
```

### Buddy().set_interests

[Show source in tables.py:77](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L77)

Stores interests as a JSON string.

#### Signature

```python
def set_interests(self, interests): ...
```

### Buddy().set_languages_spoken

[Show source in tables.py:53](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L53)

Stores a list of languages as a JSON string.

#### Signature

```python
def set_languages_spoken(self, languages): ...
```

### Buddy().set_nationality

[Show source in tables.py:61](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L61)

Stores nationality information as a JSON string.

#### Signature

```python
def set_nationality(self, nationalities): ...
```



## Esner

[Show source in tables.py:87](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L87)

Represents an ESN member who assists Erasmus students.

#### Attributes

- `id` *int* - Primary key.
- `name` *str* - First name of the ESN member.
- `surname` *str* - Last name of the ESN member.
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

[Show source in tables.py:163](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L163)

Checks if the given password matches the stored hash.

#### Signature

```python
def check_password(self, password): ...
```

### Esner().get_faculty

[Show source in tables.py:146](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L146)

Retrieves faculty information from a JSON string.

#### Signature

```python
def get_faculty(self): ...
```

### Esner().get_interests

[Show source in tables.py:154](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L154)

Retrieves interests from a JSON string.

#### Signature

```python
def get_interests(self): ...
```

### Esner().get_languages_spoken

[Show source in tables.py:130](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L130)

Retrieves the list of languages from a JSON string.

#### Signature

```python
def get_languages_spoken(self): ...
```

### Esner().get_nationality

[Show source in tables.py:138](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L138)

Retrieves nationality information from a JSON string.

#### Signature

```python
def get_nationality(self): ...
```

### Esner().set_faculty

[Show source in tables.py:142](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L142)

Stores faculty information as a JSON string.

#### Signature

```python
def set_faculty(self, faculties): ...
```

### Esner().set_interests

[Show source in tables.py:150](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L150)

Stores interests as a JSON string.

#### Signature

```python
def set_interests(self, interests): ...
```

### Esner().set_languages_spoken

[Show source in tables.py:126](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L126)

Stores a list of languages as a JSON string.

#### Signature

```python
def set_languages_spoken(self, languages): ...
```

### Esner().set_nationality

[Show source in tables.py:134](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L134)

Stores nationality information as a JSON string.

#### Signature

```python
def set_nationality(self, nationalities): ...
```

### Esner().set_password

[Show source in tables.py:159](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L159)

Hashes and stores the given password.

#### Signature

```python
def set_password(self, password): ...
```



## EsnerRole

[Show source in tables.py:188](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L188)

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



## Role

[Show source in tables.py:168](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/tables.py#L168)

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