# -*- coding:utf-8 -*-
# !bin/python/even
# author:pzq
import requests
import re
from lxml import etree
import json
from multiprocessing import Pool


class JueJin:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'X-Agent': 'Juejin/Web',
            'X-Legacy-Device-Id': '',
            'X-Legacy-Token': '',
            'X-Legacy-Uid': '',
            'Content-Type': 'application/json',
            'Host': 'web-api.juejin.im',
            'Origin': 'https://juejin.im',
        }

    def base_url(self, n):
        url = "https://web-api.juejin.im/query"
        # 利用json中的dumps将字典转成json数据发送给网站进行请求
        data = {
            'extensions': {'query': {'id': "a53db5867466eddc50d16a38cfeb0890"}},
            'operationName': "",
            'query': "",
            'variables': {
                'after': str(n * 20),
                'first': '20',
                'period': 'ALL',
                'query': "广告设计",
                'type': "ALL",
            }
        }
        try:
            response = requests.post(url, headers=self.header, data=json.dumps(data))
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                self.parse_base_url(content)
        except Exception as e:
            print(e)

    def parse_base_url(self, content):
        load_content = json.loads(content)['data']['search']
        edges = load_content['edges']
        for i in edges:
            entity = i['node']['entity']
            articles_id = entity['id']
            title = entity['title'].replace('\n', '')
            print(articles_id, title)

    def start(self):
        # groups = [i for i in range(10)]
        # pool = Pool()
        # pool.map(self.base_url, groups)
        self.base_url(0)


if __name__ == '__main__':
    jj = JueJin()
    jj.start()
