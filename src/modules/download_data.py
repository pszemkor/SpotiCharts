import concurrent.futures
import logging
from modules.fycharts_modified.SpotifyCharts import SpotifyCharts
import os

all_regions = [
    'global', 'ad', 'ar', 'at', 'au', 'be', 'bg', 'bo', 'br', 'ca', 'ch', 'cl', 'co', 'cr', 'cy', 'cz', 'de',
    'dk', 'do', 'ec', 'ee', 'es', 'fi', 'fr', 'gb', 'gr', 'gt', 'hk', 'hn', 'hu', 'id', 'ie', 'il', 'is', 'it',
    'jp', 'lt', 'lu', 'lv', 'mc', 'mt', 'mx', 'my', 'ni', 'nl', 'no', 'nz', 'pa', 'pe', 'ph', 'pl', 'pt', 'py',
    'ro', 'se', 'sg', 'sk', 'sv', 'th', 'tr', 'tw', 'us', 'uy', 'vn', 'za']

api = SpotifyCharts()


def pull_country_data(path, region, list_type, start, end):
    output_file = '{}/{}/{}.csv'.format(path, list_type, region)
    if list_type == 'viral50':
        api.viral50Daily(output_file=output_file, start=start, end=end, region=region)
    elif list_type == 'top200':
        api.top200Daily(output_file=output_file, start=start, end=end, region=region)


def save_csv_for_regions(path='./data', regions=None, list_type='top200', start='2017-01-01', end='2021-03-21'):
    if regions is None:
        regions = all_regions
    regions_types = [(path, i, list_type, start, end) for i in regions]

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    full_path = path + '/' + list_type
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(regions_types)) as executor:
        executor.map(lambda p: pull_country_data(*p), regions_types)
