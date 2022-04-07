from aiogram import Bot, Dispatcher

from data import BOT_TOKEN, cache


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=cache)
