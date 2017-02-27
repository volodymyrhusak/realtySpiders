import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class HamlanSpider(CrawlSpider):
    name = 'hamlan'
    allowed_domains = ['www.hamlan.com.au']
    start_urls = ['http://www.hamlan.com.au']
    rules = (
        Rule(LxmlLinkExtractor(allow=('https://www.hamlan.com.au/our-homes/$')), callback='ourHomes',
             follow=True),
        Rule(LxmlLinkExtractor(allow=('https://www.hamlan.com.au/house-and-land/$')),
             callback='homeLand'),
        Rule(LxmlLinkExtractor(allow=('https://www.hamlan.com.au/display-locations/$')),
             callback='displayLocations'),
    )

    logo = 'Hamlan'

    def ourHomes(self, response):
        url = 'https://www.hamlan.com.au/wp-admin/admin-ajax.php'
        for i in range(1, 3):
            formdata = {'action': 'getOurHomeResults',
                        'checkedStoreys[]': '{}'.format(i),
                        'lotLengthLower': '0',
                        'lotLengthUpper': '40',
                        'lotWidthLower': '0',
                        'lotWidthUpper': '40',
                        'homeSizeLower': '15',
                        'homeSizeUpper': '40',
                        'className': 'storeys-section',
                        'filterSwitch': '1',
                        'switchFirst': '1'}
            headers = {'Accept': '*/*',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                       'X-Requested-With': 'XMLHttpRequest'}
            # yield Request(url, method='POST', callback=self.parseItem, dont_filter=True,headers=headers)
            requests = FormRequest(url=url, formdata=formdata, callback=self.getLinks, dont_filter=True,
                                   headers=headers, meta={'data': i})
            yield requests

    def homeLand(self, response):
        hxs = HtmlXPathSelector(response)
        region = hxs.xpath('//select[@id="refine-region"]/option/@value').extract()[2::]
        url = 'https://www.hamlan.com.au/wp-admin/admin-ajax.php'
        for i in region:
            formdata = {'action': 'getHouseLandResults',
                        'selectedEstate': '',
                        'selectedRegion': '{}'.format(i),
                        'priceLower': '200000',
                        'priceUpper': '800000',
                        'homeSizeLower': '10',
                        'homeSizeUpper': '40',
                        'landSizeLower': '250',
                        'landSizeUpper': '2000',
                        'lotWidthLower': '5',
                        'lotWidthUpper': '40',
                        'className': 'estate-section',
                        'filterSwitch': '0',
                        'switchFirst': '0'}
            headers = {'Accept': '*/*',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                       'X-Requested-With': 'XMLHttpRequest'}
            # yield Request(url, method='POST', callback=self.parseItem, dont_filter=True,headers=headers)
            requests = FormRequest(url=url, formdata=formdata, callback=self.getLinks, dont_filter=True,
                                   headers=headers, meta={'data': i})
            yield requests

    def displayLocations(self, response):
        hxs = HtmlXPathSelector(response)
        region = hxs.xpath('//select[@id="display-refine-region"]/option/@value').extract()[1::]
        regionName = hxs.xpath('//select[@id="display-refine-region"]/option/text()').extract()[1::]
        url = 'https://www.hamlan.com.au/wp-admin/admin-ajax.php'
        for n,i in enumerate(region):
            formdata = {'action': 'getDisplayLocationResults',
                        'selectedRegion': '{}'.format(i)
                        }
            headers = {'Accept': '*/*',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                       'X-Requested-With': 'XMLHttpRequest'}
            # yield Request(url, method='POST', callback=self.parseItem, dont_filter=True,headers=headers)
            requests = FormRequest(url=url, formdata=formdata, callback=self.getLinks, dont_filter=True,
                                   headers=headers, meta={'data': regionName[n]})
            yield requests

    def getLinks(self, response):
        body = '<html><head></head><body>' + response.body.decode('utf-8').replace('\\', '').replace('%5C%5C',
                                                                                                     '') + '</body></html>'
        body = body.encode('utf-8')
        response = response.replace(body=body)
        # hxs = HtmlXPathSelector(response)
        # links = hxs.xpath('/html/body/div[1]/div/a/@href').extract()
        links = LxmlLinkExtractor(
            allow=('https://www.hamlan.com.au/(our-homes)|(house-and-land)|(display-locations)/[\w-]+/[\w-]+/')).extract_links(response)
        # with open('testURL', 'a') as file:
        # with open('data.html', 'a') as file:
        # file.write(response.url + '   ' + referer + '\n')
        #     file.write(str(b.body))
        # links2 = LxmlLinkExtractor(allow=('https://www.hamlan.com.au/house-and-land/[\w-]+/[\w-]+/$')).extract_links(response)
        for link in links:
            # with open('testURL', 'a') as file:
            # with open('data.html', 'a') as file:
            #     file.write(link.url+'\n')
            # file.write(str(b.body))
            try:
                meta = {'data': response.meta['data']}
            except KeyError:
                meta = {'data': None}
            yield Request(link.url, callback=self.parseItem, dont_filter=True, meta=meta)

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        # with open('testURL', 'a') as file:
        #     file.writelines('\n'.join(hxs.xpath('//div[@class="col-md-8"]/table/tbody/tr/td[1]/text()').extract()))
        inclusionsXpath = '''//div[@class="clearfix inclusions-block-inner"]/ul/li/text()'''
        imgXpath = '//input[@class="mfp-images"][{}]/@value'
        descriptionXPath = '//div[@class="admin-content"]/p/text()'

        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType', self._getBuildType(response.url))
        # l.add_value('BuilderEmailAddress', 'info@truevaluehomes.com.au')
        l.add_xpath('HomeDesignMainImage', '//div[@class="imagefill h550"]//img/@src')
        l.add_value('BuilderLogo', self.logo)

        l.add_xpath('DesignName', '/html/body/div[2]/div/section[2]/h1/text()')
        data = response.meta['data']
        if isinstance(data, int):
            l.add_xpath('Storey', str(data))
        elif data:
            l.add_value('Region', data)
        l.add_value('State', self._getState(response.url))

        l.add_xpath('Squares', '//span[@class="img-caption"]//i/text()', **{'re': '(?<=Home [Ss]ize - ).+'})
        l.add_xpath('Bedrooms', '//span[@class="facility-list clearfix"]/em[1]//strong/text()')
        l.add_xpath('Bathrooms', '//span[@class="facility-list clearfix"]/em[2]//strong/text()')
        l.add_xpath('Garage', '//span[@class="facility-list clearfix"]/em[3]//strong/text()')
        l.add_xpath('LandSize', '//span[@class="img-caption"]//i/text()', **{'re': '(?<=Land size - ).+'})
        l.add_xpath('BasePrice', '//span[@class="product-price"]/text()')
        l.add_xpath('Lot_BlockAddress', '//div[@class="admin-content"]/h3/text()')
        l.add_xpath('BrochureImage_pdf', '//a[text()="Download Flyer"]/@href')
        l.add_xpath('InclusionsImage_pdf', '//a[text()="Download Inclusions"]/@href')
        l.add_xpath('OtherInclusions',
                    '//a[text()="Download Floorplan & Options"]/@href')
        l.add_xpath('FloorPlanImage1', '//a[@class="image-lightbox"]/img/@src')
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
        l.add_xpath('HouseWidth', '//em[@class="width-length"]/i/text()', **{'re': '(?<=Lot [Ww]idth - ).+'})
        l.add_xpath('HouseLength', '//em[@class="width-length"]/i/text()', **{'re': '(?<=Lot [Ll]ength - ).+'})

        # Block Yes No
        l.add_xpath('TheatreRoom_Yes_No',
                    [descriptionXPath, inclusionsXpath])
        l.add_xpath('SeparateMeals_Yes_No',
                    [descriptionXPath, inclusionsXpath])
        l.add_xpath('Alfresco_Yes_No',
                    [descriptionXPath, inclusionsXpath])
        l.add_xpath('Study_Yes_No',
                    [descriptionXPath, inclusionsXpath])
        l.add_xpath('WalkinPantry_Yes_No',
                    [descriptionXPath, inclusionsXpath])
        l.add_xpath('BultersPantry_Yes_No',
                    [descriptionXPath, inclusionsXpath])
        l.add_xpath('SteelStructure_Yes_No',
                    [descriptionXPath, inclusionsXpath])
        l.add_xpath('Balcony_Yes_No',
                    [descriptionXPath, inclusionsXpath])

        # Гарантія
        l.add_xpath('SturturalWarranty',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*guarantee.*|.*[Ww]arranty.*'})
        # Вікна
        l.add_xpath('Windows',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Ww]indows?.*'})
        # Кухонна плита
        l.add_xpath('KitchenBenchtop',
                    [descriptionXPath, inclusionsXpath],
                    **{'re': '.*[Kk]itchen.*[Bb]enchtop.*|.*[Bb]enchtop.*[Kk]itchen.*'})
        # Сигналізація
        l.add_xpath('SecuritySystem',
                    [descriptionXPath, inclusionsXpath],
                    **{'re': '.*[Ss]ecurity.*[sS]ystem.*}.*[sS]ystem.*[Ss]ecurity.*'})
        # Клас енергозбереження
        l.add_xpath('EnergyRating',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Ee]nergy.*[rR]ating.*|.*[rR]ating.*[Ee]nergy.*'})
        # Кухонне приладдя
        l.add_xpath('KitchenAppliance',
                    [descriptionXPath, inclusionsXpath],
                    **{'re': '.*([Kk]itchen.*[Aa]ppliance).*|.*([Aa]ppliance.*[Kk]itchen).*'})
        # Бренд пристрою
        l.add_xpath('ApplianceBrand',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[\w\s]+[Ss]ecurity System.*'})
        # Kахель над умивальної раковиною
        l.add_xpath('Splashback',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Ss]plashback.*'})
        # Покриття підлоги
        l.add_xpath('FloorCovering',
                    [descriptionXPath, inclusionsXpath],
                    **{'re': '.*[Ff]loor.*[Cc]overings?.*|.*[Cc]overings?.*[Ff]loor.*'})
        # Охолодження
        l.add_xpath('Cooling',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Cc]ooling.*'})
        # Ванна
        l.add_xpath('Bath',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Ss]ecurity.*[Ss]ystem.*'})
        # Висота стели
        l.add_xpath('CeilingHeight',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Bb]ath.*'})
        # Плитка в ванній
        l.add_xpath('EnsuiteWallTiling',
                    descriptionXPath, **{'re': '.*[Tt]ile.*'})
        # Плита в ванній
        l.add_xpath('EnsuiteBenchtop',
                    [descriptionXPath, inclusionsXpath],
                    **{'re': '.*[Ee]nsuite.*[Bb]enchtop.*|.*[Bb]enchtop.*[Ee]nsuite.*'})
        # Душова
        l.add_xpath('EnsuiteShowerbase',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Ss]howerbase.*'})
        # Фарба на стінах
        l.add_xpath('WallPaint',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Ww]all.*[Pp]aint.*|.*[Pp]aint.*[Ww]all.*'})
        # Гардероб
        l.add_xpath('WIRFitouts',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*walk in robe.*|.*WIR.*'})
        # Світильники
        l.add_xpath('Downlights',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Dd]ownlights.*'})
        # Ландшафтний дизайн
        l.add_xpath('Landscaping',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Ll]andscaping.*'})
        # Дорожка до дому
        l.add_xpath('Driveway',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Dd]riveway.*'})
        # Реклама
        l.add_xpath('Promotion',
                    [descriptionXPath, inclusionsXpath], **{'re': '.*[Pp]romotion.*'})
        # # # інші штуки

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

    def _getState(self, url):
        return url.split('/')[4]

    def _getBuildType(self, url):
        if url.find('our-homes') != -1:
            return 'Our Homes'
        elif url.find('house-and-land') != -1:
            return 'Home & Land'
        elif url.find('display-locations') != -1:
            return 'Display Locations'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(HamlanSpider)
    process.start()
