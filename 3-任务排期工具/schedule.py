import datetime
import sys
from chinese_calendar import is_workday


def next_work_day(day):
    date = datetime.datetime.strptime(day, "%Y-%m-%d")
    while True:
        date = date + datetime.timedelta(days=1)
        if is_workday(date):
            break
    return date.strftime("%Y-%m-%d")


def last_work_day(day):
    date = datetime.datetime.strptime(day, "%Y-%m-%d")
    while True:
        date = date - datetime.timedelta(days=1)
        if is_workday(date):
            break
    return date.strftime("%Y-%m-%d")


class Schedule:

    def __init__(self, current_date):
        self.current_date = current_date
        self.remain_hours = 8

    def do_work(self, hours):
        start_date = self.current_date
        # 当天剩余时间减去任务时间
        self.remain_hours = self.remain_hours - hours
        while True:
            # 若当天剩余时间大于0，则返回
            if self.remain_hours > 0:
                break
            # 否则，当前日期转至下一个工作日
            self.current_date = next_work_day(self.current_date)
            # 当天剩余时间加8小时
            self.remain_hours = 8 + self.remain_hours
        # 若当前剩余时间等于8小时，则退回上一个工作日
        if self.remain_hours >= 8:
            end_date = last_work_day(self.current_date)
        else:
            end_date = self.current_date
        return start_date, end_date, self.remain_hours


if __name__ == '__main__':
    schedule = Schedule(sys.argv[2])
    print("任务工时", "开始日期", "结束日期", "当天剩余", sep=", ")
    for line in open(sys.argv[1]):
        hour = int(line)
        start_date, end_date, remain_hours = schedule.do_work(hour)
        print(hour, start_date, end_date, remain_hours, sep=", ")


