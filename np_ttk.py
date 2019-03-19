import requests
import json
from requests import RequestException
from collections import Counter
import matplotlib.pyplot as plt


class LotteryTicket:
    def __init__(self):
        header = {
            'Referer': 'http://www.cwl.gov.cn/kjxx/ssq/kjgg/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        }
        data = {
            'name': 'ssq',
            'issueCount': '100'
        }
        self.data = data
        self.header = header
        # red:store the red number
        # blue:store the blue number
        self.red = []
        self.blue = []
        # store x value of number store y value of value
        self.blue_label = []
        self.red_label = []
        self.blue_value = []
        self.red_value = []

    def parse_html(self):
        url = 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?'
        try:
            response = requests.get(url, params=self.data, headers=self.header)
            if response.status_code == 200:
                self.parse_json(response.text)
                self.draw()
        except RequestException:
            print(RequestException)

    def parse_json(self, json_content):
        # count = 0
        contents = json.loads(json_content).get('result')
        for content in contents:
            # count = 0
            blue = content.get('blue')
            red = content.get('red')
            print("红色中奖号码：{0};蓝色中奖号码：{1}".format(red, blue))
            red_number = red.split(',')
            blue_number = blue.split(',')
            for number_r in red_number:
                # if number_b == '02':
                #     count += 1
                self.red.append(number_r)
            for number_b in blue_number:
                # if number_r == '02':
                #     count += 1
                # self.red.append(red_number)
                self.blue.append(number_b)
        # List_red = Counter(self.red)
        # List_blue = Counter(self.blue)
        # for red_1 in List_red:
        #     self.x.append(red_1[0])
        #     self.y.append(red_1[1])
        # for blue_1 in List_blue:
        #     self.x.append(blue_1[0])
        #     self.y.append(blue_1[1])
        self.detail()

    def detail(self):
        # print(self.red)
        # print(self.blue)
        # exit()
        list_red = Counter(self.red)
        list_blue = Counter(self.blue)
        # print(list_red)
        # print(list_blue)
        # exit()
        for red_1 in list_red.items():
            self.red_label.append(red_1[0])
            self.red_value.append(red_1[1])
        for blue_1 in list_blue.items():
            self.blue_label.append(blue_1[0])
            self.blue_value.append(blue_1[1])

    def draw(self):
        # labels = 'A', 'B', 'C', 'D'
        # fracs = [15, 30.55, 44.44, 10]
        # explode = [0, 0.1, 0, 0]  # 0.1 凸出这部分，
        plt.axes(aspect=2)  # set this , Figure is round, otherwise it is an ellipse
        # autopct ，show percet
        plt.pie(x=self.red_value, labels=self.red_label, autopct='%3.1f %%',
                shadow=True, labeldistance=1.2, startangle=0, pctdistance=1.5
                )

        # plt.savefig('./test1.jpg')
        plt.show()
        plt.pie(x=self.blue_value, labels=self.blue_label, autopct='%3.1f %%',
                shadow=True, labeldistance=0.9, startangle=0, pctdistance=1.2
                )
        # plt.savefig('./test2.jpg')
        plt.show()


if __name__ == '__main__':
    lotteryticket = LotteryTicket()
    lotteryticket.parse_html()
