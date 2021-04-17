from enum import Enum
from functools import lru_cache

from modules.spoticharts import SpotiCharts


class Regions(Enum):
    GLOBAL = 'Global'
    US = 'United States of America'
    GB = 'United Kingdom of Great Britain and Northern Ireland'
    AE = 'United Arab Emirates'
    AR = 'Argentina'
    AT = 'Austria'
    AU = 'Australia'
    BE = 'Belgium'
    BG = 'Bulgaria'
    BO = 'Bolivia, Plurinational State of'
    BR = 'Brazil'
    CA = 'Canada'
    CH = 'Switzerland'
    CL = 'Chile'
    CO = 'Colombia'
    CR = 'Costa Rica'
    CZ = 'Czechia'
    DE = 'Germany'
    DK = 'Denmark'
    DO = 'Dominican Republic'
    EC = 'Ecuador'
    EE = 'Estonia'
    EG = 'Egypt'
    ES = 'Spain'
    FI = 'Finland'
    FR = 'France'
    GR = 'Greece'
    GT = 'Guatemala'
    HK = 'Hong Kong'
    HN = 'Honduras'
    HU = 'Hungary'
    ID = 'Indonesia'
    IE = 'Ireland'
    IL = 'Israel'
    IN = 'India'
    IS = 'Iceland'
    IT = 'Italy'
    JP = 'Japan'
    KR = 'Korea, Republic of'
    LT = 'Lithuania'
    LU = 'Luxembourg'
    LV = 'Latvia'
    MA = 'Morocco'
    MX = 'Mexico'
    MY = 'Malaysia'
    NI = 'Nicaragua'
    NL = 'Netherlands'
    NO = 'Norway'
    NZ = 'New Zealand'
    PA = 'Panama'
    PE = 'Peru'
    PH = 'Philippines'
    PL = 'Poland'
    PT = 'Portugal'
    PY = 'Paraguay'
    RO = 'Romania'
    RU = 'Russian Federation'
    SA = 'Saudi Arabia'
    SE = 'Sweden'
    SG = 'Singapore'
    SK = 'Slovakia'
    SV = 'El Salvador'
    TH = 'Thailand'
    TR = 'Turkey'
    TW = 'Taiwan, Province of China'
    UA = 'Ukraine'
    UY = 'Uruguay'
    VN = 'Viet Nam'
    ZA = 'South Africa'


COUNTRY_CODES = {
    Regions.GLOBAL: 'global',
    Regions.US: 'us',
    Regions.GB: 'gb',
    Regions.AE: 'ae',
    Regions.AR: 'ar',
    Regions.AT: 'at',
    Regions.AU: 'au',
    Regions.BE: 'be',
    Regions.BG: 'bg',
    Regions.BO: 'bo',
    Regions.BR: 'br',
    Regions.CA: 'ca',
    Regions.CH: 'ch',
    Regions.CL: 'cl',
    Regions.CO: 'co',
    Regions.CR: 'cr',
    Regions.CZ: 'cz',
    Regions.DE: 'de',
    Regions.DK: 'dk',
    Regions.DO: 'do',
    Regions.EC: 'ec',
    Regions.EE: 'ee',
    Regions.EG: 'eg',
    Regions.ES: 'es',
    Regions.FI: 'fi',
    Regions.FR: 'fr',
    Regions.GR: 'gr',
    Regions.GT: 'gt',
    Regions.HK: 'hk',
    Regions.HN: 'hn',
    Regions.HU: 'hu',
    Regions.ID: 'id',
    Regions.IE: 'ie',
    Regions.IL: 'il',
    Regions.IN: 'in',
    Regions.IS: 'is',
    Regions.IT: 'it',
    Regions.JP: 'jp',
    Regions.KR: 'kr',
    Regions.LT: 'lt',
    Regions.LU: 'lu',
    Regions.LV: 'lv',
    Regions.MA: 'ma',
    Regions.MX: 'mx',
    Regions.MY: 'my',
    Regions.NI: 'ni',
    Regions.NL: 'nl',
    Regions.NO: 'no',
    Regions.NZ: 'nz',
    Regions.PA: 'pa',
    Regions.PE: 'pe',
    Regions.PH: 'ph',
    Regions.PL: 'pl',
    Regions.PT: 'pt',
    Regions.PY: 'py',
    Regions.RO: 'ro',
    Regions.RU: 'ru',
    Regions.SA: 'sa',
    Regions.SE: 'se',
    Regions.SG: 'sg',
    Regions.SK: 'sk',
    Regions.SV: 'sv',
    Regions.TH: 'th',
    Regions.TR: 'tr',
    Regions.TW: 'tw',
    Regions.UA: 'ua',
    Regions.UY: 'uy',
    Regions.VN: 'vn',
    Regions.ZA: 'za'
}

DEMOGRAPHICS = {
    Regions.PL : 38,
    Regions.DE : 83,
    Regions.CZ : 10,
    Regions.GLOBAL: 7800,
    Regions.US: 328,
    Regions.MX: 126,
    Regions.CA: 38,
    Regions.GB: 67,
    Regions.AE: 9,
    Regions.AR: 42,
    Regions.AT: 8,
    Regions.AU: 23,
    Regions.BE: 11,
    Regions.BG: 7,
    Regions.BO: 10,
    Regions.BR: 203,
    Regions.CA: 35,
    Regions.CH: 8,
    Regions.CL: 17,
    Regions.CO: 47,
    Regions.CR: 4,
    Regions.CZ: 11,
    Regions.DE: 80,
    Regions.DK: 5,
    Regions.DO: 10,
    Regions.EC: 15,
    Regions.EE: 1,
    Regions.EG: 87,
    Regions.ES: 46,
    Regions.FI: 5,
    Regions.FR: 66,
    Regions.GR: 10,
    Regions.GT: 15,
    Regions.HK: 7,
    Regions.HN: 8,
    Regions.HU: 9,
    Regions.ID: 252,
    Regions.IE: 6,
    Regions.IL: 8,
    Regions.IN: 1263,
    Regions.IS: 0.4,
    Regions.IT: 60,
    Regions.JP: 127,
    Regions.KR: 52,
    Regions.LT: 2,
    Regions.LU: 0.6,
    Regions.LV: 1,
    Regions.MA: 33,
    Regions.MX: 119,
    Regions.MY: 30,
    Regions.NI: 6,
    Regions.NL: 16,
    Regions.NO: 5,
    Regions.NZ: 4,
    Regions.PA: 3,
    Regions.PE: 30,
    Regions.PH: 100,
    Regions.PL: 38,
    Regions.PT: 10,
    Regions.PY: 6,
    Regions.RO: 19,
    Regions.RU: 146,
    Regions.SA: 30,
    Regions.SE: 9,
    Regions.SG: 5,
    Regions.SK: 5,
    Regions.SV: 6,
    Regions.TH: 64,
    Regions.TR: 76,
    Regions.UA: 42,
    Regions.UY: 3,
    Regions.VN: 97,
    Regions.ZA: 54
} # in milions

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
