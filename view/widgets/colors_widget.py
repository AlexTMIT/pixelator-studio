from PySide6.QtWidgets import QLabel, QComboBox, QWidget, QGridLayout, QSizePolicy
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
        label_mode = QLabel("color mode:")
        label_mode.setFont(QFont("Minecraft", 12))
        label_mode.setStyleSheet("color: #FBFFD9;")
        grid.addWidget(label_mode, 0, 0, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        combo_mode = QComboBox()
        combo_mode.setFont(QFont("Minecraft", 12))
        combo_mode.setCursor(Qt.PointingHandCursor)
        combo_mode.setStyleSheet("""
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
            }
            QComboBox QAbstractItemView {
                background-color: #171514;
                color: #FBFFD9;
                selection-background-color: #FBFFD9;
                selection-color: #171514;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #FBFFD9;
                color: #171514;
            }
        """)
        # Populate with PixelationMode enum values (readable form)
        for mode in PixelationMode:
            combo_mode.addItem(mode.name.lower().replace("_", " "))
        combo_mode.setCurrentText("pythagorean color average")
        grid.addWidget(combo_mode, 0, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        # ─── Row 1: “color scheme:” label + (disabled) combo box ──────────────────────
        label_scheme = QLabel("color scheme:")
        label_scheme.setFont(QFont("Minecraft", 12))
        # Faded-out color for disabled label
        label_scheme.setStyleSheet("color: #727363;")
        grid.addWidget(label_scheme, 1, 0, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        combo_scheme = QComboBox()
        combo_scheme.setFont(QFont("Minecraft", 12))
        combo_scheme.setCursor(Qt.PointingHandCursor)
        combo_scheme.setStyleSheet("""
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
        combo_scheme.addItems([
            "warm beige",
            "cool gray",
            "vibrant sunset",
            "pastel mint"
        ])
        combo_scheme.setCurrentText("warm beige")
        # Disable so it appears greyed out
        combo_scheme.setEnabled(False)
        grid.addWidget(combo_scheme, 1, 1, alignment=Qt.AlignVCenter | Qt.AlignLeft)

        # ─── Insert the grid into a container and add it to the body_layout ───────────
        container = QWidget()
        container.setLayout(grid)

        spacer = QWidget()
        spacer.setFixedHeight(20)

        self.body_layout.addWidget(container)
        self.body_layout.addWidget(spacer)  # Spacer