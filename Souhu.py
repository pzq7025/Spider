# -*- coding:utf-8 -*-
# author:pzq
import requests
import hashlib
import re
import csv
from lxml import etree
import json
from requests import RequestException
from multiprocessing import Pool
import pymysql

"""
913:生活服务 --- 
882：智能硬件 ---
880：科学 ---
936：IT数码 --- 
934：通讯 ---
911：互联网 ---
获取的内容是从feedJQuery中获取的
将获取的author和id拼接在一起作为最后获取内容的id
利用csv进行存储  注意编码格式
"""


class Souhu:
    def __init__(self):
        page_ = ['882', '913', '880', '936', '934', '911']
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        self.header = header
        url = 'http://v2.sohu.com/public-api/feed?'
        self.url = url
        part_url = 'http://www.sohu.com/a/'
        self.basic_url = part_url

    def parse_basic(self, n):
        print("正在下载第{0}页".format(n))
        data = {
            'scene': 'CATEGORY',
            'sceneId': '913',
            'page': n,
            'size': '20',
        }
        try:
            response = requests.get(self.url, headers=self.header, params=data)
            if response.status_code == 200:
                # print(response.status_code)
                self.parse_html(response.text)
        except RequestException:
            print("wrong!")

    def parse_html(self, content):
        # print(content)
        result = json.loads(content)
        for i in range(len(result)):
            author_id = result[i].get('authorId')
            work_id = result[i].get('id')
            title = result[i].get('title')
            # part_title = re.compile('"title":"(.*?)"', re.S)
            # part_id = re.compile('{"id":(.*?),"authorId":(.*?),', re.S)
            # id_lists = re.findall(part_id, content)
            # titles = re.findall(part_title, content)
            # print(work_id, author_id, title)
            self.parse_content(str(work_id) + '_' + str(author_id), title)

    def parse_content(self, url, title):
        new_url = self.basic_url + url
        try:
            response = requests.get(new_url, headers=self.header)
            self.get_content(response.text, title, new_url)
        except RequestException:
            print('wrong!')

    def get_content(self, html, title, url):
        content = etree.HTML(html)
        # text = content.xpath('*//article[@class]//text()')
        content_text = ''.join(content.xpath('*//article[@class]/p[position()>2]//text()')).replace('\n', '').replace(' ', '')
        time_ = ''.join(content.xpath('//*[@id="news-time"]//text()'))
        origin = ''.join(content.xpath('//*[@id="user-info"]/h4/a//text()'))
        self.store_data(url, title, content_text, origin, time_)
        # print(title, text)

    def store_data(self, url, title, content, origin, time):
        print("正在下载：{0}, 时间:{1}".format(title, time))
        try:
            with open(r"F:\\生活服务.csv", 'a', encoding='utf-8', newline='') as csvfile:
                writers = csv.writer(csvfile)
                writers.writerow([url, title, content, origin, time])
        except Exception as io:
            print("OS is wrong:%s" % title)

    def start(self):
        groups = [i for i in range(1000)]
        pool = Pool(5)
        pool.map(self.parse_basic, groups)
        # self.parse_basic(1)


if __name__ == '__main__':
    souhu = Souhu()
    souhu.start()
