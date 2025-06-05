import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

def create_bordered_vbox(width, height, title):
    container = QWidget()
    container.setFixedSize(width, height)

    container.setObjectName("borderedBox")
    container.setStyleSheet(f"""
        QWidget#borderedBox {{
            border: 3px solid "#FBFFD9";
            border-radius: 3px;
        }}
    """)

    titleLabel = QLabel(title)
    titleLabel.setFont(QFont("Minecraft", 40))
    titleLabel.setStyleSheet("color: #FBFFD9;")
    titleLabel.setContentsMargins(0, 30, 0, 0)

    layout = QVBoxLayout(container)
    layout.addWidget(titleLabel, alignment=Qt.AlignTop | Qt.AlignCenter)

    
    return container

def makeLeft():
    container = QWidget()
    layout = QVBoxLayout(container)

    slidersWidget = create_bordered_vbox(400, 400, "sliders")
    colorsWidget = create_bordered_vbox(400, 250, "colors")
    layout.addWidget(slidersWidget)
    layout.addWidget(colorsWidget)

    return container

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pixelator Studio")
        self.resize(1150, 900)
        self.setStyleSheet("background-color: #171514;")  
        
        layout = QHBoxLayout()

        layout.addWidget(makeLeft())
        layout.addWidget(makeLeft())

        self.setLayout(layout)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
