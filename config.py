import os
from dotenv import load_dotenv

from aiogram.contrib.fsm_storage.redis import RedisStorage2

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
HOST: str = os.getenv('HOST')
PORT: str = os.getenv('PORT')


cache = RedisStorage2()
