# views/main_window.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from views.sidebar import Sidebar
from views.page_factory import create_app_page
from controllers.auth_controller import auth
from utils.formatters import ar
from config.settings import Settings


class MainWindow(QMainWindow):

    PAGE_TITLES = {
        'dashboard': 'لوحة التحكم',
        'properties': 'العقارات',
        'clients': 'العملاء',
        'sales': 'المبيعات',
        'rentals': 'الإيجارات',
        'contracts': 'العقود',
        'reports': 'التقارير',
        'notifications': 'الإشعارات',
        'settings': 'الإعدادات',
    }

    def __init__(self):
        super().__init__()
        self.logout_requested = False
        self.pages = {}
        self.toolbar_search = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(ar(Settings.APP_NAME))
        self.resize(1400, 900)
        self.showMaximized()

        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: white;')
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.create_toolbar())

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.menu_item_clicked.connect(self.navigate)
        self.sidebar.logout_requested.connect(self.on_logout)

        self.content_stack = QStackedWidget()

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.content_stack, 1)

        main_layout.addLayout(content_layout)

        self.navigate('dashboard')

    def navigate(self, menu_id):
        if menu_id not in self.PAGE_TITLES:
            return

        self.sidebar.set_active_item(menu_id)

        if menu_id not in self.pages:
            self.pages[menu_id] = create_app_page(menu_id)
            self.content_stack.addWidget(self.pages[menu_id])

        page = self.pages[menu_id]
        self.content_stack.setCurrentWidget(page)
        if hasattr(page, 'refresh'):
            page.refresh()

    def current_page(self):
        widget = self.content_stack.currentWidget()
        return widget

    def refresh_current_page(self):
        page = self.current_page()
        if page and hasattr(page, 'refresh'):
            page.refresh()

    def filter_current_page(self, text):
        page = self.current_page()
        if page and hasattr(page, 'filter_text'):
            page.filter_text(text)
        elif page and hasattr(page, 'reload_data'):
            page.reload_data(text)

    def create_toolbar(self):
        toolbar = QWidget()
        toolbar.setStyleSheet(
            'background-color: #f8fafc; border-bottom: 1px solid #e2e8f0;'
        )
        toolbar.setFixedHeight(50)

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)

        home_btn = QPushButton('🏠 ' + ar('الصفحة الرئيسية'))
        home_btn.setCursor(Qt.PointingHandCursor)
        home_btn.clicked.connect(lambda: self.navigate('dashboard'))
        home_btn.setStyleSheet(
            'border: none; padding: 8px 12px; border-radius: 4px; '
            'background-color: transparent; font-size: 12px;'
        )
        layout.addWidget(home_btn)

        refresh_btn = QPushButton('🔄 ' + ar('تحديث'))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_current_page)
        refresh_btn.setStyleSheet(home_btn.styleSheet())
        layout.addWidget(refresh_btn)

        layout.addStretch()

        self.toolbar_search = QLineEdit()
        self.toolbar_search.setPlaceholderText(ar('بحث...'))
        self.toolbar_search.setMaximumWidth(220)
        self.toolbar_search.textChanged.connect(self.filter_current_page)
        self.toolbar_search.setStyleSheet(
            'border: 1px solid #cbd5e1; border-radius: 4px; '
            'padding: 6px 10px; font-size: 12px;'
        )
        layout.addWidget(self.toolbar_search)

        add_btn = QPushButton('➕ ' + ar('إضافة'))
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.on_add_clicked)
        add_btn.setStyleSheet(
            'border: none; padding: 8px 12px; border-radius: 4px; '
            'background-color: #1976D2; color: white; font-size: 12px; font-weight: 600;'
        )
        layout.addWidget(add_btn)

        settings_btn = QPushButton('⚙️ ' + ar('إعدادات'))
        settings_btn.setCursor(Qt.PointingHandCursor)
        settings_btn.clicked.connect(lambda: self.navigate('settings'))
        settings_btn.setStyleSheet(home_btn.styleSheet())
        layout.addWidget(settings_btn)

        return toolbar

    def on_add_clicked(self):
        page = self.current_page()
        if page and hasattr(page, "show_add_dialog"):
            page.show_add_dialog()
            return
        title = self.PAGE_TITLES.get(self.sidebar.active_item, "")
        QMessageBox.information(
            self,
            ar("إضافة"),
            ar(f"لا تتوفر إضافة سجلات في صفحة {title}."),
        )

    def on_logout(self):
        self.logout_requested = True
        self.close()

    def closeEvent(self, event):
        if self.logout_requested:
            event.accept()
            return

        reply = QMessageBox.question(
            self,
            ar('خروج'),
            ar('هل أنت متأكد من الخروج من البرنامج؟'),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
