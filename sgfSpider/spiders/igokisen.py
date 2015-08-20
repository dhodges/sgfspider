# -*- coding: utf-8 -*-

import pdb
import scrapy
from sgfSpider.dbsgf import DBsgf
from sgfSpider.items import IgokisenGameItem
from sgfSpider.items import IgokisenNewsItem

from os.path import join, dirname
from dotenv  import load_dotenv

load_dotenv(join(dirname(__file__), '../../.env'))


class IgokisenSpider(scrapy.Spider):
  name = "igokisen"
  allowed_domains = ["igokisen.web.fc2.com"]
  start_urls = [
    'http://igokisen.web.fc2.com/topics.html'
  ]

  def parse(self, response):
    db = DBsgf()
    this_year = self.get_year(response)
    for selection in response.xpath('//table[2]//tr')[1:]:
      item = IgokisenNewsItem(this_year).parse(selection)
      if not db.exists(item):
        db.add(item)
        url = response.urljoin(item['link'])
        yield scrapy.Request(url, callback=self.parseTournamentGames)

  # see: http://doc.scrapy.org/en/latest/intro/tutorial.html#following-links
  def parseTournamentGames(self, response):
    for link in response.xpath('//table[1]//a/@href').extract():
      item = IgokisenGameItem()
      item['link'] = link
      item['file_urls'] = [response.urljoin(link)]
      yield item

  def get_year(self, response):
    year = response.css('table.right td.title-sub b')
    year = year.extract()[0] if len(year) else ''
    year = year.replace('<b>from ', '')
    year = year[0:4]
    return year
