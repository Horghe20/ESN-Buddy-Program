# EmailService

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Utils](./index.md#utils) / EmailService

> Auto-generated documentation for [utils.email_service](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py) module.

- [EmailService](#emailservice)
  - [EmailService](#emailservice-1)
    - [EmailService().send_data_elimination_notification](#emailservice()send_data_elimination_notification)
    - [EmailService().send_email](#emailservice()send_email)
    - [EmailService().send_match_notification_buddy](#emailservice()send_match_notification_buddy)
    - [EmailService().send_match_notification_esner](#emailservice()send_match_notification_esner)
    - [EmailService().send_registration_confirmation](#emailservice()send_registration_confirmation)
    - [EmailService().send_reset_password_email](#emailservice()send_reset_password_email)
    - [EmailService().send_unmatch_notification_buddy](#emailservice()send_unmatch_notification_buddy)
    - [EmailService().send_unmatch_notification_esner](#emailservice()send_unmatch_notification_esner)

## EmailService

[Show source in email_service.py:41](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L41)

A service class for handling email notifications within the ESN system.
This class is responsible for sending various types of emails, such as:
- Matching notifications between Buddies and ESNers.
- Unmatch notifications when a match is removed.
- Notifications for data elimination and password resets.
- Registration confirmation emails.

#### Signature

```python
class EmailService:
    def __init__(self): ...
```

### EmailService().send_data_elimination_notification

[Show source in email_service.py:153](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L153)

Sends a notification email to inform a user that their data has been removed from the system.

#### Arguments

- `name` - The name of the user whose data has been removed.
- `email` - The email address of the user to send the notification to.

#### Signature

```python
def send_data_elimination_notification(self, name, email): ...
```

### EmailService().send_email

[Show source in email_service.py:56](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L56)

Sends an email with the specified subject and HTML template to the given recipient.

#### Arguments

- `to_email` - The email address of the recipient.
- `subject` - The subject of the email.
- `template` - The HTML content of the email.

#### Signature

```python
def send_email(self, to_email, subject, template): ...
```

### EmailService().send_match_notification_buddy

[Show source in email_service.py:72](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L72)

Sends a match notification to a Buddy when they are matched with an ESNer.

#### Arguments

- `buddy` - The Buddy instance who is matched.
- `esner` - The ESNer instance with whom the Buddy is matched.

#### Signature

```python
def send_match_notification_buddy(self, buddy, esner): ...
```

### EmailService().send_match_notification_esner

[Show source in email_service.py:95](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L95)

Sends a match notification to an ESNer when they are assigned a Buddy.

#### Arguments

- `buddy` - The Buddy instance assigned to the ESNer.
- `esner` - The ESNer instance who is assigned a Buddy.

#### Signature

```python
def send_match_notification_esner(self, buddy, esner): ...
```

### EmailService().send_registration_confirmation

[Show source in email_service.py:199](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L199)

Sends a confirmation email to a Buddy upon successful registration.

#### Arguments

- `buddy` - The Buddy instance who has successfully registered.

#### Signature

```python
def send_registration_confirmation(self, buddy): ...
```

### EmailService().send_reset_password_email

[Show source in email_service.py:164](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L164)

Sends an email with password reset instructions when a user requests a password reset.

#### Arguments

- `email` - The email address of the user to send the password reset email to.
- `reset_link` - The link for resetting the password.

#### Signature

```python
def send_reset_password_email(self, email, reset_link): ...
```

### EmailService().send_unmatch_notification_buddy

[Show source in email_service.py:119](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L119)

Sends a notification to a Buddy when their match with an ESNer is removed.

#### Arguments

- `buddy` - The Buddy instance whose match has been removed.

#### Signature

```python
def send_unmatch_notification_buddy(self, buddy): ...
```

### EmailService().send_unmatch_notification_esner

[Show source in email_service.py:135](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/email_service.py#L135)

Sends a notification to an ESNer when their match with a Buddy is removed.

#### Arguments

- `buddy` - The Buddy instance whose match with the ESNer has been removed.
- `esner` - The ESNer instance whose match with the Buddy has been removed.

#### Signature

```python
def send_unmatch_notification_esner(self, buddy, esner): ...
```