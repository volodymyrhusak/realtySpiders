import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class L37Spider(CrawlSpider):
    name = 'l37'
    allowed_domains = ['www.l37.com.au']
    start_urls = ['http://www.l37.com.au/', 'http://www.l37.com.au/custom-home-portfolio/lt-600k/']
    rules = (
        Rule(LxmlLinkExtractor(allow=('/pre-designed-home-range/$')), follow=True, callback='parsePreDesigne'),
        Rule(LxmlLinkExtractor(allow=('/custom-home-portfolio/[\w-]+/$')), follow=True, callback='parsePortfolio'),
    )

    logo = 'Latitude 37'

    def parse(self, response):
        # if response.url == self.start_urls[2]:
        #     hxs = HtmlXPathSelector(response)
        #     itexsXpath = hxs.xpath('//div[@class="col-wrap home-location"]')
        #     for itemXpath in itexsXpath:
        #         link = itemXpath.xpath('.//div[1]/a[1]/@href').extract_first()
        #         link = self.start_urls[0][0:-1] + link
        #         print('!' * 50 + link)
        #         displayAt = itemXpath.xpath('.//div[2]/p[1]/text()').extract()
        #         pdfLink = itemXpath.xpath('.//div[@class="button medium"]/a/@href').extract_first()
        #         meta = { 'address':' '.join(displayAt).replace('\n', '').replace('\r', ''),
        #             'pdf':self.start_urls[0] + pdfLink}
        #         yield Request(link, callback=self.parseItem, dont_filter=True, meta=meta)
        # else:
        return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)

    def parsePreDesigne(self, response):
        singleLinks = LxmlLinkExtractor(allow=('/pre-designed-home-range/[\w-]+/$'),
                                        restrict_xpaths='//div[@id="double-storey"]/preceding-sibling::section').extract_links(
            response)

        doubleLinks = LxmlLinkExtractor(allow=('/pre-designed-home-range/[\w-]+/$'),
                                        restrict_xpaths='//div[@id="double-storey"]/following-sibling::section').extract_links(
            response)

        for link in singleLinks:
            meta = {'storey': 1}
            yield Request(link.url, callback=self.parseItem, dont_filter=True, meta=meta)
        for link in doubleLinks:
            meta = {'storey': 0}
            yield Request(link.url, callback=self.parseItem, dont_filter=True, meta=meta)
            # with open('testURL', 'a') as file:
            #     for l in doubleLinks:
            #         file.write(l.url + '\n')

    def parsePortfolio(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        itexsXpath = hxs.xpath('//div[@id="l37casestudies"]//section[@class="main-image"]')
        for itemXpath in itexsXpath:
            link = itemXpath.xpath('.//a/@href').extract_first()
            link = self.start_urls[0][0:-1] + link
            singlestorey = itemXpath.xpath('.//section/section/ul/li/@singlestorey').extract_first()
            meta = {'storey': int(singlestorey)}
            # with open('testURL', 'a') as file:
            #     file.write(referer+link +'   '+ singlestorey + '\n')
            yield Request(link, callback=self.parseItem, dont_filter=True, meta=meta)

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        # with open('testURL', 'a') as file:
        #     file.write(response.url + '   ' + referer + '\n')
        hxs = HtmlXPathSelector(response)
        BuildType = self._getBuildType(referer)
        imgXpath = '''//ul[@class="slides"]/li[{}]/img/@src'''
        # descriptionXPath = '//div[@id="listing_options"]/ul/li/text()'
        # areaXpath = '//div[@class="table-light"]/table/tbody/tr/td[text()="{}"]/following-sibling::td[1]/text()'
        # roomsXpath = '''//h1[text()="Room dimensions"]/following-sibling::
        #                         dl/dt[text()="{}"]/following-sibling::dd[1]/text()'''
        # data = hxs.xpath(roomsXpath).extract()
        # with open('testURL','a') as file:
        #     for i in data:
        #         file.write(i+'\n')
        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', BuildType)
        l.add_value('BuilderLogo', self.logo)
        if BuildType == 'Display Homes':
            l.add_value('Lot_BlockAddress', response.meta['address'])
        else:
            if response.meta['storey']:
                l.add_value('Storey', '1')
            else:
                l.add_value('Storey', '2')

        l.add_xpath('DesignName', '//div[@class="banner-content stick-bar"]//h2/text()')

        l.add_xpath('Bedrooms', '//span[@class="ico-beds"]/ancestor::li/text()')
        l.add_xpath('Bathrooms', '//span[@class="ico-baths"]/ancestor::li/text()')
        l.add_xpath('Garage', '//span[@class="ico-garage"]/ancestor::li/text()')
        #
        l.add_xpath('HouseWidth', '//th[text()="House Width"]/following-sibling::td/text()')
        l.add_xpath('HouseLength', '//th[text()="House Length"]/following-sibling::td/text()')
        l.add_xpath('GarageDimension', '//th[text()="Garage"]/following-sibling::td/text()')
        l.add_xpath('AlfrescoDimension', '//th[text()="Alfresco"]/following-sibling::td/text()')
        l.add_xpath('Alfresco_Yes_No', '//th[text()="Alfresco"]/following-sibling::td/text()')
        if BuildType == 'Portfolio':
            l.add_xpath('Squares',
                        'string(//div[@class="col-3 floor-plan-legend"]/p)', **{'re': '(?<=AREA|Area).*'})
        else:
            l.add_xpath('Squares',
                        '//th[text()="Total Area"]/following-sibling::td/text()')
        # l.add_xpath('MasterBedroomDimension', [roomsXpath.format('Master Bed'), roomsXpath.format('Bedroom 1')])
        # l.add_xpath('Bedroom2Dimension', [roomsXpath.format('Bed 2'), roomsXpath.format('Bedroom 2')])
        # l.add_xpath('Bedroom3Dimension', [roomsXpath.format('Bed 3'), roomsXpath.format('Bedroom 3')])
        # l.add_xpath('Bedroom4Dimension', [roomsXpath.format('Bed 4'), roomsXpath.format('Bedroom 4')])
        # l.add_xpath('Study_Yes_No', [roomsXpath.format('Study'), roomsXpath.format('Study')])
        # l.add_xpath('StudyDimension', [roomsXpath.format('Study'), roomsXpath.format('Study (ground floor)'),
        #                                roomsXpath.format('Study (first floor)'),
        #                                roomsXpath.format('Study (First floor)')])
        # l.add_xpath('FamilyDimension', [roomsXpath.format('Family')])
        # l.add_xpath('Meals_DiningDimension',
        #             [roomsXpath.format('Family / Meals'), roomsXpath.format('Meals/Family'),
        #              roomsXpath.format('Living / Meals'), roomsXpath.format('Meals')])
        # l.add_xpath('TheatreDimension', [roomsXpath.format('Theatre')])
        #
        l.add_xpath('BrochureImage_pdf',
                    '//a[text()="Download the Floor Plan"]/@href', **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('InclusionsImage_pdf',
                    '//a[text()="Download the Inclusions Brochure "]/@href', **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('BasePrice',
                    '''//a[text()="Download the Price List"]/@href''', **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('FloorPlanImage1', '//div[@class="col-wrap floor-plan-box"]//img/@src',
                    **{'myRefer': self.start_urls[0]})
        l.add_xpath('HomeDesignMainImage', '//section[@id="overview-anhor"]//img/@src',
                    **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image1', imgXpath.format('1'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image2', imgXpath.format('2'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image3', imgXpath.format('3'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image4', imgXpath.format('4'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image5', imgXpath.format('5'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image6', imgXpath.format('6'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image7', imgXpath.format('7'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image8', imgXpath.format('8'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image9', imgXpath.format('9'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image10', imgXpath.format('10'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image11', imgXpath.format('11'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image12', imgXpath.format('12'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image13', imgXpath.format('13'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image14', imgXpath.format('14'), **{'myRefer': self.start_urls[0][0:-1]})
        l.add_xpath('Image15', imgXpath.format('15'), **{'myRefer': self.start_urls[0][0:-1]})

        return l.load_item()

    def _getBuildType(self, url):
        if url.find('custom-home-portfolio') != -1:
            return 'Portfolio'
        elif url.find('display-homes') != -1:
            return 'Display Homes'
        elif url.find('pre-designed-home-range') != -1:
            return 'Pre-designed Home Range'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(L37Spider)
    process.start()
