import datetime
from dateutil.relativedelta import relativedelta


def split_date(date):
    item_list = []
    for item in date.split("-"):
        item_list.append(int(item))
    return tuple(item_list)


def get_dict_data(data, key):
    if key in data:
        return data[key]
    return None


def date_range(begin_date, end_date):
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m")
    date = begin_date
    date_list = []
    while date <= end_date:
        date_list.append(datetime.datetime.strftime(date, "%Y-%m"))
        date += relativedelta(months=1)
    return date_list