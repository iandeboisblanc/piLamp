import requests
import sys
import asyncio
from configparser import ConfigParser
# from neopixel import *
from songMapper import generateColors, piecewiseBrightness
from SpotifyApiClient import SpotifyApiClient

parser = ConfigParser()
parser.read('config.ini')


async def main(username):
    # Init Spotify API:
    SPOTIFY_CLIENT_ID = parser.get('apis', 'spotify_client_id')
    SPOTIFY_CLIENT_SECRET = parser.get('apis', 'spotify_client_secret')
    SPOTIFY_REDIRECT_URL = parser.get('apis', 'spotify_redirect_url')

    api = SpotifyApiClient(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)

    currentSongId = ''
    while True:
        song = await api.getCurrentSong()
        newSongId = song['item']['id']
        if newSongId != currentSongId:
            currentSongId = newSongId
            qualities = await api.getSongQualities(newSongId)
            print('qualities')
            print(qualities)
            # LED change song mode
            # LED set new song
        await asyncio.sleep(3)
        print(currentSongId)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print('Press Ctrl-C to quit.')
    else:
        print("Usage: %s 'spotify username'" % (sys.argv[0],))
        sys.exit()

    # token = generateSpotifyToken(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(username))
    loop.close()
