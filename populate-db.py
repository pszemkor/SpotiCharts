from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
import sys
import os
import pandas as pd

Base = declarative_base()


class Top200(Base):
    __tablename__ = 'Top200'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spotify_id = Column(String)
    date = Column(String)
    region = Column(String)
    position = Column(Integer)
    track_name = Column(String)
    artist = Column(String)
    streams = Column(Integer)


class Viral50(Base):
    __tablename__ = 'Viral50'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spotify_id = Column(String)
    date = Column(String)
    region = Column(String)
    position = Column(Integer)
    track_name = Column(String)
    artist = Column(String)


class AudioFeatures(Base):
    __tablename__ = 'AudioFeatures'
    id = Column(Integer, primary_key=True)
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


engine = create_engine('sqlite:///spoticharts.db', echo=True)
conn = engine.connect()
session = Session(bind=engine)
Base.metadata.create_all(engine)
path = sys.argv[1]
expected_dirs = {'top200': lambda item: Top200(**item), 'viral': lambda item: Viral50(**item)}
print("Reading data from:", path)
for dir in expected_dirs:
    print("Reading from:", dir)
    dir_path = os.path.join(path, dir)
    dir_df = None
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        print(file_path)
        df = pd.read_csv(file_path)
        df = df.rename({'track name': 'track_name'}, axis=1)
        values = df.T.to_dict().values()
        objects = list(map(lambda item: expected_dirs[dir](item), values))
        rows_count = len(objects)
        session.bulk_save_objects(objects)
        session.commit()
        print("{} rows from file: '{}' saved successfully".format(rows_count, file_name))
