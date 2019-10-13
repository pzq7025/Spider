# -*- coding:utf-8 -*-
# !bin/python/even
# author:pzq
import requests
from requests import RequestException
import json
from multiprocessing import Pool
import csv


class Moc:
    def __init__(self):
        #  -------------------------------------------------------------------- 课程信息 --------------------------------------------------------------------
        self.url = 'https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc?csrfKey=3cb97562f2394e6aa74e0a7ec5926bb1'
        self.header = {
            'referer': 'https://www.icourse163.org/category/all',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'cookie': 'EDUWEBDEVICE=f39e36ae944a46de9a3b4b88722c09cb; hb_MA-A976-948FFA05E931_source=www.google.com; __utmz=63145271.1570872141.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); MOOC_PRIVACY_INFO_APPROVED=true; WM_TID=88rIxVmOMeJAVAREFFNt4tr6ZCyyiH8A; bpmns=1; NTESSTUDYSI=3cb97562f2394e6aa74e0a7ec5926bb1; __utma=63145271.1003410384.1570872141.1570932686.1570945065.6; __utmc=63145271; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1570872138,1570924613,1570945065; WM_NI=1zqPtOXslrZPQBN17uwL0Lrya4tUrdFDCPV22qhrxbqF8QB%2B0Nrj5eMv6K7UGiUyhYdE6S3VVfgR0NYM4RrKFKb%2BRD%2BZvwLyFYsGEjCsTSOQRX0xSvAhgWJB%2FoSoRfYGTW8%3D; '
                      'WM_NIKE=9ca17ae2e6ffcda170e2e6ee85d765f8ecaebab47fa3ef8fa6c15a978f9bbbb734b68aab89b680b1969da5ec2af0fea7c3b92af3a6bfb1f7459cada493d95c939e82d2b67fb59400adf173a3ecbcb6f170869c8db1d53af2afa893fb6ab39af8b2c121f492be8bb86f8faafaacb65f85b79b9aeb53a89bfab4b25e96baa9b3b3469b93fcb3f1418695aeccd150e986ba98cf738687bda8c86281ad9cb4ce5b92880099d27e83b8a9b8c94aedb19d90d16e9b999cb8bb37e2a3; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1570947389',
        }
        # ---------------------------------------------------------------------- 课程评论 --------------------------------------------------------------------
        self.url_c = 'https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=3cb97562f2394e6aa74e0a7ec5926bb1'
        self.header_c = {
            'referer': 'https://www.icourse163.org/course/TONGJI-53004',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'cookie': 'EDUWEBDEVICE=f39e36ae944a46de9a3b4b88722c09cb; hb_MA-A976-948FFA05E931_source=www.google.com; __utmz=63145271.1570872141.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); MOOC_PRIVACY_INFO_APPROVED=true; WM_TID=88rIxVmOMeJAVAREFFNt4tr6ZCyyiH8A; bpmns=1; NTESSTUDYSI=3cb97562f2394e6aa74e0a7ec5926bb1; __utmc=63145271; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1570872138,1570924613,1570945065; WM_NI=1zqPtOXslrZPQBN17uwL0Lrya4tUrdFDCPV22qhrxbqF8QB%2B0Nrj5eMv6K7UGiUyhYdE6S3VVfgR0NYM4RrKFKb%2BRD%2BZvwLyFYsGEjCsTSOQRX0xSvAhgWJB%2FoSoRfYGTW8%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee85d765f8ecaebab47fa3ef8fa6c15a978f9bbbb734b68aab89b680b1969da5ec2af0fea7c3b92af3a6bfb1f7459cada493d95c939e82d2b67fb59400adf173a3ecbcb6f170869c8db1d53af2afa893fb6ab39af8b2c121f492be8bb86f8faafaacb65f85b79b9aeb53a89bfab4b25e96baa9b3b3469b93fcb3f1418695aeccd150e986ba98cf738687bda8c86281ad9cb4ce5b92880099d27e83b8a9b8c94aedb19d90d16e9b999cb8bb37e2a3; '
                      '__utma=63145271.1003410384.1570872141.1570947390.1570953812.8; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1570954316; __utmb=63145271.12.9.1570954326990',
        }
        self.course_infos = []  # 存储所有的课程信息
        self.ids = []  # 存储所有的id信息  用来抓取评论的内容
        self.comments = []  # 存储所有的评论信息

    # ----------------------------------------------------------------------------- 课程信息 -----------------------------------------------------------------
    def get_url(self, n):
        data = {
            'categoryId': '-1',
            'type': '30',
            'orderBy': '0',
            'pageIndex': str(n),
            'pageSize': '20',
        }
        response = requests.post(self.url, data=data, headers=self.header)
        try:
            if response.status_code == 200:
                self.parse_web(response.content.decode('utf-8'))
        except RequestException:
            print("Response is Wrong!")

    def parse_web(self, content):
        parse_content = json.loads(content)
        course_infos = parse_content.get('result').get('result')
        if course_infos:
            for course_info in course_infos:
                course_id = course_info.get('id')  # 课程id
                self.ids.append(course_id)
                course_name = course_info.get('name')  # 课程的名字
                school_name = course_info.get('schoolPanel').get('name')  # 开课的学校的名字
                teacher_name = [[i.get('realName'), i.get('lectorTitle')] for i in course_info.get('termPanel').get('lectorPanels') if i.get('realName') or i.get('lectorTitle')]  # 开课的老师的名字
                learner = course_info.get('learnerCount')
                special_tag = []
                if course_info.get('mocTagDtos'):
                    special_tag.append(course_info.get('mocTagDtos')[0].get('name'))
                detail_name = []
                for i, k in teacher_name:
                    if k is None:
                        detail_name.append(i)
                    else:
                        detail_name.append(i + '\\' + k)
                self.course_infos.append([course_id, course_name, school_name, learner, ''.join(special_tag), ' '.join(detail_name)])
                content = [course_id, course_name, school_name, learner, ''.join(special_tag), ' '.join(detail_name)]
                self.write_csv(content)
                print(f"正在下载{course_id}")
                for i in range(50):
                    self.get_comments(course_id, i)
                # print(course_id, course_name, school_name, learner, ''.join(special_tag), ' '.join(detail_name))

    # --------------------------------------- 用户评论 ----------------------------------------
    def get_comments(self, one_id, n):
        data = {
            'courseId': str(one_id),
            'pageIndex': str(n),
            'pageSize': '20',
            'orderBy': '3',
        }
        response = requests.post(self.url_c, data=data, headers=self.header_c)
        try:
            if response.status_code == 200:
                self.parse_comment(response.content.decode('utf-8'), one_id)
        except RequestException:
            print("Response is Wrong!")

    def parse_comment(self, content, one_id):
        parse_content = json.loads(content)
        comments = parse_content.get('result').get('list')
        if comments:
            for one in comments:
                comment = one.get('content')
                agree_counter = one.get('agreeCount')
                if comment:
                    comments = [one_id, agree_counter, comment]
                    self.write_csv_c(comments)

    def write_csv(self, source):
        # 存取信息
        try:
            with open('./source_data/source_info.csv', 'a', encoding='utf-8-sig', newline='', ) as source_f:
                source_csv = csv.writer(source_f)
                # 存入信息
                # source_csv.writerow(["id", "name", "university", "learner", "Tag", 'teacher'])
                source_csv.writerow(source)
        except IOError:
            print("Write is Wrong!")

    def write_csv_c(self, comment):
        # 存取信息
        try:
            with open('./source_data/source_comments.csv', 'a', encoding='utf-8-sig', newline='', ) as comment_f:
                comment_csv = csv.writer(comment_f)
                # 存入评论
                # comment_csv.writerow(["id", "agree_counter", "comments"])
                comment_csv.writerow(comment)
        except IOError:
            print("Write is Wrong!")

    def start(self):
        pool = Pool()
        # ------------------------- 爬取course的多进程 --------------------------------------------------
        grounds = [i for i in range(199)]
        pool.map(self.get_url, grounds)


if __name__ == '__main__':
    moc = Moc()
    moc.start()
