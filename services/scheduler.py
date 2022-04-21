from datetime import date, datetime, timedelta

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import REDIS_HOST, REDIS_PORT
from loader import bot, db_manager
from services import is_day_off
from services.graph import (get_dataframe_for_graph, get_image,
                            get_xlabel_for_graph)

DEFAULT = "default"

jobstores = {
    DEFAULT: RedisJobStore(
        host=REDIS_HOST, port=REDIS_PORT
    )
}
executors = {DEFAULT: AsyncIOExecutor()}

SCHEDULER = AsyncIOScheduler(jobstores=jobstores, executors=executors)

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


async def send_reminder_to_user(user_id: int, planned_at: datetime):
    """
    Отправляет напоминание пользователю

    :param user_id: id пользователя
    :param planned_at: дата события
    """
    reminder_text = db_manager.get_reminder_text(planned_at)

    for row in reminder_text:
        await bot.send_message(row[0], text=row[1])


def set_scheduler(
        user_id: int,
        event: str,
        event_date: str,
        event_time: str,
        comment: str,
):
    """
    Формирует задачу в планировщике и отдаёт напоминание на отправку
    пользователю в установленный срок

    :param user_id: id пользователя
    :param event: название события
    :param event_date: дата события
    :param event_time: время события
    :param comment: комментарий пользователя
    """

    text_for_scheduler = f"Напоминание! Cегодня {event}в" \
                         f" {event_time} {comment}"
    event_date = datetime.strptime(
        f"{event_date} {event_time}", "%d/%m/%Y %H:%M"
    )
    reminder_time = event_date - timedelta(minutes=1)
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
            args=[user_id, event_date],
        )
