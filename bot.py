import pandas_gbq
from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram.utils import executor

import config
from app.handlers.authorization import register_handlers_authorization
from app.handlers.common import register_handlers_common
from app.handlers.create_event import register_handlers_create_event
from app.handlers.faq import register_handlers_faq
from graph import get_dataframe_for_graph, get_image, get_xlabel_for_graph
from scheduler import TODAY, scheduler, start_sheduler

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=config.cache)

register_handlers_common(dp)
register_handlers_create_event(dp)
register_handlers_faq(dp)
register_handlers_authorization(dp)


@dp.message_handler()
async def echo_message(message: Message):
    await config.cache.set_data(
        chat=message.chat, user=message.from_user.username, data=message.text
    )  # запись в кэш
    await bot.send_message(message.from_user.id, message.text)


@dp.message_handler()
async def scheduled_all():
    """
    Отправляет график пользователю
    """
    query_users = """ SELECT DISTINCT telegram_id, fullname
         FROM TG_Bot_Stager.salaryDetailsByTrackdate """
    df_users = pandas_gbq.read_gbq(
        query_users, project_id=config.PROJECT, credentials=config.credentials
    )

    for user_id in df_users.telegram_id:

        caption = "График!"
        dataframe = get_dataframe_for_graph(user_id, TODAY)
        if not dataframe.empty:
            labels = get_xlabel_for_graph(dataframe)
            get_image(dataframe, labels)

            await bot.send_photo(
                user_id, open("saved_graph.png", "rb"), caption=caption
            )


start_sheduler(scheduled_all)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(config.webhook_url)


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp)
    executor.start_webhook(dispatcher=dp,
                           webhook_path=config.WEBHOOK_PATH,
                           on_startup=on_startup,
                           skip_updates=True,
                           host=config.WEBAPP_HOST,
                           port=config.WEBAPP_PORT)
