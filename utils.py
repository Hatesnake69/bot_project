import requests
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt


def is_day_off(date: datetime.date) -> bool:
    """
    Возвращает True, если выходной день

    :param date: проверяемая дата
    :type date: datetime.date

    :rtype: bool
    """

    year, month, day = date.year, date.month, date.day
    response = requests.get(f'https://isdayoff.ru/api/getdata?year={year}&month={month}&day={day}')
    return True if response.ok and response.text != '0' else False


def get_image(day, hour):
    sns.barplot(x=day, y=hour)
    plt.savefig('saved_graph.png')
