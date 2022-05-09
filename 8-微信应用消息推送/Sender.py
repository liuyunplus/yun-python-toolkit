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


accessToken = getAccessToken()
sendTextMsg(accessToken, "今日行情数据")
