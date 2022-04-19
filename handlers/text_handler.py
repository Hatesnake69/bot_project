from aiogram.types import Message
from loader import dp


@dp.message_handler()
async def cmd_cancel(message: Message):
    await message.answer("Добро пожаловать в чат Бот компании Ylab. Для "
                         "регистрации в Боте введите команду /reg, "
                         "или /help для получения списка доступных команд. "
                         "Если Вы не прошли регистрацию, функционал "
                         "Бота будет заблокирован.")
