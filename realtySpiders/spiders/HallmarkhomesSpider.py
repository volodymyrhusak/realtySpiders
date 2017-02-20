from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class HallmarkhomesSpider(CrawlSpider):
    name = 'hallmarkhomes'
    allowed_domains = ['hallmarkhomes.com.au']
    start_urls = ['http://hallmarkhomes.com.au/']
    rules = (
        Rule(LxmlLinkExtractor(
            allow=('http://hallmarkhomes.com.au/house-and-land/page/\d+/\?house-type=\d+$')),
            follow=True),
        Rule(LxmlLinkExtractor(
            allow=('http://hallmarkhomes.com.au/house-and-land/\?house-type=\d+$')),
            follow=True),
        Rule(LxmlLinkExtractor(
            allow=('http://hallmarkhomes.com.au/home-designs/page/\d+/\?house-type=\d+$')),
            follow=True),
        Rule(LxmlLinkExtractor(
            allow=('http://hallmarkhomes.com.au/home-designs/\?range=\d+$')),
            follow=True),
        Rule(LxmlLinkExtractor(
            allow=('http://hallmarkhomes.com.au/home-designs/\?house-type=\d+$')),
            follow=True),
        Rule(LxmlLinkExtractor(
            allow=('http://hallmarkhomes.com.au/home-designs/page/\d+/\?range=\d+$')),
            follow=True),
        Rule(LxmlLinkExtractor(allow=('http://hallmarkhomes.com.au/house-and-land/[\w-]+/$')),
             callback='parseItem'),
        Rule(LxmlLinkExtractor(allow=('http://hallmarkhomes.com.au/home-designs/[\w-]+/$')),
             callback='parseItem'),
    )
    oth = ('Activity', 'Second Alfresco', 'Patio')
    logo = 'Hallmark Homes'

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        inclusionsXpath = '''//h2[text()="Package Inclusions"]/following-sibling::div//li/text()'''
        imgXpath = '//div[@class="cycle-slideshow"]/img[{}]/@src'
        descriptionXPath = '''//div[@class="col-sm-4 col-hd-house-dimensions hd-house-dimensions"]
                              //tr/td[text()="{}"]/following-sibling::td/text()'''
        BuildType = self._getBuildType(referer)
        other = []
        for name in self.oth:
            size = hxs.xpath(descriptionXPath.format(name)).extract_first()
            if size:
                other.append('{}:{}'.format(name, size))

        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', BuildType)
        # l.add_value('BuilderEmailAddress', 'info@truevaluehomes.com.au')
        l.add_xpath('HomeDesignMainImage', imgXpath.format('1'))
        l.add_value('BuilderLogo', self.logo)

        l.add_xpath('DesignName', ['/html/body/div[3]/div/div[1]/div/div[1]/h1/text()',
                                   '/html/body/div[3]/div/div[1]/h1/text()'])
        if BuildType.find('Double'):
            l.add_value('Storey', '2')
        else:
            l.add_value('Storey', '1')
        # l.add_xpath('Region', '/html/body/div[3]/div/div[1]/div/div[1]/h3/text()')
        l.add_xpath('Region', descriptionXPath.format('Region'))
        #
        l.add_xpath('Bedrooms', '//span[@class="hh-icon-beds"]/ancestor::li/text()')
        l.add_xpath('Bathrooms', '//span[@class="hh-icon-baths"]/ancestor::li/text()')
        l.add_xpath('Garage', '//span[@class="hh-icon-car"]/ancestor::li/text()')
        l.add_xpath('BasePrice', ['/html/body/div[3]/div/div[1]/div/div[1]/h2/text()',
                                  '/html/body/div[3]/div/div[1]/h2/text()'])
        l.add_xpath('FloorPlanImage1', '//div[@class="js-fp-panzoom js-fp-panzoom-reset"]/img/@src')
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

        l.add_xpath('MasterBedroomDimension', descriptionXPath.format('Master Bedroom'))
        l.add_xpath('Bedroom2Dimension', descriptionXPath.format('Bedroom 2'))
        l.add_xpath('Bedroom3Dimension', descriptionXPath.format('Bedroom 3'))
        l.add_xpath('Bedroom4Dimension', [descriptionXPath.format('Bedroom 4'),
                                          descriptionXPath.format('Study/Bedroom 4')])
        l.add_xpath('StudyDimension', [descriptionXPath.format('Study/Bedroom 4'),
                                       descriptionXPath.format('Study')])
        l.add_xpath('Meals_DiningDimension',
                    [descriptionXPath.format('Meals'), descriptionXPath.format('Family/Meals')])
        l.add_xpath('FamilyDimension', [descriptionXPath.format('Meals'), descriptionXPath.format('Family/Meals')])
        l.add_xpath('TheatreDimension', [descriptionXPath.format('Media Room'), descriptionXPath.format('Media')])
        l.add_xpath('AlfrescoDimension', descriptionXPath.format('Alfresco'))
        l.add_xpath('HouseWidth', descriptionXPath.format('Min block width'))
        l.add_xpath('GarageDimension', descriptionXPath.format('Garage'))
        l.add_xpath('KitchenDimension', descriptionXPath.format('Kitchen'))
        l.add_xpath('Squares', descriptionXPath.format('Floor Area sqm'))
        l.add_xpath('LandSize', descriptionXPath.format('Land Size sqm'))
        l.add_xpath('LivingArea', descriptionXPath.format('Living'))

        # # Block Yes No
        l.add_xpath('TheatreRoom_Yes_No',
                    [descriptionXPath.format('Media Room'), descriptionXPath.format('Media')])
        l.add_xpath('Alfresco_Yes_No',
                    [descriptionXPath.format('Alfresco'), descriptionXPath.format('Second Alfresco')])
        l.add_xpath('Study_Yes_No',
                    [descriptionXPath.format('Study/Bedroom 4'),
                     descriptionXPath.format('Study')])
        l.add_value('OtherInclusions', ', '.join(other))

        # Гарантія
        l.add_xpath('SturturalWarranty',
                    inclusionsXpath, **{'re': '.*guarantee.*|.*[Ww]arranty.*'})
        # Вікна
        l.add_xpath('Windows',
                    inclusionsXpath, **{'re': '.*[Ww]indows?.*'})
        # Кухонна плита
        l.add_xpath('KitchenBenchtop',
                    inclusionsXpath,
                    **{'re': '.*[Kk]itchen.*[Bb]enchtop.*|.*[Bb]enchtop.*[Kk]itchen.*'})
        # Сигналізація
        l.add_xpath('SecuritySystem',
                    inclusionsXpath,
                    **{'re': '.*[Ss]ecurity.*[sS]ystem.*}.*[sS]ystem.*[Ss]ecurity.*'})
        # Клас енергозбереження
        l.add_xpath('EnergyRating',
                    inclusionsXpath, **{'re': '.*[Ee]nergy.*[rR]ating.*|.*[rR]ating.*[Ee]nergy.*'})
        # Кухонне приладдя
        l.add_xpath('KitchenAppliance',
                    inclusionsXpath,
                    **{'re': '.*([Kk]itchen.*[Aa]ppliance).*|.*([Aa]ppliance.*[Kk]itchen).*'})
        # Бренд пристрою
        l.add_xpath('ApplianceBrand',
                    inclusionsXpath, **{'re': '.*[\w\s]+[Ss]ecurity System.*'})
        # Kахель над умивальної раковиною
        l.add_xpath('Splashback',
                    inclusionsXpath, **{'re': '.*[Ss]plashback.*'})
        # Покриття підлоги
        l.add_xpath('FloorCovering',
                    inclusionsXpath,
                    **{'re': '.*[Ff]loor.*[Cc]overings?.*|.*[Cc]overings?.*[Ff]loor.*'})
        # Охолодження
        l.add_xpath('Cooling',
                    inclusionsXpath, **{'re': '.*[Cc]ooling.*'})
        # Ванна
        l.add_xpath('Bath',
                    inclusionsXpath, **{'re': '.*[Ss]ecurity.*[Ss]ystem.*'})
        # Висота стели
        l.add_xpath('CeilingHeight',
                    inclusionsXpath, **{'re': '.*[Bb]ath.*'})
        # Плитка в ванній
        l.add_xpath('EnsuiteWallTiling',
                    descriptionXPath, **{'re': '.*[Tt]ile.*'})
        # Плита в ванній
        l.add_xpath('EnsuiteBenchtop',
                    inclusionsXpath,
                    **{'re': '.*[Ee]nsuite.*[Bb]enchtop.*|.*[Bb]enchtop.*[Ee]nsuite.*'})
        # Душова
        l.add_xpath('EnsuiteShowerbase',
                    inclusionsXpath, **{'re': '.*[Ss]howerbase.*'})
        # Фарба на стінах
        l.add_xpath('WallPaint',
                    inclusionsXpath, **{'re': '.*[Ww]all.*[Pp]aint.*|.*[Pp]aint.*[Ww]all.*'})
        # Гардероб
        l.add_xpath('WIRFitouts',
                    inclusionsXpath, **{'re': '.*walk in robe.*|.*WIR.*'})
        # Світильники
        l.add_xpath('Downlights',
                    inclusionsXpath, **{'re': '.*[Dd]ownlights.*'})
        # Ландшафтний дизайн
        l.add_xpath('Landscaping',
                    inclusionsXpath, **{'re': '.*[Ll]andscaping.*'})
        # Дорожка до дому
        l.add_xpath('Driveway',
                    inclusionsXpath, **{'re': '.*[Dd]riveway.*'})
        # Реклама
        l.add_xpath('Promotion',
                    inclusionsXpath, **{'re': '.*[Pp]romotion.*'})

        return l.load_item()

    def _getState(self, url):
        return url.split('/')[4]

    def _getBuildType(self, url):
        if url.find('house-type=13') != -1:
            return 'Home Designs Single Storey'
        elif url.find('house-type=14') != -1:
            return 'Home Designs Double storey'
        elif url.find('house-type=15') != -1:
            return 'Home Designs Narrow Lot'
        elif url.find('house-type=16') != -1:
            return 'Home Designs Acreage'
        elif url.find('range=2976') != -1:
            return 'Home Designs Eclipse'
        elif url.find('house-type=11') != -1:
            return 'House and Land Single Storey'
        elif url.find('house-type=12') != -1:
            return 'House and Land Double storey'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(HallmarkhomesSpider)
    process.start()
