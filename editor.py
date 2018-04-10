import os
from shutil import copyfile
from spotify import Spotify
from artist import Artist
import id3_editor
import util
from file_system_crawler import FileSystemCrawler

# potentially create a class to represent the entire catalog to do things like statistics




def process_mp3(mp3):
    # TODO: Modify to 1) create the folder structure if necessary, 2) download the album artwork if necessary, 2) copy
    #       the file over with the appropriate name, and 4) modify the ID3 tags as needed
    print(f'process_mp3 started for {mp3}')
    path_tuple = os.path.split(mp3)
    print(f'DIRTY NAME: {path_tuple[1]}')
    cleaned_name = util.clean_file_name(path_tuple[1])
    print(f'CLEANED NAME: {cleaned_name}')
    track = sp.search(cleaned_name)
    if track is None:
        # TODO: This should have a fallback mechanism
        print(f'Could not find anything on Spotify for {mp3} using {cleaned_name}')
    else:
        print(f'TRACK: {track.to_string()}')
        file_path = save_modified_mp3(track, path_tuple[0])
        id3_editor.modify_id3_tags(track, file_path)


def save_modified_mp3(track, mp3):
    # create the new folder structure if necessary and copy the file over
    artist_dir = os.path.join(finished_mp3_path, track.artist)
    if not os.path.exists(artist_dir):
        print('making artist dir')
        os.makedirs(artist_dir)

    album_dir = os.path.join(artist_dir, track.album_name())
    if not os.path.exists(album_dir):
        print('making album dir')
        os.makedirs(album_dir)

    file_path = os.path.join(album_dir, track.file_name())
    print(f'copying {mp3} to {file_path}')
    copyfile(mp3, file_path)

    # TODO: This isn't working yet
    if not os.path.exists("art.jpg"):
        old_art_path = os.path.join(os.getcwd(), "art.jpg")
        new_art_path = os.path.join(album_dir, "art.jpg")
        copyfile(old_art_path, new_art_path)

    return file_path


def clean_music_library():
    print(f'Beginning cleaning process....')
    all_artists = os.listdir(base_path)
    for artist_name in all_artists:
        print(f'Processing artist: {artist_name}')
        artist_path = os.path.join(base_path, artist_name)
        if os.path.isdir(artist_path):
            artist = Artist()
            artist.name = artist_name

            try:
                artist.populate_metadata(sp)
            except KeyError as key_error:
                # TODO: Decide how to deal with this edge case.  Might consider doing an album search and making sure that the artist name is similar.
                print(f'Cannot process {artist_name} purely by name because we are not getting any results')
                print(key_error)
            except IndexError as index_error:
                # TODO: Decide how to deal with this edge case.  Might consider doing some sort of set union with results from album search.
                print(f'Cannot process {artist_name} purely by name because we are getting more than 1 result')
                print(index_error)

            # we have the artist now we want to get the album
            artist_albums = sp.get_artists_albums(artist.id, artist.name)
            for album in artist_albums:
                print(album.to_string())

        else:
            print(f'Processing a file at this level in the file system is currently unsupported')


def original_flawed_logic():
    # loop through folders in base_path
        # set artist to folder name
        # loop through folders in artist folder
            # loop through the files
                # if the file is an mp3:
                    # DO SOMETHING
                # else if it is a folder:
                    # set album to folder name
                    # loop through the files
                        # if the file is an mp3:
                            # set title to file name stripped of the track number and '.mp3'
                            # call Spotify's api to get the information for the song using the artist and title
                            # if the song is found in Spotify:
                            # download the album art (?)
                            # clear it's id3 tags using Mutagen
                            # set the id3 tags to the values retrieved from the api (and the album art downloaded?)
                        # else:
                            # use whatever id3 tags were already embedded
                            # save to a new file structure (artist/'year - album'/'track number-artist-album-title.mp3'
                            # if the album artwork was downloaded save it to the folder with the tracks as 'artist-album.jpg/png'
                # else ignore it
    all_artists = os.listdir(base_path)
    for artist in all_artists:
        artist_path = os.path.join(base_path, artist)
        if os.path.isdir(artist_path):
            all_material = os.listdir(artist_path)
            for item in all_material:
                item_path = os.path.join(artist_path, item)
                if os.path.isdir(item_path):
                    album = item
                    album_contents = os.listdir(item_path)
                    for content in album_contents:
                        content_path = os.path.join(item_path, content)
                        if os.path.isdir(content_path):
                            print(f'{content} is actually another directory')
                        else:
                            if content.endswith(".mp3"):
                                process_mp3(os.path.join(content_path, content))
                            else:
                                print(f'{content} is something other than an mp3 file')
                else:
                    print(f'{item} is not an album so it may be a song')
        else:
            print(f'{artist} is not an artist directory')


root = os.path.abspath(os.sep)
base_path = os.path.join(root, 'Users', 'nsd295', 'Music', 'mp3s')
finished_mp3_path = os.path.join(root, 'Users', 'nsd295', 'Music', 'modified_mp3s')
sp = Spotify()

# clean_music_library()

# extra testing stuff
# try:
#     print(sp.search_by_artist("Tool"))
# except KeyError as key_error:
#     print(f'Cannot process Tool purely by name because we are not getting any results')
#     print(key_error)
# except IndexError as index_error:
#     print(f'Cannot process Tool purely by name because we are getting more than 1 result')
#     print(index_error)
#
# try:
#     print(sp.search_by_artist("XXXXXXXXXXXX"))
# except KeyError as key_error:
#     print(f'Cannot process XXXXXXXXXXXX purely by name because we are not getting any results')
#     print(key_error)
# except IndexError as index_error:
#     print(f'Cannot process XXXXXXXXXXXX purely by name because we are getting more than 1 result')
#     print(index_error)

# rtn = sp.get_artists_albums("22bE4uQ6baNwSHPVcDxLCe", "The Rolling Stones")

crawler = FileSystemCrawler(sp)
crawler.start()



