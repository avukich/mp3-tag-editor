import os
import util
from album import Album
from artist import Artist
from track import Track


class FileSystemCrawler(object):
    def __init__(self, spotify):
        self.spotify = spotify
        self.root = os.path.abspath(os.sep)
        self.base_path = os.path.join(self.root, 'Users', 'nsd295', 'Music', 'mp3s')

    def start(self):
        print(f'Beginning file system crawling process....')
        finished = []
        all_artists = os.listdir(self.base_path)
        for artist_name in all_artists:
            print(f'Processing artist: {artist_name}')
            artist_path = os.path.join(self.base_path, artist_name)
            if os.path.isdir(artist_path):
                # we have found a folder corresponding to an artist
                artist = Artist(path=artist_path)
                artist.name = artist_name
                all_material = os.listdir(artist_path)
                for item in all_material:
                    item_path = os.path.join(artist_path, item)
                    if os.path.isdir(item_path):
                        # we have found a folder corresponding to an album
                        album = Album(path=item_path)
                        album.artist = artist.name
                        album.title = item
                        artist.albums.append(album)
                        album_contents = os.listdir(item_path)
                        for content in album_contents:
                            content_path = os.path.join(item_path, content)
                            if os.path.isdir(content_path):
                                disc_contents = os.listdir(content_path)
                                for disc_item in disc_contents:
                                    disc_item_path = os.path.join(content_path, disc_item)
                                    if os.path.isdir(disc_item_path):
                                        print(f'{disc_item}: Processing a directory at this level is currently unsupported')
                                    else:
                                        if content.endswith(".mp3") or content.endswith(".wma"):
                                            track = Track(path=content_path)
                                            track.artist = artist.name
                                            track.title = util.clean_file_name(content)
                                            track.number = util.get_track_number_from_file_name(content)
                                            # get disc number from folder name
                                            track.disc_number = 1
                                            #  a disc object needs created and the track added to the disc
                                            # album.tracks.append(track)
                                        else:
                                            print(
                                                f'{content}: Processing a file type other than mp3 at this level is currently unsupported')
                                # TODO: This must be a multi-disc set
                                print(f'{content} is actually another directory')
                            else:
                                if content.endswith(".mp3") or content.endswith(".wma"):
                                    track = Track(path=content_path)
                                    track.artist = artist.name
                                    track.title = util.clean_file_name(content)
                                    track.number = util.get_track_number_from_file_name(content)
                                    album.tracks.append(track)
                                else:
                                    print(f'{content}: Processing a file type other than mp3 at this level is currently unsupported')
                    else:
                        # we have potentially found a track that isn't associated with an album
                        if item.endswith(".mp3"):
                            track = Track(path=item_path)
                            track.artist = artist.name
                            track.title = util.clean_file_name(item)
                            track.number = util.get_track_number_from_file_name(item)
                            artist.songs.append(track)
                        else:
                            print(f'{item}: Processing a file type other than mp3 at this level is currently unsupported')
                finished.append(artist)
            else:
                print(f'{artist_name}: Processing a file at this level in the file system is currently unsupported')

        for artist in finished:
            print(artist.pretty_print(include_paths=True))
