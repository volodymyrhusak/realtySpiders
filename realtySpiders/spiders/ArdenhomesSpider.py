from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class ArdenhomesSpider(CrawlSpider):
    name = 'ardenhomes'
    allowed_domains = ['www.ardenhomes.com.au']
    start_urls = ['http://www.ardenhomes.com.au/']
    rules = (

        Rule(LxmlLinkExtractor(allow=('/home-ranges'))),
        Rule(LxmlLinkExtractor(allow=('/aspire/[\w-]+')),
             callback='parseItem'),
        Rule(LxmlLinkExtractor(allow=('/lumina/[\w-]+')),
             callback='parseItem'),
        Rule(LxmlLinkExtractor(allow=('/display-locations')),
             callback='parseLocations'),
        Rule(LxmlLinkExtractor(allow=('/display-homes-for-sale')),
             callback='parseLocations'),
    )
    oth = ('Sun Court 1','Dining/Living','Porch','Sun Court 2','Overall House Dimension','Bedroom 5',
           'First Floor','Sun Court','Ground Floor','Activity Area','Sun Court 3','Rumpus')
    logo = 'Arden'

    def parseLocations(self,response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        BuildType = self._getBuildType(response.url)
        hxs = HtmlXPathSelector(response)
        if BuildType == 'Display Locations':
            for data in hxs.xpath('//div[@class="view-content"]/div'):
                l = RealtyLoader(RealtyspidersItem(), hxs)
                l.add_value('url', response.url)
                l.add_value('BuildType', BuildType)
                l.add_value('BuilderLogo', self.logo)
                HomeDesignMainImage = data.xpath('.//div[@class="views-field views-field-field-hero"]/div/img/@src').extract_first()
                DisplayLocation = data.xpath('.//div[@class="views-field views-field-field-location-description"]/div/text()').extract_first()
                BuilderEmailAddress = data.xpath('.//div[@class="views-label views-label-field-contact-email"]/div/a/text()').extract_first()
                OtherInclusions = data.xpath('.//div[@class="views-field views-field-field-contact-mobile"]/div/text()').extract_first()
                OtherInclusions1 = data.xpath('.//div[@class="views-field views-field-field-opening-hours"]/div/text()').extract_first()
                OtherInclusions2 = data.xpath('.//div[@class="views-field views-field-field-location-map"]/div/a/@href').extract_first()
                BuilderName = data.xpath('.//div[@class="views-field views-field-title"]/span/text()').extract_first()
                l.add_value('HomeDesignMainImage',HomeDesignMainImage)
                l.add_value('DisplayLocation', DisplayLocation)
                l.add_value('BuilderEmailAddress', BuilderEmailAddress)
                l.add_value('OtherInclusions', OtherInclusions)
                l.add_value('OtherInclusions1', OtherInclusions1)
                l.add_value('OtherInclusions2', OtherInclusions2)
                l.add_value('BuilderName', BuilderName)
                yield l.load_item()
        else:
            for data in hxs.xpath('//div[@class="panel panel-home node node-dhfs node-promoted"]'):
                l = RealtyLoader(RealtyspidersItem(), hxs)
                l.add_value('url', response.url)
                l.add_value('BuildType', BuildType)
                l.add_value('BuilderLogo', self.logo)
                HomeDesignMainImage = data.xpath('.//div[@class="panel-image"]/img/@src').extract_first()
                BasePrice = data.xpath('.//div[@class="panel-footer"]/ul/li/text()').extract_first()
                BuilderName = data.xpath('.//div[@class="panel-footer"]/text()').extract_first()
                l.add_value('HomeDesignMainImage',HomeDesignMainImage)
                l.add_value('BasePrice', BasePrice)
                l.add_value('BuilderName', BuilderName)
                yield l.load_item()



    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        BuildType = self._getBuildType(referer)
        if not BuildType:
            return None
        hxs = HtmlXPathSelector(response)
        with open('testURL', 'a') as file:
            file.writelines('\n'.join(hxs.xpath('//ul[@class="measurements-list"]/li/span[1]/text()').extract()))
        inclusionsXpath = '''//div[@data-tab="inclusions"]/div/p/text()'''
        imgXpath = '//div[@data-tab="gallery/images"]/div/img[{}]/@src'
        descriptionXPath = '''//div[@class="tab-pane floorplans"][{}]/div[@class="clearfix"]/div
                /ul[@class="measurements-list"]/li/span[text()="{}"]/following-sibling::span/text()'''

        count = hxs.xpath('//a[text()="Floorplans"]/following-sibling::ul/li/a/text()').extract()
        for i, design in enumerate(count):
            other = []
            for name in self.oth:
                size = hxs.xpath(descriptionXPath.format(i+1, name)).extract_first()
                if size:
                    other.append('{}:{}'.format(name, size))
            l = RealtyLoader(RealtyspidersItem(), hxs)
            l.add_value('url', response.url)
            l.add_value('BuildType', BuildType)
            # l.add_value('BuilderEmailAddress', 'info@truevaluehomes.com.au')
            l.add_xpath('HomeDesignMainImage', '''//div[@data-tab="overview"]/img/@src''')
            l.add_value('BuilderLogo', self.logo)

            l.add_value('DesignName', design)

            l.add_xpath('Region', descriptionXPath.format(i+1,'Region'))
            #
            l.add_xpath('Bedrooms', '//span[@class="bedroom"]/ancestor::li/text()')
            l.add_xpath('Bathrooms', '//span[@class="bedroom"]/ancestor::li/text()')
            l.add_xpath('Garage', '//span[@class="bedroom"]/ancestor::li/text()')
            l.add_xpath('BrochureImage_pdf', '//a[@class="gt-after download-price-list"]/@href')
            l.add_xpath('InclusionsImage_pdf', '//div[@data-tab="inclusions"]/div/a/@href')
            l.add_xpath('OtherInclusions1', '//div[@class="tab-pane floorplans"][{}]/div/div/a/@dref'.format(i+1))
            # l.add_xpath('BasePrice', ['/html/body/div[3]/div/div[1]/div/div[1]/h2/text()',
            #                           '/html/body/div[3]/div/div[1]/h2/text()'])
            l.add_xpath('FloorPlanImage1', '//div[@class="tab-pane floorplans"][{}]/div/div/img/@src'.format(i+1))
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

            l.add_xpath('MasterBedroomDimension',
                        [descriptionXPath.format(i+1,'Master Suite'),descriptionXPath.format(i+1,'Master Bedroom')
                            ,descriptionXPath.format(i+1,'Master Bed')])
            l.add_xpath('Bedroom2Dimension', descriptionXPath.format(i+1,'Bedroom 2'))
            l.add_xpath('Bedroom3Dimension', descriptionXPath.format(i+1,'Bedroom 3'))
            l.add_xpath('Bedroom4Dimension', descriptionXPath.format(i+1,'Bedroom 4'))
            l.add_xpath('StudyDimension', [descriptionXPath.format(i+1,'Study'),descriptionXPath.format(i+1,'Study/TV Area')])
            l.add_xpath('Meals_DiningDimension',
                        [descriptionXPath.format(i+1,'Dining/Living'), descriptionXPath.format(i+1,'Family/Meals')])
            l.add_xpath('FamilyDimension', descriptionXPath.format(i+1,'Family/Meals'))
            l.add_xpath('TheatreDimension', [descriptionXPath.format(i+1,'Study/TV Area'),
                                             descriptionXPath.format(i+1,'TV Area'),descriptionXPath.format(i+1,'Home Theatre')])
            l.add_xpath('AlfrescoDimension', descriptionXPath.format(i+1,'Alfresco'))
            # l.add_xpath('HouseWidth', descriptionXPath.format('Min block width'))
            l.add_xpath('GarageDimension', [descriptionXPath.format(i+1,'Garage'),descriptionXPath.format(i+1,'Double Garage')])
            l.add_xpath('KitchenDimension', [descriptionXPath.format(i+1,'Kitchen/Meals'),descriptionXPath.format(i+1,'Kitchen')])
            l.add_xpath('LoungeDimension', descriptionXPath.format(i+1,'Lounge'))
            l.add_xpath('Squares', descriptionXPath.format(i+1,'Total Size'))
            # l.add_xpath('LandSize', descriptionXPath.format('Land Size sqm'))
            l.add_xpath('LivingArea', descriptionXPath.format(i+1,'Living'))
            #
            # Block Yes No
            l.add_xpath('TheatreRoom_Yes_No',
                        [descriptionXPath.format(i+1,'Study/TV Area'),
                         descriptionXPath.format(i+1,'TV Area'), descriptionXPath.format(i+1,'Home Theatre')])
            l.add_xpath('Alfresco_Yes_No',
                        [descriptionXPath.format(i+1,'Alfresco'), descriptionXPath.format(i+1,'Second Alfresco')])
            l.add_xpath('Study_Yes_No',
                        [descriptionXPath.format(i+1,'Study'), descriptionXPath.format(i+1,'Study/TV Area')])
            l.add_value('OtherInclusions', ', '.join(other))
            #

            l.add_xpath('SturturalWarranty',
                        inclusionsXpath, **{'re': '.*guarantee.*|.*[Ww]arranty.*'})

            l.add_xpath('Windows',
                        inclusionsXpath, **{'re': '.*[Ww]indows?.*'})

            l.add_xpath('KitchenBenchtop',
                        inclusionsXpath,
                        **{'re': '.*[Kk]itchen.*[Bb]enchtop.*|.*[Bb]enchtop.*[Kk]itchen.*'})

            l.add_xpath('SecuritySystem',
                        inclusionsXpath,
                        **{'re': '.*[Ss]ecurity.*[sS]ystem.*}.*[sS]ystem.*[Ss]ecurity.*'})

            l.add_xpath('EnergyRating',
                        inclusionsXpath, **{'re': '.*[Ee]nergy.*[rR]ating.*|.*[rR]ating.*[Ee]nergy.*'})

            l.add_xpath('KitchenAppliance',
                        inclusionsXpath,
                        **{'re': '.*([Kk]itchen.*[Aa]ppliance).*|.*([Aa]ppliance.*[Kk]itchen).*'})

            l.add_xpath('ApplianceBrand',
                        inclusionsXpath, **{'re': '.*[\w\s]+[Ss]ecurity System.*'})

            l.add_xpath('Splashback',
                        inclusionsXpath, **{'re': '.*[Ss]plashback.*'})

            l.add_xpath('FloorCovering',
                        inclusionsXpath,
                        **{'re': '.*[Ff]loor.*[Cc]overings?.*|.*[Cc]overings?.*[Ff]loor.*'})

            l.add_xpath('Cooling',
                        inclusionsXpath, **{'re': '.*[Cc]ooling.*'})

            l.add_xpath('Bath',
                        inclusionsXpath, **{'re': '.*[Ss]ecurity.*[Ss]ystem.*'})

            l.add_xpath('CeilingHeight',
                        inclusionsXpath, **{'re': '.*[Bb]ath.*'})

            l.add_xpath('EnsuiteWallTiling',
                        inclusionsXpath, **{'re': '.*[Tt]ile.*'})

            l.add_xpath('EnsuiteBenchtop',
                        inclusionsXpath,
                        **{'re': '.*[Ee]nsuite.*[Bb]enchtop.*|.*[Bb]enchtop.*[Ee]nsuite.*'})

            l.add_xpath('EnsuiteShowerbase',
                        inclusionsXpath, **{'re': '.*[Ss]howerbase.*'})

            l.add_xpath('WallPaint',
                        inclusionsXpath, **{'re': '.*[Ww]all.*[Pp]aint.*|.*[Pp]aint.*[Ww]all.*'})

            l.add_xpath('WIRFitouts',
                        inclusionsXpath, **{'re': '.*walk in robe.*|.*WIR.*'})

            l.add_xpath('Downlights',
                        inclusionsXpath, **{'re': '.*[Dd]ownlights.*'})

            l.add_xpath('Landscaping',
                        inclusionsXpath, **{'re': '.*[Ll]andscaping.*'})

            l.add_xpath('Driveway',
                        inclusionsXpath, **{'re': '.*[Dd]riveway.*'})

            l.add_xpath('Promotion',
                        inclusionsXpath, **{'re': '.*[Pp]romotion.*'})

            yield l.load_item()

    def _getBuildType(self, url):
        if url.find('home-ranges') != -1:
            return 'New Homes'
        elif url.find('display-locations') != -1:
            return 'Display Locations'
        elif url.find('display-homes-for-sale') != -1:
            return 'Display Homes For Sale'



if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ArdenhomesSpider)
    process.start()
