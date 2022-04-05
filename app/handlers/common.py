"""
Модуль содержит первичные обработчики, осуществляющие приветствие
новых пользователей, доведение полезной информации, а так же список
доступных команд и FAQ.
"""
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


async def process_start_command(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать в чат Бот компании Ylab. Для "
                         "регистрации в Боте введите команду /reg, "
                         "или /help для получения списка доступных команд.")
    await state.finish()


async def process_help_command(message: types.Message, state: FSMContext):
    # await BotStates.STATE_0.set()
    await message.answer("Здесь будет список доступных команды:\n"
                         "/reg - регистрация в боте;\n"
                         "/search - поиск зарегистрированных пользователей;\n"
                         "/faq - техническая поддержка.")
    await state.finish()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "старт",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено",
                         reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(process_start_command,
                                commands="start", state="*")
    dp.register_message_handler(process_help_command,
                                commands="help", state="*")
    dp.register_message_handler(cmd_start,
                                commands="start", state="*")
    dp.register_message_handler(cmd_cancel,
                                commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel,
                                Text(equals="отмена", ignore_case=True),
                                state="*")
