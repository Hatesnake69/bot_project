import logging
from datetime import datetime
from typing import Union

import pandas as pd
from aiogram.types import Message
from google.cloud import bigquery
from google.oauth2 import service_account

from data import CREDENTIALS_PATH, PROJECT

logging.basicConfig(
    filename="logging/bot.log",
    level=logging.ERROR,
    format="%(asctime)s - %(name)s- %(levelname)s : %(message)s",
)


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
    bqclient = bigquery.Client(credentials=credentials)

    def make_query(self, query: str) -> \
            Union[bigquery.table.RowIterator, bool]:
        """
        Отправляет запрос и возвращает результат

        :param query: запрос
        :type query: str

        :rtype: bigquery.table.RowIterator, bool
        """

        try:
            query_job = self.bqclient.query(query)
            return query_job.result()
        except Exception as e:
            logging.error(e)
            return False

    def check_user(self, message: Message) -> str:
        """
        Возвращает зарегистрирован ли пользователь или Error в случае ошибки

        :param message: сообщение пользователя
        :type message: Message

        :rtype: str
        """

        tg_id = message.from_user.id
        try:
            qry = (f"SELECT telegram_id FROM handy-digit-312214.TG_Bot_Stager."
                   f"users WHERE telegram_id = {tg_id} AND"
                   f" is_confirmed = true")
            if pd.read_gbq(qry, project_id=self.project,
                           credentials=self.credentials).empty:
                return 'Not Registered'
            return 'Registered'
        except Exception as e:
            logging.error(e)
            return 'Error'

    def check_user_role(self, message: Message, role: str) -> bool or str:
        """
        Проверяет пользователя на права админа, возвращает True/False

        :param message: сообщение пользователя
        :type message: Message
        :param role: проверяемая роль
        :type role: str


        :rtype: str, bool
        """
        tg_id = message.from_user.id
        try:
            qry = (f"SELECT role FROM handy-digit-312214.TG_Bot_Stager."
                   f"users WHERE telegram_id = {tg_id}")
            if pd.read_gbq(
                qry,
                project_id=self.project,
                credentials=self.credentials
            ).values[0][0] == role:
                return True
            return False
        except Exception as e:
            logging.error(e)
            return 'Error'

    def check_auth(self, message: Message) -> str:
        """
        Возвращает авторизован ли пользователь или Error в случае ошибки

        :param message: сообщение пользователя
        :type message: Message

        :rtype: str
        """

        tg_id = int(message.from_user.id)
        try:
            qry = (f"SELECT telegram_id FROM handy-digit-312214.TG_Bot_Stager."
                   f"users WHERE telegram_id = {tg_id} AND"
                   f" is_confirmed = false")
            if pd.read_gbq(qry, project_id=self.project,
                           credentials=self.credentials).empty:
                return 'Not auth'
            return 'Auth'
        except Exception as e:
            logging.error(e)
            return 'Error'

    def registration(self, message: Message) -> bool:
        """
        Записывает пользователя, если нет исключений вернет False

        :param message: сообщение пользователя из которого ожидается email
        :type message: types.Message
        :rtype: bool
        """

        tg_id = message.from_user.id
        tg_name = message.from_user.username
        email = message.text
        date = str(datetime.now().today())
        df = pd.DataFrame({"telegram_id": [tg_id],
                           "telegram_name": [f'@{tg_name}'],
                           "email": [email],
                           "registration_code": [None],
                           "is_confirmed": [False],
                           "regiestred_at": [date],
                           "is_active": [True],
                           "role": [None]
                           })
        try:
            df.to_gbq("handy-digit-312214.TG_Bot_Stager.users",
                      project_id=self.project,
                      credentials=self.credentials,
                      if_exists="append", )
            return False
        except Exception as e:
            logging.error(e)
            return True

    def authentication(self, message: Message) -> bool:
        """
        Аутентифицирует пользователя

        :param message: сообщение пользователя из которого ожидается
        secret key
        :type message: types.Message
        :rtype: bool
        """

        tg_id: int = message.from_user.id
        secret_key: str = message.text
        query = (f"UPDATE handy-digit-312214.TG_Bot_Stager.users"
                 f" SET is_confirmed = true ,"
                 f" registration_code = '{secret_key}'"
                 f" WHERE telegram_id = {tg_id}")
        try:
            query_job = self.bqclient.query(query)
            query_job.result()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def send_to_blacklist(self, user_id: int) -> None:
        """
        Отправляет в bigquery значение поля "is_active" True для юзера
        добавляет в блэклист простыми словами
        :param user_id: сообщение пользователя
        :type user_id: int
        """
        tg_id: int = user_id
        query: str = (
            f"UPDATE handy-digit-312214.TG_Bot_Stager.users"
            f" SET is_active = false"
            f" WHERE telegram_id = {tg_id}"
        )
        self.bqclient.query(query=query).result()

    def remove_from_blacklist(self, user_id: int) -> None:
        """
        Отправляет в bigquery значение поля "is_active" False для юзера
        убирает из блэклиста простыми словами

        :param user_id: id пользователя
        :type user_id: int
        """
        tg_id: int = user_id
        query: str = (
            f"UPDATE handy-digit-312214.TG_Bot_Stager.users"
            f" SET is_active = true"
            f" WHERE telegram_id = {tg_id}"
        )
        self.bqclient.query(query=query).result()

    def check_black_list(self, message: Message) -> bool:
        """
        Возвращает True, если пользователь в блэклисте

        :param message: сообщение пользователя
        :type message: Message

        :rtype: bool
        """

        tg_id: int = message.from_user.id
        query: str = (
            f"SELECT telegram_id FROM handy-digit-312214.TG_Bot_Stager."
            f"users WHERE telegram_id = {tg_id} AND is_active = false"
        )
        try:
            query_job = self.bqclient.query(query=query)
            return not (query_job.result().total_rows == 0)
        except Exception as e:
            logging.error(e)

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
            logging.error(e)
            return False

    def get_reminder_text(self, planned_at: datetime):

        """
        Функция выгружает из БД сообщение напоминание

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

    def get_df_for_graph(self,
                         user_id: int,
                         salary_period: datetime.date
                         ) -> bigquery.table.RowIterator:

        """
        Формирует Dataframe через запрос к БД

         :param user_id: id пользователя
         :type user_id: int

         :param salary_period: дата составления графика
         :type salary_period: datetime.date

        """
        query: str = (
            f"SELECT  trackdate, projectName, SUM(timefact) AS time FROM "
            f"TG_Bot_Stager.salaryDetailsByTrackdate  "
            f"WHERE  telegram_id = {user_id} and salaryPeriod = "
            f"'{salary_period}' "
            f"OR notApprovedSalaryPeriod  = '{salary_period}'"
            f" GROUP BY telegram_id, "
            f"trackdate, projectName order by trackdate "
        )

        try:
            query_job = self.bqclient.query(query)
            return query_job.result()
        except Exception as e:
            logging.error(e)

    def get_salary_periods_user(self,
                                user_id: int) -> bigquery.table.RowIterator:
        """
        Функция выгружает из БД зарплатные периоды

         :param user_id: id пользователя
         :type user_id: int

        """

        query: str = (
            f"SELECT DISTINCT salaryPeriod, notApprovedSalaryPeriod"
            f" FROM TG_Bot_Stager.salaryDetailsByTrackdate "
            f"WHERE telegram_id ={user_id}"
        )

        try:
            query_job = self.bqclient.query(query)
            return query_job.result()
        except Exception as e:
            logging.error(e)

    def get_df_for_faq(self, faq_key):
        """
        Функция выгружает из БД ответ по ключу FAQ и
        возвращает в строковом виде

        :param faq_key: ключ записи
        """

        query = f"SELECT answer FROM TG_Bot_Stager.faq_datas " \
                f"WHERE key = '{faq_key}'"

        reply_text = pd.read_gbq(
            query, project_id=PROJECT, credentials=self.credentials
        )

        return reply_text.values[0][0]

    def get_df_for_search(self, parse_data):

        query_data = f"""SELECT fullname, email, telegram_name
                     FROM TG_Bot_Stager.dev_search_view \
                     WHERE fullname LIKE '%{parse_data['full_name'][0]}%' OR \
                     fullname LIKE '%{parse_data['full_name'][-1]}%' OR \
                     email LIKE '%{parse_data['email']}%' OR \
                     telegram_name LIKE '%{parse_data['telegram_name']}%';"""

        frame_data = pd.read_gbq(query_data, project_id=self.project,
                                 credentials=self.credentials)
        return frame_data

    def get_user_id_list(self):
        query = (
            "SELECT DISTINCT telegram_id FROM"
            " handy-digit-312214.TG_Bot_Stager.users"
            " WHERE is_confirmed is true"
        )
        result = list(self.make_query(query=query))
        return result
