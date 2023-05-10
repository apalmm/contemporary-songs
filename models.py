import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random


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


def weightDistance(curr_row, query_idx):
    weightList = []
    weightList.append(np.linalg.norm(curr_row - query_idx))
    weightList.append(np.linalg.norm(curr_row['energy'] - query_idx['energy']))
    weightList.append(np.linalg.norm(curr_row['energy'] - query_idx['energy']))
    weightList.append(np.linalg.norm(curr_row['key'] - query_idx['key']))
    weight = np.mean(weightList)
    return weight
    

def distWeights(queryID, query_idx, songsData, columns, k):
    
    new_songs = songsData[columns].copy(deep=True)
    new_songs['dist'] = new_songs.apply(lambda x: weightDistance(x, query_idx), axis = 1)
    new_songs = new_songs.sort_values('dist')
    new_songs.drop_duplicates()
    
    return new_songs.head(k)

def queryWeight(song_ID, k):
    columns = ['instrumentalness', 'energy', 'key','danceability','liveness','loudness', 'speechiness','valence', 'popularity']
    
    idx = findSongIdx(song_ID, songs_data)
    
    querySong = songs_data[columns].loc[idx]
    
    new_recs = distWeights(song_ID, querySong, df, columns, k)
    
    songs_names, song_ids = songNames(df, new_recs.index.values)
    
    return new_recs, songs_names, song_ids

columns = ['acousticness','danceability','energy','instrumentalness','liveness','loudness', 'speechiness','valence', 
          'tempo', 'popularity']

songs_avgs = songs_data[columns].describe()

def describe_song(song_id):
    new_columns = ['danceability', 'instrumentalness','loudness', 'tempo', 'popularity']
    
    song_idx = findSongIdx(song_id, songs_data)

    past_decade = songs_data.at[song_idx,'decade']
    curr_song = songs_data.loc[[song_idx]]
    very_low = songs_avgs.loc['min']
    low = songs_avgs.loc['25%']
    avg = songs_avgs.loc['50%']
    high = songs_avgs.loc['75%']
    very_high = songs_avgs.loc['max']

    key = {
        0 : "C",
        1 : "C#",
        2 : "D",
        3 : "Eb",
        4 :"E",
        5 : "F",
        6 : "F#",
        7 : "G",
        8 : "Ab",
        9 : "A",
        10 : "Bb",
        11 : "B",
    }

    song_key = key[int(songs_data.at[song_idx, 'key'])]
    
    if past_decade > 1970:
        result = f"This song is written in the key of {song_key}.\n"
    else:
        result = ""
    
    sim_feats = []

    for feature in new_columns:
        num = random.randint(0, 10)
        
        curr_val = songs_data.at[song_idx, feature]
        
        phrases = {

        "HIGH_LOUD" : [f"Your song is (compared to most other songs) very loud!! ",],
        "LOW_LOUD" : [f"Comparatively speaking, your song is very quiet. ",
                      "Relatively speaking, your song is very quiet! It's giving study sesh vibes? ",],

        "VERY_HIGH": [f"Wow! This song has incredible levels of {feature}. I love it! ",
                      f"Wow! This song is very high in {feature}. Much higher than the average of most songs. It sounds beautiful. ",
                      f"Wow! The {feature} of this song is much higher than the average of most songs. It really sounds spectacular. ",
                     ],
            
        "HIGH":[f"This song has high levels of {feature}. ",
                f"This song is above average in terms of {feature}. ",
                f"Your song stands out in terms of {feature}! Meaning, the {feature} of this song is higher than most other songs. ",
               ],
            
        "HIGH_D": [f"I would say that your chosen song is a very danceable song. It has great energy and good vibes. ",
                    f"If I were alive during this decade, I would certainly want to dance to your song! It is very high energy. ",
                    f"Let's party! This song is very danceable and high in energy. ",
                    f"I want this song to be playing for me and my friends at the club! Or rather, this song is very danceable and high in energy. "
                   ],
            
        "LOW_D": [f"Energy-wise, this song is less-danceable. Chill. ",
                  f"Your chosen song is lower in terms of danceability. Maybe you are feeling more calm and casual today (?)! ",
                  f"This is a slower, chiller song. Not very high energy in comparison to most other songs. ",
                  f"If I were going to a party during this decade, I don't think I would want this song playing. That is, this song is relatively low energy. ",
                  f"This gives library-vibes. That is, this song has low danceability. ",
                  ],

        "AVG": [f"Your chosen song is pretty average in terms of {feature} compared to most other songs. ",
                f"In terms of {feature}, this song is quite average. Meaning, it is around the levels of most other songs. ",
               ],

        "LOW": [f"This song is low in terms of {feature}. But sometimes that's a good thing! ",
                f"In terms of {feature}, this song is quite average. So there's not a whole lot going on there. ",
               ],

        "VERY_LOW": [f"This song is very very low for {feature}. ",
                     f"Unfortunately (or fortunately!) this song is quite low in terms {feature} compared to most other songs. ",
                    ],

        "HIGH_POP": [f"It looks like your chosen song is very popular! ",
                     f"This is a very popular song! ",
                     f"Comparatively speaking, this song is very popular! ",
                     f"A lot of people have listened to this song. It is very popular! "
                     ],

        "LOW_POP": [f"Cool music taste. Your chosen song is not that popular compared to most songs. You might be looking for something more 'underground' (?). ",
                    f"It looks like your chosen song is not very popular compared to most other songs. ",
                    f"I haven't heard this song before. It looks like your chosen song is not very popular! ",
                    ]
        }
        
        label = "AVG"

        if (feature == 'loudness'):
            if curr_val > avg[feature]:
                label = "HIGH_LOUD"
            elif curr_val <= avg[feature]:
                label = "LOW_LOUD"
            
            if num % 2 == 0:
                sim_feats.append(label)
        elif (feature == 'danceability'):
            if curr_val > avg[feature]:
                label = "HIGH_D"
            elif curr_val <= avg[feature]:
                label = "LOW_D"

            if num % 2 == 0:
                sim_feats.append(label)
        elif (feature == 'popularity'):
            if curr_val > avg[feature]:
                label = "HIGH_POP"
            elif curr_val <= avg[feature]:
                label = "LOW_POP"

            if num % 2 == 0:
                sim_feats.append(label)
        else:
            if curr_val > high[feature]:
                label = "VERY_HIGH"
            elif curr_val > avg[feature]:
                label = "HIGH"
            elif curr_val < avg[feature]:
                label = "LOW"
            elif curr_val < low[feature]:
                label = "VERY_LOW"

        result += random.choice(phrases[label]) + ""

    result += "Based on these factors, we've compiled a specially curated list of songs using nearly 10 different song-descriptor characteristics. The songs listed above purposefully share many of the said characteristics with your selected song. I hope you that you give them a listen and enjoy!"
    if sim_feats:
        result += " Most notably "

    i = 0
    length = len(sim_feats)
    print(sim_feats)
    for sim in sim_feats:
        i += 1

        if sim == "HIGH_LOUD":
            result += "they are higher in volume"

        elif sim == "LOW_LOUD":
            result += "they are lower in volume"

        elif sim == "HIGH_POP":
            result += "they are all very popular compared to most other songs, just like yours" 
        elif sim == "LOW_POP":
            result += "they are all more 'underground' compared to most other songs, just like yours" 

        elif sim == "LOW_D":
            result += "they are all very chill and relaxing in terms of danceability, similar to the one you chose" 
        elif sim == "HIGH_D":
            result += "they all make you want to dance" 
        
        if i == length:
            result += '.'
        elif i == length - 1 and length > 1:
            result += ', and '
        else:
            result += ', '
        

    return result

means = songs_data.groupby(songs_data['decade']).mean(numeric_only=True).reset_index()
stds = songs_data.groupby(songs_data['decade']).std(numeric_only=True).reset_index()

def find_decade(decade, df):
    tmp = df.copy(deep=True)
    query_idx = (df.index[(means['decade'] == decade)].tolist())
    if(query_idx):
        return query_idx[0]
    
    return query_idx

# Function to calculate zscore given mean, standard deviation, and a particular value
# Used to calculate zscore for each feature in song
def calc_zscore(mean, std, value):
    return ((value - mean)/std)

# Given the zscore and trend statistics, the function calculates the value
# Used to find values in the current decade
def calc_value(mean, std, zscore):
    return ((zscore * std) + mean)

#Takes in a song ID, and creates a dummy song for the current decade that reflects relations to trends from the song's decade
def create_dummy_song(song_ID, columns):
    idx = findSongIdx(song_ID, songs_data)

    past_decade = songs_data.at[idx, 'decade']

    means_idx = find_decade(past_decade, means)
    std_idx = find_decade(past_decade, stds)
    
    querySong = songs_data[columns].loc[idx]
    zSong = querySong
        
    # Find the z-score for current song compared to its own decade
    for feature in columns:
        zSong[feature] = calc_zscore(means.at[means_idx, feature], stds.at[std_idx, feature], querySong[feature])
        
    dummySong = zSong
    
    
    # Work backwards and find the relative current values, based upon the zscores
    # The index for 2010(the modern decade) is 9
    for feature in columns:
        dummySong[feature] = calc_value(means.at[9, feature], stds.at[9, feature], zSong[feature])
    

    return dummySong

