import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class HallburyhomesSpider(CrawlSpider):
    name = 'hallburyhomes'
    allowed_domains = ['hallburyhomes.com.au']
    start_urls = ['http://hallburyhomes.com.au']
    rules = (
        Rule(LxmlLinkExtractor(allow=('http://hallburyhomes.com.au/display-homes$')), callback='parseDisplay',
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://hallburyhomes.com.au/new-homes$')), callback='parseNewHome', follow=True),
        # Rule(LinkExtractor(allow=('http://www.rawdonhill.com.au/house-and-land/.*/$')), callback='parseHL'),
        # Rule(LinkExtractor(allow=('/homes/new-home-designs/[\w-]+$')), callback='parseItem'),
    )

    oth = ('Rumpus','Bed 5','Sitting Area','Retreat','Activity','Games','Outdoor Living','Lounge','Guest Room')

    logo = 'Hallbury homes'

    def parseDisplay(self, response):
        hxs = HtmlXPathSelector(response)
        hxsSection = hxs.xpath('//section[@class="display-home"]')
        for sec in hxsSection:
            address = sec.xpath('.//address[@class="display-home_content_text"]/text()').extract()
            link = sec.xpath('.//div[@class="display-home_content_buttons"]/a[1]/@href').extract_first()
            data = {'address': ' '.join(address).replace('\n', '').replace('\r', '')}
            yield Request(str(link), callback=self.parseItem, dont_filter=True, meta=data)

    def parseNewHome(self, response):
        links = LxmlLinkExtractor(allow=('https?://hallburyhomes.com.au/new-homes/[\w-]+$'),
                                  restrict_xpaths='//div[@class="section +t-padding-none"][1]').extract_links(response)
        for link in links:
            data = {'storey': '1'}
            yield Request(link.url, callback=self.parseItem, dont_filter=True, meta=data)

        links = LxmlLinkExtractor(allow=('https?://hallburyhomes.com.au/new-homes/[\w-]+$'),
                                  restrict_xpaths='//div[@class="section +t-padding-none"][2]').extract_links(response)
        for link in links:
            data = {'storey': '2'}
            yield Request(link.url, callback=self.parseItem, dont_filter=True, meta=data)

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        BuildType = self._getBuildType(referer)
        imgXpath = '''//main[@id="content"]/div[@class="carousel -arrows flickity "]
        /div[{}]/figure/div/img/@data-flickity-lazyload'''
        # descriptionXPath = '//div[@id="listing_options"]/ul/li/text()'
        areaXpath = '//div[@class="table-light"]/table/tbody/tr/td[text()="{}"]/following-sibling::td[1]/text()'
        roomsXpath = '''//h1[text()="Room dimensions"]/following-sibling::
                        dl/dt[text()="{}"]/following-sibling::dd[1]/text()'''
        # roomsDIMENSIONSXpath = '''//h1[text()="Room dimensions"]/following-sibling::
        #                 dl/dt/text()'''
        # data = hxs.xpath(roomsDIMENSIONSXpath).extract()
        # with open('testURL','a') as file:
        #     for i in data:
        #         file.write(i+'\n')
        other = []
        for name in self.oth:
            size = hxs.xpath(roomsXpath.format(name)).extract_first()
            if size:
                other.append('{}:{}'.format(name,size))

        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', BuildType)
        l.add_value('BuilderLogo', self.logo)
        if BuildType == 'Displays Homes':
            l.add_value('Lot_BlockAddress', response.meta['address'])
        else:
            l.add_value('Storey', response.meta['storey'])
        l.add_xpath('DesignName', '//h1[@class="h1 +margin-none +color-dark"]/strong/text()')

        l.add_xpath('Bedrooms', '//dl[@class="rooms-count"]/dd[1]/text()')
        l.add_xpath('Bathrooms', '//dl[@class="rooms-count"]/dd[2]/text()')
        l.add_xpath('Garage', '//dl[@class="rooms-count"]/dd[3]/text()')
        l.add_xpath('BasePrice',
                    '''//div/small[text()="Priced From"]/ancestor::
                    div/following-sibling::div[@class="h1 +color-dark"]/text()''')

        l.add_xpath('HouseWidth', '//div[@class="h5 +color-dark"]/text()',
                    **{'re': '((?<=Exterior Width )\d+\.\d+m)'})
        l.add_xpath('HouseLength', '//div[@class="h5 +color-dark"]/text()',
                    **{'re': '((?<=Exterior Length )\d+\.\d+m)'})
        l.add_xpath('GarageDimension', areaXpath.format('Garage'))
        l.add_xpath('AlfrescoDimension', areaXpath.format('Porch'))
        l.add_xpath('Alfresco_Yes_No', areaXpath.format('Porch'))
        l.add_xpath('Squares',
                    '//div[@class="table-light"]/table/tfoot/tr/td[text()="Total Area"]/following-sibling::td[1]/text()')
        l.add_xpath('MasterBedroomDimension', [roomsXpath.format('Master Bed'), roomsXpath.format('Bedroom 1')])
        l.add_xpath('Bedroom2Dimension', [roomsXpath.format('Bed 2'), roomsXpath.format('Bedroom 2')])
        l.add_xpath('Bedroom3Dimension', [roomsXpath.format('Bed 3'), roomsXpath.format('Bedroom 3')])
        l.add_xpath('Bedroom4Dimension', [roomsXpath.format('Bed 4'), roomsXpath.format('Bedroom 4')])
        l.add_xpath('Study_Yes_No', [roomsXpath.format('Study'), roomsXpath.format('Study (ground floor)'),
                                       roomsXpath.format('Study (first floor)'),
                                       roomsXpath.format('Study (First floor)')])
        l.add_xpath('StudyDimension', [roomsXpath.format('Study'), roomsXpath.format('Study (ground floor)'),
                                       roomsXpath.format('Study (first floor)'),
                                       roomsXpath.format('Study (First floor)')])
        l.add_xpath('FamilyDimension', [roomsXpath.format('Family')])
        l.add_xpath('Meals_DiningDimension',
                    [roomsXpath.format('Family / Meals'), roomsXpath.format('Meals/Family'),
                     roomsXpath.format('Living / Meals'), roomsXpath.format('Meals')])
        l.add_xpath('TheatreRoom_Yes_No', [roomsXpath.format('Theatre')])
        l.add_xpath('TheatreDimension', [roomsXpath.format('Theatre')])
        l.add_xpath('LivingArea', [roomsXpath.format('Living')])

        l.add_xpath('BrochureImage_pdf',
                    '//div[@class="+v-spacer-xs +t-margin-sm"]/div/a[text()="\t\tDownload Floorplan\n\t"]/@href')
        l.add_xpath('FloorPlanImage1', '//div[@class="section +t-padding-md"]//img/@src')
        l.add_xpath('HomeDesignMainImage', imgXpath.format('1'))
        l.add_xpath('Image1', imgXpath.format('1'))
        l.add_xpath('Image2', imgXpath.format('2'))
        l.add_xpath('Image3', imgXpath.format('3'))
        l.add_xpath('Image4', imgXpath.format('4'))
        l.add_xpath('Image5', imgXpath.format('5'))
        l.add_xpath('Image6', imgXpath.format('6'))
        l.add_xpath('Image7', imgXpath.format('7'))
        l.add_xpath('Image8', imgXpath.format('8'))
        l.add_xpath('Image9', imgXpath.format('9'))
        l.add_xpath('Image10', imgXpath.format('10'))
        l.add_xpath('Image11', imgXpath.format('11'))
        l.add_xpath('Image12', imgXpath.format('12'))
        l.add_xpath('Image13', imgXpath.format('13'))
        l.add_xpath('Image14', imgXpath.format('14'))
        l.add_xpath('Image15', imgXpath.format('15'))

        l.add_value('OtherInclusions',', '.join(other))

        return l.load_item()

    def _getBuildType(self, url):

        if url.find('display-homes') != -1:
            return 'Displays Homes'
        elif url.find('new-homes') != -1:
            return 'New Homes'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(HallburyhomesSpider)
    process.start()
