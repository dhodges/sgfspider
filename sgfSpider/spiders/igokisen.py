# -*- coding: utf-8 -*-

import scrapy
from sgfSpider.items import IgokisenNewsItem

class IgokisenSpider(scrapy.Spider):
    name = "igokisen"
    allowed_domains = ["igokisen.web.fc2.com"]
    start_urls = [
        'http://igokisen.web.fc2.com/topics.html'
    ]

    def parse(self, response):
        this_year = self.get_year(response)
        for selection in response.xpath('//table[2]//tr')[1:]:
            yield IgokisenNewsItem(this_year).parse(selection)

    def get_year(self, response):
      year = response.css('table.right td.title-sub b')
      year = year.extract()[0] if len(year) else ''
      year = year.replace('<b>from ', '')
      year = year[0:4]
      return year
