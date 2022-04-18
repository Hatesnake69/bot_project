from aiogram.dispatcher.filters.state import State, StatesGroup


class DetailsJobForm(StatesGroup):
    """
    Устанавливает команду для отпрвки комментария пользователем
    """
    choose_kb = State()
