from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

FWD_STR = "➡️️"
BCK_STR = "⬅️"
UP_STR = "Назад ↩️"
FIN_STR = "Финансы"
ORG_STR = "Организация"
OTH_STR = "Прочее"
TECH_STR = "Тех часть"
ACC_STR = "Бухгалтерия"

fwd = KeyboardButton(FWD_STR)
bck = KeyboardButton(BCK_STR)
up = KeyboardButton(UP_STR)
fin = KeyboardButton(FIN_STR)
fin1 = KeyboardButton("В какие числа учитываются треки авансового периода?")
fin2 = KeyboardButton("В какие числа учитываются треки зарплатного периода?")
fin3 = KeyboardButton("Когда ждать ЗП по авансовому периоду?")
fin4 = KeyboardButton("Когда ждать ЗП по зарплатному периоду?")
fin5 = KeyboardButton("Когда ждать ЗП по авансовому периоду?")
fin6 = KeyboardButton("У меня неверная информация в "
                      "дата-студию к кому обратиться?")
org = KeyboardButton(ORG_STR)
org1 = KeyboardButton("Хочу оформить отпуск, кому мне написать?")
oth = KeyboardButton(OTH_STR)
oth1 = KeyboardButton("Хочу получить задачи на обучение, к кому обратиться?")
tech = KeyboardButton(TECH_STR)
tech1 = KeyboardButton("Хочу получить надбавку")
tech2 = KeyboardButton("Хочу проходить курсы, к кому "
                       "обратиться по моему обучению?")
tech3 = KeyboardButton("Есть ли у нас система грейдов?")
acc = KeyboardButton(ACC_STR)
acc1 = KeyboardButton("Мне нужна справка 2НДФЛ, к кому обратиться?")
acc2 = KeyboardButton("Когда мне придут отпускные?")

KEYBOARDS = {
    "start": ReplyKeyboardMarkup(row_width=2).add(fin, org, acc, tech, oth),
    "fin_first": ReplyKeyboardMarkup([[fin1], [fin2], [bck, fwd]]),
    "fin_second": ReplyKeyboardMarkup([[fin3], [fin4], [bck, fwd]]),
    "fin_third": ReplyKeyboardMarkup([[fin5], [fin6], [bck, up]]),
    "org": ReplyKeyboardMarkup([[org1], [bck]]),
    "oth": ReplyKeyboardMarkup([[oth1], [bck]]),
    "tech_first": ReplyKeyboardMarkup([[tech1], [tech2], [bck, fwd]]),
    "tech_second": ReplyKeyboardMarkup([[tech3], [bck, up]]),
    "acc": ReplyKeyboardMarkup([[acc1], [acc2], [bck]]),
}
