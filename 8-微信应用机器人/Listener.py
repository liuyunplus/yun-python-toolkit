import sys
sys.path.append("/opt/files/")
import wx_sdk.WXBizMsgCrypt3 as WXBizMsgCrypt
import xml.etree.cElementTree as ET
import requests
import json


token = "2OwU9Hw6aS"
encodingAESKey = "UhTmTvko505znCn2Jndob3wb73yc3rnNFvvZqoxXfSK"
corpId = "wwd5e52a75bfc03886"
wxcpt = WXBizMsgCrypt(token, encodingAESKey, corpId)
params = {}
data = {}


def verifyURL(params):
    sVerifyMsgSig = params['msg_signature']
    sVerifyTimeStamp = params['timestamp']
    sVerifyNonce = params['nonce']
    sVerifyEchoStr = params['echostr']
    ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
    return sEchoStr


def getXmlTree(params, data):
    sReqData = data
    sReqMsgSig = params['msg_signature']
    sReqTimeStamp = params['timestamp']
    sReqNonce = params['nonce']
    ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
    print(ret, sMsg)
    xml_tree = ET.fromstring(sMsg)
    return xml_tree


def getRespEncryptMsg(xmlTree, params, sMsg):
    fromUser = xmlTree.find("FromUserName").text
    sReqTimeStamp = params['timestamp']
    sReqNonce = params['nonce']
    sRespData = """
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[wwd5e52a75bfc03886]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <MsgId>%s</MsgId>
    <Content><![CDATA[%s]]></Content>
    <AgentID>1000002</AgentID>
    </xml>""" % (fromUser, sReqTimeStamp, sReqNonce, sMsg)
    print(sRespData)
    ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)
    print(sEncryptMsg)
    return sEncryptMsg


def getTuringResp(inputText):
    params = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": inputText
            }
        },
        "userInfo": {
            "apiKey": "ebaefc6cfa3a4d5cb38e3442bed15900",
            "userId": "444056"
        }
    }
    resp = requests.post("http://openapi.turingapi.com/openapi/api/v2", json=params)
    data = json.loads(resp.text)
    text = data["results"][0]["values"]["text"]
    return text


def getRespMsg(content):
    if content == "刘运":
        respMsg = "他很爱宋甜"
    elif content == "宋甜":
        respMsg = "她是刘运的小可爱^_^"
    elif content == "宋甜是谁":
        respMsg = "她是刘运的小可爱^_^"
    elif content == "宋甜是谁?":
        respMsg = "她是刘运的小可爱^_^"
    else:
        respMsg = getTuringResp(content)
    return respMsg


# 解析消息
xmlTree = getXmlTree(params, data)
content = xmlTree.find("Content").text

# 回复消息
respMsg = getRespMsg(content)
respEncryptMsg = getRespEncryptMsg(xmlTree, params, respMsg)