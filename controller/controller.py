from PySide6.QtWidgets import QFileDialog
from PIL import Image

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        sliders = self.view.sliders
        sliders.pixelAmountChanged.connect(lambda val: self.model.update_slider("pixel_amount", val))
        sliders.pixelAmountChanged.connect(lambda val: self.model.update_slider("brightness", val))
        sliders.pixelAmountChanged.connect(lambda val: self.model.update_slider("saturation", val))
        sliders.pixelAmountChanged.connect(lambda val: self.model.update_slider("contrast", val))

        self.view.options.open_button.clicked.connect(self.open_image)
        self.view.options.save_as_button.clicked.connect(self.save_image)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(self.view, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return

        image = Image.open(path).convert("RGB")
        resized = self.resize_to_fit(image, 400, 400)
        self.view.options.save_as_button.setEnabled(True)
        self.model.load_image(resized)
        self.view.preview.set_image(resized)

    def save_image(self):
        image = self.model.image
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