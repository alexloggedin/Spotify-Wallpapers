# Backend for hosted webapp version
from flask import Flask, request, redirect, render_template, jsonify
from creds import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
import spotipy

app = Flask(__name__)

app.debug = 1
app.env = 'development'

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/spcallback')
def callback():
    token = spotipy.util.prompt_for_user_token(username='username',
                                               scope='user-top-read',
                                               client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               # TODO: Create a web friendly callback
                                               redirect_uri='http://localhost:5000/spcallback', )
    if token:
        sp = spotipy.Spotify(auth=token)
        return jsonify(token)
