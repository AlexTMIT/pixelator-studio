from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from .bordered_button import create_bordered_button

class OptionsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(400)  # ✅ Enforce full width
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)  # ✅ Remove any default padding

        layout.addWidget(create_bordered_button("open"))
        layout.addWidget(create_bordered_button("save as"))
        layout.addWidget(create_bordered_button("exit"))