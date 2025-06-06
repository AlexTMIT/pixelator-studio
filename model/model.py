class AppModel:
    def __init__(self):
        self.pixel_amount = 50
        self.brightness = 50
        self.saturation = 50
        self.contrast = 50
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