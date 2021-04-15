import pandas as pd

from modules.db.connection import Session
from modules.db.model import Viral50, Top200, AudioFeatures


class SpotiCharts:
    def __init__(self):
        self.session = Session()

    def get_all_viral(self, country_codes=None, start_date=None, end_date=None, include_audio_features=True):
        return self.__get_all_by_type(Viral50, country_codes, start_date, end_date, include_audio_features)

    def get_all_top_200(self, country_codes=None, start_date=None, end_date=None, include_audio_features=True):
        return self.__get_all_by_type(Top200, country_codes, start_date, end_date, include_audio_features)

    def get_audio_features(self):
        return self.__get_dataframe(AudioFeatures)

    def __get_all_by_type(self, table, country_codes, start_date, end_date, include_audio_features):
        predicates = []
        if country_codes:
            predicates.append(table.region.in_(country_codes))
        if start_date:
            predicates.append(start_date <= table.date)
        if end_date:
            predicates.append(table.date <= end_date)
        res = self.session.query(table).filter(*predicates).all()

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
        res = self.session.query(type).all()
        if len(res) == 0:
            raise Exception('No results matching the given criteria')

        dicts = list(map(lambda item: item.__dict__, res))
        df = pd.DataFrame(dicts)
        df.drop(columns=['_sa_instance_state'], inplace=True)
        return df
