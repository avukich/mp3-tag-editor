from glob import glob
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TRCK, TCON, TDRC, TPOS


def modify_id3_tags(track, mp3):
    debug_tags(mp3)

    try:
        tags = ID3(mp3)
    except ID3NoHeaderError:
        print("Adding ID3 header")
        tags = ID3()

    print("\nBEFORE MODIFICATION")
    print(tags.keys())

    tags["TPE1"] = TPE1(encoding=3, text=track.artist)
    tags["TALB"] = TALB(encoding=3, text=track.album)
    tags["TIT2"] = TIT2(encoding=3, text=track.title)
    tags["TDRC"] = TDRC(encoding=3, text=track.year)
    tags["TRCK"] = TRCK(encoding=3, text=track.number)
    # tags["TPOS"] = TPOS(encoding=3, text=track.disc)
    tags["TCON"] = TCON(encoding=3, text=track.genres)
    tags.save(mp3)

    print("\nAFTER MODIFICATION")
    debug_tags(mp3)


def debug_tags(mp3):
    for filename in glob(mp3):
        mp3info = EasyID3(filename)
        print(f'ARTIST:       {mp3info["artist"]}')
        print(f'ALBUM:        {mp3info["album"]}')
        print(f'TITLE:        {mp3info["title"]}')
        print(f'DATE:         {mp3info["date"]}')
        print(f'TRACK NUMBER: {mp3info["tracknumber"]}')
        print(f'DISC NUMBER:  {mp3info["discnumber"]}')
        print(f'GENRE:        {mp3info["genre"]}\n')
