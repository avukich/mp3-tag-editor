import util


class Artist(object):
    def __init__(self, path=''):
        self.path = path
        self.id = ''
        self.name = ''
        self.genres = []
        self.albums = []
        self.songs = []

    def to_string(self):
        return f'{self.name}({self.genres})'

    def folder_name(self):
        return util.replace_illegal_characters(util.strip_explicit_text(f'{self.name}'))

    def populate_metadata(self, spotify):
        global spotify_artist

        try:
            if util.is_string_not_blank(self.id):
                print(f'populating artist using id of {self.id}')
                spotify_artist = spotify.get_artist(self.id)
            else:
                print(f'populating artist using name of {util.clean_title_starting_with_the(self.name)}')
                spotify_artist = spotify.search_by_artist(util.clean_title_starting_with_the(self.name))
        except (KeyError, IndexError) as error:
            # TODO: This should be logged somehow for follow-up
            print(error)
            raise

        if not spotify_artist:
            print("Couldn't find artist!")
        else:
            self.id = spotify_artist.id
            self.name = spotify_artist.name
            self.genres = spotify_artist.genres

    def pretty_print(self, include_paths=False):
        pretty_string = f'* {self.name}'
        if include_paths:
            pretty_string = pretty_string + f' [{self.path}]'
        pretty_string = pretty_string + "\n"
        if len(self.albums) > 0:
            pretty_string = pretty_string + "\tAlbums:\n"
            for album in self.albums:
                pretty_string = pretty_string + album.pretty_print(include_paths) + "\n"
        if len(self.songs) > 0:
            pretty_string = pretty_string + "\tSongs:\n"
            for song in self.songs:
                pretty_string = pretty_string + "\t\t" + song.pretty_print(include_paths) + "\n"
        return pretty_string
        #     * The Acacia Strain [path]:
        #         Albums:
        #             - The Dead Walk (2006) [path]
        #                 #01 - Sarin: The End [path]
        #                 #02 - Burnface [path]
        #                 ...
        #             - Wormwood (2010) [path]
        #                 #01 - The Beast [path]
        #                 #02 - THe Hills Have Eyes [path]
        #                 ...
        #             - Some Multi-disc Album (YYYY) [path]
        #                 Disc 1 [path]
        #                     #01 - Track 1 [path]
        #                     ...
        #                 Disc 2 [path]
        #                     #01 - Track 1 [path]
        #                     ...
        #             ...
        #         Songs:
        #             # Some random track [path]
        #             ...
