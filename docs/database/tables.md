# Tables

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Database](./index.md#database) / Tables

> Auto-generated documentation for [database.tables](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py) module.

- [Tables](#tables)
  - [Admin](#admin)
    - [Admin().check_password](#admin()check_password)
    - [Admin().set_password](#admin()set_password)
  - [Buddy](#buddy)
    - [Buddy().get_faculty](#buddy()get_faculty)
    - [Buddy().get_interests](#buddy()get_interests)
    - [Buddy().get_languages_spoken](#buddy()get_languages_spoken)
    - [Buddy().get_nationality](#buddy()get_nationality)
    - [Buddy().set_faculty](#buddy()set_faculty)
    - [Buddy().set_interests](#buddy()set_interests)
    - [Buddy().set_languages_spoken](#buddy()set_languages_spoken)
    - [Buddy().set_nationality](#buddy()set_nationality)
  - [Esners](#esners)
    - [Esners().get_faculty](#esners()get_faculty)
    - [Esners().get_interests](#esners()get_interests)
    - [Esners().get_languages_spoken](#esners()get_languages_spoken)
    - [Esners().get_nationality](#esners()get_nationality)
    - [Esners().set_faculty](#esners()set_faculty)
    - [Esners().set_interests](#esners()set_interests)
    - [Esners().set_languages_spoken](#esners()set_languages_spoken)
    - [Esners().set_nationality](#esners()set_nationality)

## Admin

[Show source in tables.py:179](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L179)

Represents an admin user who manages the system.

#### Attributes

- `id` *int* - Primary key.
- `name` *str* - First name of the admin.
- `surname` *str* - Last name of the admin.
- `phone_number` *str* - Unique contact number.
- `email` *str* - Unique email address.
- `password_hash` *str* - Hashed password for authentication.
- `role` *bool* - Boolean indicating admin privileges.

#### Signature

```python
class Admin(db.Model): ...
```

### Admin().check_password

[Show source in tables.py:206](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L206)

Checks if the given password matches the stored hash.

#### Signature

```python
def check_password(self, password): ...
```

### Admin().set_password

[Show source in tables.py:202](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L202)

Hashes and stores the given password.

#### Signature

```python
def set_password(self, password): ...
```



## Buddy

[Show source in tables.py:33](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L33)

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

[Show source in tables.py:96](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L96)

Retrieves faculty information from a JSON string.

#### Signature

```python
def get_faculty(self): ...
```

### Buddy().get_interests

[Show source in tables.py:104](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L104)

Retrieves interests from a JSON string.

#### Signature

```python
def get_interests(self): ...
```

### Buddy().get_languages_spoken

[Show source in tables.py:80](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L80)

Retrieves the list of languages from a JSON string.

#### Signature

```python
def get_languages_spoken(self): ...
```

### Buddy().get_nationality

[Show source in tables.py:88](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L88)

Retrieves nationality information from a JSON string.

#### Signature

```python
def get_nationality(self): ...
```

### Buddy().set_faculty

[Show source in tables.py:92](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L92)

Stores faculty information as a JSON string.

#### Signature

```python
def set_faculty(self, faculties): ...
```

### Buddy().set_interests

[Show source in tables.py:100](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L100)

Stores interests as a JSON string.

#### Signature

```python
def set_interests(self, interests): ...
```

### Buddy().set_languages_spoken

[Show source in tables.py:76](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L76)

Stores a list of languages as a JSON string.

#### Signature

```python
def set_languages_spoken(self, languages): ...
```

### Buddy().set_nationality

[Show source in tables.py:84](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L84)

Stores nationality information as a JSON string.

#### Signature

```python
def set_nationality(self, nationalities): ...
```



## Esners

[Show source in tables.py:110](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L110)

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
- `buddies` *relationship* - One-to-many relationship with Buddy model.

#### Signature

```python
class Esners(db.Model): ...
```

### Esners().get_faculty

[Show source in tables.py:165](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L165)

Retrieves faculty information from a JSON string.

#### Signature

```python
def get_faculty(self): ...
```

### Esners().get_interests

[Show source in tables.py:173](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L173)

Retrieves interests from a JSON string.

#### Signature

```python
def get_interests(self): ...
```

### Esners().get_languages_spoken

[Show source in tables.py:149](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L149)

Retrieves the list of languages from a JSON string.

#### Signature

```python
def get_languages_spoken(self): ...
```

### Esners().get_nationality

[Show source in tables.py:157](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L157)

Retrieves nationality information from a JSON string.

#### Signature

```python
def get_nationality(self): ...
```

### Esners().set_faculty

[Show source in tables.py:161](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L161)

Stores faculty information as a JSON string.

#### Signature

```python
def set_faculty(self, faculties): ...
```

### Esners().set_interests

[Show source in tables.py:169](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L169)

Stores interests as a JSON string.

#### Signature

```python
def set_interests(self, interests): ...
```

### Esners().set_languages_spoken

[Show source in tables.py:145](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L145)

Stores a list of languages as a JSON string.

#### Signature

```python
def set_languages_spoken(self, languages): ...
```

### Esners().set_nationality

[Show source in tables.py:153](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/database/tables.py#L153)

Stores nationality information as a JSON string.

#### Signature

```python
def set_nationality(self, nationalities): ...
```