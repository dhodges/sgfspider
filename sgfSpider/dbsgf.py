# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy     import Column, Integer, String, Date
from sqlalchemy     import Sequence
from sqlalchemy     import MetaData
from sqlalchemy     import create_engine
from sqlalchemy.sql import table
from sqlalchemy.orm import sessionmaker

from sgfSpider.items import IgokisenGameItem
from sgfSpider.items import IgokisenNewsItem

import os
import pdb
import contextlib

Base = declarative_base()

class DBNewsItem(Base):
  __tablename__ = 'tournament_news_items'
  id     = Column(Integer, Sequence('tournament_news_item_id_seq'), primary_key=True)
  date   = Column(Date)
  site   = Column(String)
  game   = Column(String)
  nation = Column(String)
  link   = Column(String)

  def __repr__(self):
    return "<TournamentNewsItem(date='%s', nation='%s', game='%s')>" % (
      self.date, self.nation, self.game)


class DBGameItem(Base):
  __tablename__ = 'tournament_games'
  id          = Column(Integer, Sequence('tournament_games_id_seq'), primary_key=True)
  date        = Column(Date)
  link        = Column(String)
  sgf         = Column(String)
  event       = Column(String)
  tournament  = Column(String)
  playerBlack = Column(String)
  playerWhite = Column(String)
  result      = Column(String)

  def __repr__(self):
    return "<TournamentGameItem(date='%s', tournament='%s', event='%s', playerBlack='%s', playerWhite='%s', result='%s')>" % (
      self.date, self.tournament, self.event, self.playerBlack, self.playerWhite, self.result)


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

