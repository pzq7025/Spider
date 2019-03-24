# -*- encoding:utf-8 -*-
# author:pzq
import requests
from requests import RequestException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
利用selenium对歌曲进行点击将点击的内容 传给播放器  
在对播放器进行解析  将得到的url信息进行解析 获取歌曲地址进行下载存储


拿到歌曲的id对获取的id和url进行拼接批量下载

"""


class QQMusic:
    def __init__(self):
        header = {
            'referer': 'https://www.pearvideo.com/category_8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        url = 'https://y.qq.com/portal/playlist.html'
        browser = webdriver.Chrome()
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)
        self.url = url
        self.header = header

    def use_selenium(self):
        self.browser.get(self.url)
        play_list = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.mod_header > div > ul.mod_top_subnav > li:nth-child(4) > a'))
        )
        hover = self.browser.find_element_by_xpath('#playlist_box > li.playlist__item.playlist__item--current > div > div.playlist__cover.mod_cover > a > img')
        # ActionChains(self.browser).move_to_element(hover).perform()
        # submit = self.browser.find_element_by_xpath('//*[@id="playlist_box"]/li[1]/div/div[1]/a/i')
        # submit.click()
        play_list.click()
        # self.browser.close()

    def get_url(self):
        try:
            response = requests.get(self.url, headers=self.header)
        except RequestException:
            print('Response wrong!')

    def start(self):
        self.use_selenium()


if __name__ == '__main__':
    music = QQMusic()
    music.start()
