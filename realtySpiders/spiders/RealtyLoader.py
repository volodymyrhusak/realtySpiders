import re
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader import XPathItemLoader
from scrapy.utils.misc import arg_to_iter, extract_regex
from scrapy.utils.python import flatten
from scrapy.loader.common import wrap_loader_context


class RealtyLoader(XPathItemLoader):
    default_output_processor = TakeFirst()

    def add_refer(self, myRefer, x):
        return '{}{}'.format(myRefer, x)

    def reSub(self, r, x):
        x = re.sub(r, '', x)
        return x

    def get_value(self, value, *processors, **kw):
        regex = kw.get('re', None)
        if regex:
            value = arg_to_iter(value)
            value = flatten(extract_regex(regex, x) for x in value)

        myRefer = kw.get('myRefer', None)
        if myRefer:
            value = arg_to_iter(value)
            value = flatten(self.add_refer(myRefer, x) for x in value)

        reg = kw.get('reSub', None)
        if reg:
            value = arg_to_iter(value)
            value = flatten(self.reSub(reg, x) for x in value)

        for proc in processors:
            if value is None:
                break
            proc = wrap_loader_context(proc, self.context)
            value = proc(value)
        return value
