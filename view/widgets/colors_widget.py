from PySide6.QtWidgets import QLabel, QComboBox, QWidget, QGridLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from model.pixel_modes import ColorScheme, PixelationMode
from .bordered_box import BorderedBox

class ColorsWidget(BorderedBox):
    def __init__(self):
        super().__init__(400, 250, "colors")

        grid = self.make_grid()

        # color mode
        self.label_mode = self.make_label_mode()
        grid.addWidget(self.label_mode, 0, 0, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.combo_mode = self.make_combo_mode()
        grid.addWidget(self.combo_mode, 0, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        grid.addWidget(self.make_spacer(), 0, 2)

        # color scheme
        self.label_scheme = self.make_label_scheme()
        grid.addWidget(self.label_scheme, 1, 0, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.combo_scheme = self.make_combo_scheme()
        grid.addWidget(self.combo_scheme, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        grid.addWidget(self.make_spacer(), 1, 2)

        container = QWidget()
        container.setLayout(grid)

        self.body_layout.addWidget(container)
        self.body_layout.addWidget(self.make_spacer(width=0, height=30))

    def make_grid(self):
        grid = QGridLayout()
        grid.setContentsMargins(22, 0, 20, 14)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(14)
        return grid
    
    def make_label_mode(self):
        label_mode = QLabel("color mode:")
        label_mode.setFont(QFont("Minecraft", 12))
        label_mode.setStyleSheet("color: #FBFFD9;")
        return label_mode
    
    def make_combo_mode(self):
        combo_mode = QComboBox()
        combo_mode.setFont(QFont("Minecraft", 12))
        combo_mode.setCursor(Qt.PointingHandCursor)
        combo_mode.setStyleSheet(self.mode_style())
        for mode in PixelationMode:
            combo_mode.addItem(mode.name.lower().replace("_", " "), mode)
        return combo_mode
    
    def make_spacer(self, width=20, height=0):
        spacer = QWidget()
        spacer.setFixedWidth(width)
        spacer.setFixedHeight(height)
        return spacer

    def make_label_scheme(self):
        label_scheme = QLabel("color scheme:")
        label_scheme.setFont(QFont("Minecraft", 12))
        label_scheme.setStyleSheet("color: #FBFFD9;")
        return label_scheme
    
    def set_enabled_scheme(self, enabled: bool):
        if enabled:
            self.label_scheme.setStyleSheet("color: #FBFFD9;")
            self.combo_scheme.setEnabled(True)
        else:
            self.label_scheme.setStyleSheet("color: #727363;")
            self.combo_scheme.setEnabled(False)

    def make_combo_scheme(self):
        combo_scheme = QComboBox()
        combo_scheme.setFont(QFont("Minecraft", 12))
        combo_scheme.setCursor(Qt.PointingHandCursor)
        combo_scheme.setStyleSheet(self.scheme_style())
        for scheme in ColorScheme:
            combo_scheme.addItem(scheme.value, scheme)
        combo_scheme.setCurrentText(ColorScheme.first().value)
        return combo_scheme

    def mode_style(self):
        return """
            QComboBox {
                border: 1px solid #FBFFD9;
                color: #FBFFD9;
                background-color: #171514;
                padding: 4px;
            }
            QComboBox:hover {
                background-color: #FBFFD9;
                color: #171514;
            }
            QComboBox::drop-down {
                border: none;
                border-radius: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #171514;
                color: #FBFFD9;
                selection-background-color: #FBFFD9;
                selection-color: #171514;
                min-width: 200px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #FBFFD9;
                color: #171514;
            }
        """

    def scheme_style(self):
        return """
            QComboBox {
                border: 1px solid #FBFFD9;
                color: #FBFFD9;
                background-color: #171514;
                padding: 4px;
            }
            QComboBox:hover:!disabled {
                background-color: #FBFFD9;
                color: #171514;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #171514;
                color: #FBFFD9;
                selection-background-color: #FBFFD9;
                selection-color: #171514;
                min-width: 130px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #FBFFD9;
                color: #171514;
            }
            /* Disabled state */
            QComboBox:disabled {
                border: 1px solid #727363;
                color: #727363;
                background-color: #171514;
            }
        """