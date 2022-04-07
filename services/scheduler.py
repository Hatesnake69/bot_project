from datetime import date, datetime, timedelta

from aiogram import Bot
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import TIMEZONE
from utils import db
from loader import bot
from services.is_day_off import is_day_off
from services.graph import get_dataframe_for_graph, get_image, \
    get_xlabel_for_graph


SCHEDULER = AsyncIOScheduler(timezone=TIMEZONE)
db_manager = db.DBManager()
TODAY = date.today()


async def send_graph_to_all():
    """
    Отправляет график пользователю
    """

    df_users = db_manager.get_df_users()

    for user_id in df_users.telegram_id:

        caption = "График!"
        dataframe = get_dataframe_for_graph(user_id, TODAY)
        if not dataframe.empty:
            labels = get_xlabel_for_graph(dataframe)
            get_image(dataframe, labels)
            await bot.send_photo(
                       user_id, open("saved_graph.png", "rb"), caption=caption
            )


def get_scheduler_for_payday():
    """
    Формирует задачу планировщика на будний день

    """
    day = TODAY
    if is_day_off(TODAY):
        while is_day_off(day):
            day += timedelta(days=1)
    SCHEDULER.add_job(send_graph_to_all, "date", run_date=f"{day} 10:00:10")


SCHEDULER.add_job(get_scheduler_for_payday, "cron", day="5,20", hour=10)


async def send_reminder_to_user(bot: Bot, user_id: int, planned_at: datetime):
    """
    Отправляет напоминание пользователю

    :param bot: объект класса Bot
    :param user_id: id пользователя
    :param planned_at: дата события
    """
    reminder_text = db_manager.get_reminder_text(user_id, planned_at)

    await bot.send_message(user_id, text=reminder_text)


def set_scheduler(
    message: Message,
    user_id: int,
    event: str,
    event_date: str,
    event_time: str,
    comment: str,
):
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
    event_date = datetime.strptime(
        f"{event_date} {event_time}", "%d/%m/%Y %H:%M"
    )
    reminder_time = event_date - timedelta(minutes=30)
    created_at = datetime.now()

    if db_manager.send_task_to_bq(
            user_id,
            text_for_scheduler,
            event_date,
            created_at
    ):

        SCHEDULER.add_job(
            send_reminder_to_user,
            "date",
            run_date=reminder_time,
            args=[message.bot, user_id, event_date],
        )
