from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import date, timedelta, datetime

from utils import is_day_off

# from bot import scheduled_all

SCHEDULER = AsyncIOScheduler(timezone='Europe/Moscow')

TODAY = date.today()


# def start_sheduler(func):
#     def get_sheduler_for_payday(func):
#         day = today
#         if is_day_off(today):
#             print(today)
#             while is_day_off(day):
#                 day += timedelta(days=1)
#         print('yes')
#         scheduler.add_job(func, 'date', run_date=f'{day} 10:00:00')
#
#     scheduler.add_job(get_sheduler_for_payday, 'cron', day='5,20', hour=10, args=(func,))


async def send_reminder_to_user(bot: Bot, user_id: int, reminder_text: str):
    """
        Отправляет напоминание пользователю

        :param bot: объект класса Bot
        :param user_id: id пользователя
        :param reminder_text:текст для напоминания

    """

    await bot.send_message(user_id, text=reminder_text)


def set_scheduler(bot: Bot, user_id: int, event: str, event_date: str, event_time: str, comment: str):
    """
        Формирует задачу в планировщике и отдаёт напоминание на отправку пользователю в установленный срок

        :param bot: объект класса Bot
        :param user_id: id пользователя
        :param event: название события
        :param event_date: дата события
        :param event_time: время события

        :param comment: комментарий пользователя
    """

    text_for_scheduler = f"Напоминание! Cегодня {event} в {event_time}: {comment}"
    reminder_time = datetime.strptime(f"{event_date} {event_time}", "%d/%m/%Y %H:%M") - timedelta(minutes=30)
    SCHEDULER.add_job(send_reminder_to_user,
                      "date", run_date=reminder_time,
                      args=[bot, user_id, text_for_scheduler]
                      )
