# -*- coding: utf-8 -*-

# see: http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html
# see: http://mapfish.org/doc/tutorials/sqlalchemy.html

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import Sequence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TournamentNewsItem(Base):
  __tablename__ = 'tournament_news_items'
  id     = Column(Integer, Sequence('tournament_news_item_id_seq'), primary_key=True)
  date   = Column(Date)
  name   = Column(String)
  nation = Column(String)
  link   = Column(String)
  def __repr__(self):
    return "<TournamentNewsItem(date='%s', nation='%s', name='%s')>" % (
      self.date, self.nation, self.name)

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

def update_tournament_news():
  Session = sessionmaker(bind=engine)
  session = Session()
  session.new

  results = session.query(TournamentNewsItem).filter_by(date=date, name=name)
  if results.length < 1:
    newsItem = TournamentNewsItem(date=date, name=name, nation=nation, link=link)
    session.add(newsItem)
    session.commit()
