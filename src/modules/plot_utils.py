import pandas as pd
import plotly.graph_objects as go
import plotly
from plotly.offline import plot
from iso3166 import countries

from modules.const import apply_producer, apply_producer_with_audio_features, COUNTRY_CODES
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


def plot_multiple_geo(data, title):
    df = pd.DataFrame()

    for region, stats in data:
        date = stats[0]
        value = stats[1]
        d = {'date': date, 'value': value}
        df_country = pd.DataFrame(d)
        df_country['country_code'] = countries.get(COUNTRY_CODES[region])[2]
        df = df.append(df_country, ignore_index=True)

    zmin = df['value'].min()
    zmax = df['value'].max()

    data_slider = []
    days = []
    for day in df['date'].unique():
        days.append(day)
        df_day = df[df['date'] == day]

        data_one_day = dict(
            type='choropleth',
            locations=df_day['country_code'],
            z=df_day['value'].astype(float),
            zmin=zmin,
            zmax=zmax,
            colorscale='greens',
        )
        data_slider.append(data_one_day)

    steps = []
    for i in range(len(days)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label='Day {}'.format(days[i]))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]
    layout = dict(
        title_text=title,
        geo=dict(scope='world',
                 showcountries=True,
                 projection={'type': 'equirectangular'}),
        sliders=sliders)
    fig = dict(data=data_slider, layout=layout)
    plotly.offline.iplot(fig)


###### plots per artists

def plot(start_date, end_date, artist_name, regions, metric, title, chart, plot_callback):
    dates_range = pd.date_range(start_date, end_date, freq='d')
    requested_dates = list(dates_range.date)
    data = []  # (country, (dates, values))
    for region in regions:
        df = apply_producer(chart, region)

        artist_all = df[(df['artist'] == artist_name)]
        values, labels = metric(region, artist_all, requested_dates)
        data.append((region, (requested_dates, values, labels)))
    plot_callback(data, title)


def plot_total_streams(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Total number of streams for: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date, end_date)
    plot(start_date, end_date, artist_name, regions, total_streams, title, chart, plot_multiple_bar)


def plot_number_of_songs(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Number of songs: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date, end_date)
    plot(start_date, end_date, artist_name, regions, number_of_songs, title, chart, plot_multiple_bar)

def plot_max_rank(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Max rank of: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date, end_date)
    plot(start_date, end_date, artist_name, regions, max_rank, title, chart, plot_multiple_bar)

def plot_total_streams_geo(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Total number of streams for: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date, end_date)
    plot(start_date, end_date, artist_name, regions, total_streams, title, chart, plot_multiple_geo)

def plot_number_of_songs_geo(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Number of songs: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date, end_date)
    plot(start_date, end_date, artist_name, regions, number_of_songs, title, chart, plot_multiple_geo)

def plot_max_rank_geo(chart, start_date, end_date, artist_name, regions):
    title = '[{}] Max rank of: "{}" from: {} to: {}'.format(chart['name'], artist_name, start_date, end_date)
    plot(start_date, end_date, artist_name, regions, max_rank, title, chart, plot_multiple_geo)

## Plots per song

def plot_songs_with_keyword(start_date, end_date, keyword, regions, metric, title, chart, plot_callback):
    dates_range = pd.date_range(start_date,end_date,freq='d')
    requested_dates = list(dates_range.date)
    data = [] # (country, (dates, values))
    for region in regions:
        df = apply_producer(chart, region)
        songs_all = df[df['track_name'].str.contains(keyword, na=False)]
        values, labels = metric(region, songs_all, requested_dates)
        data.append((region, (requested_dates, values, labels)))
    plot_callback(data, title)


def plot_total_streams_of_songs_with_keyword(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, total_streams, title, chart, plot_multiple_bar)


def plot_number_of_songs_with_keyword(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, number_of_songs, title, chart, plot_multiple_bar)


def plot_max_rank_of_songs_with_keyword(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, max_rank, title, chart, plot_multiple_bar)


def plot_total_streams_of_songs_with_keyword_geo(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, total_streams, title, chart, plot_multiple_geo)


def plot_number_of_songs_with_keyword_geo(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, number_of_songs, title, chart, plot_multiple_geo)


def plot_max_rank_of_songs_with_keyword_geo(chart, start_date, end_date, keyword, regions):
    title = '[{}] Total number of streams for: {} from: {} to: {}'.format(chart['name'], keyword, start_date, end_date)
    plot_songs_with_keyword(start_date, end_date, keyword, regions, max_rank, title, chart, plot_multiple_geo)

## Plots with aggregated feature characteristics

def plot_songs_with_audio_feature(start_date, end_date, audio_feature, regions, metric, title, chart, plot_callback):
    dates_range = pd.date_range(start_date,end_date,freq='d')
    requested_dates = list(dates_range.date)
    data = [] # (country, (dates, values))
    for region in regions:
        df = apply_producer_with_audio_features(chart, region)
        values, labels = metric(region, df, requested_dates, audio_feature)
        data.append((region, (requested_dates, values, labels)))
    plot_callback(data, title)


def plot_average_value_of_audio_feature(chart, start_date, end_date, audio_feature, regions):
    title = '[{}] Average value of metric: {} from: {} to: {}'.format(chart['name'], audio_feature, start_date, end_date)
    plot_songs_with_audio_feature(start_date, end_date, audio_feature, regions, average_metric, title, chart, plot_multiple_bar)

def plot_average_value_of_audio_feature_geo(chart, start_date, end_date, audio_feature, regions):
    title = '[{}] Average value of metric: {} from: {} to: {}'.format(chart['name'], audio_feature, start_date, end_date)
    plot_songs_with_audio_feature(start_date, end_date, audio_feature, regions, average_metric, title, chart, plot_multiple_geo)

### plot similarity

def plot_similarity(x, y, title):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=x,
               y=y,
               name='Similarity'))
    fig = add_timeline(fig, title)
    fig.show()
