from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class BorderedBox(QFrame):
    def __init__(self, width, height, title=""):
        super().__init__()
        self.setFixedSize(width, height)
        self.setObjectName("borderedBox")
        self.setStyleSheet("""
            QFrame#borderedBox {
                border: 3px solid #FBFFD9;
                background-color: #171514;
            }
        """)

        layout = QVBoxLayout(self)

        titleLabel = QLabel(title)
        titleLabel.setFont(QFont("Minecraft", 35))
        titleLabel.setStyleSheet("color: #FBFFD9;")
        titleLabel.setContentsMargins(0, 20, 0, 0)
        layout.addWidget(titleLabel, alignment=Qt.AlignTop | Qt.AlignCenter)

        self.body_layout = layout