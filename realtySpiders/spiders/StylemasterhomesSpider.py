import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class StylemasterhomesSpider(CrawlSpider):
    name = 'stylemasterhomes'
    allowed_domains = ['stylemasterhomes.com.au']
    start_urls = ['http://stylemasterhomes.com.au']
    rules = (
        Rule(LxmlLinkExtractor(allow=('http://stylemasterhomes.com.au/home-designs/$')), callback='getAjax',
             follow=True),
        # Rule(LxmlLinkExtractor(allow=('http://stylemasterhomes.com.au/sale/$')), follow=True),
        # Rule(LxmlLinkExtractor(allow=('http://stylemasterhomes.com.au/display-homes/$')), follow=True),
        Rule(LxmlLinkExtractor(allow=('http://stylemasterhomes.com.au/home/[\w-]+/$')),
             callback='parseItem'),
        # Rule(LxmlLinkExtractor(allow=('http://stylemasterhomes.com.au/display-home/[\w-]+/$')),
        #      callback='parseItem'),
        # Rule(LxmlLinkExtractor(allow=('http://stylemasterhomes.com.au/sale/[\w-]+/$')),
        #      callback='parseItem'),
    )

    logo = 'Latitude 37'

    def getAjax(self, response):
        url = 'http://stylemasterhomes.com.au/wp-admin/admin-ajax.php'
        formdata ={'action':'getOurHomeResults',
                    'lotLengthLower':'0',
                    'lotLengthUpper':'40',
                    'lotWidthLower':'0',
                    'lotWidthUpper':'40',
                    'homeSizeLower':'15',
                    'homeSizeUpper':'40',
                    'className':'storeys-section',
                    'filterSwitch':'1',
                    'switchFirst':'1'}
        headers = {'Accept':'*/*',
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                    'X-Requested-With':'XMLHttpRequest'}
        s = '''action=list_homes&params=%7B%22bedrooms%22%3A%22%22%2C%22home-series%22%3A%22%22%2C%22
            slider-price-range-min%22%3A%22100%22%2C%22slider-price-range-max%22%3A%22600%22%2C%22
            slider-block-range-min%22%3A%225%22%2C%22slider-block-range-max%22%3A%2240%22%2C%22
            slider-home-area-min%22%3A%22120%22%2C%22slider-home-area-max%22%3A%22500%22%2C%22
            homes-page%22%3A%22{}%22%7D'''
        ss = '''?action=list_homes&params=%7B%22bedrooms%22%3A%22%22%2C%22home-series%22%3A%22%22%2C%22slider-price-range-min%22%3A%22100%22%2C%22slider-price-range-max%22%3A%22600%22%2C%22slider-block-range-min%22%3A%225%22%2C%22slider-block-range-max%22%3A%2240%22%2C%22slider-home-area-min%22%3A%22120%22%2C%22slider-home-area-max%22%3A%22500%22%2C%22homes-page%22%3A%222%22%7D'''
            # yield Request(url, method='POST', callback=self.parseItem, dont_filter=True,headers=headers)
        requests = FormRequest(url=url,formdata=formdata,callback=self.parseItem, dont_filter=True,
                               headers=headers)
        return requests

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        # links = LxmlLinkExtractor(allow=('http://stylemasterhomes.com.au/home/[\w-]+/$')).extract_links(response)
        # for link in links:
        # with open('testURL', 'a') as file:
        # with open('data.html', 'a') as file:
        #     # file.write(response.url + '   ' + referer + '\n')
        #     file.write(str(response.body))

    def _getBuildType(self, url):
        if url.find('custom-home-portfolio') != -1:
            return 'Portfolio'
        elif url.find('display-homes') != -1:
            return 'Display Homes'
        elif url.find('pre-designed-home-range') != -1:
            return 'Pre-designed Home Range'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(StylemasterhomesSpider)
    process.start()
