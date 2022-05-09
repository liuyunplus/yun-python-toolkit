import sys
sys.path.append("/opt/files/")
from WXBizMsgCrypt3 import WXBizMsgCrypt
import xml.etree.cElementTree as ET

wxcpt = WXBizMsgCrypt('2OwU9Hw6aS', 'UhTmTvko505znCn2Jndob3wb73yc3rnNFvvZqoxXfSK', 'wwd5e52a75bfc03886')
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


# 解析消息
xmlTree = getXmlTree(params, data)
content = xmlTree.find("Content").text

# 回复消息
if content == "刘运":
    respMsg = "他很爱宋甜"
else:
    respMsg = "我收到消息啦"
respEncryptMsg = getRespEncryptMsg(xmlTree, params, respMsg)
