import os
from dotenv import load_dotenv

from aiogram.contrib.fsm_storage.redis import RedisStorage2

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
REDIS_HOST: str = os.getenv('REDIS_HOST')  # это для редиса
PORT: str = os.getenv('PORT')  # это для редиса


cache = RedisStorage2(host=REDIS_HOST, port=int(PORT))
