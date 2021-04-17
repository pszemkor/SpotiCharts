from contextlib import contextmanager

from modules.db.connection import Session
from modules.db.model import Viral50, Top200, AudioFeatures


@contextmanager
def db_session():
    session = Session()
    yield session
    session.close()


def get_all_by_table(session, table, country_codes, start_date, end_date):
    predicates = []
    if country_codes:
        predicates.append(table.region.in_(country_codes))
    if start_date:
        predicates.append(start_date <= table.date)
    if end_date:
        predicates.append(table.date <= end_date)
    return session.query(table).filter(*predicates).all()


class Top200Dao:
    def get_all(self, country_codes, start_date, end_date):
        with db_session() as session:
            return get_all_by_table(session, Top200, country_codes, start_date, end_date)


class Viral50Dao:
    def get_all(self, country_codes, start_date, end_date):
        with db_session() as session:
            return get_all_by_table(session, Viral50, country_codes, start_date, end_date)


class AudioFeaturesDao:
    def get_all(self):
        with db_session() as session:
            return session.query(AudioFeatures).all()
