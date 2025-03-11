# Db

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Database](./index.md#database) / Db

> Auto-generated documentation for [database.db](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/db.py) module.

#### Attributes

- `db` - Initialize the SQLAlchemy database instance: SQLAlchemy()


- [Db](#db)
  - [init_db](#init_db)

## init_db

[Show source in db.py:21](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/database/db.py#L21)

Initializes the database with the given Flask application instance.

This function binds the SQLAlchemy database instance to the Flask application,
enabling database operations.

#### Arguments

- `app` *Flask* - The Flask application instance to associate with the database.

#### Returns

None

#### Signature

```python
def init_db(app): ...
```