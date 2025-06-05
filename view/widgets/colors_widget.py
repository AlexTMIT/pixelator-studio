from .bordered_box import BorderedBox

class ColorsWidget(BorderedBox):
    def __init__(self):
        super().__init__(400, 250, "colors")
        # Populate later