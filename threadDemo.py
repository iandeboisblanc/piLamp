import sys
import threading
import time
from configparser import ConfigParser
from SpotifyApiClient import SpotifyApiClient
from NeoPixelController import NeoPixelController

parser = ConfigParser()
parser.read('config.ini')

### Global ENV vars:
SPOTIFY_CLIENT_ID       = parser.get('apis', 'spotify_client_id')
SPOTIFY_CLIENT_SECRET   = parser.get('apis', 'spotify_client_secret')
SPOTIFY_REDIRECT_URL    = parser.get('apis', 'spotify_redirect_url')
###

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
            print('Checking for new song...')
            song = self.api.getCurrentSong()
            newSongId = song['item']['id']
            if newSongId != self.currentSongId:
                print('New Song!')
                self.currentSongId = newSongId
                # print(songQualities)
                print('API THREAD start fetch')
                temp = self.api.getSongQualities(newSongId)
                print('API THEAD done fetch')
                print(temp)
                songQualities = temp
                print(songQualities)
            time.sleep(1)

class ledThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.leds = NeoPixelController()

    def run(self):
        global songQualities
        try:
            while True:
                if not songQualities:
                    # print('no q')
                    self.leds.colorWipe([255, 0, 0])
                else:
                    print('LED thread found qualities')
                    print(songQualities)
                    self.leds.mapSongQualitiesToBrightness(songQualities)
                    self.leds.mapSongQualitiesToColors(songQualities)
                    # print(songQualities)
        except Exception as err:
            print(sys.exc_info())
            print(err)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print('Press Ctrl-C to quit.')
    else:
        print("Usage: %s 'spotify username'" % (sys.argv[0],))
        sys.exit()

    # token = generateSpotifyToken(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)
    thread1 = apiThread()
    thread2 = ledThread()

    thread1.start()
    thread2.start()
