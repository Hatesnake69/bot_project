import re

import aiogram.utils.markdown as md
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup
from aiogram_calendar import SimpleCalendar, simple_cal_callback

from sсheduler import YScheduler

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, )

scheduler = YScheduler()

class Form(StatesGroup):
    """
    Состояния для команды /create_event
    """
    event_name = State()
    event_date = State()
    event_time = State()
    event_comment = State()
    event_confirm = State()


async def create_event_start(message: types.Message) -> None:
    """
    Перехватывает сообщение с командой /create_event
    Устанавливает стейт event_name
    Спрашивает у пользователя название события
    :param message: сообщение
    """
    await Form.event_name.set()
    await message.reply("Привет!\nУкажи название события.")


async def set_event_name(message: types.Message, state: FSMContext) -> None:
    """
    Перехватывает сообщение со стейтом event_name
    Записывает название события в state.proxy() по ключу "event_name"
    Устанавливает следующее значение стейта event_date
    Просит у пользователя выбрать дату и выводит календарик
    :param message: сообщение
    :param state: стейт
    """
    async with state.proxy() as data:
        data['event_name'] = message.text
    await Form.next()
    await message.answer(text="Выберите дату: ", reply_markup=await SimpleCalendar().start_calendar())


async def set_event_date(callback_query: CallbackQuery, callback_data, state: FSMContext) -> None:
    """
    Перехватывает событие нажимания на кнопку даты из календарика со стейтом event_date
    Записывает значение нажатой кнопки в state.proxy() по ключу "event_date"
    Устанавливает следующее значение стейта event_time
    Просит у пользователя написать время
    :param callback_query: callback_query
    :param callback_data: callback_data
    :param state: стейт
    """
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали: {date.strftime("%d/%m/%Y")}',
        )
        await callback_query.message.answer(
            f'Укажи время события в формате HH:MI'
        )
        async with state.proxy() as data:
            data['event_date'] = f'{date.strftime("%d/%m/%Y")}'
        await Form.next()


async def set_event_time_invalid(message: types.Message) -> None:
    """
    Перехватывает неверный формат времени со стейтом event_time
    Просит ввести время в указанном формате
    :param message: сообщение
    """
    await message.reply("Время должно быть в формате HH:MI")


async def set_event_time(message: types.Message, state: FSMContext) -> None:
    """
    Перехватывает верный ввод времени со стейтом event_time
    Записывает в state.proxy() время по ключу "event_time"
    Устанавливает стейт event_comment
    Просит написать комментарий
    :param message: сообщение
    :param state: стейт
    """
    async with state.proxy() as data:
        data['event_time'] = message.text
    await Form.next()
    await message.reply("Напиши комментарий.")


async def set_event_comment(message: types.Message, state: FSMContext) -> None:
    """
    Перехватывает комментарий со стейтом event_comment
    Записывает в state.proxy() комментарий по ключу "event_comment"
    Спрашивает у пользователя верна ли введенная информация
    Устанавливает стейт event_confirm
    Просит подтверждения
    :param message: сообщение
    :param state: стейт
    """
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


async def set_event_confirm_invalid(message: types.Message) -> None:
    """
    Перехватывает неверный формат ответа со стейтом event_confirm
    Просит ввести ответ в указанном формате
    :param message: сообщение
    """
    await message.reply("Подтвердить? (да/нет)")


async def set_event_confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            await message.reply('Событие создано')

            scheduler.set_scheduler(
                          message.bot,
                          message.from_user.id,
                          data['event_name'],
                          data['event_date'],
                          data['event_time'],
                          data['event_comment']
            )
        else:
            await message.reply('Событие не создано')

    await state.finish()


def register_handlers_create_event(dp: Dispatcher) -> None:
    """
    Функция регистрирует функции выше, а также условия их выполнения
    :param dp: диспатчер бота
    """
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
