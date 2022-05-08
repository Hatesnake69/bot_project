from aiogram.types import Message

from loader import dp
from filters import IsRegistered


@dp.message_handler()
async def cmd_cancel(message: Message) -> None:
    """
    Отправляет приветственное сообщение
    пользователю

    :param message: объект Message
    :type message: Message

    :return: None
    :rtype: NoneType
    """
    registered = await IsRegistered().check(message)

    welcome_info = f"Нужна помощь, {message.from_user.username}?\n"

    if not registered:
        welcome_info += "Для регистрации в боте введите команду /reg.\n"
    else:
        welcome_info += "Для получения списка доступных команд нажмите /help."

    await message.answer(welcome_info)
