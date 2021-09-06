import setting
import bill_flow_dao
import common


def init_data():
    bill_flow_dao.createTable()
    for bill in setting.bill_list:
        bill_flow_dao.insert_data(bill)


def get_saving_list():
    saving = setting.init_funds
    date_list = common.date_range(setting.start_month, setting.end_month)
    for date in date_list:
        year, month = common.split_date(date)
        bill_list = bill_flow_dao.select_by_month(year, month)
        for bill in bill_list:
            if bill['type'] == 0:
                saving += bill['money']
            elif bill['type'] == 1:
                saving -= bill['money']
        print(date, saving)


def get_cost_list():
    date_list = common.date_range(setting.start_month, setting.end_month)
    for date in date_list:
        year, month = common.split_date(date)
        bill_list = bill_flow_dao.select_by_month(year, month)
        cost = 0
        for bill in bill_list:
            if bill['type'] == 0:
                continue
            cost += bill['money']
        print(date, cost)


# get_saving_list()
get_cost_list()
