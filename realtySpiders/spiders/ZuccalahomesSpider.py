import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class ZuccalahomesSpider(CrawlSpider):
    name = 'zuccalahomes'
    allowed_domains = ['www.zuccalahomes.com.au']
    start_urls = ['http://www.zuccalahomes.com.au/']
    rules = (
        Rule(LinkExtractor(allow=('http://www.zuccalahomes.com.au/house-land/(page/[0-9]+/)?$')),
             callback='parseItemList', follow=True),
        Rule(LinkExtractor(allow=('http://www.zuccalahomes.com.au/display-homes/(page/[0-9]+/)?$')),
             callback='parseItemList', follow=True),
        Rule(LinkExtractor(allow=('http://.*/(page/[0-9]+/)?\?property-type=[\w-]+$')),
             callback='parseItemList', follow=True),
        # Rule(LinkExtractor(allow=('http://.*/home-designs/(page/[0-9]+/)?$')), callback='parseItemList', follow=True),
        # Rule(LinkExtractor(allow=('http://www\.zuccalahomes\.com\.au/\?property=[\w-]+$')), callback='parseItem',
        #      follow=False),

    )

    logo = 'Zuccala Homes'

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
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        Storey = self.getStorey(referer)
        hxs = HtmlXPathSelector(response)
        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('BuildType', response.meta['BuildType'])
        l.add_value('url', response.url)
        l.add_value('BuilderLogo', self.logo)
        l.add_value('State', 'VIC')
        l.add_value('Region', 'MELBOURNE')
        l.add_value('Storey', Storey)
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
        l.add_xpath('DesignName', '//h2[@class="page-title  "]/span/text()',
                    **{'reSub': '^Lot\s*\d+,\s*(St)?(Mt\.)?\s*[\w\s]+,'})
        l.add_xpath('Lot_BlockAddress', '//h2[@class="page-title  "]/span/text()',
                    **{'re': '^Lot\s*\d+,\s*(St)?(Mt\.)?\s*[\w\s]+'})

        l.add_xpath('Bedrooms',
                    '''//div[@class="single-property"]/div/span[@class="bed"]/strong/text()''')
        l.add_xpath('Bathrooms',
                    '''//div[@class="single-property"]/div/span[@class="bath"]/strong/text()''')
        l.add_xpath('Garage',
                    '''//div[@class="single-property"]/div/span[@class="car"]/strong/text()''')
        l.add_xpath('Squares',
                    '''//div[@class="single-property"]/div/span[@class="area "]/strong/text()''')
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
        if url.find('home-designs') != -1 or url.find('property-type') != -1:
            return 'Home Designs'
        elif url.find('house-land') != -1:
            return 'House Land'
        elif url.find('display-homes') != -1:
            return 'Display Homes'

    def getStorey(self, url):
        if url.find('double-storey-collection') != -1:
            return '2'
        elif url.find('single-storey-collection') != -1:
            return '1'
        else:
            return None


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ZuccalahomesSpider)
    process.start()
