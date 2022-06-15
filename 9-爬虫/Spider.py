import re
import time
import requests
from bs4 import BeautifulSoup
import EmailUtils
from playwright.sync_api import sync_playwright

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
}

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'


def get_data_list():
    url = "https://www.hermes.cn/cn/zh/category/%E5%A5%B3%E5%A3%AB/%E7%AE%B1%E5%8C%85%E5%B0%8F%E7%9A%AE%E5%85%B7/%E7" \
          "%AE%B1%E5%8C%85%E6%99%9A%E5%AE%B4%E5%8C%85/#|"
    list = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        browser.new_context(java_script_enabled=True, user_agent=user_agent)
        page = browser.new_page()
        page.goto(url)
        page_content = page.content()
        soup = BeautifulSoup(page_content, 'lxml')
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
        browser.close()
    return list



def get_data_detail(data_list):
    header['referer'] = 'https://www.hermes.cn/cn/zh/story/291557-watches-women/'
    with sync_playwright() as p:
        browser = p.chromium.launch()
        browser.new_context(java_script_enabled=True, user_agent=user_agent)
        for data in data_list:
            is_next = True
            while is_next:
                try:
                    page = browser.new_page()
                    page_path = data['detail_page']
                    page.goto(page_path)
                    page_content = page.content()
                    soup = BeautifulSoup(page_content)
                    button = soup.find('button', {"name": "add-to-cart"})
                    is_disabled = button.has_attr('disabled')
                    data['is_disabled'] = is_disabled
                    is_next = False
                except:
                    print("request error")
                    time.sleep(3)
            time.sleep(3)
        browser.close()
    return data_list


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
    with open('data.txt', 'r') as file:
        lines = file.read().splitlines()
    return lines


def write_lines(item_list):
    with open("data.txt", 'w') as file:
        file.write("\n".join(item_list))


data_list = get_data_list()
new_list = get_new_items(data_list)
dass = get_data_detail(data_list)
print(dass)
EmailUtils.send_mail("731371050@qq.com", "爱马仕商品上新监控", "\n".join(new_list))

print(new_list)
