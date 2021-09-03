import setting
import bill_flow_dao
import common


def get_saving_list():
    saving = setting.init_funds
    date_list = common.date_range("2021-08", "2022-09")
    for date in date_list:
        year, month = common.split_date(date)
        bill_list = bill_flow_dao.select_by_month(year, month)
        for bill in bill_list:
            if bill['type'] == 0:
                saving += bill['money']
            elif bill['type'] == 1:
                saving -= bill['money']
        print(date, saving)


get_saving_list()