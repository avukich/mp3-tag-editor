import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from track import Track
from album import Album
from artist import Artist


def parse_release_date(date, precision):
    if precision == "day":
        return date.split("-")[0]
    return ''


def pad_track_number(number):
    if len(str(number)) == 1:
        return "0" + str(number)
    return number


def download_album_art(url):
    f = urllib.request.urlopen(url)
    data = f.read()
    with open("art.jpg", "wb") as art:
        art.write(data)


class Spotify(object):
    def __init__(self):
        self.client_id = 'd870b01246084a03b56a30c36d3f18b7'
        self.client_secret = '8221fbada6e0410792ac35820a8a8949'

        self.client_credentials_manager = SpotifyClientCredentials(self.client_id, self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def search(self, criteria):
        print(f'searching Spotify with criteria of {criteria}')
        results = self.sp.search(q=criteria, limit=1)
        for i, t in enumerate(results['tracks']['items']):
            track = Track()
            track.title = t['name']
            track.number = pad_track_number(t['track_number'])
            album_id = t['album']['id']
            album = self.get_album_old(album_id)
            track.artist = album.artist
            track.album = album.title
            track.year = album.year
            track.genres = album.genres
            return track

    def search_by_artist(self, criteria):
        print(f'searching Spotify by artist with criteria of {criteria}')

        results = self.sp.search(q=criteria, limit=1, type="artist")

        total_found = results['artists']['total']

        if total_found <= 0:
            print(f'No artists found for {criteria}')
            raise KeyError(f'No artists found for {criteria}')

        if total_found > 1:
            print(f'Too many artists found for {criteria}.  Found {total_found}')
            raise IndexError(f'Too many artists found for {criteria}.  Found {total_found}')

        for i, a in enumerate(results['artists']['items']):
            artist = Artist()
            artist.id = a['id']
            artist.name = a['name']
            artist.genres = a['genres']
            return artist

    def get_artist(self, id):
        print(f'calling Spotify to get artist with id of {id}')
        spotify_artist = self.sp.artist(id)
        artist = Artist()
        artist.id = spotify_artist['id']
        artist.name = spotify_artist['name']
        artist.genres = spotify_artist['genres']
        return artist

    def get_artists_albums(self, id, artist_name):
        print(f'calling Spotify to get artist\'s albums with id of {id}')
        albums = []
        spotify_artist_albums = self.get_artists_albums_with_offset(id, 0)
        print(spotify_artist_albums)
        albums_to_process = spotify_artist_albums['items']
        if spotify_artist_albums['total'] > 50:
            total = spotify_artist_albums['total']
            print(f'{artist_name} has {total} albums to process')
            offset = 50
            while total > offset:
                print(f'{total} < {offset}')
                next_batch = self.get_artists_albums_with_offset(id, offset)
                albums_to_process.append(next_batch['items'])
                offset = offset + 50

        for artist_album in albums_to_process:
            if artist_name == artist_album['artists'][0]['name']:
                album = self.get_album(artist_album['id'])
                albums.append(album)
                print(album.title)
        return albums

    def get_artists_albums_with_offset(self, id, offset):
        print(f'Calling Spotify for artist id of {id} and an offset of {offset}')
        return self.sp.artist_albums(artist_id=id, limit=50, offset=offset)

    def get_album(self, id):
        spotify_album = self.sp.album(id)
        album = Album()
        album.id = id
        album.type = spotify_album['album_type']
        album.title = spotify_album['name']
        album.artist = spotify_album['artists'][0]['name']
        album.year = parse_release_date(spotify_album['release_date'], spotify_album['release_date_precision'])
        album.artwork_url = spotify_album['images'][0]['url']
        return album

    def get_album_old(self, id):
        spotify_album = self.sp.album(id)
        album = Album()
        album.title = spotify_album['name']
        album.artist = spotify_album['artists'][0]['name']
        album.genres = self.get_genres(spotify_album['artists'][0]['id'])
        album.year = parse_release_date(spotify_album['release_date'], spotify_album['release_date_precision'])
        download_album_art(spotify_album['images'][0]['url'])
        return album

    def get_genres(self, artist_id):
        spotify_artist = self.sp.artist(artist_id)
        return spotify_artist['genres']
