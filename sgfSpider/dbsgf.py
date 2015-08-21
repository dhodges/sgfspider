# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy     import MetaData
from sqlalchemy     import create_engine
from sqlalchemy.sql import table
from sqlalchemy.orm import sessionmaker

from sgfSpider.items   import IgokisenGameItem
from sgfSpider.items   import IgokisenNewsItem
from sgfSpider.dbitems import DBGameItem
from sgfSpider.dbitems import DBNewsItem

import os
import pdb
import contextlib
import logging

Base = declarative_base()

class DBsgf():
  def __init__(self):
    self._setupEngine()
    self.session = sessionmaker(bind=self.engine)()

  def _setupEngine(self):
    if not 'DB_URL' in os.environ.keys():
      raise Exception("os.environ['DB_URL'] undefined")
    self.engine = create_engine(
        os.environ['DB_URL'],
        isolation_level="READ UNCOMMITTED"
    )
    Base.metadata.create_all(self.engine)

  def _deleteAllTables(self):
    logging.warning('deleting all items in db: %s' % os.environ['DB_URL'])
    conn = self.engine.connect()
    conn.execute(table(DBGameItem.__tablename__).delete())
    conn.execute(table(DBNewsItem.__tablename__).delete())

  def _dbClass(self, item):
    if item.__class__ == IgokisenNewsItem:
      return DBNewsItem
    elif item.__class__ == IgokisenGameItem:
      return DBGameItem
    else:
      raise Exception("Unknown item class: %s" % item.__class__)

  def exists(self, item):
    self.session.new
    dbClass = self._dbClass(item)
    results = self.session.query(dbClass).filter_by(**item.queryFields()).all()
    return len(results) >= 1


  def add(self, item):
    self.session.new
    dbClass = self._dbClass(item)
    dbItem = dbClass(**item.toDict())
    self.session.add(dbItem)
    self.session.commit()

