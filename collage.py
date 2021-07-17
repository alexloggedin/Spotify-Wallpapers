"""
1. Populate image array from Spotify (or locally) **DONE**
2. Get the dimensions of the array based on screen size **DONE**
3. Create an image with correct dimensions **DONE**
4. Add Variable image size **DONE** # TODO: Implement size via small (4), medium (2), large (1) **DONE**
5. 3 Ways to generate album data:
    a) userdata **DONE**
    b) artist input
    c) album list
    d) from a playlist

6. Filter albums by color
    a) Create a color palette
    b) Create a gradient
    c) Light vs. Dark (Would That be part of the palette)

?. Make albums bigger or smaller based on something??
??. Make randomness better
???. Add a more collage like quality (vary size)
"""

import os
from creds import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from PIL import Image
import random
import requests
import spotipy
import spotipy.util
from datetime import datetime

IMG_HEIGHT = 640


class CollageMaker:

    def __init__(self, width, height, scale=2, collage_type=1, req_list=[], unique=True, palette=()):
        self.collage_height = height
        self.collage_width = width
        self.req_list = req_list
        self.albums = []
        self.scale = scale
        self.type = collage_type
        self.unique = unique
        self.palette = palette
        pass

    # Logs into Spotify and takes the top tracks from the user and places them in the album array
    # TODO: Look up individual artists and tracks (No Sign-In Required)
    def get_albums_userdata(self):
        # Sign into application
        token = spotipy.util.prompt_for_user_token(
            username='username',
            scope='user-top-read',
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            # TODO: Create a web friendly callback
            redirect_uri='http://localhost:5000/spcallback',
        )
        auth = spotipy.Spotify(auth=token)
        results = auth.current_user_top_tracks(
            time_range='medium_term',
            limit='50')
        for item in results['items']:
            img_url = item['album']['images'][0]['url']
            self.albums.append(img_url)

    def get_albums_artists(self):
        # Look up array of artists (By ID??)

        # Populate with 3 (make variable??) of artists, most popular tracks

        # return populated list
        return

    def get_albums_tracks(self):
        # Look up array of tracks (By ID)

        # Get album art

        return

    def get_playlist_albums(self):
        # Get albums from a playlist

        # Get album art

        return

    # Determine which method of get album to use then download albums
    def get_albums(self):
        if self.type == 1:
            self.get_albums_userdata()
        elif self.type == 2:
            self.get_albums_artists()
        elif self.type == 3:
            self.get_albums_tracks()
        else:
            self.get_playlist_albums()

        # TODO: Download album art to a folder
        return

    # Scale album data to a best fit size
    def scale_dimensions(self):
        # Use GCF to determine scale factor
        num1, num2 = self.collage_height, self.collage_width
        if num1 > num2:
            num1, num2 = num2, num1
        for x in range(IMG_HEIGHT, 0, -1):
            if num1 % x == 0 and num2 % x == 0:
                return int(x / self.scale)

    # Grabs an album art from the list
    # TODO: Add color and palette functionality
    def get_random_album(self, prev):
        # TODO: Implement a semi random weight system
        img = random.choice(self.albums)
        while img == prev:
            img = random.choice(self.albums)
        return img

    def create(self):
        collage = Image.new('RGB', (self.collage_width, self.collage_height))
        collage_fp = 'collages/collage' + str(self.collage_width) + 'x' + str(self.collage_height) + str(datetime.now().strftime(
            '%d-%m-%Y-%H-%M-%S')) + '.png'
        self.get_albums()
        size = self.scale_dimensions()
        rows = int(self.collage_width / size)
        cols = int(self.collage_height / size)
        print(size, rows, cols)
        prev_path = random.choice(self.albums)
        print("Total Rows: " + str(rows) + "Total Columns: " + str(cols))

        for i in range(rows):
            for j in range(cols):
                print("Photo Added -> X: " + str(i) + "Y: " + str(j))
                img_path = self.get_random_album(prev_path)
                if self.unique:
                    self.albums.remove(prev_path)
                img = Image.open(requests.get(img_path, stream=True).raw)
                img.thumbnail((size, size))
                collage.paste(img, (i * size, j * size))
                prev_path = img_path
                collage.save(collage_fp)
        return Image.open(collage_fp)


width = int(input('Enter Width: '))
height = int(input('Enter Height: '))

newcollage: CollageMaker = CollageMaker(width, height)
newcollage.create().show()
