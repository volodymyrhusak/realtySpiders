import json
import ast
import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector
from ..items import RealtyspidersItem
from misc.spider import CommonSpider


class OrphanLoader(XPathItemLoader):
    default_output_processor = TakeFirst()


class CodeguidaSpider(CrawlSpider):
    name = 'frenkenhomes'
    allowed_domains = ['www.frenkenhomes.com.au']
    start_urls = ['http://www.frenkenhomes.com.au/']
    rules = (
        Rule(LinkExtractor(allow=('/search/c/z/Display\+Homes')), callback='parse_1', follow=True),
        Rule(LinkExtractor(allow=('/search/c/z/Home\+Designs')), callback='parse_1', follow=True),
        Rule(LinkExtractor(allow=('/search/sales/houseandland/')), callback='parse_1', follow=True),
        Rule(LinkExtractor(allow=('/search/c/z/house\+and\+land\+spec\+home/')), callback='parse_1', follow=True),
    )

    con = {'Display+Homes': 'Display Homes',
           'Home+Designs': 'Home Designs',
           'houseandland': 'houseandland',
           'house+and+land+spec+home': 'house and land spec home'
           }

    def parse_1(self, response):
        # self.BuildType = response.url.split('/')[-1]
        hxs = Selector(response)
        links = hxs.xpath('//a[@class="home-feature-read-more viewdetails"]/@href').extract()
        # print(links)
        for url in links:
            url = 'http://www.frenkenhomes.com.au' + url
            yield Request(url, callback=self.parseItem)

    def parseItem(self, response):
        hxs = HtmlXPathSelector(response)
        BuildType = str(response.request.headers.get('Referer', None))
        BuildType = self.getBuildType(BuildType)

        l = OrphanLoader(RealtyspidersItem(), hxs)
        l.add_value('BuildType', BuildType)
        l.add_value('State', 'VIC')
        l.add_value('Region', 'MELBOURNE')
        if BuildType == 'Home Designs':
            l.add_xpath('DesignName', '//h2[@class="darkblue lowercase"]/text()')
        l.add_xpath('Squares', '//*[@id="details"]/tr/th[text()="Floor Area"]/following-sibling::td/text()')
        l.add_xpath('Bedrooms', '//*[@id="details"]/tr/th[text()="Bedrooms"]/following-sibling::td/text()')
        l.add_xpath('Bathrooms', '//*[@id="details"]/tr/th[text()="Bathrooms"]/following-sibling::td/text()')
        l.add_xpath('Garage', '//*[@id="details"]/tr/th[text()="Garages"]/following-sibling::td/text()')
        l.add_xpath('LandSize', '//*[@id="details"]/tr/th[text()="Land Area"]/following-sibling::td/text()')
        l.add_xpath('HomeDesignMainImage', '//li[@id="img1"]/a/img/@src')
        l.add_xpath('FloorPlanImage1',
                    '//div[@class="property-details-buttons"]/a/span[text()="Floor Plan"]/ancestor::a/@href')
        l.add_xpath('Image1', '//li[@id="img1"]/a/img/@src')
        l.add_xpath('Image2', '//li[@id="img2"]/a/img/@src')
        l.add_xpath('Image3', '//li[@id="img3"]/a/img/@src')
        l.add_xpath('Image4', '//li[@id="img4"]/a/img/@src')
        l.add_xpath('Image5', '//li[@id="img5"]/a/img/@src')
        l.add_xpath('Image6', '//li[@id="img6"]/a/img/@src')
        l.add_xpath('Image7', '//li[@id="img7"]/a/img/@src')
        l.add_xpath('Image8', '//li[@id="img8"]/a/img/@src')
        l.add_xpath('Image9', '//li[@id="img9"]/a/img/@src')
        l.add_xpath('Image10', '//li[@id="img10"]/a/img/@src')
        l.add_xpath('Image11', '//li[@id="img11"]/a/img/@src')
        l.add_xpath('Image12', '//li[@id="img12"]/a/img/@src')
        l.add_xpath('Image13', '//li[@id="img13"]/a/img/@src')
        l.add_xpath('Image14', '//li[@id="img14"]/a/img/@src')
        l.add_xpath('Image15', '//li[@id="img15"]/a/img/@src')
        l.add_value('BuilderLogo', 'Frenken Homes')
        return l.load_item()

    def getBuildType(self, BuildType):
        for v in self.con:
            if BuildType.find(v) != -1:
                return self.con[v]


p = CodeguidaSpider()
p.start_requests()
