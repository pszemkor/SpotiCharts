import pandas as pd
import plotly.graph_objects as go

from modules.const import apply_producer, apply_producer_with_audio_features
from modules.metrics import total_streams, number_of_songs, max_rank, average_metric


def plot_multiple_bar(data, title, with_labels=True):
    fig = add_multiple_sources(go.Figure(), data, with_labels)
    fig = add_timeline(fig, title)
    fig.show()


def add_multiple_sources(fig, data, with_labels=True):
    for name, values in data:
        if with_labels:
            x, y, labels = values
            fig.add_trace(
                go.Bar(x=x,
                       y=y,
                       name=name.value,
                       text=labels,
                       hoverinfo='text'))
        else:
            x, y = values
            fig.add_trace(
                go.Bar(x=x,
                       y=y,
                       name=name.value))

    return fig


def add_timeline(fig, title):
    fig.update_layout(
        title_text=title
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig


###### plots per artists

def plot(start_date, end_date, artist_name, regions, metric, title, chart):
    dates_range = pd.date_range(start_date, end_date, freq='d')
    requested_dates = list(dates_range.date)
    data = []  # (country, (dates, values))
    for region in regions:
        df = apply_producer(chart, region)

        artist_all = df[(df['artist'] == artist_name)]
        values, labels = metric(region, artist_all, requested_dates)
        data.append((region, (requested_dates, values, labels)))
    plot_multiple_bar(data, title)


def plot_total_streams(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Total number of streams for: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date,
                                                                            end_date)
    plot(start_date, end_date, artist_name, regions, total_streams, title, chart)


def plot_number_of_songs(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Number of songs: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date, end_date)
    plot(start_date, end_date, artist_name, regions, number_of_songs, title, chart)


def plot_max_rank(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Max rank of: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date, end_date)
    plot(start_date, end_date, artist_name, regions, max_rank, title, chart)


## Plots per song

def plot_songs_with_keyword(start_date, end_date, keyword, regions, metric, title, chart):
    dates_range = pd.date_range(start_date, end_date, freq='d')
    requested_dates = list(dates_range.date)
    data = []  # (country, (dates, values))
    for region in regions:
        df = apply_producer(chart, region)
        songs_all = df[df['track_name'].str.contains(keyword, na=False)]
        values, labels = metric(region, songs_all, requested_dates)
        data.append((region, (requested_dates, values, labels)))
    plot_multiple_bar(data, title)


def plot_total_streams_of_songs_with_keyword(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, total_streams, title, chart)


def plot_number_of_songs_with_keyword(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, number_of_songs, title, chart)


def plot_max_rank_of_songs_with_keyword(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, max_rank, title, chart)


## Plots with aggregated feature characteristics

def plot_songs_with_audio_feature(start_date, end_date, audio_feature, regions, metric, title, chart):
    dates_range = pd.date_range(start_date, end_date, freq='d')
    requested_dates = list(dates_range.date)
    data = []  # (country, (dates, values))
    for region in regions:
        df = apply_producer_with_audio_features(chart, region)
        values, labels = metric(region, df, requested_dates, audio_feature)
        data.append((region, (requested_dates, values, labels)))
    plot_multiple_bar(data, title)


def plot_average_value_of_audio_feature(chart, start_date, end_date, audio_feature, regions):
    title = '[{}] Average value of metric: {} from: {} to: {}'.format(chart['name'], audio_feature, start_date,
                                                                      end_date)
    plot_songs_with_audio_feature(start_date, end_date, audio_feature, regions, average_metric, title, chart)


### plot similarity


def plot_similarity(x, y, title):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=x,
               y=y,
               name='Similarity'))
    fig = add_timeline(fig, title)
    fig.show()
