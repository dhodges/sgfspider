# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy      import Column, Integer, String, Date
from sqlalchemy      import Sequence

from sgfSpider.items import IgokisenGameItem
from sgfSpider.items import IgokisenNewsItem

import pdb

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


