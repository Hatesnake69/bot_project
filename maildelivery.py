import smtplib
import string
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import FROM_EMAIL, PASSWORD
import logging


def gen_secret_key() -> str:
    """
    This function generate a secret key

    """
    alphabet = string.ascii_letters + string.digits
    secret_key = ''.join(secrets.choice(alphabet) for i in range(8))
    return secret_key


def sending_message(to_email, secret_key):
    """
    This function get email entered by the user
    in a telegram bot and send a message to email
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = 'Регистрация'
        message = f'The secret key is {secret_key}'
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.yandex.ru', 587)
        server.set_debuglevel(True)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
    except smtplib.SMTPDataError:
        pass
