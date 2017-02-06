import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class EsperancehomesSpider(CrawlSpider):
    name = 'esperancehomes'
    allowed_domains = ['www.esperancehomes.com.au',
                       'www.l37.com.au']
    start_urls = ['http://www.esperancehomes.com.au',
                  'http://www.l37.com.au/']
    rules = (
        Rule(LinkExtractor(allow=('http://www.rawdonhill.com.au/our-homes/.*/$')), callback='parseOurhomes'),
        Rule(LinkExtractor(allow=('/house-and-land/(page/\d+/)?$')), follow=True),
        Rule(LinkExtractor(allow=('http://www.rawdonhill.com.au/house-and-land/.*/$')), callback='parseHL'),
        # Rule(LinkExtractor(allow=('/homes/new-home-designs/[\w-]+$')), callback='parseItem'),
    )

    logo = 'Rawdon Hill'





if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(EsperancehomesSpider)
    process.start()