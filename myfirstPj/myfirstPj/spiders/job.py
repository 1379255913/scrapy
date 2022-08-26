import scrapy

from .jobtype import jobtype
from ..items import JobItem


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['www.liepin.com']
    # start_urls = ['https://www.liepin.com/career/java/pn0/']

    def start_requests(self):
        result = jobtype()
        for cur_first_cls in result.keys():
            for cur_second_cls in result[cur_first_cls].keys():
                for cur_third_cls in result[cur_first_cls][cur_second_cls]:
                    for i in range(10):
                        yield scrapy.Request(url=cur_third_cls[1]+'pn'+str(i), callback=self.parse, meta={'cur_first_cls':cur_first_cls,'cur_second_cls':cur_second_cls,'cur_third_cls':cur_third_cls}, dont_filter=True)
        # yield scrapy.Request(url='https://www.liepin.com/career/java/pn0', callback=self.parse)


    def parse(self, response):
        item = JobItem()
        JObList = response.xpath("/html/body[@id='sojob']/div[@class='container']/div[@class='wrap']/div[@class='job-content']/div[@class='sojob-result']/ul[@class='sojob-list']/li")
        for i in JObList:
            item['cur_first_cls'] = response.meta['cur_first_cls']
            item['cur_second_cls'] = response.meta['cur_second_cls']
            item['cur_third_cls'] = response.meta['cur_third_cls']
            item['job'] = i.xpath('./div/div[1]/span/a/text()').get()
            item['salary'] = i.xpath('./div/div[1]/p[1]/span[1]/text()').get()
            item['city'] = i.xpath('./div/div[1]/p[1]/span[2]/text()').get()
            item['education'] = i.xpath('./div/div[1]/p[1]/span[3]/text()').get()
            item['experience'] = i.xpath('./div/div[1]/p[1]/span[4]/text()').get()
            item['url'] = i.xpath('./div/div[1]/span/a/@href').get()
            yield item
