import enum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db_manager


class FaqKeyboard(str, enum.Enum):
    """
    Данный класс содержит аргументы для формирования
    клавиатуры с категорией вопросов

    Args:
    FWD_STR: кнопка вперёд
    BCK_STR: кнопка назад
    UP_STR: кнопка на стартовое меню
    FIN_STR: категория Финансы
    ORG_STR: категория Организация
    OT_STR: категория Прочие
    TECH_STR: категория Тех часть
    ACC_STR: категория Бухгалтерия
    """

    FWD_STR = "➡️️"
    BCK_STR = "⬅️"
    UP_STR = "Назад ↩️"
    FIN_STR = "Финансы"
    ORG_STR = "Организация"
    OT_STR = "Прочее"
    TECH_STR = "Тех часть"
    ACC_STR = "Бухгалтерия"
    FIN_Q1_STR = "Какие треки идут в аванс?"
    FIN_Q2_STR = "Какие треки идут в зарплату?"
    FIN_Q4_STR = "Когда ждать аванс?"
    FIN_Q3_STR = "Когда ждать зарплату?"
    FIN_Q5_STR = "Неверная инфо в Data Studio"
    ORG_Q1_STR = "Хочу оформить отпуск"
    OTH_Q1_STR = "Простои, хочу задачи на обучение"
    TECH_Q1_STR = "Хочу получить надбавку"
    TECH_Q2_STR = "Хочу проходить курсы"
    TECH_Q3_STR = "Есть ли у нас система грейдов?"
    ACC_Q1_STR = "Мне нужна справка 2НДФЛ"
    ACC_Q2_STR = "Когда придут отпускные?"


def collect_keyboard(faq_category: str,
                     user_id: int,
                     bck_button: InlineKeyboardButton) \
        -> InlineKeyboardMarkup:
    """
    Функция формирует и возвращает клавиатуру из
    полученных из BQ данных, отфильтрованных по
    категории вопросов и user_id,

    :param faq_category: категория вопросов
    :type user_id: идентификатор пользователя
    :type bck_button: объект InlineKeyboardButton

    :rtype: объект InlineKeyboardMarkup
    """

    selected_kb = InlineKeyboardMarkup(row_width=1)
    filtered_questions = db_manager.get_quest_faq(faq_category, user_id)

    for question in filtered_questions:
        button = InlineKeyboardButton(text=question[0],
                                      callback_data=question[0])
        selected_kb.add(button)

    selected_kb.add(bck_button)
    return selected_kb


fwd = InlineKeyboardButton(text=FaqKeyboard.FWD_STR,
                           callback_data=FaqKeyboard.FWD_STR)
bck = InlineKeyboardButton(text=FaqKeyboard.BCK_STR,
                           callback_data=FaqKeyboard.BCK_STR)
up = InlineKeyboardButton(text=FaqKeyboard.UP_STR,
                          callback_data=FaqKeyboard.UP_STR)
fin = InlineKeyboardButton(text=FaqKeyboard.FIN_STR,
                           callback_data=FaqKeyboard.FIN_STR)
org = InlineKeyboardButton(text=FaqKeyboard.ORG_STR,
                           callback_data=FaqKeyboard.ORG_STR)
oth = InlineKeyboardButton(text=FaqKeyboard.OT_STR,
                           callback_data=FaqKeyboard.OT_STR)
tech = InlineKeyboardButton(text=FaqKeyboard.TECH_STR,
                            callback_data=FaqKeyboard.TECH_STR)
acc = InlineKeyboardButton(text=FaqKeyboard.ACC_STR,
                           callback_data=FaqKeyboard.ACC_STR)

accept = InlineKeyboardButton(text="Согласиться", callback_data='kb1')
refuse = InlineKeyboardButton(text="Отказаться", callback_data='kb0')

category_kb = InlineKeyboardMarkup(row_width=1).add(fin, org, acc, tech, oth)
up_kb = InlineKeyboardMarkup(row_width=1).add(up)
confirmed_kb = InlineKeyboardMarkup(row_width=2).add(accept, refuse)
