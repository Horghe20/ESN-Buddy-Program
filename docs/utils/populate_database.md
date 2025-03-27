# Populate Database

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Utils](./index.md#utils) / Populate Database

> Auto-generated documentation for [utils.populate_database](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/populate_database.py) module.

#### Attributes

- `OPTIONS_FILE` - Path to the options file: './utils/options.json'


- [Populate Database](#populate-database)
  - [generate_buddy](#generate_buddy)
  - [generate_esner](#generate_esner)
  - [load_options](#load_options)
  - [main](#main)

## generate_buddy

[Show source in populate_database.py:52](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/populate_database.py#L52)

Generate a Buddy instance with random dummy data.

#### Arguments

- `fake` *Faker* - An instance of the Faker class for generating fake data.
- `options` *dict* - A dictionary of options for generating random attributes.

#### Returns

- `Buddy` - A Buddy instance populated with random data.

#### Signature

```python
def generate_buddy(fake, options): ...
```



## generate_esner

[Show source in populate_database.py:105](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/populate_database.py#L105)

Generate an Esners instance with random dummy data.

#### Arguments

- `fake` *Faker* - An instance of the Faker class for generating fake data.
- `options` *dict* - A dictionary of options for generating random attributes.

#### Returns

- `Esners` - An Esners instance populated with random data.

#### Signature

```python
def generate_esner(fake, options): ...
```



## load_options

[Show source in populate_database.py:42](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/populate_database.py#L42)

Load options (nationalities, languages, faculties, interests) from a JSON file.

#### Returns

- `dict` - A dictionary containing lists of options for nationalities, languages, faculties, and interests.

#### Signature

```python
def load_options(): ...
```



## main

[Show source in populate_database.py:158](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/populate_database.py#L158)

Main function to set up the Flask app, initialize the database, and insert dummy data.

#### Signature

```python
def main(): ...
```