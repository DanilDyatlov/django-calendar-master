import sqlite3
import datetime


def get_events():
    now = datetime.datetime.now()
    connection = sqlite3.connect("../db.sqlite3")
    cursor = connection.cursor()

    ok_date = []

    # Получили все записи из таблицы
    cursor.execute('SELECT start_time FROM cal_event')
    d = cursor.fetchall()
    for i in d:
        i_str = str(i)
        i_str = i_str.replace("(", "")
        i_str = i_str.replace("'", "")
        i_str = i_str.replace(",", "")
        i_str = i_str.replace(")", "")
        i_str = i_str[:i_str.index(" ")]
        time = datetime.datetime.strptime(i_str, "%Y-%m-%d")
        if time.year == now.year and time.month == now.month and time.day == now.day:
            ok_date.append(i)

    res = []
    for i in ok_date:
        cursor.execute('SELECT description FROM cal_event WHERE start_time = ?', (i))
        cu = cursor.fetchall()
        for c in cu:
            res.append(c)

    connection.close()
    return res


def get_by_day(now: datetime):
    connection = sqlite3.connect("../db.sqlite3")
    cursor = connection.cursor()

    ok_date = []

    # Получили все записи из таблицы
    cursor.execute('SELECT start_time FROM cal_event')
    d = cursor.fetchall()
    for i in d:
        i_str = str(i)
        i_str = i_str.replace("(", "")
        i_str = i_str.replace("'", "")
        i_str = i_str.replace(",", "")
        i_str = i_str.replace(")", "")
        i_str = i_str[:i_str.index(" ")]
        time = datetime.datetime.strptime(i_str, "%Y-%m-%d")
        if time.year == now.year and time.month == now.month and time.day == now.day:
            ok_date.append(i)

    for i in ok_date:
        cursor.execute('SELECT description FROM cal_event WHERE start_time = ?', (i))

    res = cursor.fetchall()
    connection.close()
    return res