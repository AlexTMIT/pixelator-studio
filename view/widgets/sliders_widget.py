from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt, Signal
from .bordered_box import BorderedBox

class SlidersWidget(BorderedBox):
    pixelAmountChanged = Signal(int)
    brightnessChanged = Signal(int)
    saturationChanged = Signal(int)
    contrastChanged = Signal(int)

    def __init__(self):
        super().__init__(400, 400, "sliders")

        self.sliders = {}
        for name, signal in [("pixel amount", self.pixelAmountChanged),
                             ("brightness", self.brightnessChanged),
                             ("saturation", self.saturationChanged),
                             ("contrast", self.contrastChanged)]:
            label = QLabel(name)
            label.setStyleSheet("color: #FBFFD9; font-size: 16px; font-family: Minecraft")
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(50)
            slider.valueChanged.connect(signal)
            self.body_layout.addWidget(label)
            self.body_layout.addWidget(slider)