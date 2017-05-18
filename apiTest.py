import time
import os
import requests
from ConfigParser import SafeConfigParser
import spotipy
import spotipy.util as util
import sys

parser = SafeConfigParser()
parser.read('config.ini')

# Network Config:
SPOTIFY_CLIENT_ID = parser.get('apis', 'spotify_client_id')
SPOTIFY_CLIENT_SECRET = parser.get('apis', 'spotify_client_secret')
SPOTIFY_REDIRECT_URL = parser.get('apis', 'spotify_redirect_url')

# Request Methods:
def generateSpotifyToken(username, clientId, clientSecret, referringUrl):
    scope = 'user-read-currently-playing'
    token = util.prompt_for_user_token(username, scope, clientId, clientSecret, referringUrl)
    if token:
        return token
    else:
        print "Can't get token for", username

def getMostRecentSong(token):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    r = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    return r.json()

def getSongQualities(id):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    r = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(id), headers=headers)
    return r.json()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print ('Press Ctrl-C to quit.')
    else:
        print "Usage: %s 'spotify username'" % (sys.argv[0],)
        sys.exit()

    token = generateSpotifyToken(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)

    while True:
        song = getMostRecentSong(token)
        if song['is_playing']:
            qualities = getSongQualities(song['item']['id'])
            print qualities
        time.sleep(5)
