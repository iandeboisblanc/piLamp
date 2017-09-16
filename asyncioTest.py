# import os
import requests
import sys
import asyncio
import functools
import spotipy
import spotipy.util as util
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

# Network Config:
SPOTIFY_CLIENT_ID = parser.get('apis', 'spotify_client_id')
SPOTIFY_CLIENT_SECRET = parser.get('apis', 'spotify_client_secret')
SPOTIFY_REDIRECT_URL = parser.get('apis', 'spotify_redirect_url')

def generateSpotifyToken(username, clientId, clientSecret, referringUrl):
    scope = 'user-read-currently-playing'
    token = util.prompt_for_user_token(username, scope, clientId, clientSecret, referringUrl)
    if token:
        return token
    else:
        print("Can't get token for", username)

async def checkForNewSong(token):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    r = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    # TODO: Sometimes get a 204 with no content. Causes error on .json()
    await asyncio.sleep(3)
    return 'BLAHHHH'  # r.json()

async def main(token):
    while True:
        words = await checkForNewSong(token)
        print(words)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print('Press Ctrl-C to quit.')
    else:
        print("Usage: %s 'spotify username'" % (sys.argv[0],))
        sys.exit()

    token = generateSpotifyToken(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(token))
    loop.close()
