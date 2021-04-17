import pandas as pd

from modules.db.connection import Session
from modules.db.dao import Top200Dao, Viral50Dao, AudioFeaturesDao


class SpotiCharts:
    def __init__(self):
        session = Session()
        self.top200Dao = Top200Dao(session)
        self.viral50Dao = Viral50Dao(session)
        self.audioDao = AudioFeaturesDao(session)

    def get_all_viral(self, country_codes=None, start_date=None, end_date=None, include_audio_features=True):
        res = self.top200Dao.get_all(country_codes, start_date, end_date)
        return self.__map_db_query_result(res, include_audio_features)

    def get_all_top_200(self, country_codes=None, start_date=None, end_date=None, include_audio_features=True):
        res = self.top200Dao.get_all(country_codes, start_date, end_date)
        return self.__map_db_query_result(res, include_audio_features)

    def get_audio_features(self):
        return self.__get_audio_features_dataframe()

    def __map_db_query_result(self, res, include_audio_features):
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

    def __get_audio_features_dataframe(self):
        res = self.audioDao.get_all()
        if len(res) == 0:
            raise Exception('No results matching the given criteria')

        dicts = list(map(lambda item: item.__dict__, res))
        df = pd.DataFrame(dicts)
        df.drop(columns=['_sa_instance_state'], inplace=True)
        return df
