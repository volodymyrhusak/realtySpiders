import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from realtySpiders.items import RealtyspidersItem
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from realtySpiders.spiders.RealtyLoader import RealtyLoader


class BusbyhomesSpider(CrawlSpider):
    name = 'busbyhomes'
    allowed_domains = ['busbyhomes.com.au']
    start_urls = ['https://busbyhomes.com.au/']
    rules = (
        Rule(LxmlLinkExtractor(allow=('https://busbyhomes.com.au/designer-homes/$')),
             callback='pasreLinks',follow=True),
        Rule(LxmlLinkExtractor(allow=('https://busbyhomes.com.au/new-homes/$')),
             callback='pasreLinks', follow=True),
        Rule(LxmlLinkExtractor(allow=('https://busbyhomes.com.au/recent-homes/$')),
             callback='pasreLinks', follow=True),

        # Rule(LxmlLinkExtractor(allow=('http://www.bentleyhomes.com.au/properties/[\w-]+/$'),
        #                        restrict_xpaths='//div[@class="block-content block-content-small-padding"]'),
        #      callback='parseItem', follow=True),
    )
    logo ='Busby Homes'

    def pasreLinks(self,response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        links = LxmlLinkExtractor(allow=('https://busbyhomes.com.au/portfolio-view/[\w-]+/$')).extract_links(response)
        for link in links:
            yield Request(link.url, callback=self.parseItem, dont_filter=True)


    def parseItem(self, response):
        referer = response.request.headers.get('Referer', None).decode("utf-8")
        hxs = HtmlXPathSelector(response)
        BuildType = self._getBuildType(referer)
        imgXpath = '//div[@class="portfolio-single__main-content"]/p/img[{}]/@src'
        descriptionXPath = '//div[@class="portfolio-single__main-content"]/p[2]/text()'
        l = RealtyLoader(RealtyspidersItem(), hxs)
        l.add_value('url', response.url)
        l.add_value('BuildType',BuildType)
        l.add_value('BuilderLogo', self.logo)
        if BuildType == 'PRESTIGE HOMES':
            l.add_value('State', 'MELBOURNE')
        l.add_xpath('BuilderEmailAddress',
                    '//div[@class="entry-content span5"]/p/strong[text()="Email:"]/following-sibling::a/text()')

        l.add_xpath('DesignName', '//h1[@class="title-header"]/text()')
        l.add_xpath('FloorPlanImage1', '//div[@class="entry-content span5"]/p[1]/a/@href')
        l.add_xpath('HomeDesignMainImage', '//div[@class="portfolio-single__main-content"]/p[1]/img/@src')
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
        l.add_xpath('HomeDesignMainImage', '//div[@class="portfolio-single__main-content"]/p[2]/text()')

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


        return l.load_item()


    def _getBuildType(self, url):

        if url.find('designer-homes') != -1:
            return 'DESIGNER HOMES'
        elif url.find('recent-homes') != -1:
            return 'RECENT HOMES'
        elif url.find('new-homes') != -1:
            return 'PRESTIGE HOMES'

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(BusbyhomesSpider)
    process.start()