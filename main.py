import csv
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.FrenkenhomesSpider import FrenkenhomesSpider
from realtySpiders.spiders.NostrahomesSpider import NostrahomesSpider
from realtySpiders.spiders.TruevaluehomesSpider import TruevaluehomesSpider
from realtySpiders.spiders.ZuccalahomesSpider import ZuccalahomesSpider
from realtySpiders.spiders.BentleyhomesSpider import BentleyhomesSpider
from scrapy.utils.project import get_project_settings
from realtySpiders.settings import FEED_EXPORT_FIELDS

'''
www.frenkenhomes.com.au +
www.nostrahomes.com.au +
www.hermitagehomes.com.au +
www.zuccalahomes.com.au +
www.truevaluehomes.com.au +
www.rawdonhillhomes.com.au
www.bentleyhomes.com.au -
www.busbyhomes.com.au
www.ashfordhomes.com.au
www.esperancehomes.com.au
www.hamlanhomes.com.au
www.hallsburyhomes
www.valecohomes.com.au
www.stylemasterhomes.com.au
www.hallmarkhomes.com.au
'''


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    # First milestone
    process.crawl(FrenkenhomesSpider)
    process.crawl(NostrahomesSpider)
    process.crawl(ZuccalahomesSpider)
    # Second milestone
    process.crawl(TruevaluehomesSpider)
    process.crawl(BentleyhomesSpider)
    process.start()


if __name__ == '__main__':
    with open('Result.csv', 'w') as file:
        writer = csv.DictWriter(file, FEED_EXPORT_FIELDS)
        writer.writeheader()
    main()
