#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import time


def spider():
    for page in range(1, 5):
        try:
            param = {
                "page": page,
                "country": "中国",
            }
            response = requests.get(url=init_url, headers=header, params=param)
            json = response.json()["data"]
            data = json["data"]
            for item in data:
                ip = item["ip"]
                port = item["port"]
                ip_port = ip + ":" + port
                proxies = {"http": "http://{}".format(ip_port), "https": "https://{}".format(ip_port)}
                try:
                    requests.get("http://www.baidu.com", proxies=proxies, timeout=1)
                    # ip_port_list.append(ip_port)
                    print("{:>10s} {:>12s} \033[32m[测试成功]\033[0m".format("[{}]".format(site_name), ip_port))
                except Exception:
                    print("{:>10s} {:>12s} \033[31m[测试失败]\033[0m".format("[{}]".format(site_name), ip_port))
            time.sleep(1, 5)
        except Exception:
            print("爬取出错")


site_name = "JiangXianLi"
init_url = "https://ip.jiangxianli.com/api/proxy_ips"
header = {
    "Host": "ip.jiangxianli.com",
    "Referer": "https://github.com/jiangxianli/ProxyIpLib",
    "Connection": "keep-alive",
    "Accept": "text/html, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
}

