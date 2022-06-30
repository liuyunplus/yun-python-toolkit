#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import requests
from bs4 import BeautifulSoup
import Config


def get_data_list():
    list = []
    url = "https://www.hermes.cn/cn/zh/category/%E5%A5%B3%E5%A3%AB/%E7%AE%B1%E5%8C%85%E5%B0%8F%E7%9A%AE%E5%85%B7/%E7" \
          "%AE%B1%E5%8C%85%E6%99%9A%E5%AE%B4%E5%8C%85/#|"
    payload = ""
    headers = {
        "cookie": "_gcl_au=1.1.680716924.1654744267; Hm_lvt_e6c348f2c9b16d8b005a379023cce3b3=1654744259,1655113152,1655263855; _gid=GA1.2.249683741.1655263855; _cs_mk=0.15408045765717504_1655278395101; ECOM_SESS=c42mf15mn722tjrsplcqcsl1t0; correlation_id=ea48435e46229a93b8f783a9ba9e0ad16d554e141e7184bd191c1865d359e295; datadome=.CuUrnY30lMAvcjIqmSBrtJK4R1gILdxrLxSk7Dpw2tQ-77sZ4wDZ6t8tIsgblWRMPM5Vpa.ERuoDp.u0Eel_qUee8pMd7XG_skOxXf1jwzI3~KXOBSIy8c6~65Tq-AH; Hm_lpvt_e6c348f2c9b16d8b005a379023cce3b3=1655281434; _ga_Y862HCHCQ7=GS1.1.1655278396.6.1.1655281435.0; _ga=GA1.1.931983995.1654744259",
        "authority": "www.hermes.cn",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-device-memory": "8",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        "sec-ch-ua-arch": 'x86',
        "sec-ch-ua-full-version-list": '" Not A;Brand";v="99.0.0.0", "Chromium";v="102.0.5005.61", "Google Chrome";v="102.0.5005.61"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    tag_list = soup.find_all('div', {"class": re.compile(r".*product-grid-list-item.*")})
    for tag in tag_list:
        data = {}
        meta = tag.find('div', {"class": "product-item-meta"})
        data['id'] = meta['id']
        link = tag.find('a', {"href": True})
        data['detail_page'] = 'https://www.hermes.cn' + link['href']
        img = tag.find('img')
        data['image_url'] = 'http:' + img['src']
        name = tag.find('h4', {"class": "product-item-name"})
        data['name'] = name.text
        price = tag.find('div', {"class": re.compile(r".*product-item-price.*")})
        price_text = price.text.replace(",", "")
        price_text = price_text.replace(" ", "")
        data['price'] = price_text
        list.append(data)
    return list


def get_new_items(data_list):
    new_list = []
    goods_ids = []
    lines = read_lines()
    for data in data_list:
        goods_ids.append(data['id'])
        if data['id'] not in lines:
            new_list.append("【" + data['name'] + "】" + data['detail_page'])
    write_lines(goods_ids)
    return new_list


def read_lines():
    with open(Config.FILE_NAME, 'r') as file:
        lines = file.read().splitlines()
    return lines


def write_lines(item_list):
    with open(Config.FILE_NAME, 'w') as file:
        file.write("\n".join(item_list))


def send_mail(receivers, new_list):
    if len(new_list) == 0:
        return
    # 填写真实的发邮件服务器用户名、密码
    user = '1161305061@qq.com'
    password = 'bwlanuavdmbijjff'
    # 邮件内容
    msg = MIMEText("\n".join(new_list), 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = "爱马仕商品上新监控"
    with SMTP_SSL(host="smtp.qq.com", port=465) as smtp:
        # 登录发邮件服务器
        smtp.login(user=user, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=user, to_addrs=receivers.split(','), msg=msg.as_string())


data_list = get_data_list()
new_list = get_new_items(data_list)
send_mail("liuyunplus@163.com", new_list)
print('执行成功')
