import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class BentleyhomesSpider(CrawlSpider):
    HD_1 = '''http://www.bentleyhomes.com.au/home-designs/search-home-designs/?
                  hf_property_type_filter_2%5Bitems%5D%5B0%5D%5Bvalue%5D=273&
                  hf_property_type_filter_2%5Bcount%5D=1&hf_property_price_filter_2%5Bitems%5D%5B0%5D%5
                  Brange%5D=100000%3B800000&hf_property_price_filter_2%5Bcount%5D=1&hf_property_storeys_filter
                  %5Bitems%5D%5B0%5D%5Bvalue%5D=1&hf_property_storeys_filter%5Bcount%5D=1&hf_property_area_filter
                  %5Bitems%5D%5B0%5D%5Brange%5D=50%3B500&hf_property_area_filter%5Bcount%5D=1&submit=Search'''
    HD_2 = '''http://www.bentleyhomes.com.au/home-designs/search-home-designs/
                  ?hf_property_type_filter_2%5Bitems%5D%5B0%5D%5Bvalue%5D=273&hf_property_type_filter_2%
                  5Bcount%5D=1&hf_property_price_filter_2%5Bitems%5D%5B0%5D%5Brange%5D=100000%3B800000&
                  hf_property_price_filter_2%5Bcount%5D=1&hf_property_storeys_filter%5Bitems%5D%5B0%5D%5B
                  value%5D=2&hf_property_storeys_filter%5Bcount%5D=1&hf_property_area_filter%
                  5Bitems%5D%5B0%5D%5Brange%5D=50%3B500&hf_property_area_filter%5Bcount%5D=1&submit=Search'''
    HL_1 = '''http://www.bentleyhomes.com.au/house-and-land/browse-our-hl-packages/
                  ?hf_property_type_filter_3%5Bitems%5D%5B0%5D%5Bvalue%5D=275&hf_property_type_filter_3%5Bcount%5D=1
                  &hf_property_price_filter_3%5Bitems%5D%5B0%5D%5Brange%5D=100000%3B800000&hf_property_price_filter_3%
                  5Bcount%5D=1&hf_property_storeys_filter_1%5Bitems%5D%5B0%5D%5Bvalue%5D=1&hf_property_storeys_filter_1%
                  5Bcount%5D=1&hf_property_area_filter_1%5Bitems%5D%5B0%5D%5Brange%5D=50%3B500&hf_property_area_filter_1%
                  5Bcount%5D=1&submit=Search'''
    HL_2 = '''http://www.bentleyhomes.com.au/house-and-land/browse-our-hl-packages/?
                  hf_property_type_filter_3%5Bitems%5D%5B0%5D%5Bvalue%5D=275&hf_property_type_filter_3%5Bcount%5D=1&
                  hf_property_price_filter_3%5Bitems%5D%5B0%5D%5Brange%5D=100000%3B800000&hf_property_price_filter_3%5
                  Bcount%5D=1&hf_property_storeys_filter_1%5Bitems%5D%5B0%5D%5Bvalue%5D=2&hf_property_storeys_filter_1%
                  5Bcount%5D=1&hf_property_area_filter_1%5Bitems%5D%5B0%5D%5Brange%5D=50%3B500&hf_property_area_filter_1
                  %5Bcount%5D=1&submit=Search'''
    name = 'bentleyhomes'
    allowed_domains = ['www.bentleyhomes.com.au']
    # start_urls = ['http://www.bentleyhomes.com.au/', HD_1, HD_2, HL_1, HL_2]
    start_urls = ['http://www.bentleyhomes.com.au/']
    rules = (
        Rule(LxmlLinkExtractor(allow=('http://www.bentleyhomes.com.au/home-designs/search-home-designs/$')),
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://www.bentleyhomes.com.au/house-and-land/browse-our-hl-packages/$')),
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://www.bentleyhomes.com.au/dual-occupancy/$')),
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://www.bentleyhomes.com.au/displays-homes/ex-display-homes-for-sale/$')),
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://www.bentleyhomes.com.au/displays-homes/view-displays-homes/$')),
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://www.bentleyhomes.com.au/house-and-land/completed-homes/$')),
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://www.bentleyhomes.com.au/properties/[\w-]+/$'),
                               restrict_xpaths='//div[@class="block-content block-content-small-padding"]'),
             callback='parseItem', follow=True),

    )
    logo = 'Bentley Homes'

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        # with open('testURL', 'a') as file:
        #     file.writelines('\n'.join(hxs.xpath('//div[@class="col-md-8"]/table/tbody/tr/td[1]/text()').extract()))
        roomsXpath = '''//div[@class="col-md-8"]/table/tbody/tr/td[text()="{}"]/following-sibling::td/text()'''
        overviewXpath = '''//table[@id="hf-property-overview"]/tr/td/div[text()="{}"]/ancestor::td/following-sibling::
                            td[@class="item-value"]/div/div[@class="field-value"]/text()'''
        imgXpath = '//div[@class=" flexslider_gallery image hf-property-gallery"]/div/ul/li[{}]/img/@src'
        descriptionXPath = '//div[@id="col-md-8"]/p/text()'

        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', self._getBuildType(referer))
        # l.add_value('BuilderEmailAddress', 'info@truevaluehomes.com.au')
        #
        # try:
        #     l.add_value('HomeDesignMainImage', self.itemsList[response.url])
        # except KeyError:
        #     pass
        l.add_value('BuilderLogo', self.logo)

        if response.url.find('/lot') == -1:
            l.add_xpath('DesignName', '//h1[@class="property-detail-title"]/text()', **{'re': '^\w+\s+\d+$'})
        else:
            l.add_xpath('DesignName', overviewXpath.format('Home Design'))
            l.add_xpath('Region', '//h1[@class="property-detail-title"]/text()', **{'re': ',.*$'})
            l.add_value('State', 'MELBOURNE')


        l.add_xpath('Squares', overviewXpath.format('Area'))
        l.add_xpath('Bedrooms', overviewXpath.format('Beds'))
        l.add_xpath('Bathrooms', overviewXpath.format('Baths'))
        l.add_xpath('Garage', overviewXpath.format('Garages'))
        l.add_xpath('Storey', overviewXpath.format('Storeys'))
        l.add_xpath('LandSize', overviewXpath.format('Land Size'))
        l.add_xpath('BasePrice', '//*[@id="main-content"]/div/div[1]/div/div/div[2]/div/div[2]/text()')
        l.add_xpath('BrochureImage_pdf', '//a[text()="Download Flyer"]/@href')
        l.add_xpath('InclusionsImage_pdf', '//a[text()="Specifications and Inclusions"]/@href')
        l.add_xpath('FloorPlanImage1', '//a[@class="floor-plan fancybox"]/img/@src')
        l.add_xpath('HomeDesignMainImage', imgXpath.format('1'))
        l.add_xpath('Image1', imgXpath.format('2'))
        l.add_xpath('Image2', imgXpath.format('3'))
        l.add_xpath('Image3', imgXpath.format('4'))
        l.add_xpath('Image4', imgXpath.format('5'))
        l.add_xpath('Image5', imgXpath.format('6'))
        l.add_xpath('Image6', imgXpath.format('7'))
        l.add_xpath('Image7', imgXpath.format('8'))
        l.add_xpath('Image8', imgXpath.format('9'))
        l.add_xpath('Image9', imgXpath.format('10'))
        l.add_xpath('Image10', imgXpath.format('11'))
        l.add_xpath('Image11', imgXpath.format('12'))
        l.add_xpath('Image12', imgXpath.format('13'))
        l.add_xpath('Image13', imgXpath.format('14'))
        l.add_xpath('Image14', imgXpath.format('15'))
        l.add_xpath('Image15', imgXpath.format('16'))

        l.add_xpath('MasterBedroomDimension', roomsXpath.format('Master Bedroom'))
        l.add_xpath('Bedroom2Dimension', roomsXpath.format('Bedroom 2'))
        l.add_xpath('Bedroom3Dimension', roomsXpath.format('Bedroom 3'))
        l.add_xpath('Bedroom4Dimension', roomsXpath.format('Bedroom 4'))
        l.add_xpath('StudyDimension', roomsXpath.format('Study'))
        l.add_xpath('Meals_DiningDimension', roomsXpath.format('Meals'))
        l.add_xpath('FamilyDimension', roomsXpath.format('Family'))
        l.add_xpath('AlfrescoDimension', roomsXpath.format('Alfresco'))
        l.add_xpath('HouseWidth', roomsXpath.format('Overall Width'))
        l.add_xpath('HouseLength', roomsXpath.format('Overall Length'))


        # Block Yes No
        l.add_xpath('TheatreRoom_Yes_No',
                    roomsXpath.format('Theatre'))
        l.add_xpath('SeparateMeals_Yes_No',
                    roomsXpath.format('Meals'))
        l.add_xpath('Alfresco_Yes_No',
                    roomsXpath.format('Alfresco'))
        l.add_xpath('Study_Yes_No',
                    [roomsXpath.format('Study Nook'),roomsXpath.format('Study')])
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
                    descriptionXPath, **{'re': '?.*guarantee.*|.*[Ww]arranty.*'})
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

    def parseContent(self, response):
        hxs = HtmlXPathSelector(response)
        content = hxs.xpath('//div[@class="block-content block-content-small-padding"]')
        links = LinkExtractor(allow=('$')).extract_links(content)
        with open('testURL', 'a') as file:
            file.writelines(links)

    def _getBuildType(self, url):

        if url.find('dual-occupancy') != -1:
            return 'Dual Occupancy'
        elif url.find('ex-display-homes-for-sale') != -1:
            return 'Display Homes for Sale'
        elif url.find('view-displays-homes') != -1:
            return 'Display Homes'
        elif url.find('completed-homes') != -1:
            return 'Completed Homes for Sale'
        elif url.find('search-home-designs') != -1:
            return 'Home Designs'
        elif url.find('browse-our-hl-packages') != -1:
            return 'H&L packages'
            # elif url.find('ex-display-homes-for-sale') != -1:
            #     return 'Display Homes for Sale'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(BentleyhomesSpider)
    process.start()
