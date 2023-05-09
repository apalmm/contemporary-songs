import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


songs_data = pd.read_csv("kaggle/data.csv")
songs_data.isnull().sum()
songs_data = songs_data.drop_duplicates(subset = ['name', 'artists'])
songs_data.release_date.replace({'-.*': ''}, regex=True, inplace=True)
songs_data['release_date'] = songs_data['release_date'].astype(int)
songs_data = songs_data.sort_values(by='release_date')

def get_decade(year):
    decade = int(year/10) * 10
    return decade

songs_data['decade'] = songs_data['release_date'].apply(get_decade)

df = songs_data[songs_data['release_date'] > 2010]

def queryCols(queryID, query_idx, songsData, columns, k):
    
    new_songs = songsData[columns].copy(deep=True)
    
    new_songs['dist'] = new_songs.apply(lambda x: np.linalg.norm(x-query_idx), axis=1)
    new_songs = new_songs.sort_values('dist')
    new_songs.drop_duplicates()
    
    return new_songs.head(k)

def findSongIdx(queryID, df):
    tmp = df.copy(deep=True)

    query_idx = (tmp.index[(tmp['id'] == queryID)].tolist())

    if query_idx:
        query_idx = query_idx[0]
    
    return query_idx

def songNames(df, song_arr):
    song_ids = []
    song_names = []

    for idx in song_arr:
        df_row = df.loc[[idx]]
        song_names.append((df_row['name'], df_row['artists']))
        song_ids.append(df.at[idx,'id'])

    return song_names, song_ids


def query(song_ID, k):
    columns = ['acousticness','danceability','liveness','loudness', 'speechiness','valence']

    idx = findSongIdx(song_ID, songs_data)

    querySong = songs_data[columns].loc[idx]

    new_recs = queryCols(song_ID, querySong, df, columns, k)

    songs_names, song_ids = songNames(df, new_recs.index.values)

    return song_ids

