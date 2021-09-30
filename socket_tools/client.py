import socket
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddress = ('ryanxin.cn', 11111)

# 连接服务器
chain = input('连接口令：')
send = ('#connectChain*' + chain).encode()
s.sendto(send, serverAddress)
message = eval(s.recvfrom(2048)[0].decode())
myPeer = message[0]
signature = str(message[1])
print('got myPeer: ', myPeer)

peerConnected = False


# 先连接myPeer，再互发消息
def sendToMyPeer():
    # 发送包含签名的连接请求
    global peerConnected
    while True:
        s.sendto(signature.encode(), myPeer)
        if peerConnected:
            break
        time.sleep(1)

    # 发送聊天信息
    while True:
        send_text = input("我方发送：")
        s.sendto(send_text.encode(), myPeer)


def recFromMyPeer():
    # 接收请求并验证签名or接收聊天信息
    global peerConnected
    while True:
        message = s.recvfrom(2048)[0].decode()
        if message == signature:
            if not peerConnected:
                print('connected successfully')
            peerConnected = True
        elif peerConnected:
            print('\r对方回复：' + message + '\n我方发送：', end='')


sen_thread = threading.Thread(target=sendToMyPeer)
rec_thread = threading.Thread(target=recFromMyPeer)

sen_thread.start()
rec_thread.start()

sen_thread.join()
rec_thread.join()
