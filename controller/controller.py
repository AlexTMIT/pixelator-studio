from PySide6.QtWidgets import QFileDialog
from PIL import Image
import colorsys
import numpy as np

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()

        self.load_image("assets/default.png")

    def _connect_signals(self):
        sliders = self.view.sliders
        sliders.pixelAmountChanged.connect(lambda val: self._slider_changed("pixel_amount", val))
        sliders.brightnessChanged.connect(lambda val: self._slider_changed("brightness", val))
        sliders.saturationChanged.connect(lambda val: self._slider_changed("saturation", val))
        sliders.contrastChanged.connect(lambda val: self._slider_changed("contrast", val))

        self.view.options.open_button.clicked.connect(self.open_image)
        self.view.options.save_as_button.clicked.connect(self.save_image)

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
        path, _ = QFileDialog.getOpenFileName(self.view, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
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
        format = "JPEG" if ext.lower() == "jpg" else ext

        try:
            image.save(path, format)
        except Exception as e:
            print(f"Failed to save image: {e}")

    def resize_to_fit(self, img: Image.Image, max_w=400, max_h=400) -> Image.Image:
        img.thumbnail((max_w, max_h), Image.LANCZOS)
        return img

    def _slider_changed(self, name, value):
        self.model.update_slider(name, value)
        self.render_image()

    def render_image(self):
        image = self.model.image.copy()
        if image is None:
            return
        
        pixelated_image = self.edit_pixelation(image)
        brightened_image = self.edit_brightness(pixelated_image)
        saturated_image = self.edit_saturation(brightened_image)
        contrasted_image = self.edit_contrast(saturated_image)

        self.model.image_edited = contrasted_image
        self.view.preview.set_image(contrasted_image)

    def calculate_factor(self, raw_value):
        if raw_value < 50:
            return raw_value / 50 
        else:
            return 1 + 4 * ((raw_value - 50) / 50) ** 2

    def edit_pixelation(self, image):
        value = self.model.pixel_amount

        # if value=0, don't pixelate
        # if value=1, radius=1
        # if value=100, make final image 4 pixels
        # since image is 400x400, that means radius is = to value?
        
        #radius = 

        return image

    def edit_brightness(self, image):
        factor = self.calculate_factor(self.model.brightness)
        arr = np.array(image, dtype=np.float32)
        arr *= factor
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)
    
    def edit_saturation(self, image):
        factor = self.calculate_factor(self.model.saturation)
        arr = np.array(image, dtype=np.float32) / 255.0 # convert between 0 and 1
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2] # extract rgb

        hls = np.vectorize(colorsys.rgb_to_hls)(r, g, b)
        h, l, s = hls

        s = np.clip(s * factor, 0, 1) # adjust saturation

        rgb = np.vectorize(colorsys.hls_to_rgb)(h, l, s)
        r, g, b = rgb
        out = np.stack([r, g, b], axis=-1) * 255
        return Image.fromarray(out.astype(np.uint8))

    def edit_contrast(self, image):
        factor = self.calculate_factor(self.model.contrast)
        arr = np.array(image, dtype=np.float32)
        arr = 128 + (arr - 128) * factor
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)