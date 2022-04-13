"""
Модуль содержит обработчики, осуществляющие регистрацию новых
пользователей по электронной почте, посредством команды /reg
"""
import re
import secrets

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data import cache
from loader import dp
from services import sending_message
from services.scheduler import db_manager as manager
from states import RegStates


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


async def tracker(message: Message, key: str) -> None:
    """
    Функция проверяет количество вводов имейла и паролей пользователм
    и в случае превышения лимита в 3 ед. создает в редисе запись
    с ключом 'black_list' со значением True
    """
    limit = 3
    data = await cache.get_data(
        chat=message.chat.id,
        user=message.from_user.id
    )
    try:
        if data[key] >= limit:
            data['black_list'] = True
        else:
            data[key] = data[key] + 1
    except KeyError:
        data[key] = 2
    await cache.update_data(
        chat=message.chat.id,
        user=message.from_user.id,
        data=data
    )


@dp.message_handler(commands=["reg"], state="*")
async def process_reg_command(message: Message):
    if manager.check_user(message=message):
        await message.answer("Здравствуйте, напишите адрес свой электронной "
                             "почты в домене @ylab.io для прохождения "
                             "дальнейшей регистрации!")
        await RegStates.EMAIL_MESSAGE.set()
    else:
        await message.answer("Добро пожаловать в чат Бот компании Ylab. Вы "
                             "уже зарегестрированы. Нажмите /help и выберете "
                             "команду.")


@dp.message_handler(state=RegStates.EMAIL_MESSAGE)
async def send_email_message(message: Message):
    await tracker(message=message, key='email_try')
    secret_key = secrets.token_urlsafe(8)
    await cache.update_data(
        chat=message.chat.id,
        user=message.from_user.id,
        data={'secret_key': secret_key}
    )
    if isValid(message.text):
        if manager.check_auth(message):
            manager.registration(message)
        sending_message(message.text, secret_key)
        await message.answer("На вашу почту отправлен ключ "
                             "подтверждения введите его: ")
        await cache.update_data(
            chat=message.chat.id,
            user=message.from_user.id,
            data={'email': message.text}
        )

        await RegStates.KEY_MESSAGE.set()
    else:
        await message.answer("Проверьте правильность введенного адреса")


@dp.message_handler(state=RegStates.KEY_MESSAGE)
async def input_key_message(message: Message, state: FSMContext):
    await tracker(message=message, key='password_try')
    secret_key = await cache.get_data(
        chat=message.chat.id,
        user=message.from_user.id
    )
    if secret_key['secret_key'] == message.text:
        manager.authentication(message)
        await message.answer("Вы ввели верный ключ! "
                             "Добро пожаловать в YlabBot")
        await state.finish()
    else:
        await message.answer("Ошибка")
