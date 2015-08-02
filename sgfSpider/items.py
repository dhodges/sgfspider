# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
from scrapy import Item, Field

class SgfSpiderItem(Item):
    date = Field()
    game = Field()
    link = Field()

    def parse(self, row):
        self['date'] = self.rowDate(row)
        self['game'] = self.rowGame(row)
        self['link'] = self.rowLink(row)
        return self

    def rowDate(self, row):
        str  = row.xpath('td/text()') or ''
        str  = str[0].extract() if len(str) else ''
        return str if re.match('\d\d-\d\d', str) else ''

    def rowLink(self, row):
        sgf = row.xpath('td/a/@href').extract()
        return sgf[0] if len(sgf) else ''

    def rowGame(self, row):
        text = row.xpath('td/a/text()')
        return text.extract()[0] if len(text) else ''

