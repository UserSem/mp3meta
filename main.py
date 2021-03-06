import mutagen
from mutagen.easyid3 import EasyID3
import os
import ntpath


TEST_MP3_PATH = r'"song.mp3"'
AVAILABLE_TAGS = [
    'title',
    'artist',
    'album',
    'album artist',
    'track number',
    'disc number',
    'genre',
    'language',
    'date'
]

EMPTY_TAG_OUTPUT = "<UNDEFINED>"  # Output if tag is empty
EMPTY_TAG_INPUT = "None"  # Pass this value to clear tag


def get_all_paths_to_mp3_in_dir(normal_dir_path):
    return [os.path.join(normal_dir_path, cur_file_name) for cur_file_name in os.listdir(normal_dir_path) if
            cur_file_name.endswith('.mp3')]


def split_filename(s):
    # "Artist - Title.mp3" --> (Artist, Title)
    # "Title.mp3" --> (None, Title)
    if ' - ' in s:
        s = s.split(' - ')
        artist = s[0]
        title = ''.join(s[1:])[:-4]
        return artist, title
    else:
        return "", s[:-4]


class Mp3File:
    def __init__(self, normal_path):
        self.path = normal_path
        # self.file_name = normal_path.split('\\')[-1] old
        self.file_name = ntpath.basename(normal_path)
        try:
            self.tags = EasyID3(normal_path)
        except:
            self.tags = mutagen.File(normal_path, easy=True)

    def get_tags(self):
        # Returns dict with all AVAILABLE_TAGS
        result = dict()
        for tag in AVAILABLE_TAGS:
            tag = tag.replace(' ', '')
            result[tag] = ''.join(self.tags[tag]) if tag in self.tags.keys() else None
        return result

    def set_tag(self, tag, new_val):
        tag_formatted = tag.replace(' ', '')
        if new_val == EMPTY_TAG_INPUT:
            print(f"{self.file_name}: Clearing {tag}...")
            self.tags[tag_formatted] = ""
        else:
            print(f"{self.file_name}: Setting {tag} to {new_val}...", end=' ')
            self.tags[tag_formatted] = new_val
            print(f"Set.")
        self.tags.save()

    def auto_tag(self):
        new_artist, new_title = split_filename(self.file_name)
        self.set_tag('artist', new_artist if new_artist else EMPTY_TAG_INPUT)
        self.set_tag('title', new_title)

    def print_info(self):
        print()
        tags = self.get_tags()
        for tag in AVAILABLE_TAGS:
            tag_formatted = tag.replace(' ', '')
            print("{} {}".format(
                tag.upper().ljust(15, ' '),
                tags[tag_formatted] if tags[tag_formatted] else EMPTY_TAG_OUTPUT
            ))
