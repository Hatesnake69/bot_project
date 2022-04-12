from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

import keyboards as key
from data import cache
from utils import db

db_manager = db.DBManager()


class BotStates(StatesGroup):
    """
    Класс описывает состояния функций
    """

    STATE_0 = State()
    STATE_1 = State()
    STATE_2 = State()


async def update_state(message: Message,
                       new_state: State(),
                       keyboard: str,
                       state: FSMContext):
    """
    Функция отвечает за обновление состояния
    """

    await cache.set_data(chat=message.chat,
                         user=message.from_user.username,
                         data=message.text)
    await state.set_state(new_state)
    await message.reply("choose",
                        reply_markup=key.KEYBOARDS[keyboard],
                        reply=False)


async def get_reply(message: Message,
                    faq_key: str):
    """
    Функция получает ответ на FAQ и отправляет пользователю
    """

    await cache.set_data(chat=message.chat,
                         user=message.from_user.username,
                         data=message.text)

    await message.reply(db_manager.get_df_for_faq(faq_key))
