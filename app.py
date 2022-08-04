# Backend for hosted webapp version
from flask import Flask, request, redirect, render_template, jsonify
from creds import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
import spotipy
from collageServe import CollageMaker 

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
    token = spotipy.util.prompt_for_user_token(username='username',
                                               scope='user-top-read playlist-read-private user-read-private user-read-email',
                                               client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri='http://localhost:5000')
    if token:
        # Return access token and expires in information
        return jsonify(token)
    else:
        # Return some error state
        return "error"

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
