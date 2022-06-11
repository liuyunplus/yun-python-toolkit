import re
import time
import requests
from bs4 import BeautifulSoup

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
}

url = "https://www.hermes.cn/cn/zh/category/%E5%A5%B3%E5%A3%AB/%E7%AE%B1%E5%8C%85%E5%B0%8F%E7%9A%AE%E5%85%B7/%E7%AE%B1%E5%8C%85%E6%99%9A%E5%AE%B4%E5%8C%85/#|"

resp = requests.get(url, headers=header)
soup = BeautifulSoup(resp.text, 'lxml')

tag_list = soup.find_all('div', {"class": re.compile(r".*product-grid-list-item.*")})

data_list = []
for tag in tag_list:
    data = {}
    meta = tag.find('div', {"class": "product-item-meta"})
    data['id'] = meta['id']
    link = tag.find('a', {"href": True})
    data['detail_url'] = 'https://www.hermes.cn' + link['href']
    img = tag.find('img')
    data['image_url'] = 'http:' + img['data-src']
    name = tag.find('h4', {"class": "product-item-name"})
    data['name'] = name.text
    price = tag.find('div', {"class": re.compile(r".*product-item-price.*")})
    price_text = price.text.replace(",", "")
    price_text = price_text.replace(" ", "")
    data['price'] = price_text
    data_list.append(data)

print(data_list)
header['referer'] = 'https://www.hermes.cn/cn/zh/story/291557-watches-women/'

for item in data_list:
    tag = True
    while tag:
        try:
            detail_url = item['detail_url']
            rs = requests.get(detail_url, headers=header)
            bs = BeautifulSoup(rs.text, 'lxml')
            bt = bs.find('button', {"name": "add-to-cart"})
            print(bt)
            is_disabled = bt.has_attr('disabled')
            item['is_disabled'] = is_disabled
            tag = False
        except:
            print("失败")
            time.sleep(3)
    time.sleep(3)

print(data_list)