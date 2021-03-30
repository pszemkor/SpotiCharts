from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db import AudioFeatures, Viral50, Top200
import pandas as pd
from datetime import date


class ViralService:
    def __init__(self, engine):
        self.engine = engine

    def get_all(self, include_audio_features=True):
        session = Session(bind=self.engine)
        res = session.query(Viral50).all()
        dicts = list(map(lambda item: item.__dict__, res))
        if include_audio_features:
            pass
        df = pd.DataFrame(dicts)
        df = df.drop(columns=['id', '_sa_instance_state'])
        session.close()
        return df

    def get_all_by(self, country_code, include_audio_features=True, begin_date=None,
                   end_date=None):
        session = Session(bind=self.engine)
        res = session.query(Viral50).filter(
            Viral50.region == country_code and begin_date <= Viral50.date <= end_date).all()
        dicts = list(map(lambda item: item.__dict__, res))
        if include_audio_features:
            pass
        df = pd.DataFrame(dicts)
        df = df.drop(columns=['id', '_sa_instance_state'])
        session.close()
        return df


class SpotiCharts:
    def __init__(self, db_string='sqlite:///spoticharts.db'):
        engine = create_engine(db_string, echo=True)
        engine.connect()
        self.engine = engine
        self.viral_service = ViralService(engine)

    def viral(self):
        return self.viral_service

    def get_audio_features(self):
        pass


if __name__ == '__main__':
    sc = SpotiCharts()
    df = sc.viral().get_all()
    print(df.head())
    print(df.columns)
