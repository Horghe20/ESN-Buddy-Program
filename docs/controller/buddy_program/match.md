# Match

[Esn-buddy-program Index](../../README.md#esn-buddy-program-index) / [Controller](../index.md#controller) / [Buddy Program](./index.md#buddy-program) / Match

> Auto-generated documentation for [controller.buddy_program.match](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy_program/match.py) module.

#### Attributes

- `bp` - Create a Blueprint for the match module with the URL prefix '/match': Blueprint('match', __name__, url_prefix='/match')


- [Match](#match)
  - [automatic_match](#automatic_match)
  - [confirm_match](#confirm_match)
  - [create_exel](#create_exel)
  - [export_excel](#export_excel)
  - [manual_match](#manual_match)
  - [remove_buddy](#remove_buddy)
  - [remove_match](#remove_match)

## automatic_match

[Show source in match.py:34](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy_program/match.py#L34)

Automatically assigns Buddies to ESNers based on availability.

- Retrieves ESNers with open buddy slots.
- Retrieves unmatched Buddies.
- Uses match_making utility to create matches.
- Returns the match results in an HTML template.

#### Returns

- On success: Rendered template with match data (HTTP 200).
- On failure: Error message template (HTTP 400 or 500).

#### Signature

```python
@bp.route("/automatic_match", methods=["GET"])
@login_required
@buddy_program_manager_required
def automatic_match(): ...
```

#### See also

- [buddy_program_manager_required](../auth.md#buddy_program_manager_required)
- [login_required](../auth.md#login_required)



## confirm_match

[Show source in match.py:102](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy_program/match.py#L102)

Confirms a match between a Buddy and an ESNer.

- Updates the Buddy's `esn_member_id`.
- Sends match confirmation emails.
- Handles various SMTP errors for email notifications.

#### Returns

- Success message (HTTP 200).
- Error messages (HTTP 400, 404, or 500).

#### Signature

```python
@bp.route("/confirm_match", methods=["POST"])
@login_required
@buddy_program_manager_required
def confirm_match(): ...
```

#### See also

- [buddy_program_manager_required](../auth.md#buddy_program_manager_required)
- [login_required](../auth.md#login_required)



## create_exel

[Show source in match.py:245](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy_program/match.py#L245)

Create an Excel workbook with two worksheets containing Buddy and ESNers data.

This function uses the openpyxl library to create an Excel workbook with the following structure:

1. Buddies Sheet:
   - Title: "Buddies"
   - Columns (Headers): ID, Name, Surname, Email, Nationality, Languages Spoken, Faculty,
     Phone Number, Instagram, Telegram, Interests, Gender, Description, Semester, Year,
     Date of Insert, ESN Member ID.
   - Each Buddy record is appended as a row. Date formatting is applied to date_of_insert if available.

2. ESNers Sheet:
   - Title: "ESNers"
   - Columns (Headers): ID, Name, Surname, Type, Email, Phone Number, Languages Spoken, Nationality,
     Gender, Faculty, Interests, Description.
   - Each ESNer record is appended as a row.

The workbook is then saved to a BytesIO stream, which is returned for use in a downloadable response.

#### Arguments

- `buddies` - List of Buddy instances.
- `esners` - List of ESNers instances.

#### Returns

A BytesIO stream containing the Excel file.

#### Signature

```python
def create_exel(buddies, esners): ...
```



## export_excel

[Show source in match.py:212](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy_program/match.py#L212)

Export Buddy and ESNers data into an Excel file.

GET request:
  - Retrieves all Buddy and ESNers records from the database.
  - Calls create_exel() to generate an Excel workbook containing two sheets:
      1. Buddies sheet with details for each Buddy.
      2. ESNers sheet with details for each ESNer.
  - Returns the Excel file as a downloadable response.

#### Returns

Flask send_file response containing the Excel workbook.

#### Signature

```python
@bp.route("/export_excel", methods=["GET"])
@login_required
@buddy_program_admin_required
def export_excel(): ...
```

#### See also

- [buddy_program_admin_required](../auth.md#buddy_program_admin_required)
- [login_required](../auth.md#login_required)



## manual_match

[Show source in match.py:72](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy_program/match.py#L72)

Displays ESNers and Buddies for manual matching.

- Orders ESNers by the number of Buddies they have.
- Orders Buddies by whether they are matched and by their registration date.

#### Returns

- Rendered template with ESNers and Buddies for matching.

#### Signature

```python
@bp.route("/manual_match", methods=["GET"])
@login_required
@buddy_program_manager_required
def manual_match(): ...
```

#### See also

- [buddy_program_manager_required](../auth.md#buddy_program_manager_required)
- [login_required](../auth.md#login_required)



## remove_buddy

[Show source in match.py:183](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy_program/match.py#L183)

Deletes a Buddy from the database.

- Sends an email notification of data elimination.

#### Returns

- Success message (HTTP 200).
- Error messages (HTTP 404 or 500).

#### Signature

```python
@bp.route("/remove/buddy/<int:buddy_id>", methods=["POST"])
@login_required
@buddy_program_admin_required
def remove_buddy(buddy_id): ...
```

#### See also

- [buddy_program_admin_required](../auth.md#buddy_program_admin_required)
- [login_required](../auth.md#login_required)



## remove_match

[Show source in match.py:143](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/controller/buddy_program/match.py#L143)

Removes an existing match.

- Sets the Buddy's `esn_member_id` to None.
- Sends unmatch notification emails.

#### Returns

- Success message (HTTP 200).
- Error messages (HTTP 400, 404, or 500).

#### Signature

```python
@bp.route("/remove_match", methods=["POST"])
@login_required
@buddy_program_manager_required
def remove_match(): ...
```

#### See also

- [buddy_program_manager_required](../auth.md#buddy_program_manager_required)
- [login_required](../auth.md#login_required)