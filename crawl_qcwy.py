# -*- coding:utf-8 -*-
# @descrip:前程无忧爬取
import time

import requests
import aiohttp
import asyncio
import re
from lxml import etree
import pandas as pd
import logging

data_file = "./data/"
location_file = './other/location.txt'

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Host": "jobs.51job.com",
}

# 设置爬虫的日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

df = pd.DataFrame(columns=['occupation', 'companyName', 'location', 'salary', 'date', 'education', 'experience', 'companyType', 'companySize', 'request'])


# 异步HTTP请求
async def fetch(sem11, session, url):
    async with sem11:
        async with session.get(url, headers=header) as response:
            return await response.content


# 解析网页
def parser(html):
    html = html.encode().decode(encoding='gbk', errors="ignore")
    match_html = etree.HTML(html)
    # 岗位
    occupations = match_html.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/div/p[1]/span[1]/a//text()')  # 需求值
    # print(occupations, len(occupations))
    # 学历  工作经验  公司性质  公司规模
    educations = []  # 需求值
    experiences = []  # 需求值
    company_types = []  # 需求值
    company_sizes = []  # 需求值
    total_content = match_html.xpath("/html/body/div[4]/div[2]/div[1]/div[2]/div/p[2]//text()")
    split_result = []
    pass_array = []
    for i in range(len(total_content)):
        pass_array.append(total_content[i])
        if (i + 1) % 7 == 0:
            split_result.append(pass_array)
            pass_array = []
    for i in split_result:
        one = re.compile('学历要求：(.*)', re.S).findall(i[0])
        two = re.compile('工作经验：(.*)', re.S).findall(i[2])
        three = re.compile('公司性质：(.*)', re.S).findall(i[4])
        four = re.compile('公司规模：(.*)', re.S).findall(i[6])
        if one[0] != '':
            educations.append(one[0])
        else:
            educations.append("无需求")
        if two[0] != '':
            experiences.append(two[0])
        else:
            experiences.append("默认")
        if three[0] != '':
            company_types.append(three[0])
        else:
            company_types.append("未知")
        if four[0] != '':
            company_sizes.append(four[0])
        else:
            company_sizes.append("0人")
    # print(educations, len(educations))
    # print(experiences, len(experiences))
    # print(company_types, len(company_types))
    # print(company_sizes, len(company_sizes))
    # 公司名称
    company_names = match_html.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/div/p[1]/a//text()')  # 需求值
    # print(company_names, len(company_names))
    # 所处位置
    locations = match_html.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/div/p[1]/span[2]//text()')  # 需求值
    # print(locations, len(locations))
    # 薪水
    salaries = re.compile('<span class="location">(.*?)</span>', re.S).findall(html)
    unity_salaries = []  # 需求值
    # print(salaries)
    for i in salaries:
        # print(i)
        if not i:
            unity_salaries.append("未提供")
            continue
        first, end = re.compile(r".*\d(.*)", re.S).findall(i)[0].split('/')
        result_s = list(map(float, re.compile(r"(.*\d).*", re.S).findall(i)[0].split('-')))
        if len(result_s) == 1:
            unity_salaries.append(f"{result_s[0] * 24 * 30}")
            continue
        low, high = map(float, re.compile(r"(.*\d).*", re.S).findall(i)[0].split('-'))
        new_low, new_high = 0, 0
        if first == '万' and end == '年':
            new_low, new_high = low / 12, high / 12
        if first == '万' and end == '月':
            new_low, new_high = low, high
        if first == '千' and end == '月':
            new_low, new_high = low / 10, high / 10
        if first == '元' and end == '小时':
            new_low, new_high = low * 24 * 30, high * 24 * 30
        unity_salaries.append(f"{new_low}-{new_high}")
    # print(salaries, len(salaries))
    # 发布日期
    dates = match_html.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/div/p[1]/span[4]//text()')  # 需求值
    # print(dates, len(dates))
    # 具体要求
    contents = [i.replace('\xa0', ' ').replace('\n', ' ') for i in match_html.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/div/p[3]//text()')]  # 需求值
    # print(contents, len(contents))
    # logger.info(str(df.shape[0]) + '\t' + name)
    # ['occupation', 'companyName', 'location', 'salary','date', 'education', 'experience', 'companyType', 'companySize', 'request']
    for i in list(zip(occupations, company_names, locations, unity_salaries, dates, educations, experiences, company_types, company_sizes, contents)):
        df.loc[df.shape[0] + 1] = list(i)
    logger.info(str(df.shape[0]) + '\t' + company_names[0])


# 处理网页
async def download(sem, url):
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch(sem, session, url)
            await parser(html)
        except Exception as err:
            print(err)


# def get_page(urls_page) -> list:
#     page_result = []
#     for url in urls_page[:]:
#         response = requests.get(url, headers=header)
#         try:
#             if response.status_code == 200:
#                 content = response.content.decode("gbk", errors="ignore")
#                 match_result = re.compile(r'<span class="td">共(\d+)页，到第</span>', re.S).findall(content)[0]
#                 page_result.append(match_result)
#         except Exception as e:
#             print(e)
#             print(url)
#     return page_result


if __name__ == '__main__':
    location = [(i.strip('\n').split(' ')[0], i.strip('\n').split(' ')[1]) for i in open(location_file).readlines()]
    urls = []
    page_list = [i[0] + f"hy01/p1" for i in location]
    # url构建
    for i in location:
        for k in range(1, int(i[1]) + 1):
            urls.append(i[0] + f"hy01/p{k}")
    # response = requests.get("https://jobs.51job.com/p4/", headers=header).content.decode("gbk", errors="ignore")
    # parser(response)

    # 统计该爬虫的消耗时间
    print('*' * 50)
    t_start_web = time.time()
    loop = asyncio.get_event_loop()
    sem1 = asyncio.Semaphore(100)
    tasks = [asyncio.ensure_future(download(sem1, url)) for url in urls[:]]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
    t_end_web = time.time()
    # 文件读取时间
    t_start_file = time.time()
    df.to_csv(data_file + 'result.csv', encoding='utf-8')
    t_end_file = time.time()

    print('网站爬取总共耗时：%s' % (t_end_web - t_start_web))
    print('文件读取总共耗时：%s' % (t_end_file - t_start_file))
    print('总共耗时：%s' % ((t_start_web - t_end_web) + (t_end_file - t_start_file)))
    print('*' * 50)
