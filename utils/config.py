
# Flask Config
SECRET_KEY = ''  # Change this to a random secret key in production.

# Database Config
SQLALCHEMY_DATABASE_URI="sqlite:///matchmaking.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance.

# Match Config
TOP_AUTOMATIC_MATCH = 3 #number of suggestion for finding automatic match

# Mail Config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''  # Google App Password for apps (with 2-factor auth enabled)
MAIL_DEFAULT_SENDER = ''
# MAIL_SUPPRESS_SEND = True
