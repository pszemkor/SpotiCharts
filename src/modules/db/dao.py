from modules.db.model import Viral50, Top200, AudioFeatures


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
    def __init__(self, session):
        self.session = session

    def get_all(self, country_codes, start_date, end_date):
        return get_all_by_table(self.session, Top200, country_codes, start_date, end_date)


class Viral50Dao:
    def __init__(self, session):
        self.session = session

    def get_all(self, country_codes, start_date, end_date):
        return get_all_by_table(self.session, Viral50, country_codes, start_date, end_date)


class AudioFeaturesDao:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(AudioFeatures).all()
