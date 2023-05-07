"""Create Flask App for song recommendation Application"""

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    """Displays search form and eventual table"""
    return render_template('index.html')

@app.route('/code', methods=['GET'])
def code():
    """Displays search form and eventual table"""
    return render_template('code.html')
