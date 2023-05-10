"""Create Flask App for song recommendation Application"""

from flask import Flask, render_template, redirect, make_response, request
from models import queryWeight, queryRelativeSong, describe_song, describe_song_decade

from db import get_songs, get_song_from_id
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Displays search form and results table"""
    return redirect('home')

@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    """Processes song search queries"""
    filters = ['name', 'artist']

    songs = None

    query_filters = {}

    for fltr in filters:
        query_val = request.args.get(fltr)
        if query_val is not None:
            #if something provided, then search with that
            query_filters[fltr] = query_val

    querying = any(value != '' for value in query_filters.values())

    if querying:
        songs = get_songs(query_filters)
        #song id = for song in songs: song[2]

    template = render_template('results.html',
                                songs=songs)

    res = make_response(template)
    return res

@app.route('/song-description/<string:song_id>')
def sim_songs(song_id):
    similar_songs = []
    relative_songs = []

    old_song = get_song_from_id(song_id)
    old_song_description = describe_song(song_id)

    rel_description = describe_song_decade(song_id)

    new_recs, songs_names, song_ids = queryWeight(song_id, 5)
    new_recs, songs_names, relative_ids = queryRelativeSong(song_id, 5)

    for id in song_ids:
        similar_songs.append(get_song_from_id(id))
    
    for id in relative_ids:
        relative_songs.append(get_song_from_id(id))
            
    return render_template('song.html', rel_desc=rel_description, old_song_desc=old_song_description, old_song=old_song, songs=similar_songs, relative_songs=relative_songs)