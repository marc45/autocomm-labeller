import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QLabel, QPushButton, QFileDialog, QRadioButton, QButtonGroup, \
    QScrollArea


class Toolbar(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.state.toolbar = self

        self.mode_button_group = QButtonGroup()
        self.dir_label = QLabel('')
        self.dir_label.setFixedWidth(500)

        self.init_gui()

    def init_gui(self):
        self.setMinimumSize(800, 100)
        self.setMaximumHeight(100)

        wrapper_layout = QVBoxLayout()
        box = QGroupBox('Toolbar')
        layout = QHBoxLayout()
        self._init_directory_picker(layout)
        self._init_mode_picker(layout)

        box.setLayout(layout)
        wrapper_layout.addWidget(box)
        self.setLayout(wrapper_layout)
        self.set_source_dir(os.path.join(os.getcwd(), 'images'))

    def _init_mode_picker(self, layout):
        image_button = QRadioButton('Images')
        video_button = QRadioButton('Video')
        self.mode_button_group.addButton(image_button)
        self.mode_button_group.addButton(video_button)
        image_button.clicked.connect(lambda: self.trigger_set_mode('images'))
        video_button.clicked.connect(lambda: self.trigger_set_mode('video'))
        layout.addWidget(image_button)
        layout.addWidget(video_button)
        image_button.click()

    def _init_directory_picker(self, layout):
        dir_button = QPushButton('Change Directory')
        dir_button.setToolTip('Change source directory to draw images or video from.')
        dir_button.clicked.connect(self.trigger_change_dir)

        scroll_area = QScrollArea()
        scroll_area.setFixedHeight(30)
        scroll_area.setWidget(self.dir_label)

        layout.addWidget(scroll_area)
        layout.addWidget(dir_button)

    def set_source_dir(self, val):
        self.state.source_dir = val
        self.dir_label.setText('Source Directory:  ' + self.state.source_dir)

    def trigger_change_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dirpath = QFileDialog.getExistingDirectory(self,
                                                   'QFileDialog.getExistingDirectory()',
                                                   '',
                                                   options=options) or os.getcwd()
        self.set_source_dir(dirpath)
        self.state.display.load_sources(dirpath)

    def trigger_set_mode(self, mode):
        self.state.mode = mode
