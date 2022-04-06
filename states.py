from aiogram.dispatcher.filters.state import State, StatesGroup

import keyboards as key
from config import cache


class BotStates(StatesGroup):
    """
    Класс описывает состояния функций
    """

    STATE_0 = State()
    STATE_1 = State()
    STATE_2 = State()
    INIT_FIRST_STATE = State()
    INIT_SECOND_STATE = State()
    INIT_THIRD_STATE = State()
    FIN_FIRST_STATE = State()
    FIN_SECOND_STATE = State()
    FIN_THIRD_STATE = State()
    ORG_STATE = State()
    OTH_STATE = State()
    TECH_FIRST_STATE = State()
    TECH_SECOND_STATE = State()
    ACC_STATE = State()
    EVENT_NAME = State()
    EVENT_DATE = State()
    EVENT_TIME = State()
    EVENT_COMMENT = State()
    EVENT_CONFIRM = State()
    EMAIL_MESSAGE = State()
    KEY_MESSAGE = State()


async def update_state(message, new_state, keyboard, state):
    await cache.set_data(chat=message.chat,
                         user=message.from_user.username,
                         data=message.text)
    await state.set_state(new_state)
    await message.reply("choose",
                        reply_markup=key.KEYBOARDS[keyboard],
                        reply=False)
