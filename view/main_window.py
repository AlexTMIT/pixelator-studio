from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt
from .widgets.sliders_widget import SlidersWidget
from .widgets.colors_widget import ColorsWidget
from .widgets.preview_widget import PreviewWidget
from .widgets.options_widget import OptionsWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pixelator Studio")
        self.resize(1150, 900)
        self.setStyleSheet("background-color: #171514;")

        self.sliders = SlidersWidget()
        self.colors = ColorsWidget()
        self.preview = PreviewWidget()
        self.options = OptionsWidget()

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.setSpacing(40)
        grid.setContentsMargins(0, 0, 0, 0)

        grid.addWidget(self.sliders, 0, 0, alignment=Qt.AlignTop)
        grid.addWidget(self.colors, 1, 0, alignment=Qt.AlignTop)
        grid.addWidget(self.preview, 0, 1, alignment=Qt.AlignTop)
        grid.addWidget(self.options, 1, 1, alignment=Qt.AlignTop)

        grid_container = QWidget()
        grid_container.setLayout(grid)
        outer_layout.addWidget(grid_container, alignment=Qt.AlignCenter)