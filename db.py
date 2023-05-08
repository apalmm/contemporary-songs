import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

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
    'kaggle/tracks.csv', 
    usecols=fields
)

print(df)

def get_songs(filters):
    df_filter = df[df.name.str.contains(filters['name'], na=False) & df.artists.str.contains(filters['artist'], na=False)]
    df_filter.reset_index()  # make sure indexes pair with number of rows

    song_array = []
    for index, row in df_filter.iterrows():
        song_array.append((row['name'], row['artists'], row['id']))

    return song_array