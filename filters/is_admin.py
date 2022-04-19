from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from data import cache
from loader import db_manager


class IsUserAdmin(BoundFilter):
    """
    Функция проверяет является ли пользователь администратором.
    Сначала она проверяет есть ли role в редиc, если нет, то обращается
    в bigquery, получает значение, и пишет его в редисовский кэш.
    """

    async def check(self, message: Message) -> bool:
        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            data = await cache.get_data(
                user=user_id,
                chat=chat_id
            )
            is_reg_flag = data['is_admin']
            return is_reg_flag

        except KeyError:
            is_admin = db_manager.check_user_role(message=message)
            if is_admin in [True, False]:
                await cache.update_data(
                    user=user_id,
                    chat=chat_id,
                    data={'is_admin': is_admin},
                )
                return is_admin
            else:
                await message.answer("Произошла непредвиденная ошибка, "
                                     "свяжитесь с администратором")
                return False
