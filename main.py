import csv

from scrapy.crawler import CrawlerProcess
from realtySpiders.spiders import spiders
from scrapy.utils.project import get_project_settings
from realtySpiders.settings import FEED_EXPORT_FIELDS, FEED_URI


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(spiders.FrenkenhomesSpider)
    process.crawl(spiders.NostrahomesSpider)
    process.crawl(spiders.ZuccalahomesSpider)
    process.start()

    # runner = CrawlerRunner(settings)
    # runner.crawl(spiders.FrenkenhomesSpider)
    # runner.crawl(spiders.NostrahomesSpider)
    # runner.crawl(spiders.ZuccalahomesSpider)
    # d = runner.join()
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()


if __name__ == '__main__':
    with open(FEED_URI, 'w') as file:
        writer = csv.DictWriter(file, FEED_EXPORT_FIELDS)
        writer.writeheader()
    main()
