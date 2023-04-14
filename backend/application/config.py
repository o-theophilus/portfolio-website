from os import environ

SECRET_KEY = SECURITY_PASSWORD_SALT = environ.get("SECRET_KEY")
# Email Config ######################################
# jetmail
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
# flask_mail
MAIL_DEFAULT_SENDER = ("Theophilus", "theophilus.ogbolu@gmail.com")
MAIL_SERVER = 'in-v3.mailjet.com'
MAIL_PORT = 587
MAIL_USE_TSL = True
#####################################################
DETA_KEY = environ.get("DETA_KEY")
#####################################################
ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")
EMAIL_CONFIRM_EXP = 3600
