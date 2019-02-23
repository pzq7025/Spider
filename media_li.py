import requests
import re
import os
from lxml import etree
from urllib import parse
from requests import RequestException
from multiprocessing import Pool


class Li:
    """
    get the media of li
    """

    def __init__(self):
        """
        set general param
        """
        header = {
            'Referer': 'https://www.pearvideo.com/category_8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        url = 'https://www.pearvideo.com/'
        url_total = 'https://www.pearvideo.com/category_loading.jsp?'
        self.header = header
        self.url = url
        self.total = url_total

    def basic_parse_url(self, n):
        """
        parse the origin url, through the html get the origin of code
        special: 因为request请求时需要参数  而参数是filter的  所以在写参数时不需要这个filter 直接控制start来产生新的url界面
        :param n: the param of request the url
        :return:
        """
        data = {
            'reqType': '5',
            'categoryId': '8',
            'start': n * 12,
            'mrd': '0.8390502972041403',
        }
        basic_url = self.total + parse.urlencode(data)
        try:
            response = requests.get(basic_url, headers=self.header)
            if response.status_code == 200:
                self.parse_origin_url(response.text)
        except RequestException:
            print("wrong!")

    def parse_origin_url(self, html):
        """
        parse the correspond of html get url of id and through the id to request the url and parse this url get name and media of address
        :param html: get the correspond param of html
        :return:
        """
        try:
            content = etree.HTML(html)
            # print(html)
            # part_url = re.compile(r'<div class=".*?">\n<a href="(.*?)" class=".*?">', re.S)
            # url_list = re.findall(part_url, html)
            url_list = content.xpath('*//li/div/a/@href')
            total = [url for url in url_list]
            for part in total:
                url = self.url + part
                # print(url)
                self.parse_video_url(url)
        except Exception as ee:
            print(ee)

    def parse_video_url(self, url):
        """
        get the video of url and start download for ready
        :param url: the url of address and every url
        :return:
        """
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                self.down_load(response.text)
        except RequestException:
            print("video response is wrong: %s" % RequestException)

    def down_load(self, html):
        """
        start downloading
        :param html: the video of url html get the video of address and name and the video of name as the file of name
        :return:
        """
        part_url = re.compile('srcUrl="(.*?)"', re.S)
        part_name = re.compile('<h1 class="video-tt">(.*?)</h1>', re.S)
        name = re.findall(part_name, html)
        url = re.findall(part_url, html)
        try:
            response = requests.get(url[0], headers=self.header)
            if response.status_code == 200:
                self.store_content(response.content, name[0])
        except RequestException:
            print("down response is wrong: %s" % RequestException)

    @staticmethod
    def store_content(content, name):
        """
        start downloading
        :param content: the video of binary content
        :param name: the video of name
        :return:
        """
        print("downloading:{0}".format(name))
        path = r"F:\exploitation\codes\python\Spider\videos"
        file_path = r"{0}\{1}.{2}".format(path, name, 'mp4')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()

    def pool(self):
        """
        pool and multithreading to quickly spider
        :return:
        """
        grounds = [x for x in range(1, 50)]
        pool = Pool(5)
        pool.map(self.basic_parse_url, grounds)

    def start_spider(self):
        self.pool()


if __name__ == '__main__':
    li = Li()
    li.start_spider()
