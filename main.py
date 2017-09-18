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
        try:
            while True:
                self.loop()
        except Exception as err:
            print('Error in API thread: {}'.format(err))
            # print(sys.exc_info())

    def loop(self):
        global songQualities
        print('Checking for new song...')
        song = self.api.getCurrentSong()
        newSongId = song['item']['id']
        if newSongId != self.currentSongId:
            print('New Song!')
            self.currentSongId = newSongId
            songQualities = self.api.getSongQualities(newSongId)
            print(songQualities)
        time.sleep(2)


class ledThread(threading.Thread):
    def __init__(self):
        global songQualities
        threading.Thread.__init__(self)
        self.state = 'idle'
        self.leds = NeoPixelController()

    def run(self):
        try:
            while True:
                self.loop()
        except Exception as err:
            print('Error in LED thread: {}'.format(err))
            # print(sys.exc_info())

    def loop(self):
        global songQualities
        if not songQualities:
            self.leds.colorWipe([0, 80, 160])
            self.leds.colorWipe([0, 0, 0])
            a = None
        else:
            print(songQualities)
            self.leds.mapSongQualitiesToBrightness(songQualities)
            self.leds.mapSongQualitiesToColors(songQualities)
            # brightness = self.leds.getBrightness(songQualities)
            # colors = self.leds.getColors(songQualities)
            # if transitioning: brightness = temperBrightness(brightness, amount)

        # global songQualities
        # if !songQualities:
            # newState = 'idle'
        # if songQualities:
            # newState = 'viz'
        # if newState != self.state:
            # newState = 'waiting'
        # self.state = newState


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print('Press Ctrl-C to quit.')
    else:
        print("Usage: %s 'spotify username'" % (sys.argv[0],))
        sys.exit()

    thread1 = apiThread()
    thread2 = ledThread()

    thread1.start()
    thread2.start()

    # USEFUL LOGS
    # print('Playing:', song['item']['name'])
    # # if song['is_playing']:
    # qualities = getSongQualities(token, song['item']['id'])
    # print('BPM:', qualities['tempo'])
    # print('Time Signature:', qualities['time_signature'])
    # print('Energy:', qualities['energy'])
    # print('Cheeriness', qualities['valence'])
    # print('Danciness', qualities['danceability'])
