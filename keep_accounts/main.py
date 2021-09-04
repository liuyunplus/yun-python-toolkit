import setting
import bill_flow_dao
import common


def init_data():
    bill_flow_dao.createTable()
    for bill in setting.bill_list:
        bill_flow_dao.insert_data(bill)


def get_saving_list():
    saving = setting.init_funds
    date_list = common.date_range("2021-09", "2022-07")
    for date in date_list:
        year, month = common.split_date(date)
        bill_list = bill_flow_dao.select_by_month(year, month)
        for bill in bill_list:
            if bill['type'] == 0:
                saving += bill['money']
            elif bill['type'] == 1:
                saving -= bill['money']
        print(date, saving)


# init_data()
get_saving_list()