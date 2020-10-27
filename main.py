from mutagen.easyid3 import EasyID3
import os

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


def get_abbrev(s):
    if len(s.split(' ')) == 1:
        return s[:2]
    else:
        return s.split(' ')[0][0] + s.split(' ')[1][0]


TAG_ABBREVIATIONS = {i.replace(' ', ''): get_abbrev(i) for i in AVAILABLE_TAGS}


def normalize_path(path):
    return os.path.abspath(path[1:-1]) if path.endswith("'") or path.endswith('"') else \
        os.path.abspath(path)


def file_is_mp3(normal_path):
    return os.path.isfile(normal_path) and normal_path.endswith('.mp3')


def get_all_paths_to_mp3_in_dir(normal_dir_path):
    return [os.path.join(normal_dir_path, cur_file_name) for cur_file_name in os.listdir(normal_dir_path) if
            cur_file_name.endswith('.mp3')]


def dict_is_empty(d):
    for k in d.keys():
        if d[k]:
            return False
    return True


class Mp3File:
    def __init__(self, normal_path):
        self.path = normal_path
        self.file_name = normal_path.split('\\')[-1]
        self.tags = EasyID3(normal_path)

    def get_tags(self):
        result = dict()
        for tag in AVAILABLE_TAGS:
            tag = tag.replace(' ', '')
            result[tag] = ''.join(self.tags[tag]) if tag in self.tags.keys() else None
        return result

    def print_info(self):
        print()
        tags = self.get_tags()
        for tag in tags.keys():
            print("{} {}".format(
                tag.upper().ljust(15, ' '),
                tags[tag] if tags[tag] else "<UNDEFINED>"
            ))


if __name__ == '__main__':
    f = Mp3File(normalize_path('song.mp3'))
    print(f.get_tags())
