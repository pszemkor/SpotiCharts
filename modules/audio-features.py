import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modules.db import Top200, Viral50, AudioFeatures


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def extract_relevant_features(audio_features):
    relevant_audio_features = ['danceability', 'energy', 'loudness',
                               'speechiness', 'acousticness', 'instrumentalness',
                               'liveness', 'valence', 'tempo', 'duration_ms', 'id']
    relevant_features_dict = {}
    for key in relevant_audio_features:
        val = None
        if key in audio_features:
            val = audio_features[key]
        relevant_features_dict[key] = val
    return relevant_features_dict


engine = create_engine('sqlite:///spoticharts.db', echo=True)
conn = engine.connect()
session = Session(bind=engine)
viralIds = session.query(Viral50.spotify_id).distinct(Viral50.spotify_id).all()
viralIds = list(map(lambda item: 'spotify:track:' + str(item[0]), viralIds))

top200Ids = session.query(Top200.spotify_id).distinct(Top200.spotify_id).all()
ids = list(map(lambda item: 'spotify:track:' + str(item[0]), top200Ids))
ids.extend(viralIds)
ids = list(set(ids))

print('Audio features search will be performed for {} rows'.format(len(ids)))
print('Sample ids: ', ids[:3])

load_dotenv()
ID = os.getenv('ID')
SECRET = os.getenv('SECRET')
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=ID, client_secret=SECRET))
chunk_size = 10
count = 0
for chunk in chunks(ids, chunk_size):
    try:
        res = sp.audio_features(tracks=chunk)
        res = list(map(lambda item: extract_relevant_features(item), res))
        session.add_all(list(map(lambda item: AudioFeatures(**item), res)))
        session.commit()
        count += 10
        print('Persisted {}/{}'.format(count, len(ids)))
    except Exception as e:
        print('Exception:', e)

session.close()
