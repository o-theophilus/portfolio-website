from os import environ

SECRET_KEY = SECURITY_PASSWORD_SALT = environ.get("SECRET_KEY")
DETA_KEY = environ.get("DETA_KEY")
ADMIN_EMAIL = environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")
