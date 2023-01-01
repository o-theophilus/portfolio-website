from os import environ

SECRET_KEY = SECURITY_PASSWORD_SALT = environ.get("SECRET_KEY")
ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")
DETA_KEY = environ.get("DETA_KEY")
