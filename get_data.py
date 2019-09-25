# -*- coding:utf-8 -*-
# !bin/python/even
#
import json

import requests
import re
from requests import RequestException
import csv
from multiprocessing import Pool


class Mt:
    failed_food_url = []  # 美食页失败的url
    failed_stop_url = []  # 获取店铺失败的url
    total = 0  # 计数
    shop_comment = []  # 存储评论

    def base_url(self, n):
        """
        美食网页获取id
        :param n:
        :return:
        """
        header = {
            'Referer': 'https://wh.meituan.com/meishi/pn' + str(n) + '/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }

        food_url = 'https://wh.meituan.com/meishi/pn' + str(n) + '/'
        response = requests.get(food_url, headers=header)
        try:
            if response.status_code == 200:
                result = response.content.decode('utf-8')
                self.parse_base_url(result)
        except RequestException:
            self.failed_food_url.append(food_url)
            print(f"错误请求网站:{food_url}")

    def parse_base_url(self, content):
        """
        解析id和title
        :param content:
        :return:
        """
        # print(content)
        poi_ids = re.compile(r'"poiId":(\d+)', re.S).findall(content)  # 获取所有店铺的id
        titles = re.compile(r'"frontImg":".*?","title":"(.*?)","avgScore":', re.S).findall(content)  # 获取所有店铺的名字

        # 最后的存储结果数组
        final_store = []
        for one in range(len(poi_ids))[:1]:
            self.total = 0
            self.shop_comment = []
            for i in range(11):
                self.get_shop_info(poi_ids[one], i)
            print(f"id:{poi_ids[one]}---名称:{titles[one]}---------一共{self.total}条数据")
            final_store.append([poi_ids[one], titles[one], '$'.join(self.shop_comment)])
        with open('spider.csv', 'a', encoding='utf-8-sig') as f:
            csv.writer(f, final_store)

    def get_shop_info(self, one, n):
        """
        进入到具体的商品进行响应
        :param one:
        :param n:
        :return:
        """
        shop_base_url = "https://www.meituan.com/meishi/"
        shop_url = shop_base_url + one + '/'

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Referer': shop_url,
        }

        data = {
            'uuid': 'cdf20e51-7327-435e-a15e-ddeca28d1be6',
            'platform': '1',
            'partner': '126',
            'originUrl': shop_url,
            'riskLevel': '1',
            'optimusCode': '10',
            'id': one,
            'userId': '',
            'offset': str((n - 1) * 10),
            'pageSize': '10',
            'sortType': '1',
        }

        comment_url = "https://www.meituan.com/meishi/api/poi/getMerchantComment?"
        response = requests.get(comment_url, headers=header, params=data)
        try:
            if response.status_code == 200:
                result = response.content.decode('utf-8')
                self.parse_shop_url(result)
        except RequestException:
            self.failed_stop_url.append(shop_url)
            print(f"错误请求网站:{shop_url}")

    def parse_shop_url(self, content):
        """
        获取用户评论
        :param content:
        :return:
        """
        parse_content = json.loads(content)
        comments = parse_content.get('data').get('comments')  # 获取评论
        if comments:  # 有才获取
            for one in comments:
                self.total += 1
                comment = one.get('comment').replace('\n', '').replace('\r', '')
                if comment:  # 有才获取
                    self.shop_comment.append(comment)

    def start(self):
        # 启用进程池爬取
        ground = [x for x in range(15)]
        pool = Pool(6)
        pool.map(self.base_url, ground)
        self.base_url(4)


if __name__ == '__main__':
    mt = Mt()
    mt.start()
