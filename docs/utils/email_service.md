# EmailService

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Utils](./index.md#utils) / EmailService

> Auto-generated documentation for [utils.email_service](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py) module.

- [EmailService](#emailservice)
  - [EmailService](#emailservice-1)
    - [EmailService().send_data_elimination_notification](#emailservice()send_data_elimination_notification)
    - [EmailService().send_email](#emailservice()send_email)
    - [EmailService().send_match_notification_buddy](#emailservice()send_match_notification_buddy)
    - [EmailService().send_match_notification_esner](#emailservice()send_match_notification_esner)
    - [EmailService().send_reset_password_email](#emailservice()send_reset_password_email)
    - [EmailService().send_unmatch_notification_buddy](#emailservice()send_unmatch_notification_buddy)
    - [EmailService().send_unmatch_notification_esner](#emailservice()send_unmatch_notification_esner)

## EmailService

[Show source in email_service.py:40](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py#L40)

A service class for handling email notifications within the ESN system.
This class is responsible for sending various types of emails, such as:
- Matching notifications between Buddies and ESNers.
- Unmatch notifications when a match is removed.
- Notifications for data elimination and password resets.

#### Signature

```python
class EmailService:
    def __init__(self): ...
```

### EmailService().send_data_elimination_notification

[Show source in email_service.py:143](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py#L143)

Sends a notification email to inform a user that their data has been removed from the system.

#### Arguments

- `name` - The name of the user whose data has been removed.
- `email` - The email address of the user to send the notification to.

#### Signature

```python
def send_data_elimination_notification(self, name, email): ...
```

### EmailService().send_email

[Show source in email_service.py:55](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py#L55)

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

[Show source in email_service.py:71](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py#L71)

Sends a match notification to a Buddy when they are matched with an ESNer.

#### Arguments

- `buddy` - The Buddy instance who is matched.
- `esner` - The ESNer instance with whom the Buddy is matched.

#### Signature

```python
def send_match_notification_buddy(self, buddy, esner): ...
```

### EmailService().send_match_notification_esner

[Show source in email_service.py:92](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py#L92)

Sends a match notification to an ESNer when they are assigned a Buddy.

#### Arguments

- `buddy` - The Buddy instance assigned to the ESNer.
- `esner` - The ESNer instance who is assigned a Buddy.

#### Signature

```python
def send_match_notification_esner(self, buddy, esner): ...
```

### EmailService().send_reset_password_email

[Show source in email_service.py:154](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py#L154)

Sends an email with a new password when a user requests a password reset.

#### Arguments

- `email` - The email address of the user to send the password reset email to.
- `password` - The new password to be provided to the user.

#### Signature

```python
def send_reset_password_email(self, email, password): ...
```

### EmailService().send_unmatch_notification_buddy

[Show source in email_service.py:113](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py#L113)

Sends a notification to a Buddy when their match with an ESNer is removed.

#### Arguments

- `buddy` - The Buddy instance whose match has been removed.

#### Signature

```python
def send_unmatch_notification_buddy(self, buddy): ...
```

### EmailService().send_unmatch_notification_esner

[Show source in email_service.py:127](https://github.com/Horghe20/ESN-Buddy-Program/blob/master/utils/email_service.py#L127)

Sends a notification to an ESNer when their match with a Buddy is removed.

#### Arguments

- `buddy` - The Buddy instance whose match with the ESNer has been removed.
- `esner` - The ESNer instance whose match with the Buddy has been removed.

#### Signature

```python
def send_unmatch_notification_esner(self, buddy, esner): ...
```