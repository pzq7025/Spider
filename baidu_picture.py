import requests
import re
import os
from multiprocessing import Pool
from requests import RequestException
from urllib import parse


class Bd:
    """
    spider cang teachers
    """
    def __init__(self):
        header = {
            'Referer': 'https://www.dbmeinv.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        self.header = header

    def get_url(self, n):
        data = {
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': '201326592',
            'is': '',
            'fp': 'result',
            'queryWord': '苍老师',
            'cl': '2',
            'lm': '-1',
            'ie': 'utf - 8',
            'oe': 'utf - 8',
            'adpicid': '',
            'st': '-1',
            'z': '',
            'ic': '0',
            'hd': '1',
            'latest': '0',
            'copyright': '0',
            'word': '苍老师',
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': '0',
            'istype': '2',
            'qc': '',
            'nc': '1',
            'fr': '',
            'expermode': '',
            'force': '',
            'pn': n*30,
            'rn': '30',
            'gsm': hex(n*30),
            'c': '',
            }
        url = "https://image.baidu.com/search/acjson?" + parse.urlencode(data)
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                self.parse_html(response.text)
        except RequestException:
            print("the url is wrong")

    def parse_html(self, html):
        part_url = re.compile('"thumbURL":"(.*?)"', re.S)
        part_name = re.compile('"fromPageTitleEnc":"(.*?)"', re.S)
        url_list = re.findall(part_url, html)
        name_list = re.findall(part_name, html)
        total = [(url, name) for (url, name) in zip(url_list, name_list)]
        for part in total:
            self.pic_url(part[0], part[1])

    def pic_url(self, url, name):
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                self.store_content(response.content, name)
            else:
                print(response.status_code)
        except RequestException:
            print("the picture is wrong!")

    @staticmethod
    def store_content(content, name):
        path = r"F:\exploitation\codes\python\Spider\girls_pictures"
        file_path = r"{0}\{1}.{2}".format(path, name, 'jpg')
        print("正在下载:{0}".format(name))
        try:
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(content)
        except OSError:
            print("write is wrong!")

    def pool_html(self):
        grounds = [i for i in range(1, 300)]
        pool = Pool(5)
        pool.map(self.get_url, grounds)

    def start(self):
        self.pool_html()


if __name__ == '__main__':
    db = Bd()
    db.start()