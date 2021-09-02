import datetime
import setting
import SqlliteTools
from dateutil.relativedelta import relativedelta


def initdata():
    SqlliteTools.createTable()
    for bill in setting.bill_list:
        SqlliteTools.insert_data(bill)


def date_range(begin_date, end_date):
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m")
    date = begin_date
    list = []
    while date <= end_date:
        list.append(datetime.datetime.strftime(date, "%Y-%m"))
        date += relativedelta(months=1)
    return list


def main():
    savings = setting.savings
    date_list = date_range("2021-08", "2022-09")
    for date in date_list:
        year, month = SqlliteTools.split_date(date)
        bill_list = SqlliteTools.select_by_month(year, month)
        for bill in bill_list:
            if bill['type'] == 0:
                savings += bill['money']
            elif bill['type'] == 1:
                savings -= bill['money']
        print(date, savings)


main()