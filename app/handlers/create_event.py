from aiogram.types import ReplyKeyboardMarkup

import aiogram.utils.markdown as md
from aiogram import types, Dispatcher

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


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
    await message.answer(text="Please select a date: ")


# @dp.message_handler(state=Form.event_date)
# async def nav_cal_handler(message: Message):
#
#     await Form.next()
#     await message.reply("Укажи время события.")


# simple calendar usage
# @dp.callback_query_handler(simple_cal_callback.filter(), state=Form.event_date)
# async def set_event_date(callback_query: CallbackQuery, callback_data, state: FSMContext):
#     selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
#     if selected:
#         await callback_query.message.answer(
#             f'You selected {date.strftime("%d/%m/%Y")}',
#         )
#         async with state.proxy() as data:
#             data['event_date'] = f'{date.strftime("%d/%m/%Y")}'
#         await Form.next()
#         await bot.send_message(chat_id=callback_query.message.chat.id, text="Укажи время события.")


async def set_event_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_date'] = message.text
    await Form.next()
    await message.answer(text="Укажи время события.")


# Check time.
# @dp.message_handler(lambda message: not re.match(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$', message.text), state=Form.event_time)
# async def process_time_invalid(message: types.Message):
#     """
#     If time is invalid
#     """
#     return await message.reply("Время должно быть в формате HH:MI")


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
                           # reply_markup=markup,
                           # parse_mode=ParseMode.MARKDOWN,
                           )

    await Form.next()
    await message.reply("Подтвердить? (да/нет)")


# Check time.
# @dp.message_handler(lambda message: message.text.lower not in {'да', 'нет'}, state=Form.event_confirm)
# async def process_choice_invalid(message: types.Message):
#     """
#     If time is invalid
#     """
#     return await message.reply("Подтвердить? (да/нет)")


# @dp.message_handler(state=Form.event_confirm)
async def set_event_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.reply('Событие создано')
    else:
        await message.reply('Событие не создано')
    await state.finish()


def register_handlers_create_event(dp: Dispatcher):
    dp.register_message_handler(create_event_start, commands="create_event", state="*")
    dp.register_message_handler(set_event_name, state=Form.event_name)
    dp.register_message_handler(set_event_date, state=Form.event_date)
    dp.register_message_handler(set_event_time, state=Form.event_time)
    dp.register_message_handler(set_event_comment, state=Form.event_comment)
    dp.register_message_handler(set_event_confirm, state=Form.event_confirm)
