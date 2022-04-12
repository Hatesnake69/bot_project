import logging

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import data
import filters
import handlers
import middlewares
from loader import bot, dp
from services.scheduler import SCHEDULER

logging.basicConfig(
    filename="logging/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s- %(levelname)s : %(message)s",
)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(data.webhook_url)


if __name__ == "__main__":
    SCHEDULER.start()
    executor.start_polling(dp)
    # executor.start_webhook(dispatcher=dp,
    #                        webhook_path=config.WEBHOOK_PATH,
    #                        on_startup=on_startup,
    #                        skip_updates=True,
    #                        host=config.WEBAPP_HOST,
    #                        port=config.WEBAPP_PORT)
