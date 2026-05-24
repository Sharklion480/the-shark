# widgets/search_bar.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from utils.formatters import ar
from config.themes import theme_manager


class SearchBar(QWidget):

    textChanged = pyqtSignal(str)
    returnPressed = pyqtSignal(str)

    def __init__(self, placeholder="ابحث هنا...", parent=None):
        super().__init__(parent)

        self.placeholder = placeholder
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.input = QLineEdit()
        self.input.setPlaceholderText(ar(self.placeholder))
        self.input.setClearButtonEnabled(True)
        self.input.textChanged.connect(self.textChanged.emit)
        self.input.returnPressed.connect(lambda: self.returnPressed.emit(self.input.text()))

        icon = QLabel("🔍")
        icon.setContentsMargins(8,0,8,0)

        layout.addWidget(icon)
        layout.addWidget(self.input)

        self.setFixedHeight(40)
        self.setStyleSheet(f"""
            QLineEdit {{
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                padding-left: 40px;
                background-color: {theme_manager.get_color("surface")};
                border: 1px solid {theme_manager.get_color("border")};
                font-size: 14px;
            }}

            QLineEdit:focus {{
                border: 1px solid {theme_manager.get_color("primary")};
            }}

            QLabel {{
                font-size: 16px;
            }}
        """)

    def set_text(self, text):
        self.input.setText(text)

    def clear(self):
        self.input.clear()

    def get_text(self):
        return self.input.text().strip()