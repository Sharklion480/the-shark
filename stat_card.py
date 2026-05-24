# widgets/stat_card.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from utils.formatters import format_currency, format_number, ar
from config.themes import theme_manager


class StatCard(QFrame):

    clicked = pyqtSignal()

    def __init__(self, title, value, icon, color=None, is_currency=False, parent=None):
        super().__init__(parent)

        self.title = title
        self.value = value
        self.icon = icon
        self.color = color if color else theme_manager.get_color("primary")
        self.is_currency = is_currency

        self.setup_ui()
        self.setCursor(Qt.PointingHandCursor)

    def setup_ui(self):
        self.setObjectName("StatCard")
        self.setFixedHeight(110)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # الايقونة
        icon_label = QLabel(self.icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setObjectName("StatIcon")
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                color: {self.color};
            }}
        """)

        # النص
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)

        title_label = QLabel(ar(self.title))
        title_label.setObjectName("StatTitle")

        if self.is_currency:
            formatted_value = format_currency(self.value)
        else:
            formatted_value = format_number(self.value)

        value_label = QLabel(formatted_value)
        value_label.setObjectName("StatValue")

        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)

        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(icon_label)

        self.setStyleSheet(f"""
            #StatCard {{
                background-color: {theme_manager.get_color("surface")};
                border-radius: 12px;
                border: 1px solid {theme_manager.get_color("border")};
            }}

            #StatCard:hover {{
                border: 1px solid {self.color};
            }}

            #StatTitle {{
                font-size: 13px;
                color: {theme_manager.get_color("text_secondary")};
            }}

            #StatValue {{
                font-size: 26px;
                font-weight: 700;
                color: {theme_manager.get_color("text_primary")};
            }}
        """)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def update_value(self, new_value):
        self.value = new_value
        if self.is_currency:
            self.findChild(QLabel, "StatValue").setText(format_currency(new_value))
        else:
            self.findChild(QLabel, "StatValue").setText(format_number(new_value))