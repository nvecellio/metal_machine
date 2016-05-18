import json
import pprint
import sys
import spotipy

spotify = spotipy.Spotify()

artist_input = raw_input('Enter an artist to search for: ')

artist_info = spotify.search(q=artist_input, type='artist')

artists = artist_info['artists']['items']
artist_id = None
for artist in artists:
    name = artist['name']
    if len(artist['genres']) == 0:
        choice = raw_input('Are you looking for {artist}?(Y/N)'.format(artist=name))
    else:
        genre = artist['genres'][0]
        choice = raw_input('Are you looking for {artist}, the {genre} band?(Y/N)'.format(artist=name, genre=genre))

    if choice.lower() == 'y':
        artist_id = artist['id']
        break
    elif choice.lower() == 'n':
        continue
    else:
        sys.exit('you fucked up')

related_artists = spotify.artist_related_artists(artist_id=artist_id)
genres_list = []
for artist in related_artists['artists']:
    if len(artist['genres']) > 0:
        for genre in artist['genres']:
            genres_list.append(genre)
    else:
        continue
print list(set(genres_list))




"""
Scratch code below
"""
# with open('secret.txt', 'r') as conf_file:
#     conf = json.load(conf_file)
#
# CLIENT_ID = conf['client_id']
# CLIENT_SECRECT = conf['client_secret']