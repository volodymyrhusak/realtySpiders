import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.http import FormRequest
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class AshfordhomesSpider(CrawlSpider):
    name = 'ashfordhomes'
    allowed_domains = ['www.ashfordhomes.com.au']
    start_urls = ['http://www.ashfordhomes.com.au']
    rules = (
        Rule(LxmlLinkExtractor(allow=('http://www.ashfordhomes.com.au/new-homes/$')),
             callback='parseForm', follow=True),
        Rule(LxmlLinkExtractor(allow=('/house-and-land-packages/')),
             callback='parseLinks', follow=True),
        Rule(LxmlLinkExtractor(allow=('/index.php/new-homes\?.*')),
             callback='parseLinks', follow=True),
        Rule(LxmlLinkExtractor(allow=('/displays-for-sale/')), follow=True),
        Rule(LxmlLinkExtractor(allow=('http://www.ashfordhomes.com.au/new-homes/.+/')),
             callback='parseItem', follow=False),
    )
    features = {
        '25': {'title': 'Alfresco_Yes_No', 'urls': [], 'name': 'akID[17][atSelectOptionID][]'},
        '36': {'title': 'Study_Yes_No', 'urls': [], 'name': 'akID[17][atSelectOptionID][]'},
        '35': {'title': 'TheatreRoom_Yes_No', 'urls': [], 'name': 'akID[17][atSelectOptionID][]'}
    }
    logo = 'Ashford Homes'

    def parseForm(self, response):
        for id in self.features.keys():
            name = self.features[id]['name']
            formdata = {name: id}
            yield FormRequest.from_response(response,
                                            formdata=formdata,
                                            clickdata={'name': 'Search'},
                                            callback=self.addFeaturesLinks)


    def addFeaturesLinks(self, response):
        links = LxmlLinkExtractor(allow=('/index.php/new-homes/.*/$')).extract_links(response)
        key = re.search(r'((?<=BatSelectOptionID%5D%5B%5D=)\d+)', response.url).group()
        for link in links:
            self.features[key]['urls'].append(link.url)


    def parseLinks(self, response):
        links = LxmlLinkExtractor(allow=('/index.php/new-homes/.*/$')).extract_links(response)
        # with open('testURL', 'a') as file:
        #     for link in links:
        #         file.write(link.url +'   ' + response.url + '\n')
        for link in links:
            yield Request(link.url, callback=self.parseItem)


    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        BuildType = self._getBuildType(referer)
        imgXpath = '//a[@class="proPhotoThumbLink"]/img[{}]/@src'
        descriptionXPath = '//div[@id="listing_options"]/ul/li/text()'
        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', BuildType)
        l.add_value('BuilderLogo', self.logo)
        # if BuildType == 'PRESTIGE HOMES':
        #     l.add_value('State', 'MELBOURNE')
        # l.add_xpath('BuilderEmailAddress',
        #             '//div[@class="entry-content span5"]/p/strong[text()="Email:"]/following-sibling::a/text()')
        #
        l.add_xpath('DesignName', '//div[@id="listing_options"]/h4/text()')

        l.add_xpath('Bedrooms', '//div[@id="listing_options"]/text()', **{'re': '\d(?=\sBeds)'})
        l.add_xpath('Bathrooms', '//div[@id="listing_options"]/text()', **{'re': '\d(?=\sBaths)'})
        l.add_xpath('Lot_BlockWidth', '//div[@id="listing_options"]/text()',
                    **{'re': '(?<=Ideal block width = )[\w\.\s]+'})

        l.add_xpath('LivingArea', descriptionXPath, **{'re': '(?<=Living Area - )[\w\.\s]+'})
        l.add_xpath('Squares', descriptionXPath, **{'re': '(?<=Total Area - )[\w\.\s]+'})
        l.add_xpath('GarageDimension', descriptionXPath, **{'re': '(?<=Garage Area - )[\w\.\s]+'})
        l.add_xpath('AlfrescoDimension', descriptionXPath, **{'re': '(?<=Alfresco Area - )[\w\.\s]+'})

        l.add_xpath('FloorPlanImage1', '//div[@id="listing_text"]/h4/a[text()="Download floor plan"]/@href',
                    **{'myRefer': self.start_urls[0]})
        l.add_xpath('BrochureImage_pdf', '//div[@id="listing_text"]/h4/a[text()="View the Specification"]/@href',
                    **{'myRefer': self.start_urls[0]})
        l.add_xpath('HomeDesignMainImage', '//div[@class="mainImageTarget"]/img/@src',
                    **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image1', imgXpath.format('1'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image2', imgXpath.format('2'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image3', imgXpath.format('3'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image4', imgXpath.format('4'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image5', imgXpath.format('5'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image6', imgXpath.format('6'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image7', imgXpath.format('7'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image8', imgXpath.format('8'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image9', imgXpath.format('9'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image10', imgXpath.format('10'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image11', imgXpath.format('11'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image12', imgXpath.format('12'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image13', imgXpath.format('13'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image14', imgXpath.format('14'), **{'myRefer': self.start_urls[0]})
        l.add_xpath('Image15', imgXpath.format('15'), **{'myRefer': self.start_urls[0]})
        #
        # Block Yes No
        l.add_value('TheatreRoom_Yes_No',self.getFeatures(response.url, '35'))
        # l.add_xpath('SeparateMeals_Yes_No',
        #             descriptionXPath, **{'re': '([Ss]eparate.*[Mm]eals)|([Mm]eals.*[Ss]eparate)'})
        l.add_value('Alfresco_Yes_No',self.getFeatures(response.url, '25'))
        l.add_value('Study_Yes_No',self.getFeatures(response.url, '36'))
        # l.add_xpath('WalkinPantry_Yes_No',
        #             descriptionXPath, **{'re': '([Ww]alkin|[Pp]antry)'})
        # l.add_xpath('BultersPantry_Yes_No',
        #             descriptionXPath, **{'re': '[Bb]ulter[`]?s?'})
        # l.add_xpath('BultersPantry_Yes_No',
        #             descriptionXPath, **{'re': '[Bb]ulter[`]?s?'})
        # l.add_xpath('SteelStructure_Yes_No',
        #             descriptionXPath, **{'re': '([Ss]teel.*[Ss]tructure)|([Ss]tructure.*[Ss]teel)'})
        # l.add_xpath('Balcony_Yes_No',
        #             descriptionXPath, **{'re': '[Bb]alcony'})

        return l.load_item()

    def getFeatures(self, url, features):
        if url in self.features[features]['urls']:
            # with open('testURL', 'a') as file:
            #     file.write(str(self.features[features]['urls']) + '\n')
            #     file.write(url + '\n'*2)
            return 'Yes'
        return None

    def _getBuildType(self, url):

        if url.find('displays-for-sale') != -1 or url == self.start_urls[0]:
            return 'Displays For Sale'
        elif url.find('new-homes') != -1:
            return 'New Homes'
        elif url.find('house-and-land-packages') != -1:
            return 'Displays For Sale'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(AshfordhomesSpider)
    process.start()
