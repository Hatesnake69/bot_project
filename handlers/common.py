"""
Модуль содержит первичные обработчики, осуществляющие приветствие
новых пользователей, доведение полезной информации, а так же список
доступных команд и FAQ.
"""

from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from loader import dp
from filters import IsGroupChat, IsRegistered


@dp.message_handler(IsGroupChat(), commands=["start"], state="*")
async def process_start_command(message: Message, state: FSMContext) -> None:
    """
    Перехватывает команду start и выводит
    приветственное сообщение

    :param message: объект Message
    :type message : Message
    :param state: объект FSMContext
    :type state : FSMContext

    :return: None
    :rtype: NoneType
    """
    sub_text = ""

    if message.from_user.username is not None:
        sub_text += f", {message.from_user.username}"

    welcome_info = f"Добро пожаловать в чат-бот компании Ylab{sub_text}.\n"

    registered = await IsRegistered().check(message)

    if not registered:
        welcome_info += "Для регистрации в боте введите команду /reg.\n"
    else:
        welcome_info += "Для получения списка доступных команд нажмите /help."

    await message.answer(welcome_info)
    await state.finish()


@dp.callback_query_handler(text=['/end_search'], state="*")
@dp.message_handler(IsRegistered(), commands=["help"], state="*")
async def process_help_command(
        obj: Union[Message, CallbackQuery],
        state: FSMContext
) -> None:
    """
    Выводит список доступных команд бота

    :param obj: объект Message или CallbackQuery
    :type obj : Message или CallbackQuery
    :param state: объект FSMContext
    :type state : FSMContext

    :return: None
    :rtype: NoneType
    """
    help_info = ""

    if type(obj) == Message:
        help_info += "Выберите команду:\n" \
                     "/search - поиск зарегистрированных пользователей;\n" \
                     "/create_event - создание напоминания о событии;\n" \
                     "/details_job - информация об отработанном времени;\n" \
                     "/faq - часто задаваемые вопросы;\n" \
                     "/cancel - отмена текущей команды;"

        await obj.answer(help_info)

    if type(obj) == CallbackQuery:
        help_info += "Поиск завершён."
        await obj.message.delete()
        await obj.message.answer(help_info)

    await state.finish()


@dp.message_handler(commands=["cancel"], state="*")
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """
    Перехватывает команду cancel и
    сбрасывает стейт

    :param message: объект Message
    :type message : Message
    :param state: объект FSMContext
    :type state : FSMContext

    :return: None
    :rtype: NoneType
    """

    await state.finish()
    await message.answer("Действие отменено",
                         reply_markup=ReplyKeyboardRemove())
