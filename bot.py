import pandas_gbq
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import data
import handlers
from graph import get_dataframe_for_graph, get_image, get_xlabel_for_graph
from loader import bot, dp
from scheduler import SCHEDULER, TODAY, start_sheduler


@dp.message_handler()
async def scheduled_all():
    """
    Отправляет график пользователю
    """
    query_users = """ SELECT DISTINCT telegram_id, fullname
         FROM TG_Bot_Stager.salaryDetailsByTrackdate """
    df_users = pandas_gbq.read_gbq(
        query_users, project_id=data.PROJECT, credentials=data.credentials
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
