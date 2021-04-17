####### METRICS

from modules.const import DEMOGRAPHICS
from collections import defaultdict
import statistics

def total_streams(region, artist_all, requested_dates):
    date_streams = {}
    date_songs = {}
    for vals in artist_all[['date', 'streams', 'track_name']].values:
            date_streams[vals[0]] = date_streams.get(vals[0], 0)
            date_streams[vals[0]] += vals[1]
            date_songs[vals[0]] = date_songs.get(vals[0], '')
            date_songs[vals[0]] += '<br>' + vals[2]
    return ([date_streams.get(date, 0) / DEMOGRAPHICS[region] for date in requested_dates],
            [date_songs.get(date, '') for date in requested_dates])

def number_of_songs(_region, artist_all, requested_dates):
    occurences = {}
    songs = {}
    for vals in artist_all[['date', 'position', 'track_name']].values:
            occurences[vals[0]] = occurences.get(vals[0], 0)
            occurences[vals[0]] += 1
            songs[vals[0]] = songs.get(vals[0], '')
            songs[vals[0]] += '<br>' + vals[2]
    return ([occurences.get(date, 0) for date in requested_dates],
            [songs.get(date, '') for date in requested_dates])


def max_rank(_region, artist_all, requested_dates):
    ranks = {}
    date_songs = {}
    for vals in artist_all[['date', 'position', 'track_name']].values:
        rank_of_song = vals[1]
        val = ranks.get(vals[0], 201)
        if val > rank_of_song:
            ranks[vals[0]] = rank_of_song
            date_songs[vals[0]] = vals[2]
    return ([ranks.get(date, 0) for date in requested_dates],
            [date_songs.get(date, '') for date in requested_dates])


def average_metric(_region, df, requested_dates, audio_feature):
    date_to_features = defaultdict(list)
    for vals in df[['date', audio_feature]].values:
        date_to_features[vals[0]].append(vals[1])
    return ([statistics.mean(date_to_features.get(date, [0])) for date in requested_dates],
            ['' for date in requested_dates])