from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import BOT_TOKEN, cache


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    data = await cache.get_data(chat=message.chat, user=message.from_user.username)
    print(data)
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await cache.set_data(chat=message.chat, user=message.from_user.username, data=message.text)
    print(message.text)
    await message.reply("Пиши, повторю за тобой")


@dp.message_handler()
async def echo_message(message: types.Message):
    await cache.set_data(chat=message.chat, user=message.from_user.username, data=message.text)
    print(message.text)
    await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
