from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main import *
import sys


BUTTON_FONT = QFont("Bahnschrift", 24)

OPEN_FILE_DIR_W = 240
OPEN_FILE_DIR_H = 80

OR_FONT = QFont("Bahnschrift", 32)
OR_H = 80
OR_W = 80

LOAD_BTN_W = 120
LOAD_BTN_H = 80

TAG_ENTRY_FONT = QFont("Consolas", 16)
TAG_ENTRY_W = OPEN_FILE_DIR_W
TAG_ENTRY_H = 30

TAG_ENTRY_SPACING = 20

TAG_ENTRY_X = 20
TAG_ENTRY_Y = 250


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.background = None
        self.open_dir_btn = None
        self.open_file_btn = None
        self.or_label = None
        self.load_button = None
        self.tag_entries = None
        self.auto_btn = None
        self.set_button = None

        self.path = None
        self.new_tag_list = None
        self.paths = None
        self.file = None
        self.dir = None

        self.init_ui()

    def init_ui(self):
        # BACKGROUND
        self.background = QLabel(self)
        self.background.resize(600, 900)
        self.background.setStyleSheet(f"background-color: {rgb_to_hex((50, 27, 84))};")

        # OPEN DIRECTORY BUTTON
        self.open_dir_btn = QPushButton("Open directory", self)
        self.open_dir_btn.setFont(BUTTON_FONT)
        self.open_dir_btn.clicked.connect(self.get_dir_path)
        self.open_dir_btn.resize(OPEN_FILE_DIR_W, OPEN_FILE_DIR_H)
        self.open_dir_btn.move(20, 50)

        # OPEN FILE BUTTON
        self.open_file_btn = QPushButton("Open file(s)", self)
        self.open_file_btn.setFont(BUTTON_FONT)
        self.open_file_btn.clicked.connect(self.get_file_path)
        self.open_file_btn.resize(OPEN_FILE_DIR_W, OPEN_FILE_DIR_H)
        self.open_file_btn.move(340, 50)

        # "OR" LABEL
        self.or_label = QLabel('or', self)
        self.or_label.setFont(OR_FONT)
        self.or_label.setStyleSheet("QLabel { color : white; }")
        self.or_label.setAlignment(Qt.AlignCenter)
        self.or_label.resize(OR_H, OR_W)
        self.or_label.move(260, 50)

        # LOAD BUTTON
        self.load_button = QPushButton("Load", self)
        self.load_button.setFont(BUTTON_FONT)
        self.load_button.clicked.connect(self.load_path_list)
        self.load_button.resize(LOAD_BTN_W, LOAD_BTN_H)
        self.load_button.move(240, 50 + OPEN_FILE_DIR_H + 20)
        self.load_button.setEnabled(False)

        # TAG ENTRIES
        self.tag_entries = [QLineEdit(self) for _ in AVAILABLE_TAGS]
        for i, tag in enumerate(self.tag_entries):
            self.tag_entries[i].setFont(TAG_ENTRY_FONT)
            self.tag_entries[i].setPlaceholderText(AVAILABLE_TAGS[i])
            self.tag_entries[i].resize(TAG_ENTRY_W, TAG_ENTRY_H)
            self.tag_entries[i].move(TAG_ENTRY_X, TAG_ENTRY_Y + i * (TAG_ENTRY_H + TAG_ENTRY_SPACING))
            self.tag_entries[i].setEnabled(False)

        # AUTO TAG BUTTON
        self.auto_btn = QPushButton("Auto tag", self)
        self.auto_btn.setFont(BUTTON_FONT)
        self.auto_btn.clicked.connect(self.auto_tag)
        self.auto_btn.resize(OPEN_FILE_DIR_W, OPEN_FILE_DIR_H)
        self.auto_btn.move(340, TAG_ENTRY_Y + 6 * (TAG_ENTRY_SPACING + TAG_ENTRY_H))
        self.auto_btn.setEnabled(False)

        # SET CHOSEN TAGS BUTTON
        self.set_button = QPushButton("Set tags", self)
        self.set_button.setFont(BUTTON_FONT)
        self.set_button.clicked.connect(self.set_new_tags)
        self.set_button.resize(OPEN_FILE_DIR_W, OPEN_FILE_DIR_H)
        self.set_button.move(340, TAG_ENTRY_Y)
        self.set_button.setEnabled(False)

        # WINDOW
        self.setFixedSize(600, 650)
        self.setGeometry(300, 100, 600, 650)  # x, y, w, h
        self.setWindowTitle('mp3meta')
        self.setWindowIcon(QIcon('icon0.ico'))
        self.show()

    def get_new_tag_list(self):
        self.new_tag_list = []
        for entry in self.tag_entries:
            self.new_tag_list.append(entry.text())
        print(self.new_tag_list)

    def set_new_tags(self):
        self.get_new_tag_list()
        for path in self.paths:
            f = Mp3File(path)
            for i, tag in enumerate(self.new_tag_list):
                if tag:
                    f.set_tag(AVAILABLE_TAGS[i], tag)

    def auto_tag(self):
        if self.paths:
            for path in self.paths:
                f = Mp3File(path)
                f.auto_tag()
            self.file = None
            self.path = None
        else:
            print("File is not loaded!")

    def set_title(self):
        new_title = self.title_textbox.text()
        if self.file:
            self.file.set_tag("title", new_title)
            self.file = None
            self.path = None
        else:
            print("File is not loaded!")

    def get_dir_path(self):
        self.dir = QFileDialog.getExistingDirectory(self, "Choose Directory")
        self.load_button.setEnabled(True)

    def get_file_path(self):
        self.file = QFileDialog.getOpenFileNames(self, "Open file", "*.mp3")[0]
        self.load_button.setEnabled(True)

    def load_path_list(self):
        if self.file or self.dir:
            if self.file:
                self.paths = self.file
            else:
                self.paths = get_all_paths_to_mp3_in_dir(self.dir)
            self.dir = None
            self.file = None
            for i, tag in enumerate(self.tag_entries):
                self.tag_entries[i].setEnabled(True)
            for p in self.paths:
                print(p)
            self.auto_btn.setEnabled(True)
            self.set_button.setEnabled(True)

            first_file = Mp3File(self.paths[0])
            print(first_file.get_tags().values())
            for i, tag in enumerate(self.tag_entries):
                self.tag_entries[i].setText(list(first_file.get_tags().values())[i])


        else:
            print('No path is selected!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    win = Example()
    win.show()

    sys.exit(app.exec_())
