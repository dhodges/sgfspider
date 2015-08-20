# -*- coding: utf-8 -*-

# see: http://doc.scrapy.org/en/latest/topics/items.html

import re
from scrapy import Item, Field

last_date = ''
this_year = ''

class IgokisenGameItem(Item):
    date        = Field()
    link        = Field()
    sgf         = Field()
    tournament  = Field()
    playerBlack = Field()
    playerWhite = Field()
    result      = Field()
    file_urls   = Field() # for downloaded sgf game file(s)
    files       = Field() # as used by the scrapy media pipeline

    def queryFields(self):
        return self.toDict(fields=('date', 'tournament', 'event', 'playerBlack', 'playerWhite'))

    def toDict(self, fields=('date', 'link', 'sgf', 'tournament', 'playerBlack', 'playerWhite', 'result')):
        return {k: self[k] for k in fields}

class IgokisenNewsItem(Item):
    date   = Field()
    site   = Field()
    nation = Field()
    game   = Field()
    link   = Field()

    def __init__(self, year):
        global this_year
        this_year = year
        Item.__init__(self)

    def queryFields(self):
        return self.toDict(fields=('date', 'game'))

    def toDict(self, fields=('date', 'site', 'nation', 'game', 'link')):
        return {k: self[k] for k in fields}

    def parse(self, row):
        global last_date
        self['date']   = last_date = self.rowDate(row)
        self['site']   = 'igokisen'
        self['nation'] = self.rowNation(row)
        self['game']   = self.rowGame(row)
        self['link']   = self.rowLink(row)
        return self

    def rowDate(self, row):
        global this_year
        str = self.pluck(row, 'td/text()')
        if re.match('\d\d-\d\d', str):
            return '%s-%s' % (this_year, str)
        else:
            return last_date

    def rowNation(self, row):
        return self.pluck(row, 'td/span/text()')

    def rowLink(self, row):
        return self.pluck(row, 'td/a/@href')

    def rowGame(self, row):
        return self.pluck(row, 'td/a/text()')

    def pluck(self, row, selector):
        text = row.xpath(selector).extract()
        return text[0] if len(text) else ''
