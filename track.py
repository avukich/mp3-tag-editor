import util


class Track(object):
    def __init__(self, path=''):
        self.path = path
        self.id = ''
        self.title = ''
        self.artist = ''
        self.album = ''
        self.year = ''
        self.genres = []
        self.number = ''
        self.disc_number = 0

    def to_string(self):
        return f'{self.artist}({self.genres}) - {self.album}({self.year}) - {self.number}: {self.title}'

    def file_name(self):
        return util.replace_illegal_characters(
            util.strip_explicit_text(f'{self.artist}-{self.album}-{self.number}-{self.title}.mp3'))

    def album_name(self):
        return util.replace_illegal_characters(util.strip_explicit_text(f'({self.year}) {self.album}'))

    def pretty_print(self, include_paths=False):
        pretty_string = f'#{self.number} - {self.title}'

        if include_paths:
            pretty_string = pretty_string + f' [{self.path}]'

        return pretty_string
