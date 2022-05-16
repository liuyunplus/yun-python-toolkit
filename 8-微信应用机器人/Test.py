import requests
import pymongo
from pymongo.server_api import ServerApi
import time

client = pymongo.MongoClient(
    "mongodb+srv://liuyun:aA201314@cluster0.krzhy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
    server_api=ServerApi('1'))
# 选择数据库
db = client["db0"]
# 选择集合
col = db["news"]


def getNews():
    header = {
        "Host": "papi.jiemian.com",
        "Referer": "https://www.jiemian.com/",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    }
    url = "https://papi.jiemian.com/page/api/kuaixun/getlistmore?cid=1325kb&start_time=%s&page=1&tagid=1325" % int(
        time.time())
    response = requests.get(url, headers=header).json()
    new_list = response['result']['list']
    for new_item in new_list:
        print(new_item)
        col.insert_one(new_item)


def getTimeStamp(time_str):
    timeStamp = int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S")))
    return timeStamp


s = getTimeStamp("2022-05-16 15:00:00")
print(s)

query = {
    "publishtime": {
        "$gt": getTimeStamp("2022-05-16 18:30:00"),
        "$lt": getTimeStamp("2022-05-16 15:00:00")
    }
}

rets = col.find(query).sort('publishtime', pymongo.DESCENDING)
for ret in rets:
    print(ret)
