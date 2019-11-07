# -*- coding:utf-8 -*-
# !bin/python/even
# author:***
# 2019/**/**
import requests
import re
import json


class QQ:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'cookie': '*****',
        }

    def base_url(self):
        url = "https://qun.qq.com/cgi-bin/qun_mgr/get_group_list"
        data = {
            'bkn': '******',
        }
        try:
            response = requests.post(url, headers=self.header, data=data)
            if response.status_code == 200:
                result_response = response.content.decode('utf-8')
                self.parse_base_url(result_response)
        except Exception as e:
            print(e)

    def parse_base_url(self, content):
        load_content = json.loads(content)
        join = load_content['join']
        join_list = [(i['gc'], i['gn'].replace('&nbsp;', '')) for i in join]
        for i in join_list[:1]:
            self.get_every_group_chat(i)
        manage = load_content['manage']
        manage_list = [(i['gc'], i['gn'].replace('&nbsp;', '')) for i in manage]

    def get_every_group_chat(self, group_id):
        # 这里还要获取一个长度   优化避免最后超界
        every_group_data = {
            'gc': str(group_id[0]),
            'st': '0',
            'end': '20',
            'sort': '0',
            'bkn': '*****',
        }
        url = "https://qun.qq.com/cgi-bin/qun_mgr/search_group_members"
        try:
            response = requests.post(url, headers=self.header, data=every_group_data)
            if response.status_code == 200:
                result_response = response.content.decode('utf-8')
                self.parse_group_chat(result_response)
        except Exception as e:
            print(e)

    def parse_group_chat(self, content):
        json_load = json.loads(content)
        members = json_load['mems']
        load_member = [(i['uin'], i['card'].replace('&nbsp;', ''), i['nick'].replace('&nbsp;', '')) for i in members]
        for i in load_member:
            print(i)

    def start(self):
        self.base_url()


if __name__ == '__main__':
    mt = QQ()
    mt.start()
