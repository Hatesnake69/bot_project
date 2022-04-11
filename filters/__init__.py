from aiogram import Dispatcher
from .is_reg import IsRegistered


def setup(dp: Dispatcher) -> None:
    dp.filters_factory.bind(IsRegistered, event_handlers=dp.message_handlers)
