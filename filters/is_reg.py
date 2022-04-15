
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
            is_reg_flag = data['reg_status']
            return is_reg_flag

        except KeyError:
            is_reg = db_manager.check_user(message=message)
            if is_reg == 'Registered':
                await cache.update_data(
                    user=user_id,
                    chat=chat_id,
                    data={'reg_status': True}
                )
                return True
            elif is_reg == 'Not Registered':
                await cache.update_data(
                    user=user_id,
                    chat=chat_id,
                    data={'reg_status': False}
                )
                return False
            else:
                await message.answer("Произошла непредвиденная ошибка, "
                                     "свяжитесь с администратором")
                return False
