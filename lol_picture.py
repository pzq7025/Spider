import requests
import json
from multiprocessing import Pool
import os

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}


def get_start(n):
    """
    获取所有英雄id
    :param n:
    :return:
    """
    url = 'https://lol.qq.com/biz/hero/champion.js'
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            parse_hero(response.content.decode('utf-8'))
        return None
    except TimeoutError:
        raise Exception("response is overtime")


def parse_hero(content):
    """
    处理获取的json文件获得英雄的id和name
    :param content:
    :return:
    """
    lol_js = json.loads(content.replace('if(!LOLherojs)var LOLherojs={};LOLherojs.champion=', '').replace(';', ''))
    for hero in lol_js.get('keys').items():  # lol_js.get('keys').items() object is a dict
        get_picture(hero)


def get_picture(hero):
    """
    获取每个英雄所有图片的信息
    :param hero: id name
    :return:
    """
    url = 'https://lol.qq.com/biz/hero/' + hero[1] + '.js'
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            detail_js_hero(response.content.decode('utf-8'), hero)
    except TimeoutError:
        raise Exception("time is out!")


def detail_js_hero(content, hero):
    """
    处理每个图片的信息
    :param content:
    :param hero: id name
    :return:
    """
    hero_js = json.loads(content.replace('if(!LOLherojs)var LOLherojs={champion:{}};LOLherojs.champion.' + hero[1] + '=', '').replace(';', ''))
    for one in hero_js.get('data').get('skins'):
        picture_id = one.get('id')
        hero_name = one.get('name')
        get_download(picture_id, hero_name, hero)


def get_download(picture_id, hero_name, hero):
    """
    下载图片得信息
    :param picture_id:
    :param hero_name:
    :param hero:
    :return:
    """
    hero_pic = 'https://ossweb-img.qq.com/images/lol/web201310/skin/big' + str(picture_id) + '.jpg'
    try:
        response = requests.get(hero_pic, headers=header)
        if response.status_code == 200:
            store_pic(response.content, (hero_name, picture_id), hero)
    except TimeoutError:
        raise Exception("time is out!")


def store_pic(content, hero_name_p, hero):
    """
    存储图片的信息
    :param content:
    :param hero_name_p:
    :param hero:
    :return:
    """
    print(f"正在下载:{hero_name_p[0]}")
    if not os.path.exists("..\\store_pic\\" + hero[1]):
        os.mkdir("..\\store_pic\\" + hero[1])
    path = "..\\store_pic\\" + hero[1] + '\\' + hero_name_p[1]
    if not os.path.exists(path):
        try:
            path = path + '.jpg'
            with open(path, 'wb') as f:
                f.write(content)
                f.close()
        except OSError:
            print(f"下载失败:{hero_name_p[0]}", path)


if __name__ == '__main__':
    """ 进程的开启 """
    ground = [x for x in range(200)]
    pool = Pool(5)
    pool.map(get_start, ground)
