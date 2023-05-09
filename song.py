"""Create Flask App for song recommendation Application"""

from flask import Flask, render_template, redirect, make_response, request
from recommendation_models import query

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

@app.route('/code', methods=['GET'])
def code():
    """Displays search form and eventual table"""
    return render_template('code.html')

@app.route('/song-description/<string:song_id>')
def describe_song(song_id):
    similar_songs = []
    new_ids = query(song_id, 10)

    for id in new_ids:
        similar_songs.append(get_song_from_id(id))
            
    return render_template('song.html', songs=similar_songs)