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
from realtySpiders.items import RealtyspidersItem
# from misc.spider import CommonSpider
from scrapy.crawler import CrawlerProcess


class OrphanLoader(XPathItemLoader):
    default_output_processor = TakeFirst()


class FrenkenhomesSpider(CrawlSpider):
    name = 'frenkenhomes'
    allowed_domains = ['www.frenkenhomes.com.au']
    start_urls = ['http://www.frenkenhomes.com.au/']
    rules = (
        Rule(LinkExtractor(allow=('/search/c/z/Display\+Homes')), callback='parse1', follow=True),
        Rule(LinkExtractor(allow=('/search/c/z/Home\+Designs')), callback='parse1', follow=True),
        Rule(LinkExtractor(allow=('/search/sales/houseandland/')), callback='parse1', follow=True),
        Rule(LinkExtractor(allow=('/search/c/z/house\+and\+land\+spec\+home/')), callback='parse1', follow=True),
    )

    con = {'Display+Homes': 'Display Homes',
           'Home+Designs': 'Home Designs',
           'houseandland': 'houseandland',
           'house+and+land+spec+home': 'house and land spec home'
           }

    def parse1(self, response):
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


class NostrahomesSpider(CrawlSpider):
    name = 'nostrahomes'
    allowed_domains = ['nostrahomes.com.au']
    start_urls = ['http://nostrahomes.com.au']
    rules = (
        Rule(LinkExtractor(allow=('/home_designs\.php'))),
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
        Region = self.getParams(response.url)
        Referer = str(response.request.headers.get('Referer', None))
        hxs = HtmlXPathSelector(response)
        l = OrphanLoader(RealtyspidersItem(), hxs)
        l.add_value('BuildType', self.getBuildType(Referer))
        l.add_value('url', response.url)
        l.add_value('BuilderLogo', 'Nostra Homes')
        l.add_value('Region', Region)
        l.add_xpath('State', '''//div[@class="dimensions-wrapper clearfix border-top"]/div/
                                         p[text()="Region"]/following-sibling::p/text()''')
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
                    '//div[@class="floor-plans-wrapper"]/div/a/img/@src')
        l.add_xpath('BrochureImage_pdf', '//a[@class="pdfButton"]/@href')
        l.add_xpath('Image1', '//*[@id="top-image"]/img/@src')
        l.add_xpath('Image1', '//ul[@class="slides normalize-ul"]/li[1]/img/@src')
        l.add_xpath('Image2', '//ul[@class="slides normalize-ul"]/li[2]/img/@src')
        l.add_xpath('Image3', '//ul[@class="slides normalize-ul"]/li[3]/img/@src')
        l.add_xpath('Image4', '//ul[@class="slides normalize-ul"]/li[4]/img/@src')
        l.add_xpath('Image5', '//ul[@class="slides normalize-ul"]/li[5]/img/@src')
        l.add_xpath('Image6', '//ul[@class="slides normalize-ul"]/li[6]/img/@src')
        l.add_xpath('Image7', '//ul[@class="slides normalize-ul"]/li[7]/img/@src')
        l.add_xpath('Image8', '//ul[@class="slides normalize-ul"]/li[8]/img/@src')
        l.add_xpath('Image9', '//ul[@class="slides normalize-ul"]/li[9]/img/@src')
        l.add_xpath('Image10', '//ul[@class="slides normalize-ul"]/li[10]/img/@src')
        l.add_xpath('Image11', '//ul[@class="slides normalize-ul"]/li[11]/img/@src')
        l.add_xpath('Image12', '//ul[@class="slides normalize-ul"]/li[12]/img/@src')
        l.add_xpath('Image13', '//ul[@class="slides normalize-ul"]/li[13]/img/@src')
        l.add_xpath('Image14', '//ul[@class="slides normalize-ul"]/li[14]/img/@src')
        l.add_xpath('Image15', '//ul[@class="slides normalize-ul"]/li[15]/img/@src')

        return l.load_item()

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


