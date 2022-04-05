import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_gbq
import seaborn as sns

from config import PROJECT, credentials


def get_salary_period(today):
    """
    Формирует строку зарплатного периода

    :param today: день для определения зарплатного периода
    :type today: datetime.date

    """

    DAY_OF_WEEK = {
        1: "Январь",
        2: "Февраль",
        3: "Март",
        4: "Апрель",
        5: "Май",
        6: "Июнь",
        7: "Июлю",
        8: "Август",
        9: "Сентябрь",
        10: "Октябрь",
        11: "Ноябрь",
        12: "Декабрь",
    }

    day = today.day
    month = today.month
    year = today.strftime("%y")

    if day < 6 or day > 20:
        salary_period = f"Аванс-{DAY_OF_WEEK[month]}{year}"
        return salary_period
    else:
        salary_period = f"ЗП-" \
                        f"{DAY_OF_WEEK[month - 1 if month - 1 != 0 else 12]}" \
                        f"{year}"
        return salary_period


def get_dataframe_for_graph(user_id, date):
    """
    Формирует Dataframe через запрос к БД

     :param user_id: id пользователя
     :type user_id: int

     :param date: дата составления графика
     :type date: datetime.date

    """

    salary_period = get_salary_period(date)
    sql_group_project = (
        f"SELECT  trackdate, projectName, SUM(timefact) AS time FROM "
        f"TG_Bot_Stager.salaryDetailsByTrackdate  "
        f"WHERE  telegram_id = {user_id} and salaryPeriod = "
        f"'{salary_period}' OR notApprovedSalaryPeriod  = '{salary_period}'"
        f" GROUP BY telegram_id, "
        f"trackdate, projectName order by trackdate "
    )
    df = pandas_gbq.read_gbq(
        sql_group_project, project_id=PROJECT, credentials=credentials
    )

    return df


def get_xlabel_for_graph(df):
    """
    Формирует Dataframe дат и возвращает столбец дата(день недели)

     :param df: Dataframe из БД
     :type df: pandas.core.frame.DataFrame


    """

    DAY_OF_WEEK = {
        0: "ПН", 1: "ВТ", 2: "СР", 3: "ЧТ", 4: "ПТ", 5: "СБ", 6: "ВС"
    }

    set_date = set(df["trackdate"])
    df_xlabel = pd.DataFrame(
        {"trackdate": pd.date_range(start=min(set_date), end=max(set_date))}
    )
    df_xlabel["dayOfWeek"] = pd.to_datetime(
        df_xlabel["trackdate"]
    ).dt.dayofweek.map(
        DAY_OF_WEEK
    )
    df_xlabel["xticklabels"] = (
            df_xlabel["trackdate"].astype(str) +
            "(" + df_xlabel.dayOfWeek + ")"
    )

    return df_xlabel.xticklabels


def get_image(df, xlabel):
    """
    Формирует и сохраняет картинку с графиком

            :param df: Dataframe из БД
            :type df: pandas.core.frame.DataFrame
            :param xlabel: набор данных для подписи тиков по оси Х
            :type xlabel: pandas.core.series.Series

    """

    fig = plt.figure(figsize=(16, 8))
    g = sns.histplot(
        df,
        x="trackdate",
        weights="time",
        hue="projectName",
        multiple="stack",
        shrink=0.8,
    )

    # Установка тиков по оси X
    mids = [rect.get_x() + rect.get_width() / 2 for rect in g.patches]
    g.set_xticks(list(set(mids)))
    g.set_xticklabels(xlabel.tolist())

    # Установка тиков по оси Y
    max_hour = max(df.groupby(["trackdate"])["time"].sum())
    g.set_yticks(np.arange(0, max_hour + 1, 1))

    # Добавление подписи по осям
    g.set_xlabel("Дни")
    g.set_ylabel("Часы")

    # Поворот тиков на оси Х
    fig.autofmt_xdate()

    # Сохранение в файл
    plt.savefig("saved_graph.png")
