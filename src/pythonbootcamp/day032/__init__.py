__all__ = [
]

import json
import random
import re
import pkg_resources
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MotivationQuote:

    def __init__(self):
        super(MotivationQuote, self).__init__()
        with open(pkg_resources.resource_filename(__name__, 'data/quotes.txt')) as file:
            data = file.readlines()
        self.data = {i: [{'author': author.strip(), 'text': text.strip()+'\"'}
                         for text, author in [re.split('\" - ', line) for line in data]][i]
                     for i in range(0, len(data))}

    def random_quote(self):
        return self.data[random.randint(0, len(self.data)-1)]


def email_sender():
    with open('data/email_config.json', 'r') as config_file:
        config_data = json.load(config_file)
    print(config_data['host'], ":",int(config_data['port']))
    with smtplib.SMTP_SSL(config_data['host'], int(config_data['port']),
                          ssl.create_default_context()) as connection:
        connection.login(user=config_data['email_from'], password=config_data['email_from_passwd'])

        message = MIMEMultipart("alternative")
        message["Subject"] = "Motivation Quote"
        message["From"] = config_data['email_from']
        message["To"] = config_data['email_to']

        text = MotivationQuote().random_quote()

        html = f"""
            <html><body><h3>
            <i>{text['text']}</i><br>
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;{text['author']}        
            </body><html>
            """

        message.attach(MIMEText(html, "html"))
        connection.sendmail(from_addr=config_data['email_from'], to_addrs=config_data['email_to'],
                            msg=message.as_string())


if __name__ == '__main__':
    print("Example output:")
    print(MotivationQuote().random_quote())
    email_sender()