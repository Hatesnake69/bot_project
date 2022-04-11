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
        try:
            qry = f"SELECT telegram_id FROM handy-digit-312214.TG_Bot_Stager.\
                    users WHERE telegram_id = {tg_id} AND is_confirmed = true"
            if pd.read_gbq(qry, project_id=self.project,
                           credentials=self.credentials).empty:
                return True
            return False
        except Exception as e:
            print(e.args)

    def check_auth(self, message: Message) -> bool:
        """
        Возвращает True, если пользователь не аутентифицирован
        и можно работать дальше

        :param message: сообщение пользователя
        :type message: Message

        :rtype: bool
        """

        tg_id = int(message.from_user.id)
        try:
            qry = f"SELECT telegram_id FROM handy-digit-312214.TG_Bot_Stager.\
                    users WHERE telegram_id = {tg_id} AND is_confirmed = false"
            if pd.read_gbq(qry, project_id=self.project,
                           credentials=self.credentials).empty:
                return True
            return False
        except Exception as e:
            print(e.args)

    def registration(self, message: Message) -> None:
        """
        Записывает пользователя

        :param message: сообщение пользователя из которого ожидается email
        :type message: types.Message
        """

        tg_id = message.from_user.id
        tg_name = message.from_user.username
        email = message.text
        df = pd.DataFrame({"telegram_id": [tg_id],
                           "telegram_name": [tg_name],
                           "email": [email],
                           "registration_code": [None],
                           "is_confirmed": [False],
                           "regiestred_at": [None]
                           })
        try:
            df.to_gbq("handy-digit-312214.TG_Bot_Stager.users",
                      project_id=self.project,
                      credentials=self.credentials,
                      if_exists="append", )
        except Exception as e:
            print(e.args)

    def authentication(self, message: Message) -> None:
        """
        Аутентифицирует пользователя

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

    def get_reminder_text(self, user_id: int, planned_at: datetime):

        """
        Функция выгружает из БД сообщение напоминание

        :param user_id: id пользователя
        :param planned_at: дата события
        """

        query = (
            f"SELECT * FROM "
            f"handy-digit-312214.TG_Bot_Stager.remind_msg WHERE "
            f"planned_at = DATETIME({planned_at.year}, {planned_at.month}, "
            f"{planned_at.day}, {planned_at.hour},{planned_at.minute}, 0) "
        )

        reminder_text = pd.read_gbq(
            query, project_id=PROJECT, credentials=self.credentials
        )

        return reminder_text

    def get_df_users(self):
        """
        Функция выгружает из БД id уникальных пользователей

        """

        query_users = """SELECT DISTINCT telegram_id
                      FROM TG_Bot_Stager.salaryDetailsByTrackdate"""
        df_users = pd.read_gbq(
            query_users, project_id=PROJECT, credentials=self.credentials
        )
        return df_users

    def get_df_for_graph(self, user_id, salary_period):

        """
        Формирует Dataframe через запрос к БД

         :param user_id: id пользователя
         :type user_id: int

         :param date: дата составления графика
         :type date: datetime.date

        """
        sql_group_project = (
            f"SELECT  trackdate, projectName, SUM(timefact) AS time FROM "
            f"TG_Bot_Stager.salaryDetailsByTrackdate  "
            f"WHERE  telegram_id = {user_id} and salaryPeriod = "
            f"'{salary_period}' "
            f"OR notApprovedSalaryPeriod  = '{salary_period}'"
            f" GROUP BY telegram_id, "
            f"trackdate, projectName order by trackdate "
        )
        df = pd.read_gbq(
            sql_group_project, project_id=PROJECT, credentials=self.credentials
        )
        return df
