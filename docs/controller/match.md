# Match

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Controller](./index.md#controller) / Match

> Auto-generated documentation for [controller.match](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/match.py) module.

#### Attributes

- `bp` - Create a Blueprint for the match module with the URL prefix '/match': Blueprint('match', __name__, url_prefix='/match')


- [Match](#match)
  - [automatic_match](#automatic_match)
  - [confirm_match](#confirm_match)
  - [manual_match](#manual_match)
  - [remove_buddy](#remove_buddy)
  - [remove_esner](#remove_esner)
  - [remove_match](#remove_match)

## automatic_match

[Show source in match.py:32](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/match.py#L32)

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
def automatic_match(): ...
```

#### See also

- [login_required](./auth.md#login_required)



## confirm_match

[Show source in match.py:97](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/match.py#L97)

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
def confirm_match(): ...
```

#### See also

- [login_required](./auth.md#login_required)



## manual_match

[Show source in match.py:68](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/match.py#L68)

Displays ESNers and Buddies for manual matching.

- Orders ESNers by the number of Buddies they have.
- Orders Buddies by whether they are matched and by their registration date.

#### Returns

- Rendered template with ESNers and Buddies for matching.

#### Signature

```python
@bp.route("/manual_match", methods=["GET"])
@login_required
def manual_match(): ...
```

#### See also

- [login_required](./auth.md#login_required)



## remove_buddy

[Show source in match.py:177](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/match.py#L177)

Deletes a Buddy from the database.

- Sends an email notification of data elimination.

#### Returns

- Success message (HTTP 200).
- Error messages (HTTP 404 or 500).

#### Signature

```python
@bp.route("/remove/buddy/<int:buddy_id>", methods=["POST"])
@login_required
def remove_buddy(buddy_id): ...
```

#### See also

- [login_required](./auth.md#login_required)



## remove_esner

[Show source in match.py:206](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/match.py#L206)

Deletes an ESNer from the database.

- Ensures the ESNer has no assigned Buddies before deletion.
- Sends an email notification of data elimination.

#### Returns

- Success message (HTTP 200).
- Error messages (HTTP 400, 404, or 500).

#### Signature

```python
@bp.route("/remove/esner/<int:esner_id>", methods=["POST"])
@login_required
def remove_esner(esner_id): ...
```

#### See also

- [login_required](./auth.md#login_required)



## remove_match

[Show source in match.py:138](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/controller/match.py#L138)

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
def remove_match(): ...
```

#### See also

- [login_required](./auth.md#login_required)