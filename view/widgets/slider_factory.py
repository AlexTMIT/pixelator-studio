from PySide6.QtWidgets import QWidget, QLabel, QSlider, QGridLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class Slider(QSlider):
    doubleClicked = Signal()

    def __init__(self, default, min_value, max_value):
        super().__init__(Qt.Horizontal)
        self._default_value = default
        self.setMinimum(min_value)
        self.setMaximum(max_value)
        self.setValue(default)
        self.setMinimumWidth(180)
        self.setMaximumWidth(250)
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 2px;
                background: #FBFFD9;
            }
            QSlider::handle:horizontal {
                background: #FBFFD9;
                border: none;
                width: 10px;
                height: 10px;
                margin: -4px 0;
                border-radius: 0px;
            }
            QSlider::sub-page:horizontal {
                background: #FBFFD9;
            }
            QSlider::add-page:horizontal {
                background: #FBFFD9;
            }
        """)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.doubleClicked.emit()

    @property
    def default_value(self):
        return self._default_value


class SliderBlock(QWidget):
    def __init__(self, label_text: str, default: int, min_value: int, max_value: int):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(10, 14, 20, 24)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(0)

        value_label = make_label("value")
        label = make_label(label_text)
        self.value_number = make_label(str(default))
        self.value_number.setFixedWidth(30)

        self.slider = Slider(default, min_value, max_value)
        self.slider.valueChanged.connect(self._on_value_changed)

        layout.addWidget(value_label,     0, 0)
        layout.addWidget(label,           0, 1)
        layout.addWidget(self.value_number, 1, 0, alignment=Qt.AlignVCenter)
        layout.addWidget(self.slider,     1, 1, alignment=Qt.AlignVCenter)

        self.setLayout(layout)

    def _on_value_changed(self, val):
        self.value_number.setText(str(val))

    def get_slider(self):
        return self.slider
    
def make_label(text):
    label = QLabel(text)
    label.setFont(QFont("Minecraft", 12))
    label.setStyleSheet("color: #FBFFD9;")
    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    return label