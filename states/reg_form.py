from aiogram.dispatcher.filters.state import StatesGroup, State


class RegForm(StatesGroup):
    """
    Класс описывает состояния функций, отвечающих за регистрацию
    """
    email_message = State()
    key_message = State()
