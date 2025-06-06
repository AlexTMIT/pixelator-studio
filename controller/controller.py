# controller/controller.py
from PySide6.QtWidgets import QFileDialog
from PIL import Image
import colorsys
import numpy as np

from model.pixel_modes import PixelationMode

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.load_image("assets/default.png")
        self._connect_signals()

    def _connect_signals(self):
        sliders = self.view.sliders
        sliders.pixelAmountChanged.connect(lambda val: self._slider_changed("pixel_amount", val))
        sliders.brightnessChanged.connect(lambda val: self._slider_changed("brightness", val))
        sliders.saturationChanged.connect(lambda val: self._slider_changed("saturation", val))
        sliders.contrastChanged.connect(lambda val: self._slider_changed("contrast", val))

        # File‐open / save
        self.view.options.open_button.clicked.connect(self.open_image)
        self.view.options.save_as_button.clicked.connect(self.save_image)

        # ─── HOOK UP COLOR MODE / SCHEME ───────────────────────────────────────────────
        cw = self.view.colors
        cw.combo_mode.currentTextChanged.connect(self._color_mode_changed)
        cw.combo_scheme.currentTextChanged.connect(self._color_scheme_changed)
        # Initialize both combo states on startup:
        self._color_mode_changed(cw.combo_mode.currentText())

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

    def _slider_changed(self, name, value):
        self.model.update_slider(name, value)
        self.render_image()

    def _color_mode_changed(self, new_text: str):
        # 1) Update the enum in model
        key = new_text.replace(" ", "_").upper()  # e.g. "pythagorean color average" → "PYTHAGOREAN_COLOR_AVERAGE"
        try:
            self.model.pixel_mode = PixelationMode[key]
        except KeyError:
            # If it doesn't match exactly, just leave as None or log
            self.model.pixel_mode = None

        # 2) Enable/disable combo_scheme and update label color
        cw = self.view.colors
        if new_text == "schematic approximation":
            cw.combo_scheme.setEnabled(True)
            cw.label_scheme.setStyleSheet("color: #FBFFD9;")
        else:
            cw.combo_scheme.setEnabled(False)
            cw.label_scheme.setStyleSheet("color: #727363;")
            # Clear any previously chosen scheme if disabling
            self.model.color_scheme = None

        self.render_image()

    def _color_scheme_changed(self, scheme_text: str):
        # Only store when the combo is enabled
        if self.view.colors.combo_scheme.isEnabled():
            self.model.color_scheme = scheme_text
            self.render_image()

    def render_image(self):
        img = self.model.image.copy()
        if img is None:
            return

        # Pass in mode + scheme to edit_pixelation
        pixelated = self.edit_pixelation(img)
        bright = self.edit_brightness(pixelated)
        sat = self.edit_saturation(bright)
        contr = self.edit_contrast(sat)

        self.model.image_edited = contr
        self.view.preview.set_image(contr)

    def calculate_factor(self, raw_value):
        if raw_value < 50:
            return raw_value / 50
        else:
            return 1 + 4 * ((raw_value - 50) / 50) ** 2

    def edit_pixelation(self, image: Image.Image) -> Image.Image:
        mode = self.model.pixel_mode
        amount = self.model.pixel_amount or 0

        if amount == 0:
            return image

        match mode:
            case PixelationMode.PYTHAGOREAN_COLOR_AVERAGE:
                return self.pythagorean_color_average(amount, image)
            case PixelationMode.SCHEMATIC_APPROXIMATION:
                return self.schematic_approximation(amount, image)
            case PixelationMode.MEDIAN_COLOR:
                return self.median_color(amount, image)
            case _:
                return image

    def pythagorean_color_average(self, amount: int, image: Image.Image) -> Image.Image:
        return image
    
    def schematic_approximation(self, amount: int, image: Image.Image) -> Image.Image:
        scheme = self.model.color_scheme or "warm beige"
        return image
    
    def median_color(self, amount: int, image: Image.Image) -> Image.Image:
        return image

    def edit_brightness(self, image: Image.Image) -> Image.Image:
        factor = self.calculate_factor(self.model.brightness)
        arr = np.array(image, dtype=np.float32)
        arr *= factor
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)

    def edit_saturation(self, image: Image.Image) -> Image.Image:
        factor = self.calculate_factor(self.model.saturation)
        arr = np.array(image, dtype=np.float32) / 255.0
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

        hls = np.vectorize(colorsys.rgb_to_hls)(r, g, b)
        h, l, s = hls
        s = np.clip(s * factor, 0, 1)

        rgb = np.vectorize(colorsys.hls_to_rgb)(h, l, s)
        r2, g2, b2 = rgb
        out = np.stack([r2, g2, b2], axis=-1) * 255
        return Image.fromarray(out.astype(np.uint8))

    def edit_contrast(self, image: Image.Image) -> Image.Image:
        factor = self.calculate_factor(self.model.contrast)
        arr = np.array(image, dtype=np.float32)
        arr = 128 + (arr - 128) * factor
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)