
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from data import cache
from loader import db_manager


class IsRegistered(BoundFilter):
    """
    Фильтр проверяет зарегистрирован ли пользователь.
    Сначала она обращается в редис, и если записи о регистрации там нет,
    То обращается в bigquery, получает значение, и пишет его в редисовский кэш.
    """
    async def check(self, message: Message) -> bool:
        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            data = await cache.get_data(
                user=user_id,
                chat=chat_id
            )
            is_reg = data['reg_status']

        except KeyError:
            is_reg = not db_manager.check_user(message=message)
            await cache.update_data(
                user=user_id,
                chat=chat_id,
                data={'reg_status': is_reg}
            )
        return is_reg
