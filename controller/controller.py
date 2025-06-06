from PySide6.QtWidgets import QFileDialog
from PIL import Image

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
        self.model.pixel_amount = 50
        self.model.brightness = 50
        self.model.saturation = 50
        self.model.contrast = 50

        sliders = self.view.sliders
        sliders.pixelAmountSlider.setValue(50)
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
        brightened_image = self.edit_brightness(image)
        saturated_image = self.edit_saturation(image)
        # contrast_image = self.edit_contrast(image)

        self.model.image_edited = image
        self.view.preview.set_image(brightened_image)

    def edit_pixelation(self, image):
        value = self.model.pixel_amount
        pixel_size = max(1, value // 10)  # Ensure pixel size is at least 1
        return image

    def edit_brightness(self, image):
        raw_value = self.model.brightness

        if raw_value < 50:
            factor = raw_value / 50 
        else:
            factor = 1 + 4 * ((raw_value - 50) / 50) **2  # nonlinear brighten

        for y in range(image.height):
            for x in range(image.width):
                r, g, b = image.getpixel((x, y))
                r = max(0, min(255, int(r * factor)))
                g = max(0, min(255, int(g * factor)))
                b = max(0, min(255, int(b * factor)))
                image.putpixel((x, y), (r, g, b))

        return image
    
    def edit_saturation(self, image):
        value = self.model.saturation
        return image
