from main import *
from argparse import ArgumentParser

TEST_ARGS = \
    "song.mp3 " \
    "-ti test_ti " \
    "-ar test_ar " \
    "-al test_al " \
    "-aa test_aa " \
    "-tn test_tn " \
    "-dn test_dn " \
    "-ge test_ge " \
    "-la test_la " \
    "-da 1999"

test = 1


def tag_to_arg(s, delimiter=' '):
    if len(s.split(delimiter)) == 1:
        return '-' + s[:2]
    else:
        return '-' + s.split(delimiter)[0][0] + s.split(delimiter)[1][0]


parser = ArgumentParser(description='Display/edit mp3 metadata')

parser.add_argument("file_name", type=str, help="Path to an mp3 file")

for tag in TAG_ABBREVIATIONS.keys():
    parser.add_argument("-" + TAG_ABBREVIATIONS[tag], dest=tag, nargs='?', help="Set new " + tag)

args = vars(parser.parse_args()) if not test else vars(parser.parse_args(TEST_ARGS.split()))
file_name = args.pop('file_name')
new_tags = args

file = Mp3File(file_name)

if dict_is_empty(new_tags):
    print("No arguments entered, displaying info...")
    file.print_info()
else:
    print("Setting selected tags...")
    for tag in new_tags.keys():
        if new_tags[tag]:
            print(f"Setting {tag}...", end=' ')
            file.tags[tag] = new_tags[tag]
            print("Set.")
    print("Saving...", end=' ')
    file.tags.save()
    print("Saved. \nExiting")
