"""
Модуль содержит обработчики, осуществляющие регистрацию новых
пользователей по электронной почте, посредством команды /reg
"""

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message

from config import cache
from maildelivery import gen_secret_key, sending_message
from services.registration import make_registration
from states import BotStates


async def process_reg_command(message: Message):
    await message.answer("Здравствуйте, напишите адрес свой электронной почты "
                         "в домене @ylab.io для прохождения дальнейшей "
                         "регистрации!")
    await BotStates.EMAIL_MESSAGE.set()


async def send_email_message(message: Message):
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

        await BotStates.KEY_MESSAGE.set()
    else:
        await message.answer("Вы ввели не корректный адрес")


async def input_key_message(message: Message, state: FSMContext):
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
                                state=BotStates.EMAIL_MESSAGE)
    dp.register_message_handler(input_key_message,
                                state=BotStates.KEY_MESSAGE)
