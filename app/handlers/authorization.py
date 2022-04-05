"""
Модуль содержит обработчики, осуществляющие регистрацию новых
пользователей по электронной почте, посредством команды /reg
"""
from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import cache
from maildelivery import gen_secret_key, sending_message
from aiogram.dispatcher import FSMContext
from services.registration import make_registration


class RegForm(StatesGroup):
    """
    Класс описывает состояния функций, отвечающих за регистрацию
    """
    email_message = State()
    key_message = State()


async def process_reg_command(message: types.Message):
    await message.answer("Здравствуйте, напишите адрес свой электронной почты "
                         "в домене @ylab.io для прохождения дальнейшей "
                         "регистрации!")
    await RegForm.email_message.set()


async def send_email_message(message: types.Message):
    secret_key = gen_secret_key()
    await cache.set_data(chat=message.chat,
                         user=message.from_user.username,
                         data={'secret_key': secret_key})
    if '@ylab.io' in message.text:
        sending_message(message.text, secret_key)
        await message.answer("На вашу почту отправлен ключ "
                             "подтверждения введите его: ")
        await cache.update_data(chat=message.chat,
                                user=message.from_user.username,
                                data={'email': message.text})

        await RegForm.key_message.set()
    else:
        await message.answer("Вы ввели не корректный адрес")


async def input_key_message(message: types.Message, state: FSMContext):
    secret_key = await cache.get_data(chat=message.chat,
                                      user=message.from_user.username)
    print(secret_key['secret_key'])
    if secret_key['secret_key'] == message.text and \
            await make_registration(message):
        await message.answer("Вы ввели верный ключ! "
                             "Добро пожаловать в YlabBot")
        await state.finish()
    else:
        await message.answer("Ошибка")


def register_handlers_authorization(dp: Dispatcher):
    dp.register_message_handler(process_reg_command,
                                commands="reg", state="*")
    dp.register_message_handler(send_email_message,
                                state=RegForm.email_message)
    dp.register_message_handler(input_key_message,
                                state=RegForm.key_message)
