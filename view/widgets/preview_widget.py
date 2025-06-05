from .bordered_box import BorderedBox

class PreviewWidget(BorderedBox):
    def __init__(self):
        super().__init__(400, 400)
        # No title