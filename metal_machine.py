import json
import sys

import spotipy
import spotipy.util as util

with open('secret.txt', 'r') as conf_file:
    conf = json.load(conf_file)

CLIENT_ID = conf['client_id']
CLIENT_SECRECT = conf['client_secret']
REDIRECT_URI = 'http://localhost:8080/callback'

token = util.prompt_for_user_token(username='redbeard1167', scope='user-library-modify', client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRECT,
                                   redirect_uri=REDIRECT_URI)

spotify = spotipy.Spotify(auth=token)

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

genres_list = list(set(genres_list))
genres = ','.join(genres_list)

genre_seeds = spotify.recommendation_genre_seeds()
print genre_seeds
raw_recs = spotify.recommendations(seed_genres=genres)

print raw_recs

# Make it so the band genre list searches through the seed genre list, and only searches what's available. if nothing,
# fall back to artist based recs
