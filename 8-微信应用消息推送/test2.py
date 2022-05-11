import time
import datetime
import requests
import json

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d")))
yesterday_end_time = int(time.mktime(time.strptime(str(today), "%Y-%m-%d"))) - 1

url = "https://papi.jiemian.com/page/api/kuaixun/getlistmore"
params = {
    "cid": "1325kb",
    "start_time": "1652198399",
    "page": "1",
    "tagid": "1325"
}
res = requests.get(url, params=params).json()
list = res['result']['list']

for item in list:
    publishtime = int(item['publishtime'])
    timeArray = time.localtime(publishtime)
    otherStyleTime = time.strftime("%H:%M", timeArray)
    print(otherStyleTime, item['title'])