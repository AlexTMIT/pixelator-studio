from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal

from view.widgets.slider_factory import make_slider_block
from .bordered_box import BorderedBox

class SlidersWidget(BorderedBox):
    pixelAmountChanged = Signal(int)
    brightnessChanged = Signal(int)
    saturationChanged = Signal(int)
    contrastChanged = Signal(int)

    def __init__(self):
        super().__init__(400, 400, "sliders")

        self._add_slider_row("pixel amount", 0, 100, "pixelAmountSlider", self.pixelAmountChanged)
        self._add_slider_row("brightness", 0, 100, "brightnessSlider", self.brightnessChanged)
        self._add_slider_row("saturation", 0, 100, "saturationSlider", self.saturationChanged)
        self._add_slider_row("contrast", 0, 100, "contrastSlider", self.contrastChanged)

    def _make_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Minecraft", 14))
        label.setStyleSheet("color: #FBFFD9;")
        return label

    def _add_slider_row(self, label_text, minval, maxval, attr_name, signal):
        default = int((maxval-minval)/2)
        widget, slider = make_slider_block(label_text, default, minval, maxval)
        slider.valueChanged.connect(signal)
        setattr(self, attr_name, slider)
        self.body_layout.addWidget(widget)