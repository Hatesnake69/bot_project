from aiogram.dispatcher.filters.state import State, StatesGroup


class GraphConfirmForm(StatesGroup):
    """
    Устанавливает команду для отпрвки комментария пользователем
    """
    comment_to_graph = State()
