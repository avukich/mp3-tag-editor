import util


class Album(object):
    def __init__(self, path=''):
        self.path = path
        self.id = ''
        self.type = ''
        self.artwork_url = ''
        self.title = ''
        self.artist = ''
        self.year = ''
        self.tracks = []
        self.discs = []
        self.disc_number = 0

    def to_string(self):
        return f'{self.artist} - {self.title}({self.year})'

    def album_folder_name(self):
        if self.disc_number > 0:
            return f'Disc {self.disc_number}'
        else:
            return util.replace_illegal_characters(util.strip_explicit_text(f'({self.year}) {self.title}'))

    def pretty_print(self, include_paths=False, is_disc=False):
        pretty_string = ''
        track_padding = '\t\t\t'

        if is_disc:
            pretty_string = f'\t\t\t - Disc {self.disc_number})'
            track_padding = '\t\t\t\t'
        else:
            pretty_string = f'\t\t - {self.title} ({self.year})'

        if include_paths:
            pretty_string = pretty_string + f' [{self.path}]'
        pretty_string = pretty_string + '\n'

        if len(self.tracks) > 0:
            for track in self.tracks:
                pretty_string = pretty_string + track_padding + track.pretty_print(include_paths)

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
