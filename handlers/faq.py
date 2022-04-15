from aiogram.types import CallbackQuery, Message
from google.oauth2 import service_account

import keyboards as key
from data import CREDENTIALS_PATH
from filters import IsRegistered
from loader import bot, dp

credentials = service_account.Credentials. \
    from_service_account_file(CREDENTIALS_PATH)


async def send_keyboard(call, keyboard):
    """
    Удаляет прежнее сообщение и выводит выбранное меню вопросов
    :param call: объект CallbackQuery
    :param keyboard: выбранное меню
    """

    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)
    await call.message.answer("Выберите вопрос: ",
                              reply_markup=keyboard)


@dp.message_handler(
    IsRegistered(),
    commands=['faq'])
async def start_category(message: Message):
    """
    Выводит стартовое меню FAQ
    :param message: сообщение
    """
    await message.answer(text="Выберите раздел: ",
                         reply_markup=key.category_kb)


@dp.callback_query_handler(text=key.FaqKeyboard.FIN_STR.value)
async def fin_questions(call: CallbackQuery):
    """
    Выводит меню вопросов категории Финансы
    :param call: объект CallbackQuery
    """

    await send_keyboard(call, key.fin_keyboard)


@dp.callback_query_handler(text=key.FaqKeyboard.ORG_STR.value)
async def org_questions(call: CallbackQuery):
    """
    Выводит меню вопросов категории Организация
    :param call: объект CallbackQuery
    """

    await send_keyboard(call, key.org_keyboard)


@dp.callback_query_handler(text=key.FaqKeyboard.OT_STR.value)
async def oth_questions(call: CallbackQuery):
    """
    Выводит меню вопросов категории Прочее
    :param call: объект CallbackQuery
    """

    await send_keyboard(call, key.oth_keyboard)


@dp.callback_query_handler(text=key.FaqKeyboard.ACC_STR.value)
async def acc_questions(call: CallbackQuery):
    """
    Выводит меню вопросов категории Бухгалтерия
    :param call: объект CallbackQuery
    """

    await send_keyboard(call, key.acc_keyboard)


@dp.callback_query_handler(text=key.FaqKeyboard.TECH_STR.value)
async def tech_questions(call: CallbackQuery):
    """
    Выводит меню вопросов категории Тех часть
    :param call: объект CallbackQuery
    """

    await send_keyboard(call, key.tech_keyboard)


@dp.callback_query_handler(text=key.FaqKeyboard.BCK_STR.value)
async def bck_to_category(call: CallbackQuery):
    """
    Выводит стартовое меню категорий
    :param call: объект CallbackQuery
    """

    await send_keyboard(call, key.category_kb)
