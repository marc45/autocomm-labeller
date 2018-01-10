from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QLabel, QPushButton, QRadioButton, QButtonGroup, \
    QInputDialog
from PyQt5 import QtCore


class Classbar(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.state.classbar = self

        self.classes = {}
        self.classes_group = QButtonGroup()
        self.class_label = QLabel('Current class: \n')
        self.layout = None

        self.init_gui()
        classes = list(self.state.classes)
        self.state.classes = []
        for c in classes:
            self.add_class(c)

    def init_gui(self):
        self.setMinimumHeight(400)
        self.setMaximumWidth(150)

        wrapper_layout = QVBoxLayout()
        box = QGroupBox('Classes')
        self.layout = QVBoxLayout()
        wrapper_layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        box.setLayout(self.layout)
        wrapper_layout.addWidget(box)

        self.layout.addWidget(self.class_label)
        self._init_add_remove_buttons(self.layout)

        self.setLayout(wrapper_layout)

    def _init_add_remove_buttons(self, layout):
        box = QGroupBox()
        box.setMaximumHeight(50)

        layout.addWidget(box)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        box.setLayout(layout)

        add_button = QPushButton('+')
        remove_button = QPushButton('-')
        add_button.clicked.connect(self.trigger_add_class_dialog)
        remove_button.clicked.connect(lambda: self.remove_class(self.state.active_class))

        layout.addWidget(add_button)
        layout.addWidget(remove_button)

        return box

    def add_class(self, name: str):
        if name in self.classes.keys():
            return
        self.classes[name] = QRadioButton(name)
        add_class = self.classes[name]
        self.classes_group.addButton(add_class)
        self.layout.addWidget(add_class)
        self.state.classes.append(name)
        add_class.clicked.connect(lambda: self.set_active_class(name))

    def remove_class(self, name: str):
        if not name:
            return
        if self.state.active_class == name:
            self.set_active_class('')
        self.state.classes.remove(name)
        remove_class = self.classes[name]
        del self.classes[name]
        self.classes_group.removeButton(remove_class)
        self.layout.removeWidget(remove_class)
        remove_class.deleteLater()

    def trigger_add_class_dialog(self):
        new_class, ok = QInputDialog.getText(self, 'New Class', 'Enter the name of the new class:')
        if ok:
            self.add_class(new_class)
        self.state.display.source_label.setFocus()

    def set_active_class(self, name):
        self.class_label.setText('Current Class:  \n' + name)
        self.state.active_class = name
