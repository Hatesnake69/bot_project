import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPDataError

from data.config import FROM_EMAIL, PASSWORD


def sending_message(to_email, secret_key):
    """
    Функции отправляет письмо на почту пользователя,
    которую он ввел в чат боте.
    """
    try:

        with open("services/index.html", "r") as file:
            template_old = file.read()
            template_new = re.sub(
                r"Проверочный код \w+",
                f"{secret_key}", template_old
            )
            with open("index.html", "w") as f:
                f.write(template_new)
    except IOError:
        return "Шаблон не найден"

    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Регистрация"
        msg.attach(MIMEText(template_new, "html"))
        server = SMTP("smtp.yandex.ru", 587)
        server.set_debuglevel(False)
        server.starttls()
        server.login(FROM_EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
    except SMTPDataError:
        pass
