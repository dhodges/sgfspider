#!/usr/bin/env python

import os
import pdb
import json
import subprocess

from sys      import argv, exit
from dotenv   import load_dotenv
from os.path  import join, dirname
from datetime import datetime

from sgfSpider.items      import IgokisenGameItem
from sgfSpider.dbsgf      import DBsgf

from scrapy.utils.project import get_project_settings

from tests.testing_utils  import setupEnviron

FILES_STORE = join(get_project_settings()['FILES_STORE'], 'full')


def progname():
  return argv[0].split('/')[-1:][0]

def usage_and_exit():
  print('# usage: %s <items.json>' % progname())
  exit(1)

def check_args():
  if not len(argv) == 1:
    usage_and_exit()

def verify_sgfinfo():
  try:
    subprocess.check_output(['which', 'sgfinfo'])
  except Exception:
    print("error: `sgfinfo' is not installed")
    exit(1)

def downloaded_sgf_files():
  for f in os.listdir(FILES_STORE):
    sgf_file = join(FILES_STORE, f)
    sgf_info = subprocess.check_output(['sgfinfo', sgf_file])
    sgf_info = json.loads(sgf_info)
    yield (sgf_file, sgf_info)

def first_date(datestr):
  """`datestr' may be a date range - extract the first date"""
  datestr = datestr.split(',')[0]
  return datetime.strptime(datestr, '%Y-%m-%d').date()

def game_item(f, info):
  item = IgokisenGameItem()
  item['date']         = first_date(info['Date'])
  item['result']       = info['Result']
  item['event']        = info['Event']
  item['player_black'] = info['PlayerBlackName']
  item['player_white'] = info['PlayerWhiteName']
  item['sgf'] = ''.join(open(f, 'r').readlines()).strip()
  return item

def gather_games():
  db  = DBsgf()
  num = 0
  for f, info in downloaded_sgf_files():
    try:
      db.add(game_item(f, info))
      os.remove(f)
      num += 1
    except Exception as err:
      print("error while loading file: '%s':" % f)
      print(err.message)
  print("%d new files added" % num)

if __name__ == '__main__':
  setupEnviron()
  check_args()
  verify_sgfinfo()
  gather_games()
