# views/settings_page.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from views.base_page import BasePage
from controllers.data_controller import data
from controllers.auth_controller import auth
from config.settings import Settings
from utils.formatters import ar


USER_COLUMNS = [
    {"key": "username", "title": "اسم المستخدم", "width": 120},
    {"key": "full_name", "title": "الاسم", "width": 160},
    {"key": "role", "title": "الدور", "width": 120},
    {"key": "email", "title": "البريد", "width": 160},
    {"key": "is_active", "title": "الحالة", "width": 80},
]

SETTING_COLUMNS = [
    {"key": "key", "title": "المفتاح", "width": 160},
    {"key": "value", "title": "القيمة", "width": 200},
    {"key": "category", "title": "التصنيف", "width": 100},
    {"key": "description", "title": "الوصف", "width": 220},
]


class SettingsPage(BasePage):

    def __init__(self, parent=None):
        super().__init__("الإعدادات", "إعدادات النظام والمستخدمين", parent)

        if not auth.has_permission("settings_manage"):
            self._layout.addWidget(self._denied())
            return

        tabs = QTabWidget()
        tabs.addTab(self._app_tab(), ar("التطبيق"))
        tabs.addTab(self._users_tab(), ar("المستخدمون"))
        tabs.addTab(self._system_tab(), ar("إعدادات النظام"))
        self._layout.addWidget(tabs, 1)
        self._tabs = tabs

    def _denied(self):
        lbl = QLabel(ar("ليس لديك صلاحية لإدارة الإعدادات"))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 16px; color: #e74c3c; padding: 40px;")
        return lbl

    def _app_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setAlignment(Qt.AlignTop)

        info = QLabel(
            ar(
                f"اسم التطبيق: {Settings.APP_NAME}\n"
                f"الإصدار: {Settings.APP_VERSION}\n"
                f"العملة: {Settings.get('currency', Settings.DEFAULT_CURRENCY)}\n"
                f"الثيم: {Settings.get('theme', Settings.DEFAULT_THEME)}"
            )
        )
        info.setWordWrap(True)
        info.setStyleSheet(
            "font-size: 14px; color: #334155; padding: 16px; "
            "background: #f8fafc; border-radius: 8px;"
        )
        layout.addWidget(info)
        layout.addStretch()
        return w

    def _users_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        table = DataTableWrapper(USER_COLUMNS, lambda _="": data.get_users())
        layout.addWidget(table)
        self._users_table = table
        return page

    def _system_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        table = DataTableWrapper(SETTING_COLUMNS, lambda _="": data.get_system_settings())
        layout.addWidget(table)
        self._settings_table = table
        return page

    def refresh(self):
        if hasattr(self, "_users_table"):
            self._users_table.reload_data()
        if hasattr(self, "_settings_table"):
            self._settings_table.reload_data()


class DataTableWrapper(QWidget):
    """غلاف بسيط لجدول بدون بحث"""

    def __init__(self, columns, fetch_data, parent=None):
        super().__init__(parent)
        from widgets.data_table import DataTable

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.table = DataTable(columns)
        layout.addWidget(self.table)
        self.fetch_data = fetch_data
        self.reload_data()

    def reload_data(self, search=""):
        self.table.set_data(self.fetch_data(search))
