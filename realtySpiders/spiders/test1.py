# -*- coding: utf-8 -*-
with open('test', 'r+') as f:
    data = f.readlines()
    for v in data:
        # v = v.strip()
        v = v.replace(' ','')
        # v += ' = scrapy.Field()\n'
        v = v.replace('/','_')
        v = v.replace('-','_')
        f.write(v)

