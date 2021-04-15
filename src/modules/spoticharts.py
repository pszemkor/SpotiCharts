from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modules.db import AudioFeatures, Viral50, Top200
import pandas as pd


class SpotiCharts:
    def __init__(self, db_string='sqlite:///spoticharts.db'):
        engine = create_engine(db_string, echo=True)
        engine.connect()
        self.engine = engine

    def get_all_viral(self, country_codes=None, start_date=None, end_date=None, include_audio_features=True):
        return self.__get_all_by_type(Viral50, country_codes, start_date, end_date, include_audio_features)

    def get_all_top_200(self, country_codes=None, start_date=None, end_date=None, include_audio_features=True):
        return self.__get_all_by_type(Top200, country_codes, start_date, end_date, include_audio_features)

    def get_audio_features(self):
        return self.__get_dataframe(AudioFeatures)

    def __get_all_by_type(self, table, country_codes, start_date, end_date, include_audio_features):
        session = Session(bind=self.engine)
        predicates = []
        if country_codes:
            predicates.append(table.region.in_(country_codes))
        if start_date:
            predicates.append(start_date <= table.date)
        if end_date:
            predicates.append(table.date <= end_date)
        res = session.query(table).filter(*predicates).all()
        session.close()

        dicts = list(map(lambda item: item.__dict__, res))
        if len(dicts) == 0:
            raise Exception('No results matching the given criteria')

        df = pd.DataFrame(dicts)
        df.drop(columns=['id', '_sa_instance_state'], inplace=True)
        if include_audio_features:
            audio_df = self.get_audio_features()
            audio_df.rename(columns={'id': 'spotify_id'}, inplace=True)
            df = pd.merge(df, audio_df, on="spotify_id")
        return df

    def __get_dataframe(self, type):
        session = Session(bind=self.engine)
        res = session.query(type).all()
        dicts = list(map(lambda item: item.__dict__, res))
        df = pd.DataFrame(dicts)
        df.drop(columns=['_sa_instance_state'], inplace=True)
        session.close()
        return df
