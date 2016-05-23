import json
import sys

import spotipy
import spotipy.util as util


class MetalMachine:
    def __init__(self):
        with open('secret.txt', 'r') as conf_file:
            conf = json.load(conf_file)
            self.CLIENT_ID = conf['client_id']
            self.CLIENT_SECRECT = conf['client_secret']
            self.REDIRECT_URI = 'http://localhost:8080/callback'
        self.token = util.prompt_for_user_token(username='redbeard1167', scope='user-library-modify',
                                                client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRECT,
                                                redirect_uri=self.REDIRECT_URI)
        self.spotify = spotipy.Spotify(auth=self.token)

    def artist_search(self):
        artist_input = raw_input('Enter an artist to search for: ')
        artist_info = self.spotify.search(q=artist_input, type='artist')
        artists = artist_info['artists']['items']

        for artist in artists:

            name = artist['name']

            if len(artist['genres']) == 0:
                choice = raw_input('Are you looking for {artist}?(Y/N)'.format(artist=name))
            else:
                genre = artist['genres'][0]
                choice = raw_input('Are you looking for {artist}, the {genre} band?(Y/N)'.format(artist=name,
                                                                                                 genre=genre))

            if choice.lower() == 'y':
                artist_id = artist['id']
                return artist_id
            elif choice.lower() == 'n':
                continue
            else:
                print 'Invalid Entry'
                self.artist_search()

    def get_related_artist_ids(self, artist_search_id):
        related_artists = self.spotify.artist_related_artists(artist_id=artist_search_id)
        genres_list = []
        artist_ids = []
        for artist in related_artists['artists']:
            artist_ids.append(artist['uri'])
            if len(artist['genres']) > 0:
                for genre in artist['genres']:
                    genres_list.append(genre)
            else:
                continue
            genres_list = list(set(genres_list))
        return artist_ids, genres_list

    def get_recommendations(self, artist_id_list, genres_list):
        seeds = self.spotify.recommendation_genre_seeds()
        for genre in genres_list:
            if genre in seeds:
                continue
            else:
                genres_list.remove(genre)
        genre_recs = self.spotify.recommendations(seed_genres=','.join(genres_list))
        print 'Couldn\'t find anything based on genre, searching by artists'
        if len(genre_recs['tracks']) == 0:
            rec_info = self.spotify.recommendations(seed_artists=artist_id_list)
        else:
            rec_info = genre_recs
        recommendations = {}
        for track in rec_info['tracks']:
            recommendations[track['artists'][0]['name']] = track['album']['name']

        if not recommendations:
            sys.exit('Couldn\'t find any recommendations')
        else:
            return recommendations


metal = MetalMachine()
artist = metal.artist_search()
artist_ids, genre_list = metal.get_related_artist_ids(artist)
related = metal.get_recommendations(artist_ids, genre_list)
print related

# TODO: Use the related artist to do a little recursive searching for recommendations to provide a lot of choices, then start creating playlists with songs from the recommended albums
# TODO: Something to keep in mind with those playlists is to compare some of the recommendation statistics to make sure the songs/albums added to the playlist are close in loudness/speed/stuff to the original search
# TODO: Way later: wrap all of these choices in flask web app to present to the user
