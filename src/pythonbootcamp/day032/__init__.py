__all__ = [
]

import datetime
import json
import random
import re
import pkg_resources
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MotivationQuote:
    TITLE = 'Motivation Quote'

    def __init__(self):
        super(MotivationQuote, self).__init__()
        with open(pkg_resources.resource_filename(__name__, 'data/quotes.txt')) as file:
            data = file.readlines()
        self.data = {i: [{'author': author.strip(), 'text': text.strip() + '\"'}
                         for text, author in [re.split('\" - ', line) for line in data]][i]
                     for i in range(0, len(data))}

    def random_quote(self):
        return self.data[random.randint(0, len(self.data) - 1)]


class EmailSender:

    def __init__(self, **kwargs):
        self.secret_data: dict = {}

        if kwargs.get('config_file_name') is not None:
            config_file_name = kwargs['config_file_name']
            with open(config_file_name, 'r') as config_file:
                self.secret_data = json.load(config_file)

        # this line allows to overwrite data from config file
        self.secret_data.update({key: kwargs[key] for key in kwargs if key in
                                 ['host', 'port', 'email_from', 'email_from_passwd', 'email_to']})

    def send(self, **kwargs):

        # configuration can be still changed
        self.secret_data.update({key: kwargs[key] for key in kwargs if key in
                                 ['host', 'port', 'email_from', 'email_from_passwd', 'email_to',
                                  'message_text_html', 'message_text_plain', 'subject']})

        with smtplib.SMTP_SSL(self.secret_data['host'], int(self.secret_data['port']),
                              ssl.create_default_context()) as connection:
            connection.login(user=self.secret_data['email_from'],
                             password=self.secret_data['email_from_passwd'])

            message = MIMEMultipart('alternative')
            message['From'] = self.secret_data['email_from']
            message['To'] = self.secret_data['email_to']

            # optional parameters
            message['Subject'] = self.secret_data.get('subject')
            message_text_html: str = self.secret_data.get('message_text_html')
            message_text_plain: str = self.secret_data.get('message_text_plain')

            if message_text_plain is not None:
                message.attach(MIMEText(message_text_plain.strip(), 'plain'))
            if message_text_html is not None:
                message.attach(MIMEText(message_text_html.strip(), "html"))

            connection.sendmail(from_addr=self.secret_data['email_from'],
                                to_addrs=self.secret_data['email_to'],
                                msg=message.as_string())


class MondayQuoteSender(EmailSender):

    def __init__(self, **kwargs):
        super(MondayQuoteSender, self).__init__(**kwargs)

    # Send a random Motivation Quote if it's Monday
    def send(self, day_of_week=0):
        if day_of_week == datetime.date.today().weekday():
            quote = MotivationQuote().random_quote()
            self.secret_data['message_text_plain'] = quote['text'] + '\n\n' + quote['author']
            self.secret_data['message_text_html'] = f"<html><body>" \
                                                    f"<h3><i>{quote['text']}</i><br></h3>" \
                                                    f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;" \
                                                    f"{quote['author']}" \
                                                    f"</body></html>"
            self.secret_data['subject'] = MotivationQuote.TITLE
            super().send()


if __name__ == '__main__':
    # TODO: delete line below (implement tests instead)
    MondayQuoteSender(config_file_name='data/secret.json').send(1)
