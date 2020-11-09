from main import *
from argparse import ArgumentParser

# if True, parse args from TEST_ARGS
test = False
TEST_ARGS = "song.mp3 -ti TEST_TITLE -ar TEST_ARTIST"

def tag_to_arg(s, delimiter=' '):
    # "title" --> "-ti"
    # "disc number" --> "-dn"
    if len(s.split(delimiter)) == 1:
        return '-' + s[:2]
    else:
        return '-' + s.split(delimiter)[0][0] + s.split(delimiter)[1][0]


def dict_is_empty(d):
    # True if all values are None
    for k in d.keys():
        if d[k]:
            return False
    return True


parser = ArgumentParser(description='Display/edit mp3 metadata')

parser.add_argument("path", type=str, help="Path to an mp3 file or folder")

# Adding arguments for each tag from AVAILABLE_TAGS
for tag in AVAILABLE_TAGS:
    parser.add_argument(tag_to_arg(tag), dest=tag, nargs='?', help="Set new " + tag)

parser.add_argument("--auto", action='store_true', help="Set title and artist from file name")

# Parsing arguments into Dict either from cmd or from TEST_ARGS
args = vars(parser.parse_args()) if not test else vars(parser.parse_args(TEST_ARGS.split()))

# Getting path to file/folder, removing it from Dict
path = args.pop('path')
auto = args.pop('auto')
new_tags = args

# Getting paths to files to modify
file_paths = []
if os.path.isfile(path):
    file_paths.append(path)
else:
    file_paths = get_all_paths_to_mp3_in_dir(path)

# Display info
if dict_is_empty(new_tags) and not auto:
    print("No arguments entered, displaying info...")
    for path in file_paths:
        file = Mp3File(path)
        file.print_info()

# Modify file(s)
else:
    for path in file_paths:
        file = Mp3File(path)
        print(f"Modifying {file.file_name}...")
        if auto:
            file.auto_tag()
            #new_tags['artist'], new_tags['title'] = split_filename(file.file_name)
        for tag in new_tags.keys():
            if new_tags[tag]:
                file.set_tag(tag, new_tags[tag])
        print("Saving...", end=' ')
        file.tags.save()
        print("Saved.")
        print()
