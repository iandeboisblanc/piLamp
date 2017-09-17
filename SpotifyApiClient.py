import requests
import spotipy.util as util

class SpotifyApiClient:
    def __init__(self, username, clientId, clientSecret, referringUrl):
        self.token = self._generateToken(username, clientId, clientSecret, referringUrl)

    def _generateToken(self, username, clientId, clientSecret, referringUrl):
        scope = 'user-read-currently-playing'
        token = util.prompt_for_user_token(username, scope, clientId, clientSecret, referringUrl)
        if token:
            return token
        else:
            print("Can't get token for", username)

    def getCurrentSong(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
        # TODO: Sometimes get a 204 with no content. Causes error on .json()
        return r.json()

    def getSongQualities(self, songId):
        print('start fetch')
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(songId), headers=headers)
        print('end fetch')
        return r.json()
