from enum import Enum
from functools import lru_cache

from modules.spoticharts import SpotiCharts


class Regions(Enum):
    PL = 'Poland'
    DE = 'Germany'
    CZ = 'Czechia'
    GLOBAL = 'Global'
    US = 'United States'
    MX = 'Mexico'
    CA = 'Canada'


COUNTRY_CODES = {
    Regions.PL: 'pl',
    Regions.DE: 'de',
    Regions.CZ: 'cz',
    Regions.GLOBAL: 'global',
    Regions.US: 'us',
    Regions.MX: 'mx',
    Regions.CA: 'ca'
}

DEMOGRAPHICS = {
    Regions.PL: 38,
    Regions.DE: 83,
    Regions.CZ: 10,
    Regions.GLOBAL: 7800,
    Regions.US: 328,
    Regions.MX: 126,
    Regions.CA: 38
}  # in milions

sc = SpotiCharts()

@lru_cache(maxsize=8)
def viral_50_dataframe(country_code, include_features=False):
    return sc.get_all_viral(country_codes=[country_code], include_audio_features=include_features)

@lru_cache(maxsize=8)
def top_200_dataframe(country_code, include_features=False):
    return sc.get_all_top_200(country_codes=[country_code], include_audio_features=include_features)

def apply_producer(chart, region):
    return chart['producer'](COUNTRY_CODES[region])

def apply_producer_with_audio_features(chart, region):
    return chart['producer'](COUNTRY_CODES[region], True)

CHARTS = {
    'top200' : {
        'name': 'TOP 200',
        'producer': top_200_dataframe,
    },
    'viral50': {
        'name': 'VIRAL 50',
        'producer': viral_50_dataframe,
    }
}
