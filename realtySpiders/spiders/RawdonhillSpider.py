import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class RawdonhillSpider(CrawlSpider):
    name = 'rawdonhill'
    allowed_domains = ['www.rawdonhill.com.au']
    start_urls = ['http://www.rawdonhill.com.au',
                  'http://www.rawdonhill.com.au/search/?storeys=1&bedrooms=&bathrooms=&size=',
                  'http://www.rawdonhill.com.au/search/?storeys=2&bedrooms=&bathrooms=&size=']
    rules = (
        Rule(LinkExtractor(allow=('http://www.rawdonhill.com.au/our-homes/.*/$')), callback='parseOurhomes'),
        Rule(LinkExtractor(allow=('/house-and-land/(page/\d+/)?$')), follow=True),
        Rule(LinkExtractor(allow=('http://www.rawdonhill.com.au/house-and-land/.*/$')), callback='parseHL'),
        # Rule(LinkExtractor(allow=('/homes/new-home-designs/[\w-]+$')), callback='parseItem'),
    )

    logo = 'Rawdon Hill'

    def parseOurhomes(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        areaXpath = '''//*[@id="floorplan-1"]/div[@class="specs-table"]/div/div[text()="{}"]/following-sibling::
                    div[@class="size"]/text()'''
        imgXpath = '//div[@class="home--single__gallery-images hidden-sm hidden-xs"]/a[{}]/@href'
        descrXpath = '//*[@id="sb-site"]/div[2]/div[3]/div/div/div[1]/p/text()'
        hxs = HtmlXPathSelector(response)
        # data =hxs.xpath('//div[@class="specs-table"]/div/div[@class="area"]/text()').extract()
        # with open('testURL', 'a') as file:
        #     for i in data:
        #         file.writelines(i+'\n')
        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', self._getBuildType(response.url))
        l.add_value('BuilderLogo', self.logo)
        l.add_xpath('DesignName', '//*[@id="sb-site"]/div[2]/div[1]/div/div/h1/text()')
        l.add_xpath('BrochureImage_pdf', '//*[@id="sb-site"]/div[2]/div[3]/div/div/div[2]/div[2]/a/@href')
        l.add_xpath('InclusionsImage_pdf', '//*[@id="sb-site"]/div[2]/div[3]/div/div/div[2]/div[3]/a/@href')
        l.add_xpath('Squares', '//*[@id="floorplan-1"]/div[@class="squares"]/text()')
        l.add_xpath('Bedrooms', '//*[@id="floorplan-1"]/div[@class="bedrooms"]/text()')
        l.add_xpath('Bathrooms', '//*[@id="floorplan-1"]/div[@class="bathrooms"]/text()')
        l.add_xpath('Garage', '//*[@id="floorplan-1"]/div[@class="cars"]/text()')
        l.add_xpath('FamilyDimension', areaXpath.format('Family'))
        l.add_xpath('Meals_DiningDimension',areaXpath.format('Meals'))
        l.add_xpath('LoungeDimension',areaXpath.format('Lounge'))
        l.add_xpath('AlfrescoDimension',areaXpath.format('Alfresco'))
        l.add_xpath('Alfresco_Yes_No',areaXpath.format('Alfresco'))
        l.add_xpath('GarageDimension',areaXpath.format('Garage'))
        l.add_xpath('MasterBedroomDimension',areaXpath.format('Master Bedroom'))
        l.add_xpath('Bedroom2Dimension',areaXpath.format('Bedroom 2'))
        l.add_xpath('Bedroom3Dimension',areaXpath.format('Bedroom 3'))
        l.add_xpath('Bedroom4Dimension',areaXpath.format('Bedroom 4'))
        l.add_xpath('KitchenDimension',areaXpath.format('Kitchen'))
        l.add_xpath('Study_Yes_No',areaXpath.format('Study'))
        l.add_xpath('StudyDimension',areaXpath.format('Study'))

        l.add_xpath('FloorPlanImage1', '//*[@id="floorplan-1"]/@scr')
        l.add_xpath('HomeDesignMainImage', '//*[@class="home--single__full-image"]/a/@href')
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
        l.add_xpath('BuilderEmailAddress',
                    descrXpath, **{'re': '[a-zA-Z]+@[a-z]+\.com\.au'})

        # Block Yes No
        l.add_xpath('TheatreRoom_Yes_No',descrXpath, **{'re': '[tT]heatre'})
        l.add_xpath('SeparateMeals_Yes_No',descrXpath, **{'re': '[Ss]eparate|[Mm]eals'})
        l.add_xpath('WalkinPantry_Yes_No',descrXpath, **{'re': '([Ww]alkin|[Pp]antry)'})
        l.add_xpath('BultersPantry_Yes_No',
                    descrXpath, **{'re': '[Bb]ulter[`]?s?'})
        l.add_xpath('SteelStructure_Yes_No',
                    descrXpath, **{'re': '([Ss]teel.*[Ss]tructure)|([Ss]tructure.*[Ss]teel)'})
        l.add_xpath('Balcony_Yes_No',descrXpath , **{'re': '[Bb]alcony'})
        #
        # Гарантія
        l.add_xpath('SturturalWarranty',
                    descrXpath, **{'re': '.*guarantee.*|.*[Ww]arranty.*'})
        # Вікна
        l.add_xpath('Windows',
                    descrXpath, **{'re': '.*[Ww]indows?.*'})
        # Кухонна плита
        l.add_xpath('KitchenBenchtop',
                    descrXpath, **{'re': '.*[Kk]itchen.*[Bb]enchtop.*|.*[Bb]enchtop.*[Kk]itchen.*'})
        # Сигналізація
        l.add_xpath('SecuritySystem',
                    descrXpath, **{'re': '.*[Ss]ecurity.*[sS]ystem.*}.*[sS]ystem.*[Ss]ecurity.*'})
        # Клас енергозбереження
        l.add_xpath('EnergyRating',
                    descrXpath, **{'re': '.*[Ee]nergy.*[rR]ating.*|.*[rR]ating.*[Ee]nergy.*'})
        # Кухонне приладдя
        l.add_xpath('KitchenAppliance',
                    descrXpath, **{'re': '.*([Kk]itchen.*[Aa]ppliance).*|.*([Aa]ppliance.*[Kk]itchen).*'})
        # Бренд пристрою
        l.add_xpath('ApplianceBrand',
                    descrXpath, **{'re': '.*[\w\s]+[Ss]ecurity System.*'})
        # Kахель над умивальної раковиною
        l.add_xpath('Splashback',
                    descrXpath, **{'re': '.*[Ss]plashback.*'})
        # Покриття підлоги
        l.add_xpath('FloorCovering',
                    descrXpath, **{'re': '.*[Ff]loor.*[Cc]overings?.*|.*[Cc]overings?.*[Ff]loor.*'})
        # Охолодження
        l.add_xpath('Cooling',
                    descrXpath, **{'re': '.*[Cc]ooling.*'})
        # Ванна
        l.add_xpath('Bath',
                    descrXpath, **{'re': '.*[Ss]ecurity.*[Ss]ystem.*'})
        # Висота стели
        l.add_xpath('CeilingHeight',
                    descrXpath, **{'re': '.*[Bb]ath.*'})
        # Плитка в ванній
        l.add_xpath('EnsuiteWallTiling',
                    descrXpath, **{'re': '.*[Tt]ile.*'})
        # Плита в ванній
        l.add_xpath('EnsuiteBenchtop',
                    descrXpath, **{'re': '.*[Ee]nsuite.*[Bb]enchtop.*|.*[Bb]enchtop.*[Ee]nsuite.*'})
        # Душова
        l.add_xpath('EnsuiteShowerbase',
                    descrXpath, **{'re': '.*[Ss]howerbase.*'})
        # Фарба на стінах
        l.add_xpath('WallPaint',
                    descrXpath, **{'re': '.*[Ww]all.*[Pp]aint.*|.*[Pp]aint.*[Ww]all.*'})
        # Гардероб
        l.add_xpath('WIRFitouts',
                    descrXpath, **{'re': '.*walk in robe.*|.*WIR.*'})
        # Світильники
        l.add_xpath('Downlights',
                    descrXpath, **{'re': '.*[Dd]ownlights.*'})
        # Ландшафтний дизайн
        l.add_xpath('Landscaping',
                    descrXpath, **{'re': '.*[Ll]andscaping.*'})
        # Дорожка до дому
        l.add_xpath('Driveway',
                    descrXpath, **{'re': '.*[Dd]riveway.*'})
        # Реклама
        l.add_xpath('Promotion',
                    descrXpath, **{'re': '.*[Pp]romotion.*'})

        return l.load_item()

    def parseHL(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        descrXpath = '//div[@class="houseland__description"]/pre/text()'
        imgXpath = '//div[@id="houseland_gallery-image-1"]/a/@href'
        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', self._getBuildType(response.url))
        l.add_value('BuilderLogo', self.logo)
        l.add_xpath('DesignName', '//*[@id="sb-site"]/div[2]/div/div/div[2]/div/h1/span/text()')
        l.add_xpath('DisplayLocation', '//*[@id="sb-site"]/div[2]/div/div/div[2]/div/h1/text()')
        l.add_xpath('BasePrice', '//div[@class="houseland__price"]/text()')
        l.add_xpath('Bedrooms', '//div[@class="houseland__bedrooms"]/text()')
        l.add_xpath('Bathrooms', '//div[@class="houseland__bathrooms"]/text()')
        l.add_xpath('Garage', '//div[@class="houseland__cars"]/text()')
        l.add_xpath('HomeDesignMainImage', '//div[@class="houseland__main-image"]/a/@href')
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

        l.add_xpath('TheatreRoom_Yes_No', descrXpath, **{'re': '[tT]heatre'})
        l.add_xpath('SeparateMeals_Yes_No', descrXpath, **{'re': '[Ss]eparate|[Mm]eals'})
        l.add_xpath('WalkinPantry_Yes_No', descrXpath, **{'re': '([Ww]alkin|[Pp]antry)'})
        l.add_xpath('BultersPantry_Yes_No',
                    descrXpath, **{'re': '[Bb]ulter[`]?s?'})
        l.add_xpath('SteelStructure_Yes_No',
                    descrXpath, **{'re': '([Ss]teel.*[Ss]tructure)|([Ss]tructure.*[Ss]teel)'})
        l.add_xpath('Balcony_Yes_No', descrXpath, **{'re': '[Bb]alcony'})

        return l.load_item()

    def _getBuildType(self, url):
        if url.find('our-homes') != -1:
            return 'Our Homes'
        elif url.find('house-and-land') != -1:
            return 'House & Land'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(RawdonhillSpider)
    process.start()