from PySide6.QtCore import Signal

from view.widgets.slider_factory import SliderBlock
from .bordered_box import BorderedBox

class SlidersWidget(BorderedBox):
    pixelAmountChanged = Signal(int)
    brightnessChanged = Signal(int)
    saturationChanged = Signal(int)
    contrastChanged = Signal(int)

    pixelAmountResetRequested = Signal()
    brightnessResetRequested = Signal()
    saturationResetRequested = Signal()
    contrastResetRequested = Signal()

    def __init__(self):
        super().__init__(400, 400, "sliders")
        self._add_slider_row("pixel amount", 0, 100, "pixelAmountSlider", self.pixelAmountChanged, self.pixelAmountResetRequested, 0)
        self._add_slider_row("brightness", 0, 100, "brightnessSlider", self.brightnessChanged, self.brightnessResetRequested)
        self._add_slider_row("saturation", 0, 100, "saturationSlider", self.saturationChanged, self.saturationResetRequested)
        self._add_slider_row("contrast", 0, 100, "contrastSlider", self.contrastChanged, self.contrastResetRequested)

    def _add_slider_row(self, label_text, minval, maxval, attr_name, change_signal, reset_signal, defaultval=50):
        block = SliderBlock(label_text, defaultval, minval, maxval)
        slider = block.get_slider()
        slider.valueChanged.connect(change_signal)
        slider.doubleClicked.connect(reset_signal)
        setattr(self, attr_name, slider)
        self.body_layout.addWidget(block)