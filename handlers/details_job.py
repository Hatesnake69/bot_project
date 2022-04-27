import re

import pandas as pd
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from data import cache
from filters import IsRegistered
from loader import db_manager, dp
from services import save_graph
from utils import constants


async def get_menu_salary_period(message: Message):
    """
    Функция проверяет есть ли в кеш периоды,
    если нет достает из БД и обновляет кеш

    """
    try:

        data = await cache.get_data(
            user=message.from_user.id, chat=message.chat.id
        )
        salary_periods = data["salary_periods"]
        return pd.read_json(salary_periods)

    except KeyError:
        df_iterable = db_manager.get_salary_periods_user(
            message.from_user.id
        ).to_dataframe_iterable()

        for salary_periods in df_iterable:
            df_json = salary_periods.to_json()
        await cache.update_data(
            user=message.from_user.id,
            chat=message.chat.id,
            data={"salary_periods": df_json},
        )
        return salary_periods


def sort_salary_periods(salary_periods: list) -> list:
    """
    Функция сортирует зарплатные периоды и возвращает отсортированный список

    """
    periods: list = []

    for period in salary_periods:
        for key, value in constants.MONTHS.items():
            month = re.search(r"-([а-яA-Я]+)", period).group(1)
            if value == month:
                str_period = re.sub(month, f" {key} ", period)
                periods.append(str_period.split())
                continue

    sort_periods = sorted(periods, key=lambda p: (-int(p[2]), -int(p[1])))

    return [f"{period[0]}{constants.MONTHS[int(period[1])]}{period[2]}"
            for period in sort_periods
            ]


@dp.message_handler(
    IsRegistered(), Text(equals=["/details_job"]), commands=["details_job"]
)
async def print_menu_salary_period(message: Message) -> None:
    """
    Создает запрос в БД об имеющихся ЗП
    и формирует меню
    :param message: сообщение

    """

    salary_periods = await get_menu_salary_period(message)
    df = salary_periods.melt(
        value_vars=["salaryPeriod", "notApprovedSalaryPeriod"]
    )
    df = df[
        df.value.astype(str).str.contains("ЗП")
        | df.value.astype(str).str.contains("Аванс")
        ]

    if df.empty:
        await message.answer("У вас нет доступных периодов")
    else:
        periods = sort_salary_periods(list(df.value))
        kb_periods = InlineKeyboardMarkup()

        for period in periods:
            kb_periods.add(
                InlineKeyboardButton(text=period, callback_data=f"p{period}")
            )

        await message.answer("Выберите период: ", reply_markup=kb_periods)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("p"))
async def send_graph(call: CallbackQuery) -> None:
    """
    Формирует график по ЗП и отправляет его

    """

    df_iterable = db_manager.get_df_for_graph(
        call.from_user.id, call.data[1:]
    ).to_dataframe_iterable()

    for df in df_iterable:
        if not df.empty:
            save_graph(df)
            await call.bot.send_photo(
                call.from_user.id,
                open("saved_graph.png", "rb"),
                caption=call.data[1:]
            )
        else:
            await call.answer("Заданный период не найден")
