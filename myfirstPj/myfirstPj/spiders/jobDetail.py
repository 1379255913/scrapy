import scrapy

from ..items import JobDetailsItem

class JobSpider(scrapy.Spider):
    name = 'jobDetail'
    allowed_domains = ['www.liepin.com']
    # start_urls = ['https://www.liepin.com/career/java/pn0/']

    def start_requests(self):
        # for cur_first_cls in result.keys():
        #     for cur_second_cls in result[cur_first_cls].keys():
        #         for cur_third_cls in result[cur_first_cls][cur_second_cls]:
        #             for i in range(10):
        #                 yield scrapy.Request(url=cur_third_cls[1]+'pn'+str(i), callback=self.parse, meta={'cur_first_cls':cur_first_cls,'cur_second_cls':cur_second_cls,'cur_third_cls':cur_third_cls}, dont_filter=True)
        # yield scrapy.Request(url='https://www.liepin.com/career/java/pn0', callback=self.parse)
        with open("jobslist.csv", 'r', encoding="utf-8") as f:
            lines = f.readline().replace("'", '')
            while lines:
                t = (lines.split(",")[0])
                url = lines.split(",")[-1].strip()
                print(t,url)
                lines = f.readline().replace("'", '')
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'number':t})


    def parse(self, response):
        def format_ans(data):
            if data: return data
            return ''
        item = JobDetailsItem()
        item['number'] = response.meta['number']
        item['job'] = response.xpath('/html/body/section[3]/div[1]/div[1]/span[1]/text()').get()
        item['salary'] = response.xpath('/html/body/section[3]/div[1]/div[1]/span[2]/text()').get()
        item['city'] = response.xpath('/html/body/section[3]/div[1]/div[2]/span[1]/text()').get()
        item['experience'] = response.xpath('/html/body/section[3]/div[1]/div[2]/span[3]/text()').get()
        item['education'] = response.xpath('/html/body/section[3]/div[1]/div[2]/span[5]/text()').get()
        goodListDetail = list()
        goodList = response.xpath('/html/body/section[4]/div/div[1]/span')
        if goodList:
            for i in goodList:
                goodListDetail.append(i.xpath('./text()').get())
        item['goodList'] = goodListDetail
        needListDetail = list()
        needList = response.xpath('/html/body/main/content/section[2]/dl[1]/div/ul/li')
        if needList:
            for i in needList:
                needListDetail.append(i.xpath('./text()').get())
        item['needList'] = needListDetail
        item['jobInfo'] = response.xpath('/html/body/main/content/section[2]/dl/dd/text()').get()
        item['company'] = format_ans(response.xpath('/html/body/main/aside/div[2]/div[1]/div[1]/div[1]/text()').get())
        item['companyType'] = format_ans(response.xpath('/html/body/main/aside/div[2]/div[2]/div[1]/span[2]/text()').get())
        if response.xpath('/html/body/main/aside/div[2]/div[2]/div[2]/span[1]/text()').get()=='融资阶段：':
            item['companyPeople'] = format_ans(response.xpath('/html/body/main/aside/div[2]/div[2]/div[3]/span[2]/text()').get())
            item['companyPosition'] = format_ans(response.xpath('/html/body/main/aside/div[2]/div[2]/div[4]/span[2]/text()').get())
        else:
            item['companyPeople'] = format_ans(response.xpath('/html/body/main/aside/div[2]/div[2]/div[2]/span[2]/text()').get())
            item['companyPosition'] = format_ans(response.xpath('/html/body/main/aside/div[2]/div[2]/div[3]/span[2]/text()').get())
        item['companyInfo'] = format_ans(response.xpath('/html/body/main/content/section[3]/div/div/text()').get())
        print(item)
        yield item
