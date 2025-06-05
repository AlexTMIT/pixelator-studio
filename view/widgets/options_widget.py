from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PySide6.QtCore import Qt

from .bordered_button import create_bordered_button

class OptionsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(400)
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        self.open_button = create_bordered_button("open")
        layout.addWidget(self.open_button)

        self.save_as_button = create_bordered_button("save as")
        self.save_as_button.setEnabled(False)
        layout.addWidget(self.save_as_button)

        exit_button = create_bordered_button("exit")
        exit_button.clicked.connect(QApplication.quit)
        layout.addWidget(exit_button)