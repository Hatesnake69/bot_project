"""
Модуль содержит первичные обработчики, осуществляющие приветствие
новых пользователей, доведение полезной информации, а так же список
доступных команд и FAQ.
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp


@dp.message_handler(commands=["start"], state="*")
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

    await message.answer("Добро пожаловать в чат Бот компании Ylab. Для "
                         "регистрации в Боте введите команду /reg, "
                         "или /help для получения списка доступных команд.")
    await state.finish()


@dp.callback_query_handler(text=['/end_search'], state="*")
@dp.message_handler(commands=["help"], state="*")
async def process_help_command(event, state: FSMContext) -> None:
    """
    Выводит список доступных команд бота

    :param event: объект Message или CallbackQuery
    :type event : Message или CallbackQuery
    :param state: объект FSMContext
    :type state : FSMContext

    :return: None
    :rtype: NoneType
    """
    help_info = "Список доступных команды бота:\n" \
                " /reg - регистрация в боте;\n" \
                " /search - поиск зарегистрированных пользователей;\n" \
                " /create_event - создание запланированной встречи;\n" \
                "/details_job - информация о времени работы;\n" \
                "/faq - часто задаваемые вопросы.\n" \
                "/cancel - отмена текущей команды"
    try:
        await event.message.answer(help_info)
    except AttributeError:
        await event.answer(help_info)
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
