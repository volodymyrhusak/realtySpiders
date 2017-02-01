import json
import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class NostrahomesSpider(CrawlSpider):
    name = 'nostrahomes'
    allowed_domains = ['nostrahomes.com.au']
    start_urls = ['http://nostrahomes.com.au',
                  'http://nostrahomes.com.au/home_designs.php?stories=2%20AND%202',
                  'http://nostrahomes.com.au/home_designs.php?stories=1%20AND%201']
    rules = (
        # Rule(LinkExtractor(allow=('/home_designs\.php'))),
        Rule(LinkExtractor(allow=('single_design\.php\?id=[0-9]+&name=\w+')), callback='parse1'),
        Rule(LinkExtractor(allow=('/mova\.php'))),
        Rule(LinkExtractor(allow=('range\.php\?name=.+&id=[0-9]+'))),
        Rule(LinkExtractor(allow=('/house_land\.php'))),
        Rule(LinkExtractor(allow=('/house-land-packages\.php')), callback='parse2'),
        Rule(LinkExtractor(allow=('/white-hot-packages\.php'))),
        Rule(LinkExtractor(allow=('single_project\.php\?id=[0-9]+&range=[0-9]+')), callback='parseItem'),

    )

    con = {"b'http://nostrahomes.com.au/home_designs.php'": 'Home Designs',
           "b'http://nostrahomes.com.au/house-land-packages.php'": 'HOUSE & LAND',
           "b'http://nostrahomes.com.au/white-hot-packages.php'": 'WHITE HOT PACKAGES'
           }

    def parse2(self, response):
        url = 'http://nostrahomes.com.au/php/ajax/refine-house.php?query%5B%5D=&query2%5B%5D=&page=13'
        return Request(url, callback=self.parseJSON)

    def parseJSON(self, response):
        it = RealtyspidersItem()
        data = json.loads(response.body.decode("utf-8"))[1]
        for v in data:
            it['Bathrooms'] = v['bath']
            it['BrochureImage_pdf'] = v['pdf']
            it['BasePrice'] = v['price']
            it['Garage'] = v['car']
            it['Region'] = v['location']
            it['Bedrooms'] = v['bed']
            it['State'] = v['region']
            it['BuildType'] = 'house land packages'
            it['DesignName'] = v['title']
            it['BuilderLogo'] = 'Nostra Homes'
            it['BuilderEmailAddress'] = 'info@nostrahomes.com.au'

            yield it

    def parse1(self, response):
        hxs = Selector(response)
        links = hxs.xpath('//ul[@class="normalize-ul design-list"]/li/a/@href').extract()
        # print('-'*30)
        # print(links)
        for url in links:
            # print('\n\nparse add link {}\n\n'.format(url))
            url = 'http://nostrahomes.com.au/single_design.php' + url
            yield Request(url, callback=self.parseItem)
        yield self.parseItem(response)

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        Region = self.getParams(response.url)
        Referer = str(response.request.headers.get('Referer', None))
        hxs = HtmlXPathSelector(response)
        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('BuildType', self.getBuildType(Referer))
        l.add_value('url', response.url)
        l.add_value('BuilderLogo', 'Nostra Homes')
        l.add_value('Region', Region)

        l.add_value('Storey', self._getSrorey(referer))

        l.add_xpath('State', '''//div[@class="dimensions-wrapper clearfix border-top"]/div/
                                         p[text()="Region"]/following-sibling::p/text()''')
        l.add_xpath('DesignName',
                    '''//ul[@class="normalize-ul design-list"]/li/a[@style="background-color: #e36420;"]/text()''')
        l.add_xpath('BasePrice', '''//div[@class="dimensions-wrapper clearfix border-top"]/div/
                                         p[text()="Price"]/following-sibling::p/text()''')
        l.add_xpath('Squares', '''//div[@class="dimensions-wrapper clearfix border-top"]/div/
                                 p[text()="House Size"]/following-sibling::p/text()''')
        l.add_xpath('HouseWidth', '''//div[@class="dimensions-wrapper clearfix border-top"]/div/
                                         p[text()="House Width"]/following-sibling::p/text()''')
        l.add_xpath('HouseLength', '''//div[@class="dimensions-wrapper clearfix border-top"]/div/
                                         p[text()="House Length"]/following-sibling::p/text()''')
        l.add_xpath('Bedrooms',
                    '''//div[@class="icon-wrapper clearfix"]/div/img[@alt="bed-gray"]/following-sibling::span/text()''')
        l.add_xpath('Bathrooms',
                    '''//div[@class="icon-wrapper clearfix"]/div/img[@alt="bathtub-gray"]/following-sibling::span/text()''')
        l.add_xpath('Garage',
                    '''//div[@class="icon-wrapper clearfix"]/div/img[@alt="car-gray"]/following-sibling::span/text()''')
        l.add_xpath('SturturalWarranty',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[\w\s]+guarantee'})
        l.add_xpath('TheatreRoom_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[Tt]heatre [Rr]ooms?'})
        l.add_xpath('SeparateMeals_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[Ss]eparate [Mm]eals'})
        l.add_xpath('Alfresco_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[Aa]lfresco'})
        l.add_xpath('Study_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '([Ss]tudy)|([Ss}chool)|([Uu]niversity)'})
        l.add_xpath('WalkinPantry_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '([Ww]alkin|[Pp]antry)'})
        l.add_xpath('BultersPantry_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[Bb]ulter[`]?s?'})
        l.add_xpath('BultersPantry_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[Bb]ulter[`]?s?'})
        l.add_xpath('SteelStructure_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[Ss]teel [Ss]tructure'})
        l.add_xpath('Balcony_Yes_No',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[Bb]alcony'})
        l.add_xpath('Windows',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[\w\s]+[Ww]indows?'})
        l.add_xpath('KitchenBenchtop',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[\w\s]+[Bb]enchtop'})
        l.add_xpath('SecuritySystem',
                    '//div[@class="one-halve"]/ul/li', **{'re': '[\w\s]+[Ss]ecurity System'})
        l.add_xpath('BuilderEmailAddress',
                    '//div[@class="tablet desktop editable"]/table/tbody/tr/th[text()="Email"]/following-sibling::td/text()')
        l.add_xpath('FloorPlanImage1',
                    '//div[@class="floor-plans-wrapper"]/div/a/img/@src', **{'myRefer': referer})
        l.add_xpath('BrochureImage_pdf', '//a[@class="pdfButton"]/@href', **{'myRefer': referer})
        l.add_xpath('Image1', '//*[@id="top-image"]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image1', '//ul[@class="slides normalize-ul"]/li[1]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image2', '//ul[@class="slides normalize-ul"]/li[2]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image3', '//ul[@class="slides normalize-ul"]/li[3]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image4', '//ul[@class="slides normalize-ul"]/li[4]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image5', '//ul[@class="slides normalize-ul"]/li[5]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image6', '//ul[@class="slides normalize-ul"]/li[6]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image7', '//ul[@class="slides normalize-ul"]/li[7]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image8', '//ul[@class="slides normalize-ul"]/li[8]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image9', '//ul[@class="slides normalize-ul"]/li[9]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image10', '//ul[@class="slides normalize-ul"]/li[10]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image11', '//ul[@class="slides normalize-ul"]/li[11]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image12', '//ul[@class="slides normalize-ul"]/li[12]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image13', '//ul[@class="slides normalize-ul"]/li[13]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image14', '//ul[@class="slides normalize-ul"]/li[14]/img/@src', **{'myRefer': referer})
        l.add_xpath('Image15', '//ul[@class="slides normalize-ul"]/li[15]/img/@src', **{'myRefer': referer})

        return l.load_item()

    def _getSrorey(self, url):
        sroreySearch = re.compile(r'(?<=stories=)[12]')
        r = sroreySearch.search(url)
        try:
            result = r.group()
        except AttributeError:
            return None
        return result

    def getParams(self, url):
        # paramsSearch = re.compile(r'''(?P<id>id=[0-9]+)&(?P<name>name=[a-zA-Z]+)''')
        paramsSearch = re.compile(r'(?P<name>(?<=name=)[a-zA-Z]+)')
        r = paramsSearch.search(url)
        try:
            name = r.group('name')
        except AttributeError:
            return None
        return name

    def getBuildType(self, url):
        try:
            return self.con[url]
        except:
            if url.find('range') != -1:
                return '"MOVA" BY NOSTRA'
            else:
                return 'Home Designs'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(NostrahomesSpider)
    process.start()
