import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPDataError

from data.config import FROM_EMAIL, PASSWORD
from utils import get_logger

logger = get_logger(__name__)


def sending_message(to_email: str, secret_key: str) -> None:
    """
    Функция отправляет письмо на почту пользователю,
    которую он ввел в чат боте.

    :param to_email: электронная почта
    :type to_email: str

    :param secret_key: секретный ключ
    :type secret_key: str

    :rtype: str
    """
    try:
        with open(file="services/index.html", mode="r") as mail_template:
            template_old = mail_template.read()
            template_new = re.sub(
                r"Проверочный код \w+", secret_key, template_old
            )
            with open("index.html", "w") as f:
                f.write(template_new)
    except IOError:
        logger.error("Шаблон не найден")

    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Регистрация"
        msg.attach(MIMEText(template_new, "html"))
        server = SMTP(host="smtp.yandex.ru", port=587)
        server.set_debuglevel(False)
        server.starttls()
        server.login(user=FROM_EMAIL, password=PASSWORD)
        server.send_message(msg=msg)
        server.quit()
    except SMTPDataError:
        pass
