# widgets/signature_pad.py
import base64
from io import BytesIO

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from config.themes import theme_manager
from utils.formatters import ar


class SignaturePad(QWidget):

    signatureChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.drawing = False
        self.last_point = QPoint()
        self.path = QPainterPath()

        self.setFixedHeight(200)

    def clear(self):
        """مسح التوقيع"""
        self.path = QPainterPath()
        self.drawing = False
        self.update()
        self.signatureChanged.emit()

    def is_empty(self):
        """التحقق اذا يوجد توقيع"""
        return self.path.isEmpty()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # الخلفية
        painter.fillRect(self.rect(), QColor(theme_manager.get_color("surface")))

        # الشبكة
        pen = QPen(QColor(theme_manager.get_color("border")), 1, Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(20, 160, self.width() - 20, 160)

        # التوقيع
        pen = QPen(QColor(theme_manager.get_color("text_primary")), 3)
        painter.setPen(pen)
        painter.drawPath(self.path)

        # نص تلميح
        if self.path.isEmpty():
            painter.setPen(QColor(theme_manager.get_color("text_secondary")))
            painter.drawText(self.rect(), Qt.AlignCenter, ar("ارسم التوقيع هنا"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.path.moveTo(self.last_point)

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.path.lineTo(event.pos())
            self.last_point = event.pos()
            self.update()

    def to_base64_png(self):
        """تصدير التوقيع كصورة PNG مشفرة base64"""
        if self.path.isEmpty():
            return ""
        image = QImage(self.size(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(theme_manager.get_color("text_primary")), 3)
        painter.setPen(pen)
        painter.drawPath(self.path)
        painter.end()
        buffer = BytesIO()
        image.save(buffer, "PNG")
        return base64.b64encode(buffer.getvalue()).decode("ascii")

    def mouseReleaseEvent(self, event):
        self.drawing = False
        self.signatureChanged.emit()