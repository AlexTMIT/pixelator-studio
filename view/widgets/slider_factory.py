from PySide6.QtWidgets import QWidget, QLabel, QSlider, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

def make_label(text):
    label = QLabel(text)
    label.setFont(QFont("Minecraft", 12))
    label.setStyleSheet("color: #FBFFD9;")
    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    return label

def make_slider_block(label_text, default, min_value, max_value):
    layout = QGridLayout()
    layout.setContentsMargins(10, 14, 20, 24)
    layout.setHorizontalSpacing(20)
    layout.setVerticalSpacing(0)

    # Labels
    value_label = make_label("value")
    label = make_label(label_text)
    value_number = make_label(str(default))
    value_number.setFixedWidth(30)

    # Slider
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_value)
    slider.setMaximum(max_value)
    slider.setValue(default)
    slider.setMinimumWidth(180)
    slider.setMaximumWidth(250)
    slider.setStyleSheet("""
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

    slider.valueChanged.connect(lambda val: value_number.setText(str(val)))

    layout.addWidget(value_label,     0, 0)
    layout.addWidget(label,           0, 1)
    layout.addWidget(value_number, 1, 0, alignment=Qt.AlignVCenter)
    layout.addWidget(slider, 1, 1, alignment=Qt.AlignVCenter)

    container = QWidget()
    container.setLayout(layout)
    return container, slider