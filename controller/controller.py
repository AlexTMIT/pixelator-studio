class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        sliders = self.view.sliders
        sliders.pixelAmountChanged.connect(lambda val: self._slider_changed("pixel_amount", val))
        sliders.brightnessChanged.connect(lambda val: self._slider_changed("brightness", val))
        sliders.saturationChanged.connect(lambda val: self._slider_changed("saturation", val))
        sliders.contrastChanged.connect(lambda val: self._slider_changed("contrast", val))

    def _slider_changed(self, name, value):
        self.model.update_slider(name, value)
        print(f"{name} updated to {value}")