"""
Модуль содержит обработчики, осуществляющие регистрацию новых
пользователей по электронной почте, посредством команды /reg
"""
import re
import secrets

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from utils.db import DBManager
from data import cache
from services import sending_message
from states import RegStates
from loader import dp

manager = DBManager()


def isValid(email):
    """
    Функция проверяет введенную пользователем электронную почту
    на соответствие за счет Регулярного Выражения
    """
    regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@ylab.io")
    if re.fullmatch(regex, email):
        return True
    else:
        return False


@dp.message_handler(commands=["reg"], state="*")
async def process_reg_command(message: Message):
    if manager.check_user(message):
        await message.answer("Здравствуйте, напишите адрес свой электронной "
                             "почты в домене @ylab.io для прохождения "
                             "дальнейшей регистрации!")
    else:
        await message.answer("Вы уже зарегистрированы. /help")
    await RegStates.EMAIL_MESSAGE.set()


@dp.message_handler(state=RegStates.EMAIL_MESSAGE)
async def send_email_message(message: Message):
    secret_key = secrets.token_urlsafe(8)
    await cache.set_data(chat=message.chat,
                         user=message.from_user.username,
                         data={'secret_key': secret_key})
    if isValid(message.text):
        if manager.check_auth(message):
            manager.registration(message)
        sending_message(message.text, secret_key)
        await message.answer("На вашу почту отправлен ключ "
                             "подтверждения введите его: ")
        await cache.update_data(chat=message.chat,
                                user=message.from_user.username,
                                data={'email': message.text})

        await RegStates.KEY_MESSAGE.set()
    else:
        await message.answer("Проверьте правильность введенного адреса")


@dp.message_handler(state=RegStates.KEY_MESSAGE)
async def input_key_message(message: Message, state: FSMContext):
    secret_key = await cache.get_data(chat=message.chat,
                                      user=message.from_user.username)
    if secret_key['secret_key'] == message.text:
        manager.authentication(message)
        await message.answer("Вы ввели верный ключ! "
                             "Добро пожаловать в YlabBot")
        await state.finish()
    else:
        await message.answer("Ошибка")
