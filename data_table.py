# widgets/data_table.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from utils.formatters import ar
from config.themes import theme_manager


class DataTable(QTableWidget):

    rowDoubleClicked = pyqtSignal(int, object)
    rowClicked = pyqtSignal(int, object)

    def __init__(self, columns, parent=None):
        super().__init__(parent)

        self.columns = columns
        self.data = []
        self.selected_row_id = None

        self.setup_table()

    def setup_table(self):
        # الاعدادات الاساسية
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels([ar(col['title']) for col in self.columns])

        # السلوك
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setWordWrap(False)

        # ازالة الشبكة
        self.setShowGrid(False)

        # الراس الافقي
        header = self.horizontalHeader()
        header.setSectionsMovable(True)
        header.setStretchLastSection(True)

        # ضبط عرض الاعمدة
        for i, col in enumerate(self.columns):
            if 'width' in col:
                header.resizeSection(i, col['width'])
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        # اخفاء الراس العمودي
        self.verticalHeader().setVisible(False)

        # الارتفاع الافتراضي للصفوف
        self.verticalHeader().setDefaultSectionSize(38)

        # الاحداث
        self.cellDoubleClicked.connect(self.on_row_double_clicked)
        self.cellClicked.connect(self.on_row_clicked)

        # التنسيق
        self.apply_style()

    def apply_style(self):
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {theme_manager.get_color("surface")};
                border: 1px solid {theme_manager.get_color("border")};
                border-radius: 8px;
                gridline-color: {theme_manager.get_color("divider")};
                font-size: 13px;
            }}

            QTableWidget::item {{
                padding: 8px 12px;
                border: none;
            }}

            QTableWidget::item:selected {{
                background-color: {theme_manager.get_color("table_selected")};
                color: {theme_manager.get_color("text_primary")};
            }}

            QHeaderView::section {{
                background-color: {theme_manager.get_color("table_header")};
                padding: 10px 12px;
                border: none;
                border-right: 1px solid {theme_manager.get_color("divider")};
                border-bottom: 1px solid {theme_manager.get_color("border")};
                font-weight: 600;
                font-size: 13px;
            }}

            QHeaderView::section:hover {{
                background-color: {theme_manager.get_color("table_hover")};
            }}

            QTableCornerButton::section {{
                border: none;
                background-color: {theme_manager.get_color("table_header")};
            }}

            QScrollBar:vertical {{
                width: 10px;
            }}
        """)

    def set_data(self, data):
        """تعيين بيانات الجدول"""
        self.data = data
        self.clearContents()
        self.setRowCount(len(data))

        for row_index, row in enumerate(data):
            for col_index, col in enumerate(self.columns):
                key = col['key']
                value = row.get(key, "")

                # تنسيق القيمة اذا يوجد دالة تنسيق
                if 'formatter' in col:
                    value = col['formatter'](value)

                item = QTableWidgetItem(ar(str(value)))
                item.setData(Qt.UserRole, row.get('id'))

                # لون الحالة
                if 'color' in col and row.get(col['color']):
                    item.setForeground(QColor(row.get(col['color'])))

                self.setItem(row_index, col_index, item)

    def add_row(self, row_data):
        """اضافة صف جديد"""
        self.data.append(row_data)
        self.set_data(self.data)

    def update_row(self, row_id, new_data):
        """تحديث صف موجود"""
        for i, row in enumerate(self.data):
            if row.get('id') == row_id:
                self.data[i] = new_data
                break
        self.set_data(self.data)

    def delete_row(self, row_id):
        """حذف صف"""
        self.data = [row for row in self.data if row.get('id') != row_id]
        self.set_data(self.data)

    def clear(self):
        """تفريغ الجدول"""
        self.clearContents()
        self.setRowCount(0)
        self.data = []

    def get_selected_id(self):
        """الحصول على معرف الصف المحدد"""
        selected = self.selectedItems()
        if selected:
            return selected[0].data(Qt.UserRole)
        return None

    def on_row_double_clicked(self, row, col):
        row_id = self.item(row, 0).data(Qt.UserRole)
        self.rowDoubleClicked.emit(row_id, self.data[row])

    def on_row_clicked(self, row, col):
        row_id = self.item(row, 0).data(Qt.UserRole)
        self.rowClicked.emit(row_id, self.data[row])

    def refresh(self):
        """اعادة رسم الجدول عند تغيير الثيم"""
        self.apply_style()