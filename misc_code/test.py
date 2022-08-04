from PIL import Image, ImageFilter

bg = Image.open("collages/collage3000x2000.png")

p = Image.open("samples/lil-uzi-vert-love-vs-the-world-2-1584053330-640x640.jpeg")
s = p.size
p = p.rotate(45, expand=True)
mask = Image.new("RGBA", s, color='white')
mask = mask.rotate(45, expand = True)
b = mask.filter(ImageFilter.BoxBlur(100))
bg.paste(p, (0,0), mask)
bg.save('img.png')

def get_art_from_userdata(self):
    self.cover_list = []
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
        time_range='short_term',
        limit='50')
    
    for item in results['items']:
        img_url = item['album']['images'][0]['url']
        self.cover_list.append(img_url) 