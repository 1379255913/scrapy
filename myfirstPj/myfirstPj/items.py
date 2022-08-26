# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    cur_first_cls = scrapy.Field()
    cur_second_cls = scrapy.Field()
    cur_third_cls = scrapy.Field()
    job = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    url = scrapy.Field()

class JobDetailsItem(scrapy.Item):
    number = scrapy.Field()
    job = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    goodList = scrapy.Field()
    needList = scrapy.Field()
    jobInfo = scrapy.Field()
    company = scrapy.Field()
    companyType = scrapy.Field()
    companyPeople = scrapy.Field()
    companyPosition = scrapy.Field()
    companyInfo = scrapy.Field()
