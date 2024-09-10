from dotenv import load_dotenv

import sys
import spotipy
import spotipy.util as util
import random
import os

token = ""
username = ""

load_dotenv()

def spotify_authentication(user: str):
    global token
    global username

    if user != "":
        print("Username:", user)
        username = user
        scope = 'user-library-read streaming user-read-playback-state'
        token = util.prompt_for_user_token(username, scope, os.getenv("SPOTIPY_CLIENT_ID"), os.getenv("SPOTIPY_CLIENT_SECRET"), os.getenv("SPOTIPY_REDIRECT_URI"))

    print("Authenticated user!")

def read_liked_songs():
    global token

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks(50, 0)
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'] + ' - ' + track['uri'])
    else:
        print("Can't get token for", username)