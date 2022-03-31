from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    """
    Класс описывает состояния функций

    Состояния:
    STATE_0 -- Нулевое состояние для запуска различных команд /start, /help ...
    в этом состоянии большинство handlers неактивны
    STATE_1 -- активирует def email_message()
    STATE_2 -- активирует def key_message()
    """
    STATE_0 = State()
    STATE_1 = State()
    STATE_2 = State()


