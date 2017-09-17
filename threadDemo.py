import requests
import sys
# import asyncio
import threading
import time
from configparser import ConfigParser
from songMapper import generateColors, piecewiseBrightness
from SpotifyApiClient import SpotifyApiClient
from NeoPixelController import NeoPixelController

parser = ConfigParser()
parser.read('config.ini')

### Global ENV vars:
SPOTIFY_CLIENT_ID       = parser.get('apis', 'spotify_client_id')
SPOTIFY_CLIENT_SECRET   = parser.get('apis', 'spotify_client_secret')
SPOTIFY_REDIRECT_URL    = parser.get('apis', 'spotify_redirect_url')
###

# async def main(username):
#     # Init Spotify API:
#
#     api = SpotifyApiClient(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)
#     # leds = NeoPixelController()
#
#     currentSongId = ''
#     qualities = {}
#     while True:
#         song = await api.getCurrentSong()
#         newSongId = song['item']['id']
#         if newSongId != currentSongId:
#             print('New Song!')
#             currentSongId = newSongId
#             qualities = await api.getSongQualities(newSongId)
#             # print(qualities)
#             # LED change song mode
#             # LED set new song
#         await asyncio.sleep(3)
#         print(currentSongId)

# Global shared between classes
songQualities = None

class apiThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.api = SpotifyApiClient(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)
        self.currentSongId = ''

    def run(self):
        global songQualities
        currentSongId = 'FAKE SHIT!'
        while True:
            song = self.api.getCurrentSong()
            newSongId = song['item']['id']
            if newSongId != self.currentSongId:
                print('New Song!')
                self.currentSongId = newSongId
                songQualities = self.api.getSongQualities(newSongId)

class ledThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.leds = NeoPixelController()

    def run(self):
        global songQualities
        while True:
            self.leds.mapSongQualitiesToBrightness(songQualities)
            self.leds.mapSongQualitiesToColors(songQualities)
            # print(songQualities)
            # time.sleep(2)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print('Press Ctrl-C to quit.')
    else:
        print("Usage: %s 'spotify username'" % (sys.argv[0],))
        sys.exit()

    # token = generateSpotifyToken(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)
    apiThread = apiThread()
    ledThread = ledThread()

    apiThread.start()
    ledThread.start()