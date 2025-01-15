#!/usr/bin/env python3
import requests
import json
import os
import sys
import tomllib
import tabulate
from pathlib import Path
from slugify import slugify
from icecream import ic

# Read config
with open(Path(__file__).with_name('config.toml'), "rb") as ini:
    config = tomllib.load(ini)

# Global Query options for the API
query_options = {'u': config['api_user'], 'p': config['api_key'], 'f': 'json'}

# Get the list of playlists
r_playlists = requests.get(f"{config['api_base']}/getPlaylists", query_options)
# unwrap it from the subsonic response object
playlists = (r_playlists.json())['subsonic-response']['playlists']['playlist']

# Find the playlist I'm interested in. Wrapped as a function for clarity(?)
def find_id_for_playlist(want_playlist, list_of_playlists):
    for p in list_of_playlists:
        if p['name'] == want_playlist:
            return p['id']
    raise ValueError(f"id for {want_playlist} not found.")

playlist_id = find_id_for_playlist(config['want_playlist'], playlists)

# Get the list of tracks on the playlist
featured_albums = set()
r_tracks = requests.get(f"{config['api_base']}/getPlaylist", query_options | {'id': playlist_id})
tracks = (r_tracks.json())['subsonic-response']['playlist']['entry']
for track in tracks:
    featured_albums.add(track['albumId'])

# Get the list of albums in the library
r_albums = requests.get(f"{config['api_base']}/getAlbumList", query_options | {'size': 500, 'type': 'newest'})
albumlist = (r_albums.json())['subsonic-response']['albumList']['album']
unfeatured_albums = dict()
for album in albumlist:
    if not album['id'] in featured_albums:
        pass
        unfeatured_albums[album['id']] = album

table = list()
for album in unfeatured_albums:
    table.append([unfeatured_albums[album]['artist'], unfeatured_albums[album]['title']])

print(tabulate.tabulate(table))
