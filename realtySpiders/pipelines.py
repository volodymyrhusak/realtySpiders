# -*- coding: utf-8 -*-
import csv
import os
# from six import string_types
# from scrapy import signals
from realtySpiders.settings import FEED_EXPORT_FIELDS
# from scrapy.xlib.pydispatch import dispatcher
from scrapy.exporters import CsvItemExporter


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class HeadlessCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        # args[0] is (opened) file handler
        # if file is not empty then skip headers

        kwargs['include_headers_line'] = False
        include_headers_line = True

        super(HeadlessCsvItemExporter, self).__init__(*args, **kwargs)


headers_not_written = True


class RealtyspidersPipeline(object):
    def __init__(self, **kwargs):
        self.file = open(os.path.abspath('Result.csv'), 'a')
        self.writer = csv.DictWriter(self.file, FEED_EXPORT_FIELDS)
        include_headers_line = False

        # self._writeHeaders()
        self._runSpiders = []

    # def _writeHeaders(self):
    #     global headers_not_written
    #     if headers_not_written:
    #         headers_not_written = False
    #         self.writer.writeheader()

    def process_item(self, item, spider):
        item = self._getYesNo(item)
        for i, v in item.items():
            item[i] = self._cleanItem(v)
        self.writer.writerow(item)
        return item

    def open_spider(self, spider):
        self._runSpiders.append(spider)

    # def close_spider(self, spider):
    #     self.file.close()

    def _cleanItem(self, item):
        return item.strip()

    def _getYesNo(self, item):
        if item['TheatreRoom_Yes_No']:
            item['TheatreRoom_Yes_No'] = 'Yes'
        else:
            item['TheatreRoom_Yes_No'] = 'N/A'

        if item['SeparateMeals_Yes_No']:
            item['SeparateMeals_Yes_No'] = 'Yes'
        else:
            item['SeparateMeals_Yes_No'] = 'N/A'

        if item['Alfresco_Yes_No']:
            item['Alfresco_Yes_No'] = 'Yes'
        else:
            item['Alfresco_Yes_No'] = 'N/A'

        if item['Study_Yes_No']:
            item['Study_Yes_No'] = 'Yes'
        else:
            item['Study_Yes_No'] = 'N/A'

        if item['WalkinPantry_Yes_No']:
            item['WalkinPantry_Yes_No'] = 'Yes'
        else:
            item['WalkinPantry_Yes_No'] = 'N/A'

        if item['BultersPantry_Yes_No']:
            item['BultersPantry_Yes_No'] = 'Yes'
        else:
            item['BultersPantry_Yes_No'] = 'N/A'

        if item['Void_Yes_No']:
            item['Void_Yes_No'] = 'Yes'
        else:
            item['Void_Yes_No'] = 'N/A'

        if item['His_HerWIR_Yes_No']:
            item['His_HerWIR_Yes_No'] = 'Yes'
        else:
            item['His_HerWIR_Yes_No'] = 'N/A'

        if item['BedroomGrFloor_Yes_No']:
            item['BedroomGrFloor_Yes_No'] = 'Yes'
        else:
            item['BedroomGrFloor_Yes_No'] = 'N/A'

        if item['SteelStructure_Yes_No']:
            item['SteelStructure_Yes_No'] = 'Yes'
        else:
            item['SteelStructure_Yes_No'] = 'N/A'

        if item['Balcony_Yes_No']:
            item['Balcony_Yes_No'] = 'Yes'
        else:
            item['Balcony_Yes_No'] = 'N/A'

        return item
