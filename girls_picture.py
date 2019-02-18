import requests
import os
from lxml import etree
from requests import RequestException
from multiprocessing import Pool


class Picture:
    def __init__(self):
        header = {
            'Referer': 'https://www.dbmeinv.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        self.header = header

    def _get_url(self, n):
        url = 'https://www.dbmeinv.com/?pager_offset=' + str(n)
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                self.parse_html(response.text)
            return None
        except RequestException:
            print("The url response is wrong!")

    def parse_html(self, html):
        content = etree.HTML(html)
        urls = content.xpath('*//img/@src')
        names = content.xpath('*//img/@title')
        infos = [(url, name) for (url, name) in zip(urls, names)]
        for info in infos:
            self.parse_picture_url(info[0], info[1])

    def parse_picture_url(self, url, name):
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                self.store_picture(response.content, name)
            return None
        except RequestException:
            print("The picture response is wrong!")

    def store_picture(self, content, name):
        path = r"F:\exploitation\codes\python\Spider\girls_pictures"
        file_name = r"{0}\{1}.{2}".format(path, name, 'jpg')
        print("已经下载{0}正在下载{1}".format(self.n, name))
        try:
            if not os.path.exists(file_name):
                with open(file_name, 'wb') as f:
                    f.write(content)
                    f.close()
            print("pictures is already exist")
        except OSError:
            print("Write is wrong!")

    def main(self):
        grounds = [x for x in range(1, 50)]
        pool = Pool(5)
        pool.map(self._get_url, grounds)


if __name__ == '__main__':
    picture = Picture()
    picture.main()
