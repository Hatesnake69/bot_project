"""
Модуль содержит обработчики, осуществляющие регистрацию новых
пользователей по электронной почте, посредством команды /reg
"""
import secrets

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data import cache
from handlers.search import is_data_valid
from loader import db_manager as manager
from loader import dp
from services import sending_message
from states import RegStates


async def tracker(message: Message, key: str, state: FSMContext) -> None:
    """
    Функция проверяет количество вводов имейла и паролей пользователем
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
            manager.send_to_blacklist(user_id=message.from_user.id)
            data.pop('email_try', None)
            data.pop('password_try', None)
            await state.finish()
        else:
            data[key] += 1
    except KeyError:
        data[key] = 2
    await cache.update_data(
        chat=message.chat.id,
        user=message.from_user.id,
        data=data
    )


@dp.message_handler(commands=["reg"], state="*")
async def process_reg_command(message: Message):
    check_user = await manager.check_user(message=message)
    if check_user:
        await message.answer("Добро пожаловать в чат Бот компании Ylab. Вы "
                             "уже зарегестрированы. Нажмите /help и выберите "
                             "команду.")
    else:
        await message.answer("Здравствуйте, напишите адрес свой электронной "
                             "почты в домене @ylab.io для прохождения "
                             "дальнейшей регистрации!")
        await RegStates.EMAIL_MESSAGE.set()


@dp.message_handler(state=RegStates.EMAIL_MESSAGE)
async def send_email_message(message: Message, state: FSMContext) -> None:
    await tracker(message=message, key='email_try', state=state)
    secret_key = secrets.token_urlsafe(8)
    await cache.update_data(
        chat=message.chat.id,
        user=message.from_user.id,
        data={'secret_key': secret_key}
    )
    if is_data_valid(message.text, 'email'):
        check_auth: bool = await manager.check_auth(message)
        if not check_auth:
            await manager.registration(message)
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
async def input_key_message(message: Message, state: FSMContext) -> None:
    await tracker(message=message, key='password_try', state=state)
    secret_key = await cache.get_data(
        chat=message.chat.id,
        user=message.from_user.id
    )
    if secret_key['secret_key'] == message.text:
        await manager.authentication(message)
        await message.answer("Вы ввели верный ключ! "
                             "Добро пожаловать в YlabBot")
        await state.finish()

    else:
        await message.answer("Неверный пароль. Пожалуйста, повторите попытку.")
