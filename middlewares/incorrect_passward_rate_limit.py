from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data import cache


class ThrottlingMiddleware(BaseMiddleware):
    """
    Миддлвейр, который отслеживает в кэше значение ключа 'black_list'
    и в случае значения True: отменяет все команды пользователя
    """

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param message:
        """

        data = await cache.get_data(
            user=message.from_user.id,
            chat=message.chat.id)
        if data.get('black_list'):
            await message.answer('Доступ заблокирован')
            raise CancelHandler()
