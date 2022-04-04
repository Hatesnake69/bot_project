from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import date, timedelta, datetime

from config import cache
from utils import is_day_off

# from bot import scheduled_all

# scheduler = AsyncIOScheduler()

today = date.today()


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


class YScheduler(AsyncIOScheduler):

    def __init__(self):
        super().__init__()

        # jobstores = {
        #     'default': RedisJobStore()
        # }
        # super(YScheduler, self).__init__(jobstores=jobstores)
        # self.bot = bot

    async def send_reminder_to_user(self, bot, user_id: int, reminder_text: str):
        """
        Отправляет напоминание пользователю
        :param user_id: id пользователя
        :param reminder_text:текст для напоминания
        """

        await bot.send_message(user_id, text=reminder_text)

    def set_scheduler(self, bot, user_id: int, event: str, event_date: str, event_time: str, comment: str):
        """
        Формирует задачу в планировщике и отдаёт напоминание на отправку пользователю в установленный срок

        :param user_id: id пользователя
        :param event: название события
        :param event_date: дата события
        :param event_time: время события
        :param comment: текст для напоминания
        """
        text_for_scheduler = f'Напоминание! Cегодня {event} в {event_time}: {comment}'
        reminder_time = datetime.strptime(f"{event_date} {event_time}", "%d/%m/%Y %H:%M") - timedelta(minutes=30)
        # scheduler.add_jobstore('redis', cache)
        super().add_job(self.send_reminder_to_user,
                        'date', run_date=reminder_time,
                        args=[bot, user_id, text_for_scheduler])
