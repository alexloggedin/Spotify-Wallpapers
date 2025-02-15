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
                                redirect_uri='http://localhost:8080'
                                )
                                
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
    def getTopTracks(self, tr = 'short_term'):
        data = self.sp.current_user_top_tracks(time_range=tr, limit=50, offset=2)
        c = []
        for item in data['items']:
            img_url = item['album']['images'][0]['url']
            c.append(img_url)
        return c

    def getPlaylists(self):
        return self.sp.current_user_playlist()

    def getPlaylistTracks(self, playlistId):
        data = self.sp.playlist_items(playlistId)
        c = []
        for item in data['items']:
            img_url = item['track']['album']['images'][0]['url']
            c.append(img_url)
        return c

    def getArtistCovers(self, artistId):
        pass

    def getArtistIds(self, list):
        # Search for each artist
        # return Id of artist

        pass

    def getMultipleArtistCovers(self, list):
        c = []
        for id in list:
            ac = self.getArtistCovers(id) 
            c.append(ac)
        return c

