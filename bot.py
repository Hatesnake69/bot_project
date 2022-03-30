from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import BOT_TOKEN, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, cache, webhook_url


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


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


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(webhook_url)


if __name__ == '__main__':
    # executor.start_polling(dp)
    executor.start_webhook(dispatcher=dp,
                           webhook_path=WEBHOOK_PATH,
                           on_startup=on_startup,
                           skip_updates=True,
                           host=WEBAPP_HOST,
                           port=WEBAPP_PORT)
