# Backend for hosted webapp version
from flask import Flask, request, redirect, render_template, jsonify
from Handlers.creds import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
import spotipy
from CollageMaker import CollageMaker 

app = Flask(__name__)

app.debug = 1
app.env = 'development'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', method = 'POST')
def login():
    # Get a code from client
    # Create a new instance of Login Using their code using client id, client secret, and a redirect
    # Send back an access token and a refresh token, and the expiration time
    auth_manager=SpotifyOAuth(scope='user-top-read,playlist-read-private,user-read-private,user-read-email',
                                client_id = SPOTIFY_CLIENT_ID,
                                client_secret = SPOTIFY_CLIENT_SECRET,
                                redirect_uri='http://localhost:5000'
                            )
                                
        sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route('/render', method = 'GET')
def render():
    # Recieve parameters to render an image
        # covers (list of covers)
        # shape (rectangle or square)
        # grid | collage
    
    # Create Collage
    # Save To Location
    # Return link to picture
    return 
