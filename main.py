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

EMPTY_TAG_OUTPUT = "<UNDEFINED>"  #  Output if tag is empty
EMPTY_TAG_INPUT = "None"  #  Pass this value to clear tag

def get_abbrev(s):
    # "title" --> "ti"
    # "disc number" --> "dn"
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
        # Returns dict with all AVALIABLE_TAGS
        result = dict()
        for tag in AVAILABLE_TAGS:
            tag = tag.replace(' ', '')
            result[tag] = ''.join(self.tags[tag]) if tag in self.tags.keys() else None
        return result

    def set_tag(self, tag, new_val):
        tag_formatted = tag.replace(' ', '')
        if new_val == EMPTY_TAG_INPUT:
            print(f"Clearing {tag}...")
            self.tags[tag_formatted] = ""
        else:
            print(f"Setting {tag} to {new_val}...")
            self.tags[tag_formatted] = new_val
        f.tags.save()

    def print_info(self):
        print()
        tags = self.get_tags()
        for tag in tags.keys():
            print("{} {}".format(
                tag.upper().ljust(15, ' '),
                tags[tag] if tags[tag] else EMPTY_TAG_OUTPUT
            ))


if __name__ == '__main__':
    TEST_FOLDER = r"C:\Users\users_x2jxvc2\Desktop\test"
    for p in get_all_paths_to_mp3_in_dir(TEST_FOLDER):
        f = Mp3File(p)
        print(f.get_tags())
        f.set_tag("album artist", "Qwe")
        f.set_tag("album", "ALBUM")
        f.tags.save()
