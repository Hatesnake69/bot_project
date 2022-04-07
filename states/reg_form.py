from aiogram.dispatcher.filters.state import State, StatesGroup


class RegForm(StatesGroup):
    """
    Класс описывает состояния функций, отвечающих за регистрацию
    """
    EMAIL_MESSAGE = State()
    KEY_MESSAGE = State()
