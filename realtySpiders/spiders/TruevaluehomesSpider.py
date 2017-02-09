import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class TruevaluehomesSpider(CrawlSpider):
    name = 'truevaluehomes'
    allowed_domains = ['www.truevaluehomes.com.au']
    start_urls = ['http://www.truevaluehomes.com.au']
    rules = (
        Rule(LinkExtractor(allow=('/homes/new-home-designs(/[\w-]+)?$')), callback='parseItem', follow=True),
        Rule(LinkExtractor(allow=('/homes/house-land-packages(\?start=[0-9]+)?$')), callback='parseList', follow=True),
        Rule(LinkExtractor(allow=('/homes/house-land-packages$')), callback='parseList', follow=True),
        # Rule(LinkExtractor(allow=('/homes/new-home-designs/[\w-]+$')), callback='parseItem'),
    )

    logo = 'True Value Homes'

    def parseList(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        hxsItemsList = hxs.select('//div[@id="itemListPrimary"]/div[@class="itemContainer itemContainerLast"]')
        for hxsItems in hxsItemsList:
            l = RealtyLoader(RealtyspidersItem(), hxsItems)
            l.add_value('BuildType', self._getBuildType(response.url))
            l.add_value('BuilderEmailAddress', 'info@truevaluehomes.com.au')
            l.add_value('BuilderLogo', self.logo)
            l.add_value('url', response.url)
            l.add_xpath('DesignName', './/div[@class="packages-cat-title"]/text()', **{'re': '.*-'})
            l.add_xpath('Squares', './/div[@class="packages-cat-title"]/text()', **{'re': '\d+\ssq'})
            l.add_xpath('Region', './/div[@class="packages-cat-middle"]/div[@class="estate"]/text()', **{'re': ',.*'})
            l.add_xpath('DisplayLocation', './/div[@class="packages-cat-middle"]/div[@class="estate"]/text()',
                        **{'re': '.*,'})
            l.add_xpath('LandSize', './/div[@class="packages-cat-middle"]/div[@class="sq"]/text()')
            l.add_xpath('Bedrooms', './/div[@class="packages-cat-middle"]/div[@class="bed"]/text()')
            l.add_xpath('Bathrooms', './/div[@class="packages-cat-middle"]/div[@class="bath"]/text()')
            l.add_xpath('Garage', './/div[@class="packages-cat-middle"]/div[@class="car"]/text()')
            l.add_xpath('BrochureImage_pdf', './/div[@class="brochure"]/a/@href', **{'myRefer': referer})
            l.add_xpath('BasePrice', '''.//div[@class="price"]/strong/text()''')
            l.add_xpath('HomeDesignMainImage', './/div[@class="packages-cat-left"]/img/@src',
                        **{'myRefer': self.start_urls[0]})
            yield l.load_item()




            # item = RealtyspidersItem()
            # with open('data.html', 'a') as file:
            #     file.write(hxsItems.extract())
            #     file.write('-' * 100 + '\n')
            # # print(hxsItems is hxs)
            # print(type(hxsItems.root.xpath))
            # print(hxsItems.namespaces)
            # item['DesignName'] = hxsItems.xpath('//div[@class="packages-cat-title"]/text()').extract()
            # item['BasePrice'] = hxsItems.select('.//div[@class="price"]/strong/text()').extract()
            # print(item['BasePrice'])
            # print(hxsItems.extract())
            # print(hxsItems.xpath('//div[@class="price"]/strong/text()'))

    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        if self._chakURL(response.url):
            if re.search(r'\d+-special-offers', response.url):
                return None
            hxs = HtmlXPathSelector(response)
            l = RealtyLoader(RealtyspidersItem(), hxs)
            l.add_value('BuildType', self._getBuildType(response.url))
            l.add_value('BuilderEmailAddress', 'info@truevaluehomes.com.au')

            try:
                l.add_value('HomeDesignMainImage', self.start_urls[0] + self.itemsList[response.url])
            except KeyError:
                pass
            l.add_value('BuilderLogo', self.logo)
            l.add_xpath('DesignName', '//div[@class="content-columns"]/h2[1]/text()')
            l.add_xpath('Squares', '//div[@id="house-details"]/div[@class="sq"]/text()')
            l.add_xpath('Bedrooms', '//div[@id="house-details"]/div[@class="bed"]/text()')
            l.add_xpath('Bathrooms', '//div[@id="house-details"]/div[@class="bath"]/text()')
            l.add_xpath('Garage', '//div[@id="house-details"]/div[@class="car"]/text()')
            l.add_xpath('BrochureImage_pdf', '//div[@class="house-attachment"]/a[text()="Download Brochure"]/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('FloorPlanImage1',
                        '//li[@class="sigProThumb"][1]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image1', '//li[@class="sigProThumb"][2]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image2', '//li[@class="sigProThumb"][3]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image3', '//li[@class="sigProThumb"][4]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image4', '//li[@class="sigProThumb"][5]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image5', '//li[@class="sigProThumb"][6]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image6', '//li[@class="sigProThumb"][7]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image7', '//li[@class="sigProThumb"][8]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image8', '//li[@class="sigProThumb"][9]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image9', '//li[@class="sigProThumb"][10]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image10', '//li[@class="sigProThumb"][11]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image11', '//li[@class="sigProThumb"][12]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image12', '//li[@class="sigProThumb"][12]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image13', '//li[@class="sigProThumb"][14]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image14', '//li[@class="sigProThumb"][15]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_xpath('Image15', '//li[@class="sigProThumb"][16]/span/span/a/@href',
                        **{'myRefer': self.start_urls[0]})
            l.add_value('url', response.url)

            descriptionXPath = '//div[@id="content-body"]/div/ul/li/span/text()'
            # Block Yes No
            l.add_xpath('TheatreRoom_Yes_No',
                        descriptionXPath, **{'re': '([Tt]heatre.*[Rr]ooms?)|([Rr]ooms?.*[Tt]heatre)'})
            l.add_xpath('SeparateMeals_Yes_No',
                        descriptionXPath, **{'re': '([Ss]eparate.*[Mm]eals)|([Mm]eals.*[Ss]eparate)'})
            l.add_xpath('Alfresco_Yes_No',
                        descriptionXPath, **{'re': '[Aa]lfresco'})
            l.add_xpath('Study_Yes_No',
                        descriptionXPath, **{'re': '([Ss]tudy)|([Ss}chool)|([Uu]niversity)'})
            l.add_xpath('WalkinPantry_Yes_No',
                        descriptionXPath, **{'re': '([Ww]alkin|[Pp]antry)'})
            l.add_xpath('BultersPantry_Yes_No',
                        descriptionXPath, **{'re': '[Bb]ulter[`]?s?'})
            l.add_xpath('BultersPantry_Yes_No',
                        descriptionXPath, **{'re': '[Bb]ulter[`]?s?'})
            l.add_xpath('SteelStructure_Yes_No',
                        descriptionXPath, **{'re': '([Ss]teel.*[Ss]tructure)|([Ss]tructure.*[Ss]teel)'})
            l.add_xpath('Balcony_Yes_No',
                        descriptionXPath, **{'re': '[Bb]alcony'})

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
            # l.add_xpath('KitchenAppliance',
            #             descriptionXPath, **{'re': '.*([Kk]itchen.*[Aa]ppliance).*|.*([Aa]ppliance.*[Kk]itchen).*'})
            # Бренд пристрою
            # l.add_xpath('ApplianceBrand',
            #             descriptionXPath, **{'re': '.*[\w\s]+[Ss]ecurity System.*'})
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
            # # інші штуки
            # l.add_xpath('OtherInclusions',
            #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
            # l.add_xpath('OtherInclusions1',
            #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
            # l.add_xpath('OtherInclusions2',
            #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
            # l.add_xpath('OtherInclusions3',
            #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
            # l.add_xpath('OtherInclusions4',
            #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})
            # l.add_xpath('OtherInclusions5',
            #             descriptionXPath, **{'re': '[\w\s]+[Ss]ecurity System'})


            return l.load_item()
        else:
            hxs = HtmlXPathSelector(response)
            itemsURL = hxs.xpath('//div[@class="homes-cat-left"]/a/@href').extract()
            imgURL = hxs.xpath('//div[@class="homes-cat-left"]/a/img/@src').extract()
            itemsURL = list(map(lambda x: self.start_urls[0] + x, itemsURL))
            self.itemsList = {items: img for items, img in zip(itemsURL, imgURL)}

    def _chakURL(self, url):
        if re.search(r'http://www.truevaluehomes.com.au/homes/new-home-designs$', url):
            return False
        return True

    def _getBuildType(self, url):
        if url.find('new-home-designs') != -1:
            return 'Home Designs'
        elif url.find('house-land-packages') != -1:
            return 'House & Land Packages'
            # elif url.find('display-homes') != -1:
            #     return 'Display Homes'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(TruevaluehomesSpider)
    process.start()
