from datetime import date, datetime, timedelta

import pandas as pd
from aiogram import Bot
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from google.oauth2 import service_account

from data import CREDENTIALS_PATH, PROJECT
from services import is_day_off
from utils import db

SCHEDULER = AsyncIOScheduler(timezone='Europe/Moscow')


TODAY = date.today()

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH
)


def start_sheduler(func):
    """
    Запускает планировщик 5 и 20 числа каждого месяца в 10:00

    :param func: принимает на вход функцию
    """

    def get_scheduler_for_payday(func):
        """
        Формирует задачу планировщика на будний день

        :param func: принимает на вход функцию
        """
        day = TODAY
        if is_day_off(TODAY):
            while is_day_off(day):
                day += timedelta(days=1)
            SCHEDULER.add_job(func, "date", run_date=f"{day} 10:00:00")

    SCHEDULER.add_job(
        get_scheduler_for_payday, "cron", day="5,20", hour=10, args=(func,)
    )


async def send_reminder_to_user(bot: Bot,
                                user_id: int,
                                planned_at: datetime):
    """
        Отправляет напоминание пользователю

        :param bot: объект класса Bot
        :param user_id: id пользователя
        :param planned_at: дата события
    """

    query = f"SELECT message_text FROM " \
            f"handy-digit-312214.TG_Bot_Stager.remind_msg WHERE " \
            f"planned_at = DATETIME({planned_at.year}, {planned_at.month}, " \
            f"{planned_at.day}, {planned_at.hour},{planned_at.minute}, 0) " \
            f"AND telegram_id = {user_id} "

    reminder_text = pd.read_gbq(query,
                                project_id=PROJECT,
                                credentials=credentials)

    await bot.send_message(user_id, text=reminder_text['message_text'][0])


def set_scheduler(message: Message,
                  user_id: int,
                  event: str,
                  event_date: str,
                  event_time: str,
                  comment: str):
    """
        Формирует задачу в планировщике и отдаёт напоминание на отправку
        пользователю в установленный срок

        :param message: объект класса Message
        :param user_id: id пользователя
        :param event: название события
        :param event_date: дата события
        :param event_time: время события
        :param comment: комментарий пользователя
    """

    text_for_scheduler = f"Напоминание! Cегодня {event} в" \
                         f" {event_time}: {comment}"
    event_date = datetime.strptime(f"{event_date} {event_time}",
                                   "%d/%m/%Y %H:%M")
    reminder_time = event_date - timedelta(minutes=30)
    created_at = datetime.now()

    db_manager = db.DBManager()
    if db_manager.send_task_to_bq(
                       user_id,
                       text_for_scheduler,
                       event_date,
                       created_at):

        SCHEDULER.add_job(send_reminder_to_user,
                          "date", run_date=reminder_time,
                          args=[message.bot,
                                user_id,
                                event_date])
