# widgets/image_gallery.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from config.settings import Settings
from config.themes import theme_manager


class ImageGallery(QScrollArea):

    imageDeleted = pyqtSignal(str)
    primaryChanged = pyqtSignal(str)
    imagesReordered = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.images = []
        self.setup_ui()

    def setup_ui(self):
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setSpacing(12)
        self.grid_layout.setAlignment(Qt.AlignTop)

        self.setWidget(container)

    def add_image(self, filename, is_primary=False):
        """اضافة صورة للمعرض"""

        card = QFrame()
        card.setObjectName("ImageCard")
        card.setFixedSize(160, 160)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(4,4,4,4)

        # الصورة
        thumb_path = Settings.PROPERTIES_IMAGES_DIR / f"thumb_{filename}"
        full_path = Settings.PROPERTIES_IMAGES_DIR / filename
        load_path = thumb_path if thumb_path.exists() else full_path
        pixmap = QPixmap(str(load_path))
        if pixmap.isNull():
            pixmap = QPixmap(150, 150)
            pixmap.fill(QColor(theme_manager.get_color("border")))
        else:
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        img_label = QLabel()
        img_label.setPixmap(pixmap)
        img_label.setAlignment(Qt.AlignCenter)

        # ازرار التحكم
        buttons_layout = QHBoxLayout()

        primary_btn = QCheckBox("⭐")
        primary_btn.setChecked(is_primary)
        primary_btn.setToolTip("صورة رئيسية")
        primary_btn.clicked.connect(lambda: self.primaryChanged.emit(filename))

        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(24,24)
        delete_btn.clicked.connect(lambda: self.imageDeleted.emit(filename))

        buttons_layout.addWidget(primary_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(delete_btn)

        layout.addWidget(img_label)
        layout.addLayout(buttons_layout)

        self.grid_layout.addWidget(card, len(self.images) // 4, len(self.images) % 4)
        self.images.append(filename)

        card.setStyleSheet(f"""
            #ImageCard {{
                background-color: {theme_manager.get_color("surface")};
                border-radius: 8px;
                border: 1px solid {theme_manager.get_color("border")};
            }}
            QPushButton {{
                border: none;
                background-color: transparent;
                font-size: 16px;
            }}
        """)

    def set_images(self, images_list):
        """تعيين قائمة الصور"""
        self.clear()
        for img in images_list:
            self.add_image(img['filename'], img['is_primary'])

    def clear(self):
        """تفريغ المعرض"""
        while self.grid_layout.count() > 0:
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.images = []