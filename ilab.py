# -*- coding:utf-8 -*-
# !bin/python/even
# author:pzq
import requests
import re
from lxml import etree
import json
import pandas as pd
from multiprocessing import Pool
import csv
import time

base_path = './data_file/'
tear_path = base_path + 'term.csv'
source_path = base_path + 'source.csv'


class Mt:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }

    def base_url(self, n):
        url = "http://www.ilab-x.com/json/projects?"
        data = {
            'status': '1',
            'del': '0',
            'proLevel': '1',
            'isToDeclare': '1',
            'limit': '9',
            'start': str(n * 9 + 1),
            'sortby': 'pubSeq',
            'reverse': 'true',
            # 'declareYear': '2019',
            'ts': '',
        }
        try:
            response = requests.get(url, headers=self.header, params=data)
            if response.status_code == 200:
                result = response.content.decode('utf-8')
                self.parse_base_url(result)
        except Exception as e:
            print(e)

    def parse_base_url(self, content):
        parse_json = json.loads(content)
        data_all = parse_json['data']
        for i in data_all[:]:
            source_id = i['id']
            brief = i['brief'].replace('\n', '').replace('"', '')
            keywords = i['courseKeyWords']
            course = i['course']
            year = i['declareYear']
            big_category = i['sps1']['title']
            small_category = i['sps2']['title']
            # category = i['expSub03']['title']
            category = ''
            title = i['expTitle']
            school_title = i['schoolTitle']
            score = i['score']
            score_count = i['scoreCount']
            video_path = i['videoPath']
            view_count = i['viewCount']
            address = i['userInfo']['address'].replace('\n', '')
            admin_duty = i['userInfo']['adminDuty']
            faculty = i['userInfo']['faculty']
            name = i['userInfo']['name']
            value_list = [name, faculty, admin_duty, address, school_title, source_id, title, course, keywords, year, big_category, small_category, category, score, score_count, video_path, view_count, brief]
            if value_list:
                self.write_source_csv(value_list)
            # print(source_id, brief, keywords, course, year, big_category, small_category, category, title, school_title, score, score_count)
            # print(video_path, view_count, address, admin_duty, faculty, name)
            self.get_team_core_url(source_id, 0)
            self.get_team_other_url(source_id, 0)

    def get_team_core_url(self, course_id, n):
        # 核心成员不止五个
        url = "http://www.ilab-x.com/json/project/team/search?"
        data = {
            'sortby': 'id',
            'reverse': 'false',
            'status': '1',
            'memberType': '1',
            'limit': '5',
            'start': str(n * 5 + 1),
            'projectId': course_id,
            'ts': '',
        }
        try:
            response = requests.get(url, headers=self.header, params=data)
            if response.status_code == 200:
                result = response.content.decode('utf-8')
                self.parse_core_url(result, course_id, n)
        except Exception as e:
            print(e)

    def get_team_other_url(self, course_id, n):
        # 其他成员可能还有多个
        url = "http://www.ilab-x.com/json/project/team/search?"
        data = {
            'sortby': 'id',
            'reverse': 'false',
            'status': '1',
            'memberType': '2',
            'limit': '5',
            'start': str(n * 5 + 1),
            'projectId': course_id,
            'ts': '',
        }
        try:
            response = requests.get(url, headers=self.header, params=data)
            if response.status_code == 200:
                result = response.content.decode('utf-8')
                self.parse_other_url(result, course_id, n)
        except Exception as e:
            print(e)

    def parse_core_url(self, content, course_id, n):
        parse_content = json.loads(content)
        if n == 0:
            total_data = parse_content['data']
            terms = []
            for i in total_data:
                name = i['name']
                unit = i['unit']
                unit_wash = unit.replace('\n', '') if unit else 'none'
                pa_tech_duty = i['PATechDuty']
                pa_tech_duty_wash = pa_tech_duty.replace('\n', '') if pa_tech_duty else 'none'
                pa_admin_duty = i['PAAdminDuty']
                pa_admin_duty_wash = pa_admin_duty.replace('\n', '') if pa_admin_duty else 'none'
                duty = i['duty']
                duty_wash = duty.replace('\n', '') if duty else 'none'
                remark = i['remark']
                remark_wash = remark.replace('\n', '') if remark else 'none'
                terms.append([course_id, name, unit_wash, pa_tech_duty_wash, pa_admin_duty_wash, duty_wash, remark_wash])
            if terms:
                self.write_term_csv(terms)
            self.get_team_core_url(course_id, 1)
        else:
            total = int(parse_content['meta']['total'])
            around_y = 0
            if total > 5:
                around_y = total // 5
            total_data = parse_content['data']
            terms = []
            for i in total_data:
                name = i['name']
                unit = i['unit']
                unit_wash = unit.replace('\n', '') if unit else 'none'
                pa_tech_duty = i['PATechDuty']
                pa_tech_duty_wash = pa_tech_duty.replace('\n', '') if pa_tech_duty else 'none'
                pa_admin_duty = i['PAAdminDuty']
                pa_admin_duty_wash = pa_admin_duty.replace('\n', '') if pa_admin_duty else 'none'
                duty = i['duty']
                duty_wash = duty.replace('\n', '') if duty else 'none'
                remark = i['remark']
                remark_wash = remark.replace('\n', '') if remark else 'none'
                terms.append([course_id, name, unit_wash, pa_tech_duty_wash, pa_admin_duty_wash, duty_wash, remark_wash])
            if terms:
                self.write_term_csv(terms)
            while n < around_y:
                n += 1
                self.get_team_core_url(course_id, n)

    def parse_other_url(self, content, course_id, n):
        parse_content = json.loads(content)
        if n == 0:
            total_data = parse_content['data']
            terms = []
            for i in total_data:
                name = i['name']
                unit = i['unit']
                unit_wash = unit.replace('\n', '') if unit else 'none'
                pa_tech_duty = i['PATechDuty']
                pa_tech_duty_wash = pa_tech_duty.replace('\n', '') if pa_tech_duty else 'none'
                pa_admin_duty = i['PAAdminDuty']
                pa_admin_duty_wash = pa_admin_duty.replace('\n', '') if pa_admin_duty else 'none'
                duty = i['duty']
                duty_wash = duty.replace('\n', '') if duty else 'none'
                remark = i['remark']
                remark_wash = remark.replace('\n', '') if remark else 'none'
                terms.append([course_id, name, unit_wash, pa_tech_duty_wash, pa_admin_duty_wash, duty_wash, remark_wash])
            if terms:
                self.write_term_csv(terms)
            self.get_team_other_url(course_id, 1)
        else:
            total = int(parse_content['meta']['total'])
            around_x = 0
            if total > 5:
                around_x = total // 5
            total_data = parse_content['data']
            terms = []
            for i in total_data:
                name = i['name']
                unit = i['unit']
                unit_wash = unit.replace('\n', '') if unit else 'none'
                pa_tech_duty = i['PATechDuty']
                pa_tech_duty_wash = pa_tech_duty.replace('\n', '') if pa_tech_duty else 'none'
                pa_admin_duty = i['PAAdminDuty']
                pa_admin_duty_wash = pa_admin_duty.replace('\n', '') if pa_admin_duty else 'none'
                duty = i['duty']
                duty_wash = duty.replace('\n', '') if duty else 'none'
                remark = i['remark']
                remark_wash = remark.replace('\n', '') if remark else 'none'
                terms.append([course_id, name, unit_wash, pa_tech_duty_wash, pa_admin_duty_wash, duty_wash, remark_wash])
            if terms:
                self.write_term_csv(terms)
            while n < around_x:
                n += 1
                self.get_team_other_url(course_id, n)

    def write_source_csv(self, values_list=None, head=True):
        with open(source_path, 'a', encoding='utf-8-sig', newline='') as f_csv:
            write_buffer = csv.writer(f_csv)
            if head:
                print(f"正在写入数据{values_list}")
                write_buffer.writerow(values_list)
            else:
                head_value = ['name', 'faculty', 'admin_duty', 'address', 'school_title', 'source_id', 'title', 'course', 'keywords', 'year', 'big_category', 'small_category', 'category', 'score', 'score_count', 'video_path', 'view_count', 'brief']
                write_buffer.writerow(head_value)

    def write_term_csv(self, values_list=None, head=True):
        with open(tear_path, 'a', encoding='utf-8-sig', newline='') as f_csv:
            write_buffer = csv.writer(f_csv)
            if head:
                print(f"正在写入数据{values_list}")
                write_buffer.writerows(values_list)
            else:
                head_value = ['course_id', 'name', 'unit', 'PATechDuty', 'PAAdminDuty', 'duty', 'remark']
                write_buffer.writerow(head_value)

    def start(self):
        # 最大值112
        # 写入头
        self.write_source_csv(head=False)
        self.write_term_csv(head=False)
        # for i in range(113):
        groups = [x for x in range(123)]
        pool = Pool()
        pool.map(self.base_url, groups)
        # self.base_url(4)
        #     time.sleep(1)


if __name__ == '__main__':
    mt = Mt()
    mt.start()
