# Flask Config
SECRET_KEY = 'secret_key'  # Change this to a random secret key in production.

# Database Config
SQLALCHEMY_DATABASE_URI="postgresql://neondb_owner:npg_GMy8nBvmRZY6@ep-white-tree-a22urp94.eu-central-1.aws.neon.tech/neondb?sslmode=require"


# Match Config
# Maximum number of automatically generated match suggestions displayed to the user
TOP_AUTOMATIC_MATCH = 3

# Mail Config
# For use, remove the comments and fill with your own datas. Decomment line 95 and 96 in app.py
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = ''
# MAIL_PASSWORD = ''  # Google App Password for apps (with 2-factor auth enabled)
# MAIL_DEFAULT_SENDER = ''
# # MAIL_SUPPRESS_SEND = True
