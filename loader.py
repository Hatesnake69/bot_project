from aiogram import Bot, Dispatcher

from data import BOT_TOKEN, cache
from utils import db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=cache)
db_manager = db.DBManager()
