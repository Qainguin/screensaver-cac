import sys
import spotipy
import spotipy.util as util
import random
import keys

token = ""
username = ""

def spotify_authentication(user: str):
    global token
    global username

    if user != "":
        username = user
        scope = 'user-library-read streaming'
        token = util.prompt_for_user_token(username, scope)

    print("Authenticated user!")

def read_liked_songs():
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks(50, 0)
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'] + ' - ' + track['uri'])
    else:
        print("Can't get token for", username)