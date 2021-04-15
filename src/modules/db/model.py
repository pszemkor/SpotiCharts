from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Top200(Base):
    __tablename__ = 'Top200'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spotify_id = Column(String)
    date = Column(Date)
    region = Column(String)
    position = Column(Integer)
    track_name = Column(String)
    artist = Column(String)
    streams = Column(Integer)


class Viral50(Base):
    __tablename__ = 'Viral50'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spotify_id = Column(String)
    date = Column(Date)
    region = Column(String)
    position = Column(Integer)
    track_name = Column(String)
    artist = Column(String)


class AudioFeatures(Base):
    __tablename__ = 'AudioFeatures'
    id = Column(String, primary_key=True)
    danceability = Column(Float)
    energy = Column(Float)
    loudness = Column(Float)
    speechiness = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    duration_ms = Column(Integer)