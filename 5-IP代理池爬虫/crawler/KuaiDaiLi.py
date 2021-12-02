#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import re
import time
import requests


def spider():
    for i in range(1, 10):
        url = init_urls.format(page=i)
        do_crawl(url)
        time.sleep(random.randint(1, 5))


def do_crawl(url):
    response = requests.get(url, headers=header)
    parse_data(response.text)


def parse_data(html):
    lines = re.findall(r"<tr>(.*?)</tr>", html, re.M | re.I | re.S)
    if lines is None:
        return
    for line in lines:
        try:
            ip = re.findall(r"<td data-title=\"IP\">(.*?)</td>", line, re.S)
            port = re.findall(r"<td data-title=\"PORT\">(.*?)</td>", line, re.S)
            if not ip or not port:
                continue
            ip_port = ip[0] + ":" + port[0]
            proxies = {"http": "http://{}".format(ip_port), "https": "https://{}".format(ip_port)}
            try:
                requests.get("http://www.baidu.com", proxies=proxies, timeout=1)
                # ip_port_list.append(ip_port)
                print("{:>10s} {:>12s} \033[32m[测试成功]\033[0m".format("[{}]".format(site_name), ip_port))
            except Exception:
                print("{:>10s} {:>12s} \033[31m[测试失败]\033[0m".format("[{}]".format(site_name), ip_port))
        except Exception as e:
            print("爬取出错")
            continue


site_name = "快代理"
init_urls = "https://www.kuaidaili.com/free/inha/{page}/"
header = {
    "Host": "www.kuaidaili.com",
    "Referer": "https://www.kuaidaili.com/free/",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
}