from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

def create_bordered_button(text):
    button = QPushButton(text)
    button.setFixedSize(400, 70)
    button.setFont(QFont("Minecraft", 25)) 
    button.setCursor(Qt.PointingHandCursor)

    button.setStyleSheet("""
        QPushButton {
            border: 3px solid #FBFFD9;
            color: #FBFFD9;
            background-color: #171514;
        }
        QPushButton:hover {
            background-color: #FBFFD9;
            color: #171514;
        }
            QPushButton:disabled {
            border: 3px solid #727363;
            color: #727363;
            background-color: #171514;
        }
     """)
    
    return button