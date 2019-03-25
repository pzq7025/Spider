#!bin/even/python3.6
# -*- encoding:utf-8 -*-
# author:pzq
import requests
import os
import re
import json
from requests import RequestException
from multiprocessing import Pool
from lxml import etree

"""
'http://dl.stream.qqmusic.qq.com/'  这个网站结合从歌曲信息获取到的purl进行拼接  就可以得到播放的地址然后对内容进行下载
参数信息：
purl

歌曲的播放地址用上述的拼接进行获取
http://dl.stream.qqmusic.qq.com/C400002CJIg01yHquI.m4a?guid=8874756349&vkey=A3B648A1F511D4064C57684BF64F8FCBBA87ED01422023D2BF20110B8D7E18D25009BA93268E7334E133B0A113361EB777CCCE1F9A8E9965&uin=0&fromtag=66


获取purl信息的url地址：https://u.y.qq.com/cgi-bin/musicu.fcg?
参数：
-: getplaysongvkey3736817870528528
g_tk: 5381
loginUin: 0
hostUin: 0
format: json
inCharset: utf8
outCharset: utf-8
notice: 0
platform: yqq.json
needNewCode: 0
data: {"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8874756349","songmid":["003XCbA520zgXW"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}


-: getplaysongvkey15410530308016956
g_tk: 5381
loginUin: 0
hostUin: 0
format: json
inCharset: utf8
outCharset: utf-8
notice: 0
platform: yqq.json
needNewCode: 0
data: {"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8874756349","songmid":["000zmYjO01BWe2"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}



https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?  这个是歌曲信息的url
参数信息：
'type': '1',
'json': '1',
'utf8': '1',
'onlysong': '0',
'disstid': '6796775368',
'g_tk': '5381',
'loginUin': '0',
'hostUin': '0',
'format': 'json',
'inCharset': 'utf8',
'outCharset': 'utf - 8',
'notice': '0',
'platform': 'yqq.json',
'needNewCode': '0',



https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?  这个是歌单的url  先获取20个歌单  在对每个歌单的歌曲进行进行解析就可以获的到所有的歌曲信息
参数信息：
picmid: 1
rnd: 0.59461213653597
g_tk: 5381
loginUin: 0
hostUin: 0
format: json
inCharset: utf8
outCharset: utf-8
notice: 0
platform: yqq.json
needNewCode: 0
categoryId: 10000000
sortId: 5
sin: 0
ein: 19
"""


class QQMusic:
    def __init__(self):
        """
        header_origin: play list header
        header_song: songs list header
        header_download: down_load songs header
        download_url: download url to download songs
        """
        header_origin = {
            # 'referer': 'https://www.pearvideo.com/category_8',
            'Referer': 'https://y.qq.com/portal/playlist.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        header_song = {
            # 'referer': 'https://www.pearvideo.com/category_8',
            'Referer': 'https://y.qq.com/portal/player.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        header_download = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        download_url = 'http://isure.stream.qqmusic.qq.com/'
        song_info_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?'
        self.song_info_url = song_info_url
        self.header_song = header_song
        self.header_origin = header_origin
        self.download_url = download_url
        self.header_download = header_download

    def parse_origin(self):
        """
        parse the origin url get the album of id to song's list
        the part of data should to put the def __init__()
        :return:
        """
        url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?'
        data = {
            'picmid': '1',
            'rnd': '',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
            'categoryId': '10000000',
            'sortId': '5',
            'sin': '0',
            'ein': '19',
        }
        try:
            response = requests.get(url, params=data, headers=self.header_origin)
            if response.status_code == 200:
                self.get_album_id(response.text)
        except RequestException:
            print('Response wrong!')

    def get_album_id(self, content):
        """
        from play of html to get play of id information, put this information in group, so that i can use the multiprocessing
        this method can accelerate crawl speed
        :param content: origin html's content
        :return:
        """
        grounds = []
        infos = json.loads(content)
        ids = infos.get('data').get('list')
        for id_in in ids:
            id = id_in.get('dissid')
            grounds.append(id)
            # here to open some pool use the number information
        self.pool_function(grounds)

    def pool_function(self, group):
        """
        excess and start pool
        :param group: id grounds, according to this group of number to pass the parse function and to get the play list id
        :return:
        """
        pool = Pool(5)
        pool.map(self.parse_song_id, group)

    def parse_song_id(self, id):
        """
        get play menu's id and get songs information
        :param id: everyone play menu of id can gain every songs information
        :return:
        """
        header_song_list = {
            'Referer': 'https://y.qq.com/n/yqq/playsquare/' + str(id) + '.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        base_url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?'
        """唯一的不同在于disstid  disstid就是我需要获取的歌单id"""
        data = {
            'type': '1',
            'json': '1',
            'utf8': '1',
            'onlysong': '0',
            'disstid': str(id),
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf - 8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
        }
        try:
            response = requests.get(base_url, params=data, headers=header_song_list)
            if response.status_code == 200:
                self.parse_songs_info(response.text)
        except RequestException:
            print('Response songs list is wrong!')

    def parse_songs_info(self, content):
        """
        get menu's of information parse every html get songmid: in order to get vkey and get start download songs
        :param content: every html information and get id start
        :return:
        """
        infos_ = json.loads(content)
        infos = infos_.get('cdlist')[0].get('songlist')
        for info in infos:
            song_mid = info.get('songmid')
            song_name = info.get('songname')
            self.parse_song((song_mid, song_name))

    def parse_song(self, song_info):
        """
        song_info is list id is the first param
        :param song_info: including sond_mid and song_name to get songs content and start download
        :return:
        """
        data = {
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf - 8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
            'data': '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8874756349","songmid":["' + song_info[0] + '"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}',
        }
        try:
            response = requests.get(self.song_info_url, params=data, headers=self.header_song)
            if response.status_code == 200:
                self.parse_play_id(response.text, song_info)
        except RequestException:
            print('Song response is wrong!')

    def parse_play_id(self, content, song_info):
        """
        get purl it's include vkey and other params and begin download
        :param content: get play html and get purl because this param can direct get songs information
        :param song_info: is list id is the first param name is the second param
        :return:
        """
        info = json.loads(content)
        part_url = info.get('req_0').get('data').get('midurlinfo')[0].get('purl')
        try:
            response = requests.get(self.download_url + part_url, headers=self.header_download)
            if response.status_code == 200:
                self.store_song(response.content, song_info[1])
        except RequestException:
            print("Song response is wrong!")

    def store_song(self, content, song_name):
        """
        store songs to file
        :param content: song's information
        :param song_name: filename use every song's name as file name
        :return:
        """
        try:
            print("正在下载：{0}".format(song_name))
            path_store = r'..\videos\{0}.{1}'.format(song_name, 'm4a')
            if not os.path.exists(path_store):
                with open(path_store, 'wb') as f:
                    f.write(content)
                    f.close()
        except OSError:
            print("writing songs:{0} is wrong!".format(song_name))

    def start_function(self):
        self.parse_origin()


if __name__ == '__main__':
    qq_music = QQMusic()
    qq_music.start_function()
