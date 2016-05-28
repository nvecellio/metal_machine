import json
import sys

import spotipy
import spotipy.util as util


class MetalMachine:
    def __init__(self):
        """
        Initialize authentication and spotify api connection
        """
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
        """
        Search for an artist, and give the user options for results, based on genre
        :return artist_id string - ID for the selected artist
        """
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

    def get_extended_artist_ids(self):
        pass

    def get_related_artist_ids(self, artist_search_id):
        """
        Takes an artist ID and returns related artists(IDs) and genres(by name)
        :param   artist_search_id - ID returned from self.artist_search(), or, a spotify artist ID
        :returns artist_ids:   list - Contains IDs of artists related to input artist
                 genres_list:  list - Contains genre names (i.e. 'Metal', 'Rock') found in related artists
        """
        related_artists = self.spotify.artist_related_artists(artist_id=artist_search_id)
        genres_list = []
        artist_ids = []
        for artist in related_artists['artists']:
            artist_ids.append(artist['id'])
            if len(artist['genres']) > 0:
                for genre in artist['genres']:
                    genres_list.append(genre)
            else:
                continue
            genres_list = list(set(genres_list))  # Remove duplicates and return list
        return artist_ids, genres_list

    def get_recommendations(self, artist_ids, genres=None):
        """
        :param artist_id_list   - list of artists returned from self.get_related_artist_ids()
        :param genres_list      - list of genres returned from self.get_related_artist_ids()
        :return recommendations - dict - related albums in artist['album_name'] format
        """
        seed_genres = None
        genre_recs = None
        rec_info = None
        if genres:
            seeds = self.spotify.recommendation_genre_seeds()
            for genre in genres:
                if genre not in seeds:
                    genres.remove(genre)
            if genres:
                seed_genres = ','.join(genres)
        if seed_genres:
            genre_recs = self.spotify.recommendations(seed_genres=seed_genres)
            if not len(genre_recs['tracks']):
                rec_info = self.spotify.recommendations(seed_artists=artist_ids)
        else:
            rec_info = self.spotify.recommendations(seed_artists=artist_ids)
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
related = {}
related_key = 0
related[related_key] = metal.get_recommendations(artist_ids, genre_list)

for artist_id in artist_ids:
    related_key += 1
    artist_id_list = []
    artist_id_list.append(artist_id)
    related[related_key] = metal.get_recommendations(artist_ids=artist_id_list)

for k,v in related.iteritems():
    # this just prints the related artists and their albums, make it clear in the future
    for key, val in v.iteritems():
        print key + ': ' + val


# TODO: start creating playlists with songs from the recommended albums
# TODO: Something to keep in mind with those playlists is to compare some of the recommendation statistics to make sure the songs/albums added to the playlist are close in loudness/speed/stuff to the original search
# TODO: Way later: wrap all of these choices in flask web app to present to the user
