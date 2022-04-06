from datetime import datetime

import pandas as pd
from aiogram.types import Message
from google.oauth2 import service_account

from config import CREDENTIALS_PATH, PROJECT, cache


class DBManager:
    """
    Данный класс содержит методы для работы с базой данных

    Args:
    credentials (service_account.Credentials): файл доступа
    project (str): название проекта
    """

    credentials = service_account.Credentials.\
        from_service_account_file(CREDENTIALS_PATH)
    project = PROJECT

    def check_user(self, message: Message) -> bool:
        """
        Возвращает True, если пользователь не зарегистрирован
        и можно работать дальше

        :param message: сообщение пользователя
        :type message: types.Message

        :rtype: bool
        """

        tg_id = int(message.from_user.id)
        query = f"SELECT telegram_id FROM handy-digit-312214.TG_Bot_Stager.\
                users WHERE telegram_id = {tg_id}"
        if pd.read_gbq(query, project_id=self.project,
                       credentials=self.credentials).empty:
            return True
        return False

    async def make_registration(self, message: Message) -> bool:
        """
        Возвращает True, если запись успешно создана, создает запись

        :param message: сообщение пользователя
        :type message: types.Message

        :rtype: bool
        """

        data = await cache.get_data(chat=message.chat,
                                    user=message.from_user.username)
        tg_id, tg_name = message.from_user.id, message.from_user.username
        date = bytes(str(message.date.date()), "utf-8")
        if self.check_user(message):
            try:
                df = pd.DataFrame({"telegram_id": [tg_id],
                                   "telegram_name": [tg_name],
                                   "email": [data["email"]],
                                   "registration_code": [data["secret_key"]],
                                   "is_confirmed": [True],
                                   "regiestred_at": [date]})
                df.to_gbq("handy-digit-312214.TG_Bot_Stager.users",
                          project_id=self.project,
                          credentials=self.credentials,
                          if_exists="append")
                return True
            except (Exception,):
                return False
        return False

    def send_task_to_bq(self,
                        user_id:
                        int, message_text: str,
                        planned_at: datetime,
                        created_at: datetime):
        """
            Отправляет данные о событии в хранилище BigQuery

            :param user_id: id пользователя
            :param message_text: текст дл напоминания
            :param planned_at: дата события
            :param created_at: время создания
        """

        try:
            schema = [
                {"name": "telegram_id", "type": "INTEGER"},
                {"name": "message_text", "type": "STRING"},
                {"name": "planned_at", "type": "DATETIME"},
                {"name": "is_sent", "type": "BOOLEAN"},
                {"name": "created_at", "type": "DATETIME"}
            ]
            df = pd.DataFrame({"telegram_id": [user_id],
                               "message_text": [message_text],
                               "planned_at": [planned_at],
                               "is_sent": [True],
                               "created_at": [created_at]
                               })

            df.to_gbq("handy-digit-312214.TG_Bot_Stager.remind_msg",
                      project_id=PROJECT,
                      credentials=self.credentials,
                      if_exists="append",
                      table_schema=schema)

            return True
        except Exception as e:
            print(e.args)
            return False
