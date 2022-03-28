from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from google.cloud import bigquery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import date, timedelta

from utils import get_image, is_day_off

from config import BOT_TOKEN, cache

today = date.today()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

# scheduler = AsyncIOScheduler(timezone='Europe/Moscow',)
scheduler = AsyncIOScheduler()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await cache.set_data(chat=message.chat, user=message.from_user.username, data=message.text)  # запись в кэш

    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await cache.set_data(chat=message.chat, user=message.from_user.username, data=message.text)     # запись в кэш
    await message.reply("Пиши, повторю за тобой")


@dp.message_handler()
async def echo_message(message: types.Message):
    await cache.set_data(chat=message.chat, user=message.from_user.username, data=message.text)     # запись в кэш
    await bot.send_message(message.from_user.id, message.text)

def query_to_bigquery(query):
    client = bigquery.Client()
    query_job = client.query(query)
    result = query_job.result()
    # dataframe = result.to_dataframe()
    return result


@scheduler.scheduled_job('cron', day='5,20', hour=10)
def get_day_send():
    day = today
    if is_day_off(today):
        while is_day_off(day):
            day += timedelta(days=1)
    scheduler.add_job(scheduled_all, 'date', run_date=str(day) + ' 10:00:00')


@dp.message_handler()
async def scheduled_all():
    query = (
        'SELECT * FROM table LIMIT 100')
    result = query_to_bigquery(query)
    for row in result:
        caption = 'График!'
        get_image(day=list(row.keys())[1:], hour=list(map(int, row[1:])))
        await bot.send_photo(row.telegram_id, open('saved_graph.png', 'rb'), caption=caption)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp)

