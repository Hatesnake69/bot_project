import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data import cache
from filters import UserRoleFilter
from loader import db_manager, dp
from states import BanUserForm


@dp.message_handler(
    UserRoleFilter(role='admin'),
    commands=["ban_user"],
    state="*"
)
async def ban_user_start(message: Message) -> None:
    """
    Перехватывает команду "/ban_user"

    :param message: объект Message
    :type message : Message

    :return: None
    :rtype: NoneType
    """

    await BanUserForm.ban_user_name.set()
    await message.reply("Укажите id пользователя")


@dp.message_handler(state=BanUserForm.ban_user_name)
async def unban_user_name(message: Message, state: FSMContext) -> None:
    """
    Записывает в state.proxy id пользователя

    :param message: объект Message
    :type message : Message
    :param state: FSMContext
    :type state : объект FSMContext

    :return: None
    :rtype: NoneType
    """

    async with state.proxy() as data:
        data['user_id'] = message.text
    await message.answer(
        'Вы действительно хотите заблокировать пользователя? (да/нет)'
    )
    await BanUserForm.next()


@dp.message_handler(state=BanUserForm.ban_confirm)
async def unban_user_confirm(message: Message, state: FSMContext) -> None:
    """
    В зависимости от ответа отправляет запрос в бд

    :param message: объект Message
    :type message : Message
    :param state: FSMContext
    :type state : объект FSMContext

    :return: None
    :rtype: NoneType
    """

    if message.text.lower() in {"да", "нет"}:
        if message.text.lower() == "да":
            async with state.proxy() as data:
                user_id = data['user_id']
                try:
                    db_manager.send_to_blacklist(user_id=user_id)
                    await cache.update_data(
                        user=user_id,
                        data={'black_list': True}
                    )
                    await message.answer('Пользователь забанен')
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
