#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gmusicapi import Mobileclient
import spotipy
from spotipy import util
import argparse
import re

feat_regex = re.compile('(\([feat].*\))')

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--spotify-user', dest="spotify_user", help='Username for spotify', required=True)
parser.add_argument('-sc', '--spotify-client', dest="spotify_client", help='Client id for spotify', required=True)
parser.add_argument('-ss', '--spotify-secret', dest="spotify_secret", help='Client secret for spotify', required=True)
parser.add_argument('-g', '--google-user', dest="g_user", help='Google user email', required=True)
parser.add_argument('-gpw', '--google-pw', dest="g_password", help='Google user password', required=True)
parser.add_argument('-sr', '--spotify-redirect', dest="spotify_redirect", default='http://localhost',
                    help='Redicrect url for spotify-authentication. http://spotipy.readthedocs.io/en/latest/#authorized-requests')
parser.add_argument('--merge', dest="merge", action='store_true',
                    help='Merge playlist if name already exists. Crude implementation.')
parser.add_argument('--rm-feat', dest="rmfeat", action='store_false',
                    help='Remove (feat artistname) from titles for google music. Messes up spotify search, default on.')
config = parser.parse_args()

spotify_username = config.spotify_user

google_api = Mobileclient()
google_api.login(config.g_user, config.g_password, Mobileclient.FROM_MAC_ADDRESS)

token = util.prompt_for_user_token(spotify_username, scope='playlist-modify-public', client_id=config.spotify_client,
                                   client_secret=config.spotify_secret,redirect_uri=config.spotify_redirect)
spotify_api = spotipy.Spotify(auth=token)

playlists = google_api.get_all_user_playlist_contents()

output = ["[{}]: {}".format(i, name['name']) for i, name in enumerate(playlists)]
print("\n".join(output))
n = int(input('Select playlist number: '))
selected_playlist = playlists[n]
tracks = selected_playlist['tracks']

failed_song_count = 0

failed_searches = []
collected_tracks = []
for track in tracks:
    try:
        track = track['track']
        song = track['title']
        artist = track['artist']
        try:
            if config.rmfeat:
                song = feat_regex.sub('', song)
            resp = spotify_api.search('{} {}'.format(artist, song))
            track_uri = resp['tracks']['items'][0]['uri']
            collected_tracks.append(track_uri)
        except:
            failed_searches.append('{} - {}'.format(artist, song))
            failed_song_count += 1
    except:
        failed_song_count += 1

def create_playlist(name):
    return spotify_api.user_playlist_create(spotify_username, name)['id']

def dedup_tracks(uri_list, playlist_id):
    current_pl_uris = [item['track']['uri'] for item in spotify_api.user_playlist(spotify_username, playlist_id)['tracks']['items']]
    return [x for x in uri_list if x not in current_pl_uris]

pl_name = selected_playlist['name']
if config.merge:
    user_sp_playlists = spotify_api.user_playlists(spotify_username)['items']
    for entry in user_sp_playlists:
        if entry['name'].lower() == pl_name.lower():
            print('Found existing playlist, merging...\n')
            pl_id = entry['id']
            break
    if not pl_id:
        print('Creating new playlist...\n')
        pl_id = create_playlist(pl_name)
else:
    pl_id = create_playlist(pl_name)

collected_tracks = dedup_tracks(collected_tracks, pl_id)

if len(collected_tracks) > 0:
    spotify_api.user_playlist_add_tracks(spotify_username, pl_id, collected_tracks)

print("Added non-dudplicate songs: {}\n".format(len(collected_tracks)))
print("num failed song-transfers: {}\n".format(failed_song_count))
print("Search failed for the following songs:\n{}".format("\n".join(failed_searches)))
