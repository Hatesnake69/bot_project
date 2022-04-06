from aiogram.types import Message
from google.oauth2 import service_account
from pandas import DataFrame, read_gbq

from config import CREDENTIALS_PATH, PROJECT, cache

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH
)


def check_user(message: Message) -> bool:
    """
    Возвращает True, если пользователь
    не зарегистрирован и можно работать дальше

    :param message: сообщение пользователя
    :type message: types.Message

    :rtype: bool
    """

    tg_id = int(message.from_user.id)
    query = f"SELECT telegram_id " \
            f"FROM handy-digit-312214.TG_Bot_Stager.users " \
            f"WHERE telegram_id = {tg_id}"
    return (
        True
        if read_gbq(query, project_id=PROJECT,
                    credentials=credentials).empty
        else False
    )


async def make_registration(message: Message) -> bool:
    """
    Возвращает True, если запись успешно создана, создает запись

    :param message: сообщение пользователя
    :type message: types.Message

    :rtype: bool
    """

    data = await cache.get_data(chat=message.chat,
                                user=message.from_user.username)
    if check_user(message):
        try:
            df = DataFrame(
                {
                    "telegram_id": [message.from_user.id],
                    "telegram_name": [message.from_user.username],
                    "email": [data["email"]],
                    "registration_code": [data["secret_key"]],
                    "is_confirmed": [True],
                    "regiestred_at": [
                        bytes(str(message.date.date()), "utf-8")
                    ],
                }
            )
            df.to_gbq(
                "handy-digit-312214.TG_Bot_Stager.users",
                project_id=PROJECT,
                credentials=credentials,
                if_exists="append",
            )
            return True
        except (Exception,):
            return False
    return False
