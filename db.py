import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from spotipy.oauth2 import SpotifyClientCredentials

import spotipy

client_credentials_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
'''for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
'''

fields = [
    'id',
    'name', #song name
    'artists', #song artist
]

df = pd.read_csv(
    'kaggle/data.csv', 
    usecols=fields
)

def get_songs(filters):
    df_filter = df[df.name.str.contains(filters['name'], na=False) & df.artists.str.contains(filters['artist'], na=False)].head(25)
    df_filter.reset_index()  # make sure indexes pair with number of rows

    song_array = []

    for index, row in df_filter.iterrows():
        song = spotify.track(row['id'])
        append_obj = []
        append_obj.append(row['name'])
        append_obj.append(row['artists'])
        append_obj.append(row['id'])

        if song['album']['images']:
            append_obj.append(song['album']['images'][0]['url'])

        song_array.append(append_obj)

    return song_array

def get_song_from_id(song_id):
    song_data = []
    song = spotify.track(str(song_id))
    song_title = song['name']
    song_artist = song['artists'][0]['name']

    song_data.append(song_title)
    song_data.append(song_artist)
    
    if song['album']['images']:
        album_cover = song['album']['images'][0]['url']
        song_data.append(album_cover)

    song_data.append(song['id'])
    return song_data