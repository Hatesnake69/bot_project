from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from filters import UserRoleFilter
from loader import bot, db_manager, dp
from states import AdminMessageStates
from utils import get_logger

logger = get_logger(__name__)


@dp.message_handler(
    UserRoleFilter(role='admin'),
    commands=["admin_message"],
    state="*"
)
async def admin_message_start(message: Message) -> None:
    """
    Перехватывает команду "/ban_user"

    :param message: объект Message
    :type message : Message

    :return: None
    :rtype: NoneType
    """

    await AdminMessageStates.admin_message_text.set()
    await message.reply("Введите сообщение для всех пользователей")


@dp.message_handler(state=AdminMessageStates.admin_message_text)
async def admin_message_text(message: Message, state: FSMContext) -> None:
    """
    Пишет текст сообщения для всех пользователей в proxy

    :param message: объект Message
    :type message : Message
    :param state: FSMContext
    :type state : объект FSMContext

    :return: None
    :rtype: NoneType
    """

    async with state.proxy() as data:
        data['message_text'] = message.text
    await AdminMessageStates.next()
    await message.reply(
        "Подтвердите, вы точно хотите отправить это "
        "сообщение остальным пользователям? (да/нет)"
    )


@dp.message_handler(state=AdminMessageStates.admin_message_confirm)
async def admin_message_fin(message: Message, state: FSMContext) -> None:
    """
    Подтверждение, завершение работы

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
                text = data['message_text']
            result = db_manager.get_user_id_list()
            if not result:
                await message.answer('Произошла ошибка')
            for row in result:
                try:
                    await bot.send_message(chat_id=row[0], text=text)
                except Exception as e:
                    logger.error(e)
        else:
            await message.answer('Операция отменена.')
        await state.finish()
    else:
        await message.reply(
            "Подтвердите, вы точно хотите отправить это "
            "сообщение остальным пользователям? (да/нет)"
        )
