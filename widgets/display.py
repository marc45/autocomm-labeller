import os
import imageio

from utils.state import AppState
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QLabel, QPushButton, QFileDialog, QRadioButton, QButtonGroup, \
    QScrollArea, QSizePolicy
from PyQt5.QtGui import QImage, QPainter, QPen, QPixmap
from PyQt5 import QtCore


class DisplayLabel(QLabel):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._pixmap = None
        self._temp_pixmap = None
        self._original_image = None

        self.start_coord, self.end_coord = (0, 0), (0, 0)
        self.painting = False
        self.setFocus()

    def _setPixmap(self, q_source):
        size = (self.width(), self.height())
        q_source = QPixmap.fromImage(q_source).scaled(*size, QtCore.Qt.KeepAspectRatio)
        super().setPixmap(q_source)
        self._pixmap = q_source

    def setPixmap(self, q_source):
        size = (self.width(), self.height())
        self._original_image = q_source
        q_source = QPixmap.fromImage(q_source).scaled(*size, QtCore.Qt.KeepAspectRatio)
        super().setPixmap(q_source)
        self._pixmap = q_source

    def translate_coords_to_ratios(self, x, y):
        temp_x, temp_y = self._pixmap.width(), self._pixmap.height()
        return x / temp_x, y / temp_y

    def resizeEvent(self, QResizeEvent):
        size = (QResizeEvent.size().width(), QResizeEvent.size().height())
        if self._original_image:
            self._setPixmap(self._original_image)

    def keyPressEvent(self, QKeyEvent):
        key = QKeyEvent.key()
        if key == QtCore.Qt.Key_Return:
            pass

    def mousePressEvent(self, QMouseEvent):
        self.start_coord = (QMouseEvent.x(), QMouseEvent.y())

    def mouseMoveEvent(self, QMouseEvent):
        if self.painting:
            return
        self.painting = True
        self.end_coord = (QMouseEvent.x(), QMouseEvent.y())
        self._temp_pixmap = self._pixmap.copy()

        top_left = (min(self.start_coord[0], self.end_coord[0]), min(self.start_coord[1], self.end_coord[1]))
        bottom_right = (max(self.start_coord[0], self.end_coord[0]), max(self.start_coord[1], self.end_coord[1]))
        width, height = bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]

        self.drawRect(self._temp_pixmap, *top_left, width, height)

        self.painting = False

    def drawRect(self, pixmap, x, y, w, h):
        painter = QPainter(pixmap)
        pen = QPen(QtCore.Qt.red)
        painter.setPen(pen)
        painter.drawRect(x, y, w, h)
        painter.end()
        super().setPixmap(pixmap)


class Display(QWidget):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        self.state.display = self
        self.source_paths = []

        self.load_sources(self.state.source_dir)
        self.curr_i = -1
        self.layout = QVBoxLayout()

        self.painter = None
        self.source_label = DisplayLabel(self.state)

        self.init_gui()

    def _init_next_prev_save_buttons(self, layout):
        box = QGroupBox()
        box.setMaximumHeight(100)

        layout.addWidget(box)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        box.setLayout(layout)

        next_button = QPushButton('>')
        prev_button = QPushButton('<')
        save_button = QPushButton('Save')
        next_button.clicked.connect(lambda: self.change_source(self.curr_i + 1))
        prev_button.clicked.connect(lambda: self.change_source(self.curr_i - 1))
        save_button.clicked.connect(self.save_curr_source)

        layout.addWidget(prev_button)
        layout.addWidget(save_button)
        layout.addWidget(next_button)

        return box

    def load_sources(self, dirpath):
        self.source_paths = [os.path.join(dirpath, source_name) for source_name in os.listdir(dirpath)]
        self.curr_source_i = -1
        label_dir_path = os.path.join(dirpath, '..', 'labels')
        if not os.path.exists(label_dir_path):
            os.makedirs(label_dir_path)

    def get_source_from_np(self, source):
        height, width, channel = source.shape
        if channel == 4:
            q_source = QImage(source, width, height, QImage.Format_RGBA8888)
        else:
            q_source = QImage(source, width, height, QImage.Format_RGB888)
        return q_source

    def init_gui(self):
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self._init_next_prev_save_buttons(self.layout)
        self.layout.addWidget(self.source_label)

        self.setLayout(self.layout)

    def save_curr_source(self):
        pass

    def change_source(self, index):
        if index >= len(self.source_paths) or index < 0:
            return
        self.curr_i = index
        source = imageio.imread(self.source_paths[self.curr_i])
        self.source_label.setPixmap(self.get_source_from_np(source))