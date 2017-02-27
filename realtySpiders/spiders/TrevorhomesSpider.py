import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader
from scrapy.http import FormRequest , Request


class TrevorhomesSpider(CrawlSpider):

    name = 'trevorhomes'
    allowed_domains = ['trevorhomes.com.au']
    start_urls = ['http://trevorhomes.com.au']
    rules = (
        Rule(LxmlLinkExtractor(allow=('http://trevorhomes.com.au/home-designs/$')),
             follow=True, callback='parseLinks'),
        Rule(LxmlLinkExtractor(allow=('http://trevorhomes.com.au/house-land-packages/$')),
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://trevorhomes.com.au/estate/[\w-]+/$')),
             follow=True),
        Rule(LxmlLinkExtractor(allow=('http://trevorhomes.com.au/homeland/[\w-]+/$')),
             follow=True, callback='parseItem'),


    )
    oth = ('Porch ','Depth ','Residence ')
    logo = 'Trevor Homes'


    def parseLinks(self, response):
        linkSingle = LxmlLinkExtractor(allow=('http://trevorhomes.com.au/homedesign/[\w-]+/$'),
                                  restrict_xpaths='//div[@class="group-homedesign"][1]').extract_links(response)
        linksDouble = LxmlLinkExtractor(allow=('http://trevorhomes.com.au/homedesign/[\w-]+/$'),
                                       restrict_xpaths='//div[@class="group-homedesign"][2]').extract_links(response)
        for link in linkSingle:
            yield Request(link.url, callback=self.parseItem, meta={'Storey':'Single'})
        for link in linksDouble:
            yield Request(link.url, callback=self.parseItem, meta={'Storey':'Double'})




    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        BuildType = self._getBuildType(referer)
        # with open('testURL', 'a') as file:
        #     file.write(str(response.url)+ '\n')
        #     file.writelines('\n'.join(hxs.xpath('//div[@class="col-md-8"]/table/tbody/tr/td[1]/text()').extract()))
        roomsXpath = '''//div[@class="infor-house"]/p[text()="{}"]/span/text()'''
        # roomsXpath = '''//div[@class="infor-house"]/p/text()'''
        overviewXpath = '''//table[@id="hf-property-overview"]/tr/td/div[text()="{}"]/ancestor::td/following-sibling::
                            td[@class="item-value"]/div/div[@class="field-value"]/text()'''
        imgXpath = '//div[@class=" flexslider_gallery image hf-property-gallery"]/div/ul/li[{}]/img/@src'
        descriptionXPath = '//div[@class="left-popup"]/p/text()'
        # data = hxs.xpath(roomsXpath).extract()
        # with open('testURL','a') as file:
        #     for i in data:
        #         file.write(i+'\n')
        other = []
        for name in self.oth:
            size = hxs.xpath(roomsXpath.format(name)).extract_first()
            if size:
                other.append('{}:{}'.format(name, size))

        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', BuildType)
        l.add_value('BuilderLogo', self.logo)

        if BuildType == 'Home Designs':
            l.add_xpath('HomeDesignMainImage', '//div[@class="left-popup"]/img/@src')
            l.add_xpath('DesignName', '//div[@class="left-popup"]/h2/text()')
            l.add_value('Storey', response.meta['Storey'])
            l.add_xpath('Alfresco_Yes_No',
                        roomsXpath.format('Alfresco'))

        else:
            l.add_xpath('BasePrice',
                    '//div[@class="popup-handl-3d-image"]/h2/text()', **{'re':'(?<=$).+'})
            l.add_xpath('HomeDesignMainImage', '//div[@class="popup-handl-3d-image"]/img/@src')
            l.add_xpath('LandSize', '//div[@class="left-popup"]/p/strong[text()="Land Size: "]/ancestor::p/text()')
            # Block Yes No
            l.add_xpath('TheatreRoom_Yes_No',
                        descriptionXPath)
            l.add_xpath('SeparateMeals_Yes_No',
                        descriptionXPath)

            l.add_xpath('Study_Yes_No',
                        descriptionXPath)
            l.add_xpath('WalkinPantry_Yes_No',
                        descriptionXPath, **{'re': '([Ww]alkin|[Pp]antry)'})
            l.add_xpath('BultersPantry_Yes_No',
                        descriptionXPath, **{'re': '[Bb]ulter[`]?s?'})
            l.add_xpath('SteelStructure_Yes_No',
                        descriptionXPath, **{'re': '([Ss]teel.*[Ss]tructure)|([Ss]tructure.*[Ss]teel)'})
            l.add_xpath('Balcony_Yes_No',
                        descriptionXPath)
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

        # l.add_value('State', 'MELBOURNE')
        l.add_xpath('Bedrooms', '//span[@class="bedroom"]/text()')
        l.add_xpath('Bathrooms', '//span[@class="toalet"]/text()')
        l.add_xpath('Garage', '//span[@class="cars"]/text()')
        l.add_xpath('LivingArea', '//span[@class="living"]/text()')


        # l.add_xpath('HouseLength', '//div[text()="\n                        MIN. BLOCK LENGTH"]/text()[2]')
        l.add_xpath('BrochureImage_pdf',
                    ['//a[text()="Download brochure"]/@href', '//a[text()="Download brochue"]/@href'])
        l.add_xpath('InclusionsImage_pdf', '//a[text()="Download inclusions"]/@href')
        l.add_xpath('FloorPlanImage1', '//div[@class="right-popup"]/img/@src')
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




        l.add_xpath('GarageDimension', roomsXpath.format('Garage '))
        l.add_xpath('HouseWidth', roomsXpath.format('Width '))
        l.add_xpath('AlfrescoDimension', roomsXpath.format('Alfresco '))
        # l.add_xpath('Bedroom2Dimension', roomsXpath.format('Bedroom 2'))
        # l.add_xpath('Bedroom3Dimension', roomsXpath.format('Bedroom 3'))
        # l.add_xpath('Bedroom4Dimension', roomsXpath.format('Bedroom 4'))
        # l.add_xpath('StudyDimension', [roomsXpath.format('Study'),roomsXpath.format('Study nook')])
        # l.add_xpath('Meals_DiningDimension', roomsXpath.format('Meals'))
        # l.add_xpath('FamilyDimension', roomsXpath.format('Family'))
        # l.add_xpath('LoungeDimension', roomsXpath.format('Lounge'))
        # l.add_xpath('TheatreDimension', roomsXpath.format('Theatre'))
        # l.add_value('OtherInclusions', ', '.join(other))


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





    def _getBuildType(self, url):

        if url.find('home-designs') != -1:
            return 'Home Designs'
        elif url.find('house-land-package') != -1:
            return 'House & Land Packages'



if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(TrevorhomesSpider)
    process.start()