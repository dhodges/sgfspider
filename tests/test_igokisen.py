#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pdb
import unittest

from datetime import date

from testing_utils     import setupTestDB, fake_response_from_file

from scrapy.http       import Response, Request, HtmlResponse
from sgfSpider.dbsgf   import DBsgf, DBNewsItem

from sgfSpider.spiders.igokisen import IgokisenSpider


class TestIgokisenSpider(unittest.TestCase):
  def setUp(self):
    setupTestDB()
    self.spider = IgokisenSpider()

  def testIgokisenNewsParsing(self):
    results = self.spider.parse(fake_response_from_file('Go_Topics.html'))
    # there should be 48 items
    for x in range(48):
      results.next()

    dbitems = DBsgf().session.query(DBNewsItem).order_by(DBNewsItem.date).all()
    self.assertEqual(len(dbitems), 48)

    item = dbitems[7]
    self.assertEqual(item.date.strftime('%Y-%m-%d'), '2015-04-02')
    self.assertEqual(item.game,  'GS Caltex Cup')
    self.assertEqual(item.link,  'file:///var/folders/08/1yh0yp1955z8rg6jdhrps2vw0000gn/T/kr/gs.html')
    self.assertEqual(item.nation,'Korea')
    self.assertEqual(item.site,  'igokisen')

  def testIgokisenGameParsing(self):
    results = self.spider.parseTournamentGames(fake_response_from_file('Gosei.html'))
    urls = []
    # there should be 4 items
    urls.extend(results.next()['file_urls'])
    urls.extend(results.next()['file_urls'])
    urls.extend(results.next()['file_urls'])
    urls.extend(results.next()['file_urls'])
    self.assertEqual(sorted(urls), [
      u'http://igokisen.web.fc2.com/jp/sgf/40goseit1.sgf',
      u'http://igokisen.web.fc2.com/jp/sgf/40goseit2.sgf',
      u'http://igokisen.web.fc2.com/jp/sgf/40goseit3.sgf',
      u'http://igokisen.web.fc2.com/jp/sgf/40goseit4.sgf'
    ])

if __name__ == '__main__':
    unittest.main()
