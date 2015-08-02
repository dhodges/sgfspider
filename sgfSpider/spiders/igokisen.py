# -*- coding: utf-8 -*-

import scrapy
from sgfSpider.items import SgfSpiderItem

class IgokisenSpider(scrapy.Spider):
    name = "igokisen"
    allowed_domains = ["igokisen.web.fc2.com"]
    start_urls = [
        'http://igokisen.web.fc2.com/topics.html'
    ]

    def parse(self, response):
        for xpath_selection in response.xpath('//table[2]//tr'):
            yield SgfSpiderItem().parse(xpath_selection)
