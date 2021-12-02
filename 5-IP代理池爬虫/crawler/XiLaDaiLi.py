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
    return True


def parse_data(html):
    table = re.search(r"<table class=\"fl-table\">(.*?)</table>", html, re.M | re.I | re.S).group(1)
    tbody = re.search(r"<tbody>(.*?)</tbody>", table, re.M | re.I | re.S).group(1)
    lines = re.findall(r"<tr>(.*?)</tr>", tbody, re.M | re.I | re.S)
    if lines is None:
        return
    for line in lines:
        try:
            ip_port = re.findall(r"<td>(.*?)</td>", line, re.M | re.I | re.S)[0]
            if ip_port is None:
                continue
            proxies = {"http": "http://{}".format(ip_port), "https": "https://{}".format(ip_port)}
            try:
                requests.get("http://www.baidu.com", proxies=proxies, timeout=1)
                # ip_port_list.append(ip_port)
                print("{:>10s} {:>12s} \033[32m[测试成功]\033[0m".format("[{}]".format(site_name), ip_port))
            except Exception:
                print("{:>10s} {:>12s} \033[31m[测试失败]\033[0m".format("[{}]".format(site_name), ip_port))
        except Exception:
            print("爬取出错")
            continue


site_name = "西拉代理"
init_urls = "http://www.xiladaili.com/gaoni/{page}/"
header = {
    "Host": "www.xiladaili.com",
    "Referer": "http://www.xiladaili.com/gaoni/",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
}