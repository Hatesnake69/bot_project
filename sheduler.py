from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import date, timedelta

from utils import is_day_off
from bot import scheduled_all

scheduler = AsyncIOScheduler()
#scheduler = AsyncIOScheduler(timezone='Europe/Moscow',)
today = date.today()


def start_sheduler(func):

    def get_sheduler_for_payday(func):
        day = today
        if is_day_off(today):
            print(today)
            while is_day_off(day):
                day += timedelta(days=1)
        print('yes')
        scheduler.add_job(func, 'date', run_date=f'{day} 10:00:00')


    scheduler.add_job(get_sheduler_for_payday, 'cron', day='5,20', hour=10, args=(func,))



scheduler.start()