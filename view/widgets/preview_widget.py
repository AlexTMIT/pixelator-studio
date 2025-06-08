from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QImage, QCursor
from PySide6.QtCore import Qt, Signal
from PIL.ImageQt import ImageQt

class PreviewWidget(QLabel):
    clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 400)
        self.setStyleSheet("border: 3px solid #FBFFD9; background-color: #171514;")
        self.setAlignment(Qt.AlignCenter)

    def set_image(self, pil_image):
        qt_image = ImageQt(pil_image)
        pixmap = QPixmap.fromImage(QImage(qt_image))
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event):
        self.unsetCursor()