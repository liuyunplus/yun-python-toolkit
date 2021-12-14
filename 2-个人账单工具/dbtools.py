import sqlite3


def get_conn():
    conn = sqlite3.connect('data.db')
    return conn


def get_warp_data(cursor):
    """ 获取包装好的对象 """
    line_list = cursor.fetchall()
    if not line_list:
        return []

    def get_field_map(cursor):
        """ 获取字段名下标映射 """
        field_map = {}
        index = 0
        for desc in cursor.description:
            field_map[index] = desc[0]
            index = index + 1
        return field_map

    field_map = get_field_map(cursor)
    data_list = []
    for line in line_list:
        data = {}
        for index, value in enumerate(line):
            field_name = field_map[index]
            data[field_name] = value
        data_list.append(data)
    return data_list

