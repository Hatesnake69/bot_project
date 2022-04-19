from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchStates(StatesGroup):
    """
    Класс описывает состояния обработчиков, отвечающих за поиск пользователей
    """
    SEARCH_PROCESS = State()
    AFTER_SEARCH_PROCESS = State()