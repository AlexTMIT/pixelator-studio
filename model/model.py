class AppModel:
    def __init__(self):
        self.pixel_amount = 14
        self.brightness = 48
        self.saturation = 59
        self.contrast = 28
        self.image = None
    
    def update_slider(self, name, value):
        setattr(self, name, value)
    
    def load_image(self, image):
        self.image = image
    
    def get_slider_values(self):
        return {
            "pixel_amount": self.pixel_amount,
            "brightness": self.brightness,
            "saturation": self.saturation,
            "contrast": self.contrast
        }