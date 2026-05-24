# widgets/date_picker_hijri.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from hijri_converter import convert

from utils.formatters import ar, format_date


class DatePickerHijri(QWidget):

    dateChanged = pyqtSignal(QDate)

    HIJRI_MONTHS = [
        "محرم", "صفر", "ربيع الأول", "ربيع الثاني", "جمادى الأولى", "جمادى الثانية",
        "رجب", "شعبان", "رمضان", "شوال", "ذو القعدة", "ذو الحجة"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mode = "gregorian"
        self.selected_date = QDate.currentDate()

        self.setup_ui()
        self.update_date()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)

        self.toggle_btn = QPushButton("🌙")
        self.toggle_btn.setFixedSize(32,32)
        self.toggle_btn.clicked.connect(self.toggle_mode)

        self.picker_btn = QPushButton("📅")
        self.picker_btn.setFixedSize(32,32)
        self.picker_btn.clicked.connect(self.open_picker)

        layout.addWidget(self.date_label)
        layout.addStretch()
        layout.addWidget(self.toggle_btn)
        layout.addWidget(self.picker_btn)

    def toggle_mode(self):
        """التبديل بين الهجري والميلادي"""
        self.mode = "hijri" if self.mode == "gregorian" else "gregorian"
        self.update_date()

    def update_date(self):
        """تحديث عرض التاريخ"""
        d = self.selected_date

        if self.mode == "gregorian":
            text = format_date(d.toPyDate())
        else:
            hijri = convert.Gregorian(d.year(), d.month(), d.day()).to_hijri()
            text = ar(f"{hijri.day} {self.HIJRI_MONTHS[hijri.month -1]} {hijri.year} هـ")

        self.date_label.setText(text)

    def open_picker(self):
        """فتح منتقي التاريخ"""
        dialog = QDialog(self)
        dialog.setWindowTitle(ar("اختر التاريخ"))
        layout = QVBoxLayout(dialog)

        date_edit = QDateEdit(dialog)
        date_edit.setCalendarPopup(True)
        date_edit.setDate(self.selected_date)
        layout.addWidget(date_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            dialog,
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            self.selected_date = date_edit.date()
            self.update_date()
            self.dateChanged.emit(self.selected_date)

    def get_date(self):
        return self.selected_date.toPyDate()

    def set_date(self, date):
        if isinstance(date, QDate):
            self.selected_date = date
        else:
            self.selected_date = QDate(date.year, date.month, date.day)
        self.update_date()