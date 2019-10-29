# -*- coding:utf-8 -*-
# !bin/python/even
# author:pzq
# time:2019/10/28/12:03
import csv
import json

import requests
from multiprocessing import Pool
from lxml import etree

path = './data_complete/2017_university_evaluation.csv'


class Mt:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }

    def base_url(self):
        url = "https://souky.eol.cn/api/newapi/assess_result#"
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                content_url = response.content.decode('utf-8')
                self.parse_base(content_url)
        except Exception as e:
            print(e)

    def parse_base(self, content):
        index_content = etree.HTML(content)
        # 获取每个课程的value值
        profession_value = index_content.xpath('/html/body/div[4]/div[1]/ul/li/ul/li/@value')
        pool = Pool()
        pool.map(self.parse_list, profession_value)
        # for i in profession_value:
        #     self.parse_list(i)

    def parse_list(self, one):
        """
        parse every profession, to get this list how many universities.
        :param one:
        :return:
        """
        url = "https://souky.eol.cn/api/newapi/assess_result?"
        data = {
            'xid': one,
            'flag': '1',
        }
        try:
            response = requests.get(url, params=data, headers=self.header)
            if response.status_code == 200:
                content_url = response.content.decode('utf-8')
                self.parse_every_html(content_url)
        except Exception as e:
            print(e)

    def parse_every_html(self, json_content):
        finally_result = []
        parse_dict = json.loads(json_content)[0]
        name = parse_dict['name']
        parse_dict_list = json.loads(json_content)[1]
        for i in parse_dict_list:
            result = i['result']
            sname = i['sname']
            finally_result.append([name, sname, result])
        self.write_csv(finally_result)

    def write_csv(self, data):
        try:
            with open(path, 'a', newline='', encoding='utf-8-sig') as f_csv:
                csv_write = csv.writer(f_csv)
                csv_write.writerows(data)
            print("Successful!")
        except OSError:
            print("Write is wrong!")

    def write_head(self):
        try:
            with open(path, 'w', newline='', encoding='utf-8-sig') as f_csv:
                csv_write = csv.writer(f_csv)
                csv_write.writerow(['profession', 'university', 'level'])
        except OSError:
            print("Write is wrong!")

    def start(self):
        self.write_head()
        self.base_url()


if __name__ == '__main__':
    mt = Mt()
    mt.start()
