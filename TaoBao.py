import re
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from multiprocessing import Pool
from lxml import etree
from requests import RequestException


class Tao_bao:
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 设置option
        # driver = webdriver.Chrome(chrome_options=option)  # 调用带参数的谷歌浏览器
        # service_args = [
        #     '--disk-cache=true',
        #     '--load-images=false',
        # ]
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        # browser = webdriver.PhantomJS(service_args=service_args)
        # browser = webdriver.Chrome()
        browser = webdriver.Chrome(chrome_options=option)
        url = 'https://www.taobao.com/?spm=a2e15.8261149.1581860521.1.302d29b4z6guXp'
        key = '美食'
        self.key = key
        self.url = url
        # self.browser = browser.set_window_size(1400, 900)
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)
        self.header = header
        self.n = 0

    def search(self):
        """
        start this program and go to function of name is recycle the get_content function to crawl this information
        :return:
        """
        try:
            self.browser.get(self.url)
            input_content = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
            )
            submit = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
            )
            now_handle = self.browser.current_window_handle
            input_content.send_keys(self.key)
            submit.click()
            self.browser.switch_to_window(now_handle)
            total = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
            )
            return total.text
        except TimeoutException:
            print('Wrong!')

    def start_interface(self):
        content = self.search()
        total = int(re.compile(r'(\d+)', re.S).search(content).group(1))
        for i in range(2, total + 1):
            self.next_page(i)

    def next_page(self, number):
        try:
            print("正在翻第{0}页".format(number))
            input_content = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
            )
            submit = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
            )
            input_content.clear()
            input_content.send_keys(number)
            submit.click()
            self.wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(number))
            )
            self.get_content()
        except TimeoutException:
            return self.next_page(number)

    def get_content(self):
        """
        get content and download this content
        :return:
        """
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist > div > div > div:nth-child(1)'))
        )
        # get the page of source
        html = self.browser.page_source
        content_text = etree.HTML(html)
        names = content_text.xpath('*//div[@class="pic"]/a/img/@alt')
        srcs = content_text.xpath('*//div[@class="pic"]/a/img/@data-src')
        totals = [(name, src) for (name, src) in zip(names, srcs)]
        for total in totals:
            self.download(total[1], total[0])

    def download(self, url, name):
        print('正在下载：{0},{1}'.format(('https:' + url), name))
        try:
            response = requests.get('https:' + url, headers=self.header)
            if response.status_code == 200:
                self.store(response.content, name)
        except RequestException:
            print("Response is wrong!")

    def store(self, content, name):
        try:
            part_path = r'F:\exploitation\codes\python\Spider\picture_hero'
            path = r"{0}\{1}.{2}".format(part_path, name, 'jpg')
            with open(path, 'wb') as f:
                f.write(content)
                f.close()
        except OSError:
            self.n += 1
            if self.n < 5:
                return self.store(content, name)
            else:
                print("Content is wrong!")


if __name__ == '__main__':
    taobao = Tao_bao()
    taobao.start_interface()
