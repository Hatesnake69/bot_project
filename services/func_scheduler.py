import logging
from datetime import date, datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data import CHAT_ID
from keyboards import confirmed_kb
from loader import bot, db_manager, dp
from services.graph import get_image, get_salary_period, get_xlabel_for_graph
from states import GraphConfirmForm


def save_graph(df) -> None:
    """
    Функция принимает DataFrame, формирует ось Х и сохраняет график.

    :param df: DataFrame пользователя по зарплатному периоду
    :type df: DataFrame
    """
    labels = get_xlabel_for_graph(df)
    get_image(df, labels)


async def send_graph_to_all() -> None:
    """
    Отправляет график пользователю и делает отметку в БД,
    если сообщение было успешно доставлено.
    """
    salary_period = get_salary_period(date.today())
    df_iterable = db_manager.get_users_salaryperiod(
        salary_period
    ).to_dataframe_iterable()
    for df in df_iterable:
        user_ids = df.telegram_id.unique()

        for user_id in user_ids:
            dataframe = df.loc[df.telegram_id == user_id].sort_values(
                 by=['trackdate']
             )
            save_graph(dataframe)
            try:
                caption = salary_period
                msg = await bot.send_photo(
                    user_id, open("saved_graph.png", "rb"), caption=caption
                )
                message_id = msg.message_id
                db_manager.send_confirm_for_salaryperiod(
                     user_id, message_id, datetime.now(), salary_period)
                state = dp.current_state(user=user_id)
                await set_keyboard(user_id)
                async with state.proxy() as data:
                    data["message_id"] = message_id
            except Exception as e:
                logging.error(e)


async def set_keyboard(user_id: int) -> None:
    """
    Функция устанавливает две кнопки "согласиться/отклонить".
    """
    await bot.send_message(
        chat_id=user_id,
        text="Подтвердить часы",
        reply_markup=confirmed_kb,
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("kb"))
async def confirmed_call(callback_query: CallbackQuery,
                         state: FSMContext) -> None:
    """
    Функция определяет нажатую кнопку и в случае, если пользователь нажал на
    кнопку "согласиться", его ответ загружается в БД, в противном случае
    пользователю предлагается ввести комментарий.
    """
    code: int = int(callback_query.data[-1])
    async with state.proxy() as data:
        data["is_confirmed"] = bool(code)
    if code:

        try:
            db_manager.update_data_for_salaryperiod(
                 callback_query.from_user.id,
                 data["message_id"],
                 data["is_confirmed"],
                 None,
                 datetime.now(),
             )
            await callback_query.message.answer(
                "Отработанное время согласованно!"
            )
            await state.finish()
        except Exception as e:
            await callback_query.message.answer("Возникла ошибка")
            logging.error(e)
    else:
        await callback_query.message.answer(
            "Отработанное время не согласованно, укажите причину!"
        )
        await GraphConfirmForm.comment_to_graph.set()

    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )


@dp.message_handler(state=GraphConfirmForm.comment_to_graph)
async def send_confirmed_to_db(message: Message, state: FSMContext) -> None:
    """
    Функция принимает комментарий и загружает ответ в БД.
    """
    async with state.proxy() as data:
        data["response_comment"] = message.text
    try:
        db_manager.update_data_for_salaryperiod(
            message.from_user.id,
            data["message_id"],
            data["is_confirmed"],
            data["response_comment"],
            datetime.now(),
        )
        await message.answer("Комментарий отправлен")
    except Exception as e:
        await message.answer("Возникла ошибка при отправки комментария")
        logging.error(e)
    await state.finish()


async def send_reminder_to_user(user_id: int, planned_at: datetime) -> None:
    """
    Отправляет напоминание пользователю.

    :param user_id: id пользователя
    :param planned_at: дата события
    """

    reminder_text = db_manager.get_reminder_text(planned_at)

    for row in reminder_text:
        if CHAT_ID and user_id == int(CHAT_ID):
            for telegram_id in db_manager.get_user_id_list():
                await bot.send_message(telegram_id, text=row[1])
        await bot.send_message(row[0], text=row[1])
