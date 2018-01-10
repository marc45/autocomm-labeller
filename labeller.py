import sys

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QGroupBox, QVBoxLayout

from widgets.display import Display
from widgets.classbar import Classbar
from widgets.toolbar import Toolbar
from utils.state import AppState


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Autocomm Labeller - Dataset Labelling for AI'
        self.left, self.top, self.width, self.height = 100, 100, 1000, 600

        self.state = AppState()

        self.toolbar = Toolbar(self.state)
        self.classbar = Classbar(self.state)
        self.display = Display(self.state)
        self.main_widget = self.create_main_widget()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

        # Wrapper layout for entire window
        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(5, 5, 5, 5)
        window_layout.setSpacing(0)
        window_layout.addWidget(self.toolbar)
        window_layout.addWidget(self.main_widget)
        self.setLayout(window_layout)

    def create_main_widget(self):
        """
        Creates the main layout for the annotation part of the application
        :return: QGridLayout
        """
        box = QGroupBox()
        box.setFlat(True)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.classbar)
        layout.addWidget(self.display)
        box.setLayout(layout)

        self.main_widget = box
        return self.main_widget

    def closeEvent(self, QCloseEvent):
        self.state.write_state()

app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