def queryRelativeSong(song_ID, k):
    columns = ['instrumentalness', 'energy', 'key','danceability','liveness','loudness', 'speechiness','valence', 'popularity']
    
    querySong = create_dummy_song(song_ID, columns)
    print(querySong)
    
    new_recs = queryCols(song_ID, querySong, df, columns, k)
    
    songs_names, song_ids = songNames(df, new_recs.index.values)
    
    return new_recs, songs_names, song_ids

def describe_song_decade(song_id):
    
    idx = findSongIdx(song_id, songs_data)
    
    new_columns = ['danceability', 'instrumentalness','loudness', 'tempo', 'popularity']
    
    past_decade = songs_data.at[idx,'decade']
    means_decade = means[new_columns].loc[find_decade(past_decade, means)]
    
    result = f"This song was released in the {past_decade}s.\n"
    
    for feature in new_columns:
        
        phrases = {
            
        #Generic high, low phrases
        "HIGH":[f"Wow! Your chosen song has high levels of {feature} compared to most other songs from the {past_decade}s. That's pretty neat. ",
                f"This song is above average in terms of {feature} for its time period, and it sounds awesome. "
                f"I am impressed with the {feature} of this song. It is very high relative to most other songs from the {past_decade}! "
                f"This song has an incredibly high {feature}, which is really unique for its decade of release, the {past_decade}s! "
               ],
            
        "LOW": [f"This song is lacking in terms of {feature}, but that is the beauty of it. ",
                f"In terms of {feature} in the {past_decade}s, this song is below average. "
               ],
        "AVG": [f"Your chosen song is just average in terms of {feature}. It sounds great. ",
                f"In terms of {feature}, this song is quite average. Still sounds nice though. ",
                f"This song is nothing out of the blue in terms of this song's {feature}. Especially in the context of other songs from the {past_decade}s, but even this fact has its own beauty. "
               ],
            
        #High, low phrases for danceability and energy
        "HIGH_D": [f"Your chosen song is very danceable, meaning, it is very high energy for its time! ",
                    f"If I were living during this decade, I would certainly want to dance to your song! It is very high energy. ",
                    f"Let's party like its {past_decade}! This song is very danceable and high in energy for its time. "
                   ],
            
        "LOW_D": [f"Energy-wise, this song is danceable, but nothing special. Maybe it was one of the slower songs of the {past_decade}s. ",
                  f"Relative to most of {past_decade}’s music, this song isn't too danceable. It doesn't get me grooving. ",
                  f"If I were partying during the {past_decade}s, I don't think I would want this song playing. That is, it has relatively low energy energy compared to most other songs during the {past_decade}s. "
                  ],
        
        # High, low phrases for popularity
        "HIGH_POP": [f"Your chosen song was very popular during the {past_decade}s, I loveee this song. ",
                     f"Popular alert! Your chosen song was more popular than mose during the {past_decade}s. This is reflected in the results. "],
        "LOW_POP": [f"Great music taste. Your chosen song was not as popular during the {past_decade}s, but we\'ll still be able to find a similar song for you (it may just be a little lesser known by today's standards)! "]
            
        }
        
        curr_val = songs_data.at[idx, feature]
        
        label = "AVG"
        
        if (feature == 'danceability'):
            
            if curr_val > means_decade[feature]:
                label = "HIGH_D"
            elif curr_val <= means_decade[feature]:
                label = "LOW_D"
                
        elif (feature == 'popularity'):
            
            if curr_val > means_decade[feature]:
                label = "HIGH_POP"
            elif curr_val <= means_decade[feature]:
                label = "LOW_POP"
        
        else:
            
            if curr_val > means_decade[feature]:
                label = "HIGH"
                
            elif curr_val < means_decade[feature]:
                label = "LOW"
                

        result += random.choice(phrases[label])
    
    result += " I have taken each of these important relative-factors into account when choosing the contemporary songs listed above. Relatively speaking, these songs all share similar deviations from the average danceability, tempo, energy, popularity, and several other factors by today's music industry standards! I hope you find one or two that you enjoy and can add to your playlists!"

    return result
