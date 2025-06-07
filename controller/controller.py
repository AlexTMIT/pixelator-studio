from PySide6.QtWidgets import QFileDialog
from PIL import Image

from model.pixel_modes import PixelationMode
from processing.image_processor import ImageProcessor

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.processor = ImageProcessor()
        self.load_image("assets/default.png")
        self._connect_signals()

    def _connect_signals(self):
        # Sliders
        sliders = self.view.sliders
        sliders.pixelAmountChanged.connect(lambda val: self._update_and_render("pixel_amount", val))
        sliders.brightnessChanged.connect(lambda val: self._update_and_render("brightness", val))
        sliders.saturationChanged.connect(lambda val: self._update_and_render("saturation", val))
        sliders.contrastChanged.connect(lambda val: self._update_and_render("contrast", val))

        # File‐open / save
        self.view.options.open_button.clicked.connect(self.open_image)
        self.view.options.save_as_button.clicked.connect(self.save_image)

        # Color mode and scheme
        self.view.colors.combo_mode.currentIndexChanged.connect(self._on_mode_changed)
        self.view.colors.combo_scheme.currentIndexChanged.connect(self._on_scheme_changed)

    def _update_and_render(self, name: str, val: int):
        self.model.update_slider(name, val)
        self.render_image()

    def _on_mode_changed(self, idx: int):
        mode = self.view.colors.combo_mode.itemData(idx)
        self.model.pixel_mode = mode
        self.view.colors.combo_scheme.setEnabled(mode == PixelationMode.SCHEMATIC_APPROXIMATION)
        self.render_image()

    def _on_scheme_changed(self, idx: int):
        if not self.view.colors.combo_scheme.isEnabled(): return
        scheme = self.view.colors.combo_scheme.itemData(idx)
        self.model.color_scheme = scheme
        self.render_image()

    def reset_parameters(self):
        self.model.pixel_amount = 0
        self.model.brightness = 50
        self.model.saturation = 50
        self.model.contrast = 50

        sliders = self.view.sliders
        sliders.pixelAmountSlider.setValue(0)
        sliders.brightnessSlider.setValue(50)
        sliders.saturationSlider.setValue(50)
        sliders.contrastSlider.setValue(50)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self.view, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if not path:
            return
        self.load_image(path)

    def load_image(self, path):
        image = Image.open(path).convert("RGB")
        resized = self.resize_to_fit(image, 400, 400)
        self.reset_parameters()
        self.view.options.save_as_button.setEnabled(True)
        self.model.load_image(resized)
        self.view.preview.set_image(resized)

    def save_image(self):
        image = self.model.image_edited
        if image is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self.view, "Save Image As", "", "JPEG (*.jpg);;PNG (*.png);;All Files (*)"
        )
        if not path:
            return

        ext = path.split('.')[-1].upper()
        fmt = "JPEG" if ext.lower() == "jpg" else ext
        try:
            image.save(path, fmt)
        except Exception as e:
            print(f"Failed to save image: {e}")

    def resize_to_fit(self, img: Image.Image, max_w=400, max_h=400) -> Image.Image:
        img.thumbnail((max_w, max_h), Image.LANCZOS)
        return img

    def render_image(self):
        img = self.model.image.copy()
        pm = self.model.pixel_mode
        amt = self.model.pixel_amount or 0

        img = self.processor.pixelate(pm, amt, img, self.model.color_scheme)
        img = self.processor.edit_brightness(img, self.model.brightness)
        img = self.processor.edit_saturation(img, self.model.saturation)
        img = self.processor.edit_contrast(img, self.model.contrast)

        self.model.image_edited = img
        self.view.preview.set_image(img)

    def calculate_factor(self, raw_value):
        if raw_value < 50:
            return raw_value / 50
        else:
            return 1 + 4 * ((raw_value - 50) / 50) ** 2