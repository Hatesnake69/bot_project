from aiogram import Dispatcher

from .is_reg import IsRegistered
from .is_admin import IsUserAdmin


def setup(dp: Dispatcher) -> None:
    dp.filters_factory.bind(IsRegistered, event_handlers=dp.message_handlers)
    dp.filters_factory.bind(IsUserAdmin, event_handlers=dp.message_handlers)
