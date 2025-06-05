from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont

def create_bordered_button(text):
    button = QPushButton(text)
    button.setFixedSize(400, 70)
    button.setFont(QFont("Minecraft", 25)) 
    button.setStyleSheet("""
        QPushButton {
            border: 3px solid #FBFFD9;
            border-radius: 3px;
            color: #FBFFD9;
            background-color: #171514;
        }
        QPushButton:hover {
            background-color: #FBFFD9;
            color: #171514;
        }
    """)
    
    return button