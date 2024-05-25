from flask import current_app
import re
from mailjet_rest import Client
import os

mailjet = Client(auth=(
    os.environ["MAILJET_API_KEY"],
    os.environ["MAILJET_SECRET_KEY"]),
    version='v3.1')


def send_mail(
    to,
    name,
    subject,
    body
):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": current_app.config["DEFAULT_ADMIN"][1],
                    "Name": current_app.config["DEFAULT_ADMIN"][0]
                },
                "To": [
                    {
                        "Email": to,
                        "Name": name
                    }
                ],
                "Subject": subject,
                "HTMLPart": re.sub('&amp;', '&', body)
            }
        ]
    }
    if current_app.config["DEBUG"]:
        print(data)
    else:
        result = mailjet.send.create(data=data)
        print(result.json())
