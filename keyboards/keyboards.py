from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

FWD_STR = "➡️️"
BCK_STR = "⬅️"
UP_STR = "Назад ↩️"
FIN_STR = "Финансы"
ORG_STR = "Организация"
OTH_STR = "Прочее"
TECH_STR = "Тех часть"
ACC_STR = "Бухгалтерия"
FIN_Q1_STR = "В какие числа учитываются треки авансового периода?"
FIN_Q2_STR = "В какие числа учитываются треки зарплатного периода?"
FIN_Q4_STR = "Когда ждать аванс?"
FIN_Q3_STR = "Когда ждать зарплату?"
FIN_Q5_STR = "Неверная информация в отчёте Data Studio"
ORG_Q1_STR = "Хочу оформить отпуск"
OTH_Q1_STR = "У меня простои, я хочу получить задачи на обучение"
TECH_Q1_STR = "Хочу получить надбавку"
TECH_Q2_STR = "Хочу проходить курсы"
TECH_Q3_STR = "Есть ли у нас система грейдов?"
ACC_Q1_STR = "Мне нужна справка 2НДФЛ"
ACC_Q2_STR = "Когда придут отпускные?"


fwd = KeyboardButton(FWD_STR)
bck = KeyboardButton(BCK_STR)
up = KeyboardButton(UP_STR)
fin = KeyboardButton(FIN_STR)
fin1 = KeyboardButton(FIN_Q1_STR)
fin2 = KeyboardButton(FIN_Q2_STR)
fin3 = KeyboardButton(FIN_Q3_STR)
fin4 = KeyboardButton(FIN_Q4_STR)
fin6 = KeyboardButton(FIN_Q5_STR)
org = KeyboardButton(ORG_STR)
org1 = KeyboardButton(ORG_Q1_STR)
oth = KeyboardButton(OTH_STR)
oth1 = KeyboardButton(OTH_Q1_STR)
tech = KeyboardButton(TECH_STR)
tech1 = KeyboardButton(TECH_Q1_STR)
tech2 = KeyboardButton(TECH_Q2_STR)
tech3 = KeyboardButton(TECH_Q3_STR)
acc = KeyboardButton(ACC_STR)
acc1 = KeyboardButton(ACC_Q1_STR)
acc2 = KeyboardButton(ACC_Q2_STR)

KEYBOARDS = {
    "start": ReplyKeyboardMarkup(row_width=2).add(fin, org, acc, tech, oth),
    "fin_first": ReplyKeyboardMarkup([[fin1], [fin2], [bck, fwd]]),
    "fin_second": ReplyKeyboardMarkup([[fin3], [fin4], [bck, fwd]]),
    "fin_third": ReplyKeyboardMarkup([[fin6], [bck, up]]),
    "org": ReplyKeyboardMarkup([[org1], [bck]]),
    "oth": ReplyKeyboardMarkup([[oth1], [bck]]),
    "tech_first": ReplyKeyboardMarkup([[tech1], [tech2], [bck, fwd]]),
    "tech_second": ReplyKeyboardMarkup([[tech3], [bck, up]]),
    "acc": ReplyKeyboardMarkup([[acc1], [acc2], [bck]]),
}