class ZuccalahomesSpider(CrawlSpider):
    name = 'zuccalahomes'
    allowed_domains = ['www.zuccalahomes.com.au']
    start_urls = ['http://www.zuccalahomes.com.au/']
    rules = (
        Rule(LinkExtractor(allow=('http://.*/home-designs/(page/[0-9]+/)?$')), callback='parseItemList', follow=True),
        Rule(LinkExtractor(allow=('http://www.zuccalahomes.com.au/house-land/(page/[0-9]+/)?$')),
             callback='parseItemList', follow=True),
        Rule(LinkExtractor(allow=('http://www.zuccalahomes.com.au/display-homes/(page/[0-9]+/)?$')),
             callback='parseItemList', follow=True),
        # Rule(LinkExtractor(allow=('http://www\.zuccalahomes\.com\.au/\?property=[\w-]+$')), callback='parseItem',
        #      follow=False),
        # Rule(LinkExtractor(allow=('http://.*/(page/[0-9]+/)?\?property-type=[\w-]+$')), callback='parseListItems',
        #      follow=True),
    )

    def parseItemList(self, response):
        links = LinkExtractor(allow=('http://www\.zuccalahomes\.com\.au/\?property=[\w-]+$')).extract_links(response)
        item = {}
        hxs = Selector(response)
        BuildType = self._getBuildType(response.url)
        for v in links:
            item['BuildType'] = BuildType
            info = hxs.select('''//li[@class="clearfix grid-item type-"]/div[@class="property-block"]/
            a[@href="{}"]/following-sibling::div[@class="property-info"]/text()'''.format(v.url)).extract()
            # with open('links from parseItem', 'a') as f:
            #     f.write(str(info) + '\n\n\n\n\n\n\n\n\n\n')
            #     f.close()

            squCom = re.compile(r'((?<=Size:)(\s+)?\d+\.\d+[a-zA-Z]+)')
            hwCom = re.compile(r'((?<=Lot Length:)(\s+)?\d+[a-zA-Z]+)')
            hlCom = re.compile(r'((?<=Lot Width:)(\s+)?\d+[a-zA-Z]+)')
            for i in info:
                try:
                    item['Squares'] = squCom.search(i).group()
                except AttributeError:
                    pass
                try:
                    item['HouseWidth'] = hwCom.search(i).group()
                except AttributeError:
                    pass
                try:
                    item['HouseLength'] = hlCom.search(i).group()
                except AttributeError:
                    pass
            yield Request(v.url, callback=self.parseItem, meta=item)

    def parseItem(self, response):
        hxs = HtmlXPathSelector(response)
        l = OrphanLoader(RealtyspidersItem(), hxs)
        l.add_value('BuildType', response.meta['BuildType'])
        l.add_value('url', response.url)
        l.add_value('BuilderLogo', 'zuccala homes')
        l.add_value('State', 'VIC')
        l.add_value('Region', 'MELBOURNE')
        try:
            l.add_value('Squares', response.meta['Squares'])
        except KeyError:
            pass
        try:
            l.add_value('HouseWidth', response.meta['HouseWidth'])
        except KeyError:
            pass
        try:
            l.add_value('HouseLength', response.meta['HouseLength'])
        except KeyError:
            pass
        l.add_xpath('Lot_BlockAddress', '//h2[@class="page-title  "]/span/text()')
        l.add_xpath('Bedrooms',
                    '''//div[@class="single-property"]/div/span[@class="bed"]/strong/text()''')
        l.add_xpath('Bathrooms',
                    '''//div[@class="single-property"]/div/span[@class="bath"]/strong/text()''')
        l.add_xpath('Garage',
                    '''//div[@class="single-property"]/div/span[@class="car"]/strong/text()''')
        l.add_xpath('SturturalWarranty',
                    '//div[@id="description"]/p/text()', **{'re': '"?.*[\w\s]+guarantee.*"?'})

        l.add_xpath('TheatreRoom_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '[Tt]heatre [Rr]ooms?'})
        l.add_xpath('SeparateMeals_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '[Ss]eparate [Mm]eals'})
        l.add_xpath('Alfresco_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '[Aa]lfresco'})
        l.add_xpath('Study_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '([Ss]tudy)|([Ss}chool)|([Uu]niversity)'})
        l.add_xpath('WalkinPantry_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '([Ww]alkin|[Pp]antry)'})
        l.add_xpath('BultersPantry_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '[Bb]ulter[`]?s?'})
        l.add_xpath('BultersPantry_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '[Bb]ulter[`]?s?'})
        l.add_xpath('SteelStructure_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '[Ss]teel [Ss]tructure'})
        l.add_xpath('Balcony_Yes_No',
                    '//div[@id="description"]/p/text()', **{'re': '[Bb]alcony'})

        l.add_xpath('Windows',
                    '//div[@id="description"]/p/text()', **{'re': '"?.*[\w\s]+[Ww]indows?.*"?'})
        l.add_xpath('KitchenBenchtop',
                    '//div[@id="description"]/p/text()', **{'re': '"?.*[\w\s]+[Bb]enchtop.*"?'})
        l.add_xpath('SecuritySystem',
                    '//div[@id="description"]/p/text()', **{'re': '"?.*[\w\s]+[Ss]ecurity System.*"?'})

        l.add_xpath('FloorPlanImage1',
                    '//div[@id="floor-plan"]/a/img/@src')
        l.add_xpath('BrochureImage_pdf', '//a[text()="View property brochure PDF"]/@href')
        l.add_xpath('HomeDesignMainImage', '//div[@id="property-images"]/ul/li[1]/img/@src')
        l.add_xpath('Image1', '//div[@id="property-images"]/ul/li[1]/img/@src')
        l.add_xpath('Image2', '//div[@id="property-images"]/ul/li[2]/img/@src')
        l.add_xpath('Image3', '//div[@id="property-images"]/ul/li[3]/img/@src')
        l.add_xpath('Image4', '//div[@id="property-images"]/ul/li[4]/img/@src')
        l.add_xpath('Image5', '//div[@id="property-images"]/ul/li[5]/img/@src')
        l.add_xpath('Image6', '//div[@id="property-images"]/ul/li[6]/img/@src')
        l.add_xpath('Image7', '//div[@id="property-images"]/ul/li[7]/img/@src')
        l.add_xpath('Image8', '//div[@id="property-images"]/ul/li[8]/img/@src')
        l.add_xpath('Image9', '//div[@id="property-images"]/ul/li[9]/img/@src')
        l.add_xpath('Image10', '//div[@id="property-images"]/ul/li[10]/img/@src')
        l.add_xpath('Image11', '//div[@id="property-images"]/ul/li[11]/img/@src')
        l.add_xpath('Image12', '//div[@id="property-images"]/ul/li[12]/img/@src')
        l.add_xpath('Image13', '//div[@id="property-images"]/ul/li[13]/img/@src')
        l.add_xpath('Image14', '//div[@id="property-images"]/ul/li[14]/img/@src')
        l.add_xpath('Image15', '//div[@id="property-images"]/ul/li[15]/img/@src')

        return l.load_item()

    def _getBuildType(self, url):
        if url.find('home-designs') != -1:
            return 'Home Designs'
        elif url.find('house-land') != -1:
            return 'House Land'
        elif url.find('display-homes') != -1:
            return 'Display Homes'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(FrenkenhomesSpider)
    process.crawl(NostrahomesSpider)
    process.crawl(ZuccalahomesSpider)
    process.start()
