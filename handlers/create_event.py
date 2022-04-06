import re

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup
from aiogram.utils.markdown import text
from aiogram_calendar import SimpleCalendar, simple_cal_callback

from scheduler import set_scheduler
from states import CreateEventForm
from loader import dp


start_kb = ReplyKeyboardMarkup(resize_keyboard=True)


@dp.message_handler(commands=["create_event"], state="*")
async def create_event_start(message: Message) -> None:
    """
    Перехватывает сообщение с командой /create_event
    Устанавливает стейт event_name
    Спрашивает у пользователя название события
    :param message: сообщение
    """
    await CreateEventForm.event_name.set()
    await message.reply("Привет!\nУкажи название события.")


@dp.message_handler(state=CreateEventForm.event_name)
async def set_event_name(message: Message, state: FSMContext) -> None:
    """
    Перехватывает сообщение со стейтом event_name
    Записывает название события в state.proxy() по ключу "event_name"
    Устанавливает следующее значение стейта event_date
    Просит у пользователя выбрать дату и выводит календарик
    :param message: сообщение
    :param state: стейт
    """
    async with state.proxy() as data:
        data["event_name"] = message.text
    await CreateEventForm.next()
    await message.answer(
        text="Выберите дату: ",
        reply_markup=await SimpleCalendar().start_calendar()
    )


@dp.callback_query_handler(
    simple_cal_callback.filter(),
    state=CreateEventForm.event_date)
async def set_event_date(
        callback_query: CallbackQuery, callback_data, state: FSMContext
) -> None:
    """
    Перехватывает событие нажимания на кнопку
    даты из календарика со стейтом event_date
    Записывает значение нажатой кнопки в state.proxy() по ключу "event_date"
    Устанавливает следующее значение стейта event_time
    Просит у пользователя написать время
    :param callback_query: callback_query
    :param callback_data: callback_data
    :param state: стейт
    """
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data
    )
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали: {date.strftime("%d/%m/%Y")}',
        )
        await callback_query.message.answer(
            "Укажи время события в формате HH:MI"
        )
        async with state.proxy() as data:
            data["event_date"] = f'{date.strftime("%d/%m/%Y")}'
        await CreateEventForm.next()


@dp.message_handler(
    lambda message: not re.match(
        r"^(([01]\d|2[0-3]):([0-5]\d)|24:00)$",
        message.text),
    state=CreateEventForm.event_time)
async def set_event_time_invalid(message: Message) -> None:
    """
    Перехватывает неверный формат времени со стейтом event_time
    Просит ввести время в указанном формате
    :param message: сообщение
    """
    await message.reply("Время должно быть в формате HH:MI")


@dp.message_handler(state=CreateEventForm.event_time)
async def set_event_time(message: Message, state: FSMContext) -> None:
    """
    Перехватывает верный ввод времени со стейтом event_time
    Записывает в state.proxy() время по ключу "event_time"
    Устанавливает стейт event_comment
    Просит написать комментарий
    :param message: сообщение
    :param state: стейт
    """
    async with state.proxy() as data:
        data["event_time"] = message.text
    await CreateEventForm.next()
    await message.reply("Напиши комментарий.")


@dp.message_handler(state=CreateEventForm.event_comment)
async def set_event_comment(message: Message, state: FSMContext) -> None:
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
        data["event_comment"] = message.text

    await message.answer(
        text(
            text(message.chat.id),
            text(data["event_name"]),
            text(data["event_date"]),
            text(data["event_time"]),
            text(data["event_comment"]),
            sep="\n",
        ),
    )

    await CreateEventForm.next()
    await message.reply("Подтвердить? (да/нет)")


@dp.message_handler(
    lambda message: message.text.lower() not in {"да", "нет"},
    state=CreateEventForm.event_confirm)
async def set_event_confirm_invalid(message: Message) -> None:
    """
    Перехватывает неверный формат ответа со стейтом event_confirm
    Просит ввести ответ в указанном формате
    :param message: сообщение
    """
    await message.reply("Подтвердить? (да/нет)")


@dp.message_handler(state=CreateEventForm.event_confirm)
async def set_event_confirm(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "да":
            await message.reply("Событие создано")
            set_scheduler(
                message,
                message.from_user.id,
                data["event_name"],
                data["event_date"],
                data["event_time"],
                data["event_comment"],
            )
        else:
            await message.reply("Событие не создано")

    await state.finish()
