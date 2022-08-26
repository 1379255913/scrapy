import requests
from lxml import etree
import pymysql
import time

header = headers = {
    'Accept': 'text/html,application/xhtml xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400'}


class Crawl:
    def __init__(self):
        resp = requests.get("https://www.liepin.com/", headers=headers)
        self.tree = etree.HTML(resp.text)
        self.result = {}
        self.first_class_lst = self.tree.xpath('/html/body/section[8]/div/div[2]/ul/li')
        self.cnt = 0

    def job_division_url(self):  # 获取每个类别页面的url，以获取每一个职位的url
        for first_class in self.first_class_lst:
            # self.result[first_class.xpath('./a/text()')[0]] = []
            # print('大类：', first_class.xpath('./a/text()')[0])
            cur_first_class = first_class.xpath('./a/text()')[0]
            self.result[cur_first_class] = {}
            second_class_lst = first_class.xpath('./div/div')
            for second_class in second_class_lst:
                # print('中类', second_class.xpath('./a/text()')[0])
                cur_second_class = second_class.xpath('./a/text()')[0]
                self.result[cur_first_class][cur_second_class] = []
                smalls = second_class.xpath('./div/a')
                for s in smalls:
                    self.result[cur_first_class][cur_second_class].append((s.xpath('./text()')[0], s.xpath('@href')[0]))

    def job_urls(self, division_url):
        resp = requests.get(division_url, headers=headers)
        tree = etree.HTML(resp.text)
        lst = tree.xpath('//*[@class="job-name"]')
        for li in lst:
            job_name = li.xpath('./a/text()')[0]
            job_url = li.xpath('./a/@href')[0]
            yield job_name, job_url

    def save_data(self):
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="jobs",
            charset="utf8mb4")

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = f"insert into job_url(first_cls, second_cls, third_cls, job_name, job_url) values (%s, %s, %s, %s, %s);"
        for cur_first_cls in self.result.keys():
            for cur_second_cls in self.result[cur_first_cls].keys():
                for cur_third_cls in self.result[cur_first_cls][cur_second_cls]:
                    for job_name, job_url in self.job_urls(cur_third_cls[1]):
                        try:
                            cursor.execute(sql, [cur_first_cls, cur_second_cls, cur_third_cls[0], job_name, job_url])
                            # print(cur_first_cls, cur_second_cls, cur_third_cls[0], job_name, job_url)
                            print(self.cnt)
                            self.cnt += 1
                            if self.cnt % 100 == 0:
                                time.sleep(10)
                            conn.commit()
                        except pymysql.err.DataError:
                            print('啊哦')

        cursor.close()
        conn.close()

    def __call__(self):
        self.job_division_url()
        self.save_data()
        # print(self.result)


if __name__ == "__main__":
    crawl = Crawl()
    crawl()
