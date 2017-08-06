from oauth2client.client import OAuth2WebServerFlow
import oauth2client.file
from collections import namedtuple
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--code', dest="code", help='Authenticateion-code', required=True)
parser.add_argument('--path', dest="path", default="gmusic.creds", help='Path to save credentials.')
config = parser.parse_args()


OAuthInfo = namedtuple('OAuthInfo', 'client_id client_secret scope redirect')
oauth = OAuthInfo(
    '652850857958.apps.googleusercontent.com',
    'ji1rklciNp2bfsFJnEH_i6al',
    'https://www.googleapis.com/auth/musicmanager',
    'urn:ietf:wg:oauth:2.0:oob'
)

flow = OAuth2WebServerFlow(*oauth)

credentials = flow.step2_exchange(config.code)
storage_filepath = config.path

if storage_filepath is not None:
    storage = oauth2client.file.Storage(storage_filepath)
    storage.put(credentials)
