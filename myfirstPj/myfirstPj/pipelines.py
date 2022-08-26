# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from pymysql.converters import escape_string


class MyfirstpjPipeline:
    def __init__(self, mysql_url, mysql_db, mysql_user, mysql_password):
        self.mysql_url = mysql_url
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.numbers = 1

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mysql_url=crawler.settings.get('MYSQL_URL'), mysql_db=crawler.settings.get('MYSQL_DB'),
                   mysql_user=crawler.settings.get('MYSQL_USER'), mysql_password=crawler.settings.get('MYSQL_PASSWORD'))

    def open_spider(self, spider):
        self.client = pymysql.connect(user=self.mysql_user, password=self.mysql_password, host=self.mysql_url,
                                      db=self.mysql_db)
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        table = 'jobslist'  # 数据库的表名
        data = {
            'number': str(self.numbers),
            'first_cls': item['cur_first_cls'],
            'second_cls': item['cur_second_cls'],
            'third_cls' : item['cur_third_cls'][0],
            'job': item['job'],
            'salary': item['salary'],
            'city': item['city'],
            'education': item['education'],
            'experience': item['experience'],
            'url': item['url'],
        }  # 存储的数据模板
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys,
                                                                     values=values)  # 储存入数据库的sql语句
        try:
            self.cursor.execute(sql, tuple(data.values()))
            print('第' + str(self.numbers) + '条爬取完成')
            self.numbers += 1
        except:
            print('第' + str(self.numbers) + '条爬取失败')
            self.client.rollback()
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.client.close()


class JobDetailPipeline:
    def __init__(self, mysql_url, mysql_db, mysql_user, mysql_password):
        self.mysql_url = mysql_url
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mysql_url=crawler.settings.get('MYSQL_URL'), mysql_db=crawler.settings.get('MYSQL_DB'),
                   mysql_user=crawler.settings.get('MYSQL_USER'), mysql_password=crawler.settings.get('MYSQL_PASSWORD'))

    def open_spider(self, spider):
        self.client = pymysql.connect(user=self.mysql_user, password=self.mysql_password, host=self.mysql_url,
                                      db=self.mysql_db)
        self.cursor = self.client.cursor()


    def process_item(self, item, spider):
        table = 'jobDetail'  # 数据库的表名
        data = {
            'number': item['number'],
            'job': item['job'],
            'city': item['city'],
            'salary': item['salary'],
            'education': item['education'],
            'experience': item['experience'],
            'goodList': str(item['goodList']),
            'needList': str(item['needList']),
            'jobInfo': item['jobInfo'],
            'company': item['company'],
            'companyType': item['companyType'],
            'companyPeople': item['companyPeople'],
            'companyPosition': item['companyPosition'],
            'companyInfo': item['companyInfo'],
        }  # 存储的数据模板
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys,
                                                                     values=values)  # 储存入数据库的sql语句
        try:
            self.cursor.execute(sql, tuple(data.values()))
            print('第' + item['number'] + '条爬取完成')
        except:
            print('第' + item['number'] + '条爬取失败')
            self.client.rollback()
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.client.close()
