from datetime import datetime
import requests


def is_day_off(date: datetime.date) -> bool:
    """
    Возвращает True, если выходной день

    :param date: проверяемая дата
    :type date: datetime.date

    :rtype: bool
    """

    year, month, day = date.year, date.month, date.day
    link = f'https://isdayoff.ru/api/getdata?year={year}\
           &month={month}&day={day}'
    response = requests.get(link)
    return True if response.ok and response.text != '0' else False
