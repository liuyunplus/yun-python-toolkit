from smtplib import SMTP_SSL
from email.mime.text import MIMEText


def send_mail(receivers, subject, message):
    # 填写真实的发邮件服务器用户名、密码
    user = '1161305061@qq.com'
    password = 'bwlanuavdmbijjff'
    # 邮件内容
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = subject
    with SMTP_SSL(host="smtp.qq.com", port=465) as smtp:
        # 登录发邮件服务器
        smtp.login(user=user, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=user, to_addrs=receivers.split(','), msg=msg.as_string())


def get_conn_host(email):
    ss = email.split('@')[1]
    if ss == '':
        return ()