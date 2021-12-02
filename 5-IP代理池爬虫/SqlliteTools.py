import sqlite3


def getConn():
    conn = sqlite3.connect('ProxyPool.db')


def createTable():
    conn = getConn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS proxy_pool(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        protocol TEXT NOT NULL,
        ip TEXT NOT NULL,
        port TEXT NOT NULL,
        check_times INTEGER
    )
    """)
    conn.commit()
    conn.close()


def insert_data():
    conn = getConn()
    c = conn.cursor()
    c.execute("insert into proxy_pool(protocol, ip, port, check_times) values('HTTP', '192.168.1.123', '5000', 2)")
    conn.commit()
    conn.close()


def select_data():
    conn = getConn()
    c = conn.cursor()
    c.execute("select * from proxy_pool")
    data = c.fetchall()
    conn.close()