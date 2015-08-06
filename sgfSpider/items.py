# -*- coding: utf-8 -*-

# see: http://doc.scrapy.org/en/latest/topics/items.html

import re
from scrapy import Item, Field

last_date = ''

class IgokisenNewsItem(Item):
    date   = Field()
    game   = Field()
    link   = Field()

    def parse(self, row):
        global last_date
        self['date']   = last_date = self.rowDate(row)
        self['game']   = self.rowGame(row)
        self['link']   = self.rowLink(row)
        return self

    def rowDate(self, row):
        str = self.pluck(row, 'td/text()')
        return str if re.match('\d\d-\d\d', str) else last_date

    def rowLink(self, row):
        return self.pluck(row, 'td/a/@href')

    def rowGame(self, row):
        return self.pluck(row, 'td/a/text()')

    def pluck(self, row, selector):
        text = row.xpath(selector).extract()
        return text[0] if len(text) else ''
