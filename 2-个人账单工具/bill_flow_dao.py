import dbtools
import common


def createTable():
    conn = dbtools.get_conn()
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
    conn = dbtools.get_conn()
    cursor = conn.cursor()
    year, month, day = common.split_date(data['date'])
    notes = common.get_dict_data(data, 'notes')
    sql = "insert into bill_flow (year, month, day, type, money, notes) values (?,?,?,?,?,?)"
    var = (year, month, day, data['type'], data['money'], notes)
    cursor.execute(sql, var)
    conn.commit()
    conn.close()


def select_by_month(year, month):
    conn = dbtools.get_conn()
    cursor = conn.cursor()
    sql = "select * from bill_flow where year = ? and month = ?"
    var = (year, month)
    cursor.execute(sql, var)
    data = dbtools.get_warp_data(cursor)
    conn.commit()
    conn.close()
    return data