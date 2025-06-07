from PySide6.QtWidgets import QLabel, QComboBox, QWidget, QGridLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from model.pixel_modes import PixelationMode
from .bordered_box import BorderedBox

class ColorsWidget(BorderedBox):
    def __init__(self):
        super().__init__(400, 250, "colors")

        grid = QGridLayout()
        grid.setContentsMargins(22, 0, 20, 14)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(14)

        # ─── Row 0: “color mode:” label + combo box ──────────────────────────────────
        self.label_mode = QLabel("color mode:")
        self.label_mode.setFont(QFont("Minecraft", 12))
        self.label_mode.setStyleSheet("color: #FBFFD9;")
        grid.addWidget(self.label_mode, 0, 0, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        self.combo_mode = QComboBox()
        self.combo_mode.setFont(QFont("Minecraft", 12))
        self.combo_mode.setCursor(Qt.PointingHandCursor)
        self.combo_mode.setStyleSheet("""
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
        """)
        for mode in PixelationMode:
            self.combo_mode.addItem(mode.name.lower().replace("_", " "))
        self.combo_mode.setCurrentText("schematic approximation")
        grid.addWidget(self.combo_mode, 0, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        spacer = QWidget()
        spacer.setFixedWidth(20)
        grid.addWidget(spacer, 0, 2)

        # ─── Row 1: “color scheme:” label + (disabled) combo box ──────────────────────
        self.label_scheme = QLabel("color scheme:")
        self.label_scheme.setFont(QFont("Minecraft", 12))
        self.label_scheme.setStyleSheet("color: #727363;")  # greyed‐out initially
        grid.addWidget(self.label_scheme, 1, 0, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        self.combo_scheme = QComboBox()
        self.combo_scheme.setFont(QFont("Minecraft", 12))
        self.combo_scheme.setCursor(Qt.PointingHandCursor)
        self.combo_scheme.setStyleSheet("""
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
        """)
        self.combo_scheme.addItems([
            "warm beige",
            "cool gray",
            "vibrant sunset",
            "pastel mint"
        ])
        self.combo_scheme.setCurrentText("warm beige")
        self.combo_scheme.setEnabled(False)  # greyed‐out by default
        grid.addWidget(self.combo_scheme, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        grid.addWidget(spacer, 1, 2)

        container = QWidget()
        container.setLayout(grid)

        spacer2 = QWidget()
        spacer2.setFixedHeight(20)

        self.body_layout.addWidget(container)
        self.body_layout.addWidget(spacer2)