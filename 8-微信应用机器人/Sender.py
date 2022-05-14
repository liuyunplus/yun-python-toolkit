import time
import requests


def getAccessToken():
    params = {
        # 企业ID
        "corpid": "wwd5e52a75bfc03886",
        # 企业应用密钥
        "corpsecret": "z2Mf85JF8xGFMNriDcT7Ac8X2Pz8H5W4Xx9KT3tI41A"
    }
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    res = requests.get(url, params=params).json()
    return res['access_token']


def sendTextMsg(access_token, message):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
    data = {
        "touser": "@all",
        "msgtype": "text",
        "agentid": "1000002",
        "text": {
            "content": message
        }
    }
    res = requests.post(url, json=data).json()
    print(res)


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
    url = "https://papi.jiemian.com/page/api/kuaixun/getlistmore?cid=1325kb&start_time=%s&page=1&tagid=1325" % int(time.time())
    response = requests.get(url, headers=header).json()
    new_list = response['result']['list']
    context = "【早知天下事】\n"
    title_no = 1
    for new_item in new_list:
        context += str(title_no) + "、" + new_item['title'] + "\n"
        title_no += 1
    return context


accessToken = getAccessToken()
sendTextMsg(accessToken, getNews())
