import time
import datetime
import requests

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

start_time = int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d")))
end_time = int(time.mktime(time.strptime(str(today), "%Y-%m-%d"))) - 1

page = 1
break_tag = False

url = "https://papi.jiemian.com/page/api/kuaixun/getlistmore"

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

while True:
    url = "https://papi.jiemian.com/page/api/kuaixun/getlistmore?cid=1325kb&start_time=%s&page=%s&tagid=1325" % (int(time.time()), page)
    print(url)
    res = requests.get(url, headers=header).json()
    new_list = res['result']['list']
    print(new_list)
    for new_item in new_list:
        publishtime = int(new_item['publishtime'])
        if start_time <= publishtime <= end_time:
            publish_str = time.strftime("%H:%M", time.localtime(publishtime))
            print(publish_str, new_item['title'])
        if publishtime < start_time:
            break_tag = True
    if break_tag:
        break
    else:
        page += 1
    time.sleep(3)
