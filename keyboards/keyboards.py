import enum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class FaqKeyboard(str, enum.Enum):
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
    FIN_Q5_STR = "Неверная инфо в отчёте Data Studio"
    ORG_Q1_STR = "Хочу оформить отпуск"
    OTH_Q1_STR = "Простои, хочу задачи на обучение"
    TECH_Q1_STR = "Хочу получить надбавку"
    TECH_Q2_STR = "Хочу проходить курсы"
    TECH_Q3_STR = "Есть ли у нас система грейдов?"
    ACC_Q1_STR = "Мне нужна справка 2НДФЛ"
    ACC_Q2_STR = "Когда придут отпускные?"


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
org1 = InlineKeyboardButton(text=FaqKeyboard.ORG_Q1_STR,
                            callback_data=FaqKeyboard.ORG_Q1_STR)
fin1 = InlineKeyboardButton(text=FaqKeyboard.FIN_Q1_STR,
                            callback_data=FaqKeyboard.FIN_Q1_STR)
fin2 = InlineKeyboardButton(text=FaqKeyboard.FIN_Q2_STR,
                            callback_data=FaqKeyboard.FIN_Q2_STR)
fin3 = InlineKeyboardButton(text=FaqKeyboard.FIN_Q3_STR,
                            callback_data=FaqKeyboard.FIN_Q3_STR)
fin4 = InlineKeyboardButton(text=FaqKeyboard.FIN_Q4_STR,
                            callback_data=FaqKeyboard.FIN_Q4_STR)
fin6 = InlineKeyboardButton(text=FaqKeyboard.FIN_Q5_STR,
                            callback_data=FaqKeyboard.FIN_Q5_STR)
oth1 = InlineKeyboardButton(text=FaqKeyboard.OTH_Q1_STR,
                            callback_data=FaqKeyboard.OTH_Q1_STR)
tech1 = InlineKeyboardButton(text=FaqKeyboard.TECH_Q1_STR,
                             callback_data=FaqKeyboard.TECH_Q1_STR)
tech2 = InlineKeyboardButton(text=FaqKeyboard.TECH_Q2_STR,
                             callback_data=FaqKeyboard.TECH_Q2_STR)
tech3 = InlineKeyboardButton(text=FaqKeyboard.TECH_Q3_STR,
                             callback_data=FaqKeyboard.TECH_Q3_STR)
acc1 = InlineKeyboardButton(text=FaqKeyboard.ACC_Q1_STR,
                            callback_data=FaqKeyboard.ACC_Q1_STR)
acc2 = InlineKeyboardButton(text=FaqKeyboard.ACC_Q2_STR,
                            callback_data=FaqKeyboard.ACC_Q2_STR)

category_kb = InlineKeyboardMarkup(row_width=1).add(fin, org, acc, tech, oth)
fin_keyboard = InlineKeyboardMarkup(row_width=1).add(fin1, fin2,
                                                     fin3, fin4, fin6, bck)
org_keyboard = InlineKeyboardMarkup(row_width=1).add(org1, bck)
oth_keyboard = InlineKeyboardMarkup(row_width=1).add(oth1, bck)
acc_keyboard = InlineKeyboardMarkup(row_width=1).add(acc1, acc2, bck)
tech_keyboard = InlineKeyboardMarkup(row_width=1).add(tech1, tech2, tech3, bck)
