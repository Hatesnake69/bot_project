from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data import cache
from loader import db_manager as manager


class ThrottlingMiddleware(BaseMiddleware):
    """
    Миддлвейр, который отслеживает в кэше значение ключа 'black_list'
    и в случае значения True: отменяет все команды пользователя
    """

    async def on_process_message(
            self,
            message: types.Message,
            data: dict
    ) -> None:
        """
        This handler is called when dispatcher receives a message

        :param message:
        """
        data = await cache.get_data(
            user=message.from_user.id,
            chat=message.chat.id
        )
        try:
            if data['black_list']:
                await message.answer('Доступ заблокирован')
                raise CancelHandler()
        except KeyError:
            if manager.check_black_list(message=message):
                data['black_list'] = True
                cache.update_data(
                    user=message.from_user.id,
                    chat=message.chat.id,
                    data=data
                )
                await message.answer('Доступ заблокирован')
                raise CancelHandler()
            else:
                data['black_list'] = False
