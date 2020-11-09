# mp3meta
## Features
* Change following ID3 tags of an mp3 file:
    * title
    * artist
    * album
    * album artist
    * track number
    * disc number
    * genre
    * language
    * date
* Change tags of every mp3 file in folder;
* Auto-assign tags to a file based on file name;

## Required modules
* mutagen
* argparse
* pyinstaller (for compiling to .exe)

## Usage
```
usage: no_gui.py [-h] [-ti [TITLE]] [-ar [ARTIST]] [-al [ALBUM]] [-aa [ALBUM ARTIST]] [-tn [TRACK NUMBER]]
                 [-dn [DISC NUMBER]] [-ge [GENRE]] [-la [LANGUAGE]] [-da [DATE]] [--auto]
                 path

positional arguments:
  path                Path to an mp3 file or folder

optional arguments:
  -h, --help          show this help message and exit
  -ti [TITLE]         Set new title
  -ar [ARTIST]        Set new artist
  -al [ALBUM]         Set new album
  -aa [ALBUM ARTIST]  Set new album artist
  -tn [TRACK NUMBER]  Set new track number
  -dn [DISC NUMBER]   Set new disc number
  -ge [GENRE]         Set new genre
  -la [LANGUAGE]      Set new language
  -da [DATE]          Set new date
  --auto              Set title and artist from file name
```

## Examples

| Command                                                          | Action                                                                           |
|------------------------------------------------------------------|----------------------------------------------------------------------------------|
| ```no_gui.py song.mp3```                                         | Display tags of song.mp3                                                         |
| ```no_gui.py song.mp3 -ti "I'm a title"```                       | Set title to "I'm a title"                                                       |
| ```no_gui.py "C:\Music\Powerwolf - Incense & Iron.mp3" --auto``` | Set artist to "Powerwolf", set title to "Incense & Iron"                         |
| ```no_gui.py "C:\Music" -da 2018 -la "Ancient Babylonian" ```    | Set date to 2018 and language to "Ancient Babylonian" for each file in C:\Music\ |
