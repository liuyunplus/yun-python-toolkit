import sqlite3


def getConn():
    conn = sqlite3.connect('database.db')
    return conn


def createTable():
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bill_flow(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL,
        type INTEGER NOT NULL,
        money INTEGER NOT NULL,
        notes TEXT
    )
    """)
    conn.commit()
    conn.close()


def insert_data(data):
    conn = getConn()
    cursor = conn.cursor()
    year, month, day = split_date(data['date'])
    notes = None
    if 'notes' in data:
        notes = data['notes']
    sql = "insert into bill_flow (year, month, day, type, money, notes) values (?,?,?,?,?,?)"
    var = (year, month, day, data['type'], data['money'], notes)
    cursor.execute(sql, var)
    conn.commit()
    conn.close()


def select_by_month(year, month):
    conn = getConn()
    cursor = conn.cursor()
    sql = "select * from bill_flow where year = ? and month = ?"
    var = (year, month)
    cursor.execute(sql, var)
    line_list = cursor.fetchall()
    conn.commit()
    conn.close()
    if not line_list:
        return []
    data_list = []
    for line in line_list:
        data = {
            "year": line[1],
            "month": line[2],
            "day": line[3],
            "type": line[4],
            "money": line[5],
            "notes": line[6],
        }
        data_list.append(data)
    return data_list


def split_date(date):
    list = date.split("-")
    if len(list) == 2:
        return int(list[0]), int(list[1])
    elif len(list) == 3:
        return int(list[0]), int(list[1]), int(list[2])

