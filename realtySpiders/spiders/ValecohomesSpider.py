import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class ValecohomesSpider(CrawlSpider):
    name = 'valecohomes'
    allowed_domains = ['www.valecohomes.com.au']
    start_urls = ['http://www.valecohomes.com.au/']
    rules = (
        Rule(LxmlLinkExtractor(allow=('http://www.valecohomes.com.au/home-designs/$')), follow=True),
        # Rule(LxmlLinkExtractor(allow=('http://www.valecohomes.com.au/display-homes/$')), follow=True),
        Rule(LxmlLinkExtractor(allow=('http://www.valecohomes.com.au/property-item/[\w-]+/$')), callback='parseItem',
             follow=True),
        # Rule(LxmlLinkExtractor(allow=('http://www.valecohomes.com.au/wp-content/themes/homeland-child/map.php.*')), callback='parseItem2',
        #      follow=True),
    )

    logo = 'Valeco Homes'

    def parseItem2(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        data = hxs.xpath('div[@class="markerContent"]').extract()
        with open('data.html', 'w') as file:
            file.writelines(response.text)

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        # all = hxs.select('//div[@class="property-info-agent clear"]/span/strong/text()').extract()
        # with open('testURL', 'a') as file:
        #     for l in all:
        #         file.writelines(l+'\n')
        roomsXpath = '''//div[@class="property-info-agent clear"]/span/strong[text()="{}"]/ancestor::span/text()'''
        Bedrooms = hxs.xpath(roomsXpath.format('Bedrooms:')).extract()
        Bathrooms = hxs.xpath(roomsXpath.format('Bathrooms:')).extract()
        Garage = hxs.xpath(roomsXpath.format('Car Spaces:')).extract()
        HouseWidth = hxs.xpath(roomsXpath.format('Overall Width:')).extract()
        GarageDimension = hxs.xpath(roomsXpath.format('Garage:')).extract()
        AlfrescoDimension = hxs.xpath(roomsXpath.format('Alfresco:')).extract()
        Alfresco_Yes_No = hxs.xpath(roomsXpath.format('Alfresco:')).extract()
        Squares = hxs.xpath(roomsXpath.format('Total:')).extract()
        Storey = hxs.xpath(roomsXpath.format('First Floor Living:')).extract()

        # overviewXpath = '''//table[@id="hf-property-overview"]/tr/td/div[text()="{}"]/ancestor::td/following-sibling::
        #                     td[@class="item-value"]/div/div[@class="field-value"]/text()'''
        # imgXpath = '//div[@class=" flexslider_gallery image hf-property-gallery"]/div/ul/li[{}]/img/@src'
        descriptionXPath = '//div[@id="0"]//li/text()'

        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', 'HOME DESIGNS')
        # l.add_value('BuilderEmailAddress', 'info@truevaluehomes.com.au')
        #
        # try:
        #     l.add_value('HomeDesignMainImage', self.itemsList[response.url])
        # except KeyError:
        #     pass
        l.add_value('BuilderLogo', self.logo)

        l.add_xpath('DesignName', ['//section[@class="page-title-block header-bg"]/div/h2/text()',
                                   '//section[@class="page-title-block-default header-bg"]/div/h2/text()'])
        # if response.url.find('/lot') == -1:
        # else:
        #     l.add_xpath('DesignName', overviewXpath.format('Home Design'))
        #     l.add_xpath('Region', '//h1[@class="property-detail-title"]/text()', **{'re': ',.*$'})
        #     l.add_value('State', 'MELBOURNE')

        # l.add_xpath('Squares', overviewXpath.format('Area'))
        l.add_value('Bedrooms', self._stripJoin(Bedrooms))
        l.add_value('Bathrooms', self._stripJoin(Bathrooms))
        l.add_value('Garage', self._stripJoin(Garage))
        if Storey:
            l.add_value('Storey', '2')
        else:
            l.add_value('Storey', '1')

        l.add_value('HouseWidth', self._stripJoin(HouseWidth))
        l.add_value('GarageDimension', self._stripJoin(GarageDimension))
        l.add_value('AlfrescoDimension', self._stripJoin(AlfrescoDimension))
        l.add_value('Alfresco_Yes_No', self._stripJoin(Alfresco_Yes_No))
        l.add_value('Squares', self._stripJoin(Squares))
        # l.add_xpath('LandSize', overviewXpath.format('Land Size'))
        # l.add_xpath('BasePrice', '//*[@id="main-content"]/div/div[1]/div/div/div[2]/div/div[2]/text()')
        l.add_xpath('BrochureImage_pdf', '//div[@id="0"]//a/@href')
        # l.add_xpath('InclusionsImage_pdf', '//a[text()="Specifications and Inclusions"]/@href')
        l.add_xpath('FloorPlanImage1', '//div[@id="1"]/img/@src')
        l.add_xpath('HomeDesignMainImage', '//ul[@class="slides"]//a/@href')
        # l.add_xpath('Image1', imgXpath.format('2'))
        # l.add_xpath('Image2', imgXpath.format('3'))
        # l.add_xpath('Image3', imgXpath.format('4'))
        # l.add_xpath('Image4', imgXpath.format('5'))
        # l.add_xpath('Image5', imgXpath.format('6'))
        # l.add_xpath('Image6', imgXpath.format('7'))
        # l.add_xpath('Image7', imgXpath.format('8'))
        # l.add_xpath('Image8', imgXpath.format('9'))
        # l.add_xpath('Image9', imgXpath.format('10'))
        # l.add_xpath('Image10', imgXpath.format('11'))
        # l.add_xpath('Image11', imgXpath.format('12'))
        # l.add_xpath('Image12', imgXpath.format('13'))
        # l.add_xpath('Image13', imgXpath.format('14'))
        # l.add_xpath('Image14', imgXpath.format('15'))
        # l.add_xpath('Image15', imgXpath.format('16'))
        #
        # l.add_xpath('MasterBedroomDimension', roomsXpath.format('Master Bedroom'))
        # l.add_xpath('Bedroom2Dimension', roomsXpath.format('Bedroom 2'))
        # l.add_xpath('Bedroom3Dimension', roomsXpath.format('Bedroom 3'))
        # l.add_xpath('Bedroom4Dimension', roomsXpath.format('Bedroom 4'))
        # l.add_xpath('StudyDimension', roomsXpath.format('Study'))
        # l.add_xpath('Meals_DiningDimension', roomsXpath.format('Meals'))
        # l.add_xpath('FamilyDimension', roomsXpath.format('Family'))
        # l.add_xpath('AlfrescoDimension', roomsXpath.format('Alfresco'))
        # l.add_xpath('HouseWidth', roomsXpath.format('Overall Width'))
        # l.add_xpath('HouseLength', roomsXpath.format('Overall Length'))
        #
        # Block Yes No
        l.add_xpath('WalkinPantry_Yes_No',
                    descriptionXPath, **{'re': '([Ww]alkin|[Pp]antry)'})
        l.add_xpath('BultersPantry_Yes_No',
                    descriptionXPath, **{'re': '[Bb]ulter[`]?s?'})
        l.add_xpath('SteelStructure_Yes_No',
                    descriptionXPath, **{'re': '([Ss]teel.*[Ss]tructure)|([Ss]tructure.*[Ss]teel)'})
        l.add_xpath('Balcony_Yes_No',
                    roomsXpath.format('Balcony'))
        #
        # Гарантія
        l.add_xpath('SturturalWarranty',
                    descriptionXPath, **{'re': '.*guarantee.*|.*[Ww]arranty.*'})
        # Вікна
        l.add_xpath('Windows',
                    descriptionXPath, **{'re': '.*[Ww]indows?.*'})
        # Кухонна плита
        l.add_xpath('KitchenBenchtop',
                    descriptionXPath, **{'re': '.*[Kk]itchen.*[Bb]enchtop.*|.*[Bb]enchtop.*[Kk]itchen.*'})
        # Сигналізація
        l.add_xpath('SecuritySystem',
                    descriptionXPath, **{'re': '.*[Ss]ecurity.*[sS]ystem.*}.*[sS]ystem.*[Ss]ecurity.*'})
        # Клас енергозбереження
        l.add_xpath('EnergyRating',
                    descriptionXPath, **{'re': '.*[Ee]nergy.*[rR]ating.*|.*[rR]ating.*[Ee]nergy.*'})
        # Кухонне приладдя
        l.add_xpath('KitchenAppliance',
                    descriptionXPath, **{'re': '.*([Kk]itchen.*[Aa]ppliance).*|.*([Aa]ppliance.*[Kk]itchen).*'})
        # Бренд пристрою
        l.add_xpath('ApplianceBrand',
                    descriptionXPath, **{'re': '.*[\w\s]+[Ss]ecurity System.*'})
        # Kахель над умивальної раковиною
        l.add_xpath('Splashback',
                    descriptionXPath, **{'re': '.*[Ss]plashback.*'})
        # Покриття підлоги
        l.add_xpath('FloorCovering',
                    descriptionXPath, **{'re': '.*[Ff]loor.*[Cc]overings?.*|.*[Cc]overings?.*[Ff]loor.*'})
        # Охолодження
        l.add_xpath('Cooling',
                    descriptionXPath, **{'re': '.*[Cc]ooling.*'})
        # Ванна
        l.add_xpath('Bath',
                    descriptionXPath, **{'re': '.*[Ss]ecurity.*[Ss]ystem.*'})
        # Висота стели
        l.add_xpath('CeilingHeight',
                    descriptionXPath, **{'re': '.*[Bb]ath.*'})
        # Плитка в ванній
        l.add_xpath('EnsuiteWallTiling',
                    descriptionXPath, **{'re': '.*[Tt]ile.*'})
        # Плита в ванній
        l.add_xpath('EnsuiteBenchtop',
                    descriptionXPath, **{'re': '.*[Ee]nsuite.*[Bb]enchtop.*|.*[Bb]enchtop.*[Ee]nsuite.*'})
        # Душова
        l.add_xpath('EnsuiteShowerbase',
                    descriptionXPath, **{'re': '.*[Ss]howerbase.*'})
        # Фарба на стінах
        l.add_xpath('WallPaint',
                    descriptionXPath, **{'re': '.*[Ww]all.*[Pp]aint.*|.*[Pp]aint.*[Ww]all.*'})
        # Гардероб
        l.add_xpath('WIRFitouts',
                    descriptionXPath, **{'re': '.*walk in robe.*|.*WIR.*'})
        # Світильники
        l.add_xpath('Downlights',
                    descriptionXPath, **{'re': '.*[Dd]ownlights.*'})
        # Ландшафтний дизайн
        l.add_xpath('Landscaping',
                    descriptionXPath, **{'re': '.*[Ll]andscaping.*'})
        # Дорожка до дому
        l.add_xpath('Driveway',
                    descriptionXPath, **{'re': '.*[Dd]riveway.*'})
        # Реклама
        l.add_xpath('Promotion',
                    descriptionXPath, **{'re': '.*[Pp]romotion.*'})
        # # # інші штуки
        # # l.add_xpath('OtherInclusions',
        # #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
        # # l.add_xpath('OtherInclusions1',
        # #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
        # # l.add_xpath('OtherInclusions2',
        # #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
        # # l.add_xpath('OtherInclusions3',
        # #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
        # # l.add_xpath('OtherInclusions4',
        # #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
        # # l.add_xpath('OtherInclusions5',
        # #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
        return l.load_item()

    def _stripJoin(self, data):
        return ''.join(data).strip()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ValecohomesSpider)
    process.start()
