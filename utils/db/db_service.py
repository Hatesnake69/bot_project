from datetime import datetime

import pandas as pd
from aiogram.types import Message
from google.oauth2 import service_account

from data import CREDENTIALS_PATH, PROJECT


class DBManager:
    """
    Данный класс содержит методы для работы с базой данных

    Args:
    credentials (service_account.Credentials): файл доступа
    project (str): название проекта
    """

    credentials = service_account.Credentials. \
        from_service_account_file(CREDENTIALS_PATH)
    project = PROJECT

    def check_user(self, message: Message) -> bool:
        """
        Возвращает True, если пользователь не зарегистрирован
        и можно работать дальше

        :param message: сообщение пользователя
        :type message: Message

        :rtype: bool
        """

        tg_id = int(message.from_user.id)
        query = f"SELECT telegram_id FROM handy-digit-312214.TG_Bot_Stager.\
                users WHERE telegram_id = {tg_id} AND is_confirmed = true"
        if pd.read_gbq(query, project_id=self.project,
                       credentials=self.credentials).empty:
            return True
        return False

    def registration(self, message: Message) -> None:
        """
        Записывает пользователя

        :param message: сообщение пользователя из которого ожидается email
        :type message: types.Message
        """

        tg_id = message.from_user.id
        tg_name = message.from_user.username
        email = message.text
        date = message.date
        df = pd.DataFrame({"telegram_id": [tg_id],
                           "telegram_name": [tg_name],
                           "email": [email],
                           "registration_code": [None],
                           "is_confirmed": [False],
                           "regiestred_at": [date]
                           })
        try:
            df.to_gbq("handy-digit-312214.TG_Bot_Stager.users",
                      project_id=self.project,
                      credentials=self.credentials,
                      if_exists="append")
        except Exception as e:
            print(e.args)

    def authentication(self, message: Message):
        """
        Аутенцифицирует пользователя

        :param message: сообщение пользователя из которого ожидается
        secret key
        :type message: types.Message
        """

        tg_id = message.from_user.id
        secret_key = message.text
        query = "SELECT * FROM handy-digit-312214.TG_Bot_Stager.users"
        df = pd.read_gbq(query, project_id=self.project,
                         credentials=self.credentials)
        df2 = pd.DataFrame({'telegram_id': tg_id, 'is_confirmed': True,
                            'registration_code': secret_key}, index=[0])
        df.loc[df.telegram_id == tg_id, 'is_confirmed'] = \
            df2[df2.telegram_id == tg_id].loc[0]['is_confirmed']
        df.loc[df.telegram_id == tg_id, 'registration_code'] = \
            df2[df2.telegram_id == tg_id].loc[0]['registration_code']
        try:
            df.to_gbq("handy-digit-312214.TG_Bot_Stager.users",
                      project_id=self.project,
                      credentials=self.credentials,
                      if_exists="replace")
        except Exception as e:
            print(e.args)

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
