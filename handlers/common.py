"""
Модуль содержит первичные обработчики, осуществляющие приветствие
новых пользователей, доведение полезной информации, а так же список
доступных команд и FAQ.
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp


@dp.message_handler(commands=["start"], state="*")
async def process_start_command(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать в чат Бот компании Ylab. Для "
                         "регистрации в Боте введите команду /reg, "
                         "или /help для получения списка доступных команд.")
    await state.finish()


@dp.message_handler(commands=["help"], state="*")
async def process_help_command(message: Message, state: FSMContext):
    await message.answer("Здесь будет список доступных команды:\n"
                         "/reg - регистрация в боте;\n"
                         "/search - поиск зарегистрированных пользователей;\n"
                         "/create_event - создание запланированной встречи;\n"
                         "/faq - часто задаваемые вопросы.\n"
                         "/cancel - отмена текущей команды")
    await state.finish()


@dp.message_handler(commands=["cancel"], state="*")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено",
                         reply_markup=ReplyKeyboardRemove())
