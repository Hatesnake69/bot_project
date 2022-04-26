import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data import cache
from filters import UserRoleFilter
from loader import db_manager, dp
from states import UnBanUserForm


@dp.message_handler(
    UserRoleFilter(role='admin'),
    commands=["unban_user"],
    state="*"
)
async def unban_user_start(message: Message) -> None:
    """
    Перехватывает команду "/unban_user"
    :param message: Message
    """
    await UnBanUserForm.unban_user_name.set()
    await message.reply("Укажите id пользователя")


@dp.message_handler(state=UnBanUserForm.unban_user_name)
async def unban_user_name(message: Message, state: FSMContext) -> None:
    """
    Записывает в state.proxy id пользователя
    :param message: Message
    :param state: FSMContext
    """
    async with state.proxy() as data:
        data['user_id'] = message.text
    await message.answer(
        'Вы действительно хотите разблокировать пользователя? (да/нет)'
    )
    await UnBanUserForm.next()


@dp.message_handler(state=UnBanUserForm.unban_confirm)
async def unban_user_confirm(message: Message, state: FSMContext) -> None:
    """
    В зависимости от ответа отправляет запрос в бд
    :param message: Message
    :param state: FSMContext
    """
    if message.text.lower() in {"да", "нет"}:
        if message.text.lower() == "да":
            async with state.proxy() as data:
                user_id = data['user_id']
                try:
                    db_manager.remove_from_blacklist(user_id=user_id)
                    await cache.update_data(
                        user=user_id,
                        data={'black_list': False}
                    )
                    await message.answer('Пользователь разбанен')
                except Exception as e:
                    logging.error(e)
                    await message.answer('Произошла ошибка')
        else:
            await message.answer('Операция отменена.')
        await state.finish()
    else:
        await message.reply(
            'Вы действительно хотите разблокировать пользователя? (да/нет)'
        )
