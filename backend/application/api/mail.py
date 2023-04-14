from flask import current_app
from flask_mail import Mail, Message
import re

mail = Mail()


def send_mail(to, subject, body):
    body = re.sub('&amp;', '&', body)

    if current_app.config["DEBUG"]:
        print(body)
    else:
        msg = Message(
            subject,
            recipients=[to],
            html=body
        )
        mail.send(msg)
