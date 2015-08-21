#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pdb
import contextlib
import unittest

from dotenv  import load_dotenv
from os.path import join, dirname, realpath

from scrapy.http     import Response, Request, HtmlResponse
from sgfSpider.dbsgf import DBsgf


def setupEnviron():
  dot_env_file = join(dirname(__file__), '../.env')
  if not os.path.exists(dot_env_file):
    raise Exception('missing .env file')
  load_dotenv(dot_env_file)
  if not 'DB_URL' in os.environ.keys():
    raise Exception("os.environ['DB_URL'] undefined")

def setupTestEnviron():
  setupEnviron()
  if not os.environ['DB_URL'].endswith('_test'):
    os.environ['DB_URL'] = os.environ['DB_URL'] + '_test'


def setupTestDB():
  setupTestEnviron()
  db = DBsgf()
  db._deleteAllTables()

  # with contextlib.closing(DBsgf().engine.connect()) as con:
  #   meta  = MetaData()
  #   trans = con.begin()
  #   for table in reversed(meta.sorted_tables):
  #     con.execute(table.delete())
  #   trans.commit()


def fixture(file_name):
  if not file_name[0] == '/':
      root_dir  = dirname(realpath(__file__))
      file_name = join(root_dir, 'fixtures/responses', file_name)
  return open(file_name, 'r').read()

# based upon:
# http://stackoverflow.com/questions/6456304/scrapy-unit-testing

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


