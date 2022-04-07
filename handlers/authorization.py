"""
Модуль содержит обработчики, осуществляющие регистрацию новых
пользователей по электронной почте, посредством команды /reg
"""

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data import cache
from loader import dp
from services import gen_secret_key, sending_message
from utils.db import DBManager
from states import RegForm

manager = DBManager()


@dp.message_handler(commands=["reg"], state="*")
async def process_reg_command(message: Message):
    if manager.check_user(message):
        await message.answer("Здравствуйте, напишите адрес своей электронной"
                             "почты в домене @ylab.io для прохождения "
                             "дальнейшей регистрации!")
    else:
        await message.answer("Вы уже зарегистрированы. /help")
    await RegForm.EMAIL_MESSAGE.set()


@dp.message_handler(state=RegForm.EMAIL_MESSAGE)
async def send_email_message(message: Message):
    secret_key = gen_secret_key()
    await cache.set_data(chat=message.chat,
                         user=message.from_user.username,
                         data={'secret_key': secret_key})
    if '@ylab.io' in message.text:
        if manager.check_auth(message):
            manager.registration(message)
        sending_message(message.text, secret_key)
        await message.answer("На вашу почту отправлен ключ "
                             "подтверждения введите его: ")
        await cache.update_data(chat=message.chat,
                                user=message.from_user.username,
                                data={'email': message.text})

        await RegForm.KEY_MESSAGE.set()
    else:
        await message.answer("Вы ввели не корректный адрес")


@dp.message_handler(state=RegForm.KEY_MESSAGE)
async def input_key_message(message: Message, state: FSMContext):
    secret_key = await cache.get_data(chat=message.chat,
                                      user=message.from_user.username)
    if secret_key['secret_key'] == message.text:
        manager.authentication(message)
        await message.answer("Вы ввели верный ключ! "
                             "Добро пожаловать в YlabBot")
        await state.finish()
    else:
        await message.answer("Вы ввели неверный ключ")
