from aiogram.types import CallbackQuery, ReplyKeyboardMarkup

import re

import aiogram.utils.markdown as md
from aiogram import types, Dispatcher

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from aiogram_calendar import SimpleCalendar, simple_cal_callback

start_kb = ReplyKeyboardMarkup(resize_keyboard=True,)


class Form(StatesGroup):
    event_name = State()
    event_date = State()
    event_time = State()
    event_comment = State()
    event_confirm = State()


async def create_event_start(message: types.Message):
    await Form.event_name.set()
    await message.reply("Привет!\nУкажи название события.")


async def set_event_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_name'] = message.text

    await Form.next()
    await message.answer(text="Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())


async def set_event_date(callback_query: CallbackQuery, callback_data, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}\nУкажи время события.',
        )
        async with state.proxy() as data:
            data['event_date'] = f'{date.strftime("%d/%m/%Y")}'
        await Form.next()


async def set_event_time_invalid(message: types.Message):
    """
    If time is invalid
    """
    return await message.reply("Время должно быть в формате HH:MI")


async def set_event_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_time'] = message.text

    await Form.next()
    await message.reply("Напиши комментарий.")


async def set_event_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_comment'] = message.text

    await message.answer(
                           md.text(
                               md.text(message.chat.id),
                               md.text(data['event_name']),
                               md.text(data['event_date']),
                               md.text(data['event_time']),
                               md.text(data['event_comment']),
                               sep='\n',
                           ),
                        )

    await Form.next()
    await message.reply("Подтвердить? (да/нет)")


async def set_event_confirm_invalid(message: types.Message):
    """
    If time is invalid
    """
    return await message.reply("Подтвердить? (да/нет)")


async def set_event_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.reply('Событие создано')
    else:
        await message.reply('Событие не создано')
    await state.finish()


def register_handlers_create_event(dp: Dispatcher):
    dp.register_message_handler(create_event_start, commands="create_event", state="*")
    dp.register_message_handler(set_event_name, state=Form.event_name)
    dp.register_callback_query_handler(set_event_date, simple_cal_callback.filter(), state=Form.event_date)
    dp.register_message_handler(set_event_time_invalid,
                                lambda message: not re.match(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$', message.text),
                                state=Form.event_time)
    dp.register_message_handler(set_event_time, state=Form.event_time)
    dp.register_message_handler(set_event_comment, state=Form.event_comment)
    dp.register_message_handler(set_event_confirm_invalid,
                                lambda message: message.text.lower() not in {'да', 'нет'},
                                state=Form.event_confirm)
    dp.register_message_handler(set_event_confirm, state=Form.event_confirm)