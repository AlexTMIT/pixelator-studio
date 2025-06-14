from model.pixel_modes import ColorScheme, PixelationMode
import numpy as np

class AppModel:
    def __init__(self):
        self.pixel_mode: PixelationMode = PixelationMode.SCHEMATIC_APPROXIMATION
        self.color_scheme: ColorScheme   = ColorScheme.first()

        self.pixel_amount: int = None
        self.brightness: int = None
        self.saturation: int = None
        self.contrast: int = None

        self.image = None
        self.image_edited = None

    def update_slider(self, name, value):
        setattr(self, name, value)
    
    def load_image(self, image):
        self.image = image
        self.image_edit = image
    
    def get_slider_values(self):
        return {
            "pixel_amount": self.pixel_amount,
            "brightness": self.brightness,
            "saturation": self.saturation,
            "contrast": self.contrast
        }