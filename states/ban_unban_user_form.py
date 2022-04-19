from aiogram.dispatcher.filters.state import State, StatesGroup


class BanUserForm(StatesGroup):
    ban_user_name = State()
    ban_confirm = State()


class UnBanUserForm(StatesGroup):
    unban_user_name = State()
    unban_confirm = State()
