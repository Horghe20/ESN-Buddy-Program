
# Flask Config
SECRET_KEY = 'dev'  # Change this to a random secret key in production.

# Database Config
#dev
SQLALCHEMY_DATABASE_URI="sqlite:///matchmaking.db" #Change with your database url or leave this one for local use

SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance.

# Match Config
TOP_AUTOMATIC_MATCH = 3

# Mail Config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = '' # Your email
MAIL_PASSWORD = ''  # Google App Password for apps (with 2-factor auth enabled)
MAIL_DEFAULT_SENDER = ''
