from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from app.handlers.common import register_handlers_common
from app.handlers.create_event import register_handlers_create_event
from app.handlers.faq import register_handlers_faq
from app.handlers.authorization import register_handlers_authorization
from config import BOT_TOKEN
from config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, webhook_url


from config import cache
from scheduler import scheduler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=cache)

register_handlers_common(dp)
register_handlers_create_event(dp)
register_handlers_faq(dp)
register_handlers_authorization(dp)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(webhook_url)


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp)
    executor.start_webhook(dispatcher=dp,
                           webhook_path=WEBHOOK_PATH,
                           on_startup=on_startup,
                           skip_updates=True,
                           host=WEBAPP_HOST,
                           port=WEBAPP_PORT)
