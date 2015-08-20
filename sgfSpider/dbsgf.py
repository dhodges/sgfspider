# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy     import Column, Integer, String, Date
from sqlalchemy     import Sequence
from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
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


class DBsgf():
  def __init__(self):
    self.setupEngine()
    self.session = sessionmaker(bind=self.engine)()

  def setupEngine(self):
    self.engine = create_engine(
        os.environ['DB_URL'],
        isolation_level="READ UNCOMMITTED"
    )
    Base.metadata.create_all(self.engine)

  def addNewsItem(self, item):
    self.session.new
    results = self.session.query(DBNewsItem).filter_by(date=item['date'], game=item['game']).all()
    if len(results) < 1:
      newsItem = DBNewsItem(date=item['date'], site=item['site'], game=item['game'], nation=item['nation'], link=item['link'])
      self.session.add(newsItem)
      self.session.commit()
