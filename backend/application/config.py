import os

SECRET_KEY = SECURITY_PASSWORD_SALT = os.environ["SECRET_KEY"]
# Email Config ######################################
MAILJET_API_KEY = os.environ["MAILJET_API_KEY"]
MAILJET_SECRET_KEY = os.environ["MAILJET_SECRET_KEY"]
#####################################################
DEFAULT_ADMIN = (
    "Theophilus",
    "theophilus.ogbolu@gmail.com",
    os.environ["ADMIN_PASSWORD"]
)
EMAIL_CONFIRM_EXP = 3600
