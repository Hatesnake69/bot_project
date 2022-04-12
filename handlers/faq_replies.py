from aiogram.types import Message

import keyboards as key
from loader import dp
from states import FaqStates, get_reply


@dp.message_handler(text=[key.FIN_Q1_STR], state=FaqStates.FIN_FIRST_STATE)
async def answer_fin_1(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'FIN-1'
    :param message: сообщение
    """

    await get_reply(message, 'FIN-1')


@dp.message_handler(text=[key.FIN_Q2_STR], state=FaqStates.FIN_FIRST_STATE)
async def answer_fin_2(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'FIN-2'
    :param message: сообщение
    """

    await get_reply(message, 'FIN-2')


@dp.message_handler(text=[key.FIN_Q3_STR], state=FaqStates.FIN_SECOND_STATE)
async def answer_fin_3(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'FIN-3'
    :param message: сообщение
    """

    await get_reply(message, 'FIN-3')


@dp.message_handler(text=[key.FIN_Q4_STR], state=FaqStates.FIN_SECOND_STATE)
async def answer_fin_4(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'FIN-4'
    :param message: сообщение
    """

    await get_reply(message, 'FIN-4')


@dp.message_handler(text=[key.FIN_Q5_STR], state=FaqStates.FIN_THIRD_STATE)
async def answer_fin_5(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'FIN-5'
    :param message: сообщение
    """

    await get_reply(message, 'FIN-5')


@dp.message_handler(text=[key.TECH_Q1_STR], state=FaqStates.TECH_FIRST_STATE)
async def answer_tech_1(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'TDP-1'
    :param message: сообщение
    """

    await get_reply(message, 'TDP-1')


@dp.message_handler(text=[key.TECH_Q2_STR], state=FaqStates.TECH_FIRST_STATE)
async def answer_tech_2(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'TDP-2'
    :param message: сообщение
    """

    await get_reply(message, 'TDP-2')


@dp.message_handler(text=[key.TECH_Q3_STR], state=FaqStates.TECH_SECOND_STATE)
async def answer_tech_3(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'TDP-3'
    :param message: сообщение
    """

    await get_reply(message, 'TDP-3')


@dp.message_handler(text=[key.ACC_Q1_STR], state=FaqStates.ACC_STATE)
async def answer_acc_1(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'ACC-1'
    :param message: сообщение
    """

    await get_reply(message, 'ACC-1')


@dp.message_handler(text=[key.ACC_Q2_STR], state=FaqStates.ACC_STATE)
async def answer_acc_2(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'ACC-2'
    :param message: сообщение
    """

    await get_reply(message, 'ACC-2')


@dp.message_handler(text=[key.ORG_Q1_STR], state=FaqStates.ORG_STATE)
async def answer_org_1(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'ORG-1'
    :param message: сообщение
    """

    await get_reply(message, 'ORG-1')


@dp.message_handler(text=[key.OTH_Q1_STR], state=FaqStates.OTH_STATE)
async def answer_oth_1(message: Message):
    """
    Отправляет ответ в чат пользователю по записи 'ANO-1'
    :param message: сообщение
    """

    await get_reply(message, 'ANO-1')
