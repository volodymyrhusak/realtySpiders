import json
import ast
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from ..items import DemoSpidersItem
from misc.spider import CommonSpider


class CodeguidaSpider(CommonSpider):
    name = "demo1"
    allowed_domains = ["www.freshfields.com"]
    start_urls = ["http://www.freshfields.com/PeopleFinder.aspx?searchQuery=&locationName=&practiceGroup=&role=&language=en&region=global"]
    rules = [Rule(LinkExtractor(allow=('/profiles/')), callback='parse_1', follow=True)]
    LinkExtractor()
    list_css_rules = {
            'employeeName': 'h1.mobile_profiles::text',
            'emailAddress': '#ctl00_ContentPlaceHolder1_ProfileUc1_lnkEmail::text'
    }

    def parse_1(self, response):
        dataList = self.parse_with_rules(response, self.list_css_rules, dict)
        print('type(dataList) ',type(dataList[0]))
        data = DemoSpidersItem()
        # print('dataList[employeeName] ' + str(dataList['employeeName']))
        # print('dataList[emailAddress] ' + str(dataList['emailAddress']))
        data['employeeName'] = dataList[0]['employeeName'][0]
        data['emailAddress'] = dataList[0]['emailAddress'][0]
        return data


p = CodeguidaSpider()
p.start_requests()