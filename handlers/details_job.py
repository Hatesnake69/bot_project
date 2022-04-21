from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from filters import IsRegistered
from loader import db_manager, dp
from services.graph import get_image, get_xlabel_for_graph
from states import DetailsJobForm


@dp.message_handler(IsRegistered(), Text(equals=['/details_job']),
                    commands=['details_job'])
async def get_menu_salary_period(message: Message) -> None:
    """
       Создает запрос в БД об имеющихся ЗП
       и формирует меню
       :param message: сообщение

    """
    kb_period = ReplyKeyboardMarkup()
    df_iterable = db_manager.get_salary_periods_user(
        message.chat.id
    ).to_dataframe_iterable()
    for salary_periods in df_iterable:
        df = salary_periods.melt(
            value_vars=['salaryPeriod', 'notApprovedSalaryPeriod']
        )
    df = df[
        df.value.astype(str).str.contains('ЗП') |
        df.value.astype(str).str.contains('Аванс')
        ]

    if df.empty:
        await message.answer("У вас нет доступных периодов")
    else:
        for period in df.value:
            kb_period.row(period)
        await DetailsJobForm.choose_kb.set()
        await message.answer("Выберите период: ", reply_markup=kb_period)


@dp.message_handler(state=DetailsJobForm.choose_kb)
async def send_graph(message: Message, state: FSMContext) -> None:
    """
       Формирует график по ЗП и отправляет его
       :param message: сообщение

    """
    df_iterable = db_manager.get_df_for_graph(
        message.chat.id, message.text
    ).to_dataframe_iterable()
    for df in df_iterable:
        if not df.empty:
            labels = get_xlabel_for_graph(df)
            get_image(df, labels)
            await message.bot.send_photo(
                message.chat.id, open("saved_graph.png", "rb"),
                caption=message.text, reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer("Заданный период не найден",
                                 reply_markup=ReplyKeyboardRemove())
    await state.finish()
