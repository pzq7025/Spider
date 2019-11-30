# -*- coding:utf-8 -*-
# !bin/python/even
# author:pzq
import requests
import re
from lxml import etree
# import json
import csv
from multiprocessing import Pool


class Mt:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }
        self.store_data = []

    def base_url(self, n):
        url = "https://book.douban.com/tag/%E5%8A%B1%E5%BF%97?"
        data = {
            'start': str(20 * n),
            'type': 'T',
        }
        # try:
        response = requests.get(url, headers=self.header, params=data)
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            self.parse_base_url(result)
        # except Exception as e:
        #     print(e)

    def parse_base_url(self, content):
        xpath_content = etree.HTML(content)
        ids = re.compile(r'<a href="https://book.douban.com/subject/(\d+)/" title=".*?"', re.S).findall(content)
        pictures_url = xpath_content.xpath('//*[@id="subject_list"]/ul/li/div[1]/a/img/@src')
        book_name = [k for k in [i.replace('\n', '').replace(' ', '') for i in xpath_content.xpath('//*[@id="subject_list"]/ul/li/div[2]/h2/a/text()')] if k]
        book_info = [i.replace('\n', '').replace(' ', '').replace('元', '').replace('CNY', '').split('/') for i in xpath_content.xpath('//*[@id="subject_list"]/ul/li/div[2]/div[1]//text()')]
        for i in book_info:
            if len(i) == 4:
                i.insert(1, "LaLa")
            if len(i) == 3:
                i.insert(1, "LaLa")
                i.insert(3, "2019-6-10")
        combine_result = []
        for i in list(zip(ids, pictures_url, book_name, book_info))[:]:
            list_content = {
                'book_id': i[0],
                'book_name': i[2],
                'book_author': i[3][0],
                'book_price': i[3][4],
                'book_year': i[3][3],
                'book_publish': i[3][2],
                'book_img': i[1],
                'book_describe': '',
                'book_content': '',
            }
            return_result = self.get_next_url(list_content)
            combine_result.append(return_result)
        self.write_csv(combine_result)

    def get_next_url(self, list_content):
        url = "https://book.douban.com/subject/" + str(list_content['book_id']) + "/"
        # try:
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            return self.parse_next_url(result, list_content)
        # except Exception as e:
        #     print(e)

    @staticmethod
    def parse_next_url(content, list_content):
        parse_content = etree.HTML(content)
        # book_describe = ''.join(parse_content.xpath('//*[@id="info"]/a[2]//text()')).replace('\n', '')
        book_content = ''.join(parse_content.xpath('//*[@id="link-report"]/div[1]/div/p[position()]//text()')).replace('\n', '').replace(' ', '')
        list_content['book_describe'] = list_content['book_author'] + "撰写的《" + list_content['book_name'] + "》是一本非常励志且受到广泛好评的书籍"
        if book_content == '':
            book_content = ''.join(parse_content.xpath('//*[@id="link-report"]/span[1]/div/p[position()]//text()')).replace('\n', '').replace(' ', '')
            list_content['book_content'] = book_content
        else:
            # re.compile(r'\W+', re.S).sub('', book_content)
            list_content['book_content'] = book_content
        result = [i[1] for i in list_content.items()]
        print(f"获取完成：{result[1]}")
        return result

    @staticmethod
    def write_csv(content):
        with open('../download_file/crawl_data_book_name_page_10.csv', 'w', encoding='utf-8-sig', newline="") as csv_file:
            content_csv = csv.writer(csv_file)
            content_csv.writerow(['book_id', 'book_name', 'book_author', 'book_price', 'book_year', 'book_publish', 'book_img', 'book_describe', 'book_content'])
            content_csv.writerows(content)

    def start(self):
        # group = [x for x in range(3)]
        # pool = Pool()
        # pool.map(self.base_url, group)
        self.base_url(10)


if __name__ == '__main__':
    mt = Mt()
    mt.start()
