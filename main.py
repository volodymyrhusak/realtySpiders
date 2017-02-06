import csv
import argparse
from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders.FrenkenhomesSpider import FrenkenhomesSpider
from realtySpiders.spiders.NostrahomesSpider import NostrahomesSpider
from realtySpiders.spiders.TruevaluehomesSpider import TruevaluehomesSpider
from realtySpiders.spiders.ZuccalahomesSpider import ZuccalahomesSpider
from realtySpiders.spiders.BentleyhomesSpider import BentleyhomesSpider
from realtySpiders.spiders.BusbyhomesSpider import BusbyhomesSpider
from realtySpiders.spiders.AshfordhomesSpider import AshfordhomesSpider
from realtySpiders.spiders.RawdonhillSpider import RawdonhillSpider
from realtySpiders.spiders.EsperancehomesSpider import EsperancehomesSpider
from realtySpiders.spiders.HallburyhomesSpiders import HallburyhomesSpider
from scrapy.utils.project import get_project_settings
from realtySpiders.settings import FEED_EXPORT_FIELDS

'''
www.frenkenhomes.com.au +
www.nostrahomes.com.au +
www.hermitagehomes.com.au +
www.zuccalahomes.com.au +
www.truevaluehomes.com.au +
www.bentleyhomes.com.au +
www.busbyhomes.com.au +
www.ashfordhomes.com.au +
www.rawdonhill.com.au +
www.esperancehomes.com.au -
www.hamlan.com.au
hallburyhomes.com.au -
www.valecohomes.com.au
www.stylemasterhomes.com.au
www.hallmarkhomes.com.au
'''

# First milestone
# process.crawl(FrenkenhomesSpider)
# process.crawl(NostrahomesSpider)
# process.crawl(ZuccalahomesSpider)
# Second milestone
# process.crawl(TruevaluehomesSpider)
# process.crawl(BentleyhomesSpider)
# process.crawl(BusbyhomesSpider)
# process.crawl(AshfordhomesSpider)

spiders = {
    'FrenkenhomesSpider': {'class': FrenkenhomesSpider, 'logo': FrenkenhomesSpider.logo},
    'NostrahomesSpider': {'class': NostrahomesSpider, 'logo': NostrahomesSpider.logo},
    'ZuccalahomesSpider': {'class': ZuccalahomesSpider, 'logo': ZuccalahomesSpider.logo},
    'TruevaluehomesSpider': {'class': TruevaluehomesSpider, 'logo': TruevaluehomesSpider.logo},
    'BentleyhomesSpider': {'class': BentleyhomesSpider, 'logo': BentleyhomesSpider.logo},
    'BusbyhomesSpider': {'class': BusbyhomesSpider, 'logo': BusbyhomesSpider.logo},
    'RawdonhillSpider': {'class': RawdonhillSpider, 'logo': RawdonhillSpider.logo},
    'EsperancehomesSpider': {'class': EsperancehomesSpider, 'logo': EsperancehomesSpider.logo},
    'HallburyhomesSpider': {'class': HallburyhomesSpider, 'logo': HallburyhomesSpider.logo},
    'AshfordhomesSpider': {'class': AshfordhomesSpider, 'logo': AshfordhomesSpider.logo}
}


def main(sName):
    global spiders
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    data = []

    if sName:
        with open('Result.csv', 'r') as rFile:
            for row in csv.reader(rFile):
                if row[-2] != spiders[sName]['logo']:
                    data.append(row)
            rFile.close()

        with open('Result.csv', 'w') as rFile:
            writer = csv.writer(rFile)
            for row in data:
                writer.writerow(row)
            rFile.close()

        process.crawl(spiders[sName]['class'])
    else:
        with open('Result.csv', 'w') as wFile:
            writer = csv.DictWriter(wFile, FEED_EXPORT_FIELDS)
            writer.writeheader()
        for s in spiders:
            process.crawl(spiders[s]['class'])
            print(spiders[s]['class'])
    process.start()


if __name__ == '__main__':
    help = ','.join([v for v in spiders])
    parse = parser = argparse.ArgumentParser()
    parse.add_argument('one', type=str, nargs='?', const='const-one', default=False, help=str(help))
    arg = parse.parse_args()
    sName = arg.one
    main(sName)
