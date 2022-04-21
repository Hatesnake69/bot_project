import logging
from datetime import datetime
from typing import Union

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
            qry: str = (f"SELECT telegram_id FROM "
                        f"handy-digit-312214.TG_Bot_Stager.users "
                        f"WHERE telegram_id = {tg_id} AND "
                        f"is_confirmed = true")

            if len(list(self.bqclient.query(qry).result())) == 0:
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
            qry: str = (f"SELECT role FROM handy-digit-312214.TG_Bot_Stager."
                        f"users WHERE telegram_id = {tg_id}")

            if list(self.bqclient.query(qry).result())[0][0] == role:
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
            qry: str = (f"SELECT telegram_id FROM "
                        f"handy-digit-312214.TG_Bot_Stager."
                        f"users WHERE telegram_id = {tg_id} AND"
                        f" is_confirmed = false")
            if len(list(self.bqclient.query(qry).result())) == 0:
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
        query: str = (
            f"INSERT INTO handy-digit-312214.TG_Bot_Stager.users"
            f"(telegram_id, telegram_name, email, registration_code, "
            f"is_confirmed, regiestred_at, is_active, role)"
            f" VALUES ({tg_id}, f'@{tg_name}', '{email}', "
            f"{None}, {False}, '{date}', {True}, {None})"
        )

        try:
            result = self.bqclient.query(query=query)
            result.result()

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
        query: str = (f"UPDATE handy-digit-312214.TG_Bot_Stager.users"
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

        query: str = (
            f"INSERT INTO handy-digit-312214.TG_Bot_Stager.remind_msg"
            f"(telegram_id, message_text, planned_at, is_sent, created_at)"
            f" VALUES ({user_id}, '{message_text}', '{planned_at}', {True},"
            f"'{created_at}')"
        )

        try:
            result = self.bqclient.query(query=query)
            result.result()

            return True
        except Exception as e:
            logging.error(e)
            return False

    def get_reminder_text(self, planned_at: datetime):

        """
        Функция выгружает из БД сообщение напоминание

        :param planned_at: дата события
        """

        query: str = (
            f"SELECT * FROM "
            f"handy-digit-312214.TG_Bot_Stager.remind_msg WHERE "
            f"planned_at = DATETIME({planned_at.year}, {planned_at.month}, "
            f"{planned_at.day}, {planned_at.hour},{planned_at.minute}, 0) "
        )

        return list(self.bqclient.query(query).result())

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
            f"trackdate, projectName, salaryPeriod, notApprovedSalaryPeriod "
            f" order by trackdate "
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

        query: str = (f"SELECT * FROM "
                      f"handy-digit-312214.TG_Bot_Stager.faq_datas "
                      f"WHERE key ='{faq_key}'")

        return list(self.bqclient.query(query).result())[0][3]

    def send_confirm_for_salary_period(
            self, user_id: int,
            message_id: int,
            mailing_date: datetime,
            salary_period: str) -> None:
        """
        Функция добавляет в БД данные по зарплатному периоду

        """

        query: str = (
            f"INSERT INTO handy-digit-312214.TG_Bot_Stager.salary_response"
            f"(mailing_date, telegram_id, message_id, salary_period)"
            f"VALUES ('{mailing_date.strftime('%Y-%m-%d %H:%M:%S')}',"
            f"{user_id}, "
            f"{message_id},'{salary_period}')"
        )

        try:
            bq = bigquery.Client(credentials=self.credentials)
            result = bq.query(query=query)
            result.result()
        except Exception as e:
            logging.error(e)

    def update_data_for_salaryperiod(
            self,
            user_id: int,
            message_id: int,
            is_confirmed: bool,
            response_comment: str,
            cofirmed_at: datetime
    ) -> None:
        """
        Функция обновляет значения согласовано/не согласовано отработанное
        время, проставляет время согласования и заполняет поле комментарий,
        если он есть

        """
        if response_comment:
            query: str = (
                f"UPDATE handy-digit-312214.TG_Bot_Stager.salary_response "
                f"SET is_confirmed = {is_confirmed},"
                f"response_comment = '{response_comment}',"
                f"confirmed_at = '{cofirmed_at.strftime('%Y-%m-%d %H:%M:%S')}'"
                f"WHERE telegram_id = {user_id} "
                f"AND message_id = {message_id}"
            )

        else:
            query: str = (
                f"UPDATE handy-digit-312214.TG_Bot_Stager.salary_response "
                f"SET is_confirmed = {is_confirmed}, "
                f"confirmed_at = '{cofirmed_at.strftime('%Y-%m-%d %H:%M:%S')}'"
                f"WHERE telegram_id = {user_id} "
                f"AND message_id = {message_id}"
            )

        try:
            query_job = self.bqclient.query(query)
            query_job.result()
        except Exception as e:
            logging.error(e)

    def get_df_for_search(self, parse_data):

        query_data: str = f"""SELECT fullname, email, telegram_name
                     FROM TG_Bot_Stager.dev_search_view \
                     WHERE fullname LIKE '%{parse_data['full_name'][0]}%' OR \
                     fullname LIKE '%{parse_data['full_name'][-1]}%' OR \
                     email LIKE '%{parse_data['email']}%' OR \
                     telegram_name LIKE '%{parse_data['telegram_name']}%';"""

        try:
            query_job = self.bqclient.query(query_data)
            return query_job.result()
        except Exception as e:
            logging.error(e)

    def get_users_selaryperiod(
            self,
            salary_period: str
    ) -> bigquery.table.RowIterator:
        """
        Функция выгружает из БД всех пользователей по заданному периоду

        """

        query: str = (f"SELECT us.telegram_id, sal.trackdate,"
                      f"sal.projectName, SUM(sal.timefact) as time "
                      f"FROM TG_Bot_Stager.users as us "
                      f"JOIN TG_Bot_Stager.salaryDetailsByTrackdate as sal "
                      f"ON us.telegram_id = sal.telegram_id "
                      f"WHERE  us.is_active = True AND us.is_confirmed = True "
                      f"AND sal.salaryPeriod = '{salary_period}'"
                      f"OR sal.notApprovedSalaryPeriod  = '{salary_period}'"
                      f"GROUP BY us.telegram_id, sal.trackdate,"
                      f" sal.projectName"
                      f" ORDER BY us.telegram_id "
                      )

        try:
            query_job = self.bqclient.query(query)
            return query_job.result()
        except Exception as e:
            logging.error(e)

    def get_user_id_list(self):

        query = (
            "SELECT DISTINCT telegram_id FROM"
            " handy-digit-312214.TG_Bot_Stager.users"
            " WHERE is_confirmed is true"
        )
        result = list(self.make_query(query=query))
        return result
