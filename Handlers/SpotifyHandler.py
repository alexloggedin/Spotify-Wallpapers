from http import client
from Handlers.creds import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import spotipy
from spotipy.oauth2 import SpotifyOAuth



class AlbumCoverGetter:
    def __init__(self):

        auth_manager=SpotifyOAuth(
                                scope='user-top-read,playlist-read-private,user-read-private,user-read-email',
                                client_id = SPOTIFY_CLIENT_ID,
                                client_secret = SPOTIFY_CLIENT_SECRET,
                                redirect_uri='http://localhost:5000'
                                )
                                
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
    def getTopTracks(self, tr = 'short_term'):
        data = self.sp.current_user_top_tracks(time_range=tr, limit='50')
        c = []
        for item in data['items']:
            img_url = item['album']['images'][0]['url']
            c.append(img_url)
        return c

    def getPlaylists(self):
        return self.sp.current_user_playlist()

    def getPlaylistTracks(self, playlistId):
        data = self.sp.playlist_items(playlistId)
        print(data)
    
# 'user-top-read playlist-read-private user-read-private user-read-email'

        # token = spotipy.util.prompt_for_user_token(
        #     username='user',
        #     scope='user-top-read playlist-read-private user-read-private user-read-email',
        #     client_id=SPOTIFY_CLIENT_ID,
        #     client_secret=SPOTIFY_CLIENT_SECRET,
        #     redirect_uri='http://localhost:5000/spcallback'
        #     )
        # self.sp = spotipy.Spotify(auth=token)