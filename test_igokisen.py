#!/usr/bin/env python
# -*- coding: utf-8 -*-

# based upon:
# http://stackoverflow.com/questions/6456304/scrapy-unit-testing

import pdb
import unittest

from os.path import dirname
from os.path import realpath
from os.path import join

from scrapy.http       import Response, Request, HtmlResponse
from sgfSpider.items   import IgokisenNewsItem
from sgfSpider.spiders.igokisen import IgokisenSpider


def fixture(file_name):
  if not file_name[0] == '/':
      root_dir  = dirname(realpath(__file__))
      file_name = join(root_dir, 'fixtures/responses', file_name)
  return open(file_name, 'r').read()

def fake_response_from_file(file_name, url='http://www.example.com'):
    """
    Create a Scrapy fake HTTP response from an HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    response = HtmlResponse(
        url     = url,
        request = Request(url=url),
        body    = fixture(file_name),
        encoding = 'utf-8'
    )
    return response


class TestIgokisenSpider(unittest.TestCase):

  def setUp(self):
    self.spider  = IgokisenSpider()
    self.results = self.spider.parse(fake_response_from_file('Go_Topics.html'))

  def testIgokisenSpider(self):
    self.assertEqual(self.results.__sizeof__(), 48)
    item = self.results.next()
    self.assertEqual(item['game'],   'Gosei')
    self.assertEqual(item['date'],   '2015-07-27')
    self.assertEqual(item['nation'], 'Japan')
    self.assertEqual(item['link'],   'file:///var/folders/08/1yh0yp1955z8rg6jdhrps2vw0000gn/T/jp/gosei.html')


if __name__ == '__main__':
    unittest.main()
