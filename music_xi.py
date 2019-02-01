import hashlib
import time
from urllib.parse import urlencode
from multiprocessing import Pool
from requests.exceptions import RequestException
from hashlib import md5
import re
import os
import redis
import requests


class Music:
    def __init__(self):
        """
        creation the header
        """
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            # 'Host': 'www.ximalaya.com',
            # 'Referer': 'https://www.ximalaya.com/yinyue/3627097/'
        }
        # data = {
        #     "albumId": 3627097,
        #         "pageNum": n,
        #     "sort": -1,
        #     "pageSize": 30
        # }
        self.header = header
        # self.data = data

    def parse(self, n):
        data = {
            "albumId": 3627097,
            "pageNum": n,
            "sort": -1,
            "pageSize": 30
        }
        url_1 = "https://www.ximalaya.com/revision/play/album?" + urlencode(data)
        # url = "http://audio.xmcdn.com/group55/M01/23/24/wKgLf1xRahDA8VoqACdm6sv6XRE171.m4a"
        try:
            response = requests.get(url_1, headers=self.header)
            # print(url_1)
            if response.status_code == 200:
                html = response.text
                self.parse_html(html)
                # self.get_content(response.content)
            else:
                print(response.status_code)
        except RequestException:
            print("response is wrong!")
            print()
            return None

    def parse_html(self, parse_html):
        """
        get url and name for the parse_json

        special:
            name_compile = re.compile("trickName=(.*?)", re.S)
            name = re.findall(name_compile, parse_json)
            url_compile = re.compile("src=(.*?)", re.S)
            url = re.findall(url_compile, parse_json)
            info = [(name, url) for (name, url) in zip(name, url)]
            print(info)
        this code is use the re, but the parse_json is dict, so one method is don't use the json.loads
        and the other is use the dict of method to detail this content
        :param parse_html: get the song of information including url and name
        :return:
        """
        name_compile = re.compile(r'"trackName":"(.*?)"', re.S)
        name = re.findall(name_compile, parse_html)
        url_compile = re.compile(r'"src":"(.*?)"', re.S)
        url = re.findall(url_compile, parse_html)
        info = [(name, url) for (name, url) in zip(name, url)]
        for info_1 in info:
            try:
                response = requests.get(info_1[1], headers=self.header)
                if response.status_code == 200:
                    self.get_content(response.content, info_1[0])
                    # time.sleep(5)
            except RequestException:
                print("404")
                return None

    def get_content(self, content, name):
        """
        get_content and to store to this file and show the process
        :param content: write the content to the file
        :param name: get the song of name as the file of name to store
        :return:
        """
        try:
            print("正在下载: %s" % name)
            # ==============================================================

            # hashlib.md5(name.encode('utf8')).hexdigest().upper()
            # hash编码  还是喜欢Unicode
            # ==============================================================
            path = "F:\\exploitation\\codes\\python\\Spider\\video_s\\" + name + '.m4a'
            if not os.path.exists(path):
                with open(path, "wb") as f:
                    f.write(content)
                    f.close()
        except OSError:
            print("write is wrong")

    def download(self):
        groups = [x for x in range(1, 34)]
        pool = Pool(5)
        pool.map(self.parse, groups)

    # connection redis
    def connect_redis(self):
        r = redis.StrictRedis(host="localhost", port=6397, db=0)


if __name__ == '__main__':
    # for i in range(1, 34):
    music = Music()
    music.download()
    # music.download()
    # groups = [x * 30 for x in range(1, 34)]
    # pool = Pool()
    # # pool.map(Music(i for i in range(1, 34)))
    # pool.map(Music.parse(), groups)
