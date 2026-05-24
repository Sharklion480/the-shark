# views/sidebar.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5.QtCore as QtCore

from controllers.auth_controller import auth
from utils.formatters import ar
from config.settings import Settings
from config.themes import theme_manager


class Sidebar(QWidget):

    menu_item_clicked = pyqtSignal(str)
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.active_item = 'dashboard'
        self.setup_ui()

    menu_items = [
        {'id': 'dashboard', 'icon': '📊', 'title': 'لوحة التحكم', 'permission': None},
        {'id': 'properties', 'icon': '🏠', 'title': 'العقارات', 'permission': 'properties_view'},
        {'id': 'clients', 'icon': '👥', 'title': 'العملاء', 'permission': 'clients_view'},
        {'id': 'sales', 'icon': '💰', 'title': 'المبيعات', 'permission': 'sales_view'},
        {'id': 'rentals', 'icon': '📅', 'title': 'الإيجارات', 'permission': 'rentals_view'},
        {'id': 'contracts', 'icon': '📋', 'title': 'العقود', 'permission': 'contracts_view'},
        {'id': 'reports', 'icon': '📄', 'title': 'التقارير', 'permission': 'reports_view'},
        {'id': 'notifications', 'icon': '🔔', 'title': 'الإشعارات', 'permission': None},
        {'id': 'settings', 'icon': '⚙️', 'title': 'الإعدادات', 'permission': 'settings_manage'},
    ]

    def setup_ui(self):
        self.setFixedWidth(280)
        self.setObjectName("Sidebar")
        self.setStyleSheet(f"""
            #Sidebar {{
                background-color: {theme_manager.get_color("sidebar")};
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # رأس القائمة
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20,20,20,20)

        logo = QLabel("🏢")
        logo.setStyleSheet("font-size: 32px;")

        app_name = QLabel(ar(Settings.APP_NAME))
        app_name.setObjectName("SidebarTitle")

        header_layout.addWidget(logo)
        header_layout.addWidget(app_name)
        header_layout.addStretch()

        layout.addWidget(header)

        # الفاصل
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addWidget(line)
        layout.addSpacing(10)

        # عناصر القائمة
        for item in self.menu_items:

            # اخفاء العناصر التي ليس لها صلاحية
            if item['permission'] and not auth.has_permission(item['permission']):
                continue

            btn = QPushButton(f"{item['icon']}  {ar(item['title'])}")
            btn.setObjectName("SidebarButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, id=item['id']: self.item_clicked(id))
            btn.setProperty('menu_id', item['id'])
            btn.setMinimumHeight(45)
            btn.setMaximumHeight(50)
            btn.setIconSize(QtCore.QSize(24, 24))

            layout.addWidget(btn)

        layout.addStretch()

        # معلومات المستخدم في الاسفل
        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        user_layout.setContentsMargins(20, 15, 20, 15)

        user_icon = QLabel("👤")
        user_name_string = auth.current_user.get('full_name') if isinstance(auth.current_user, dict) else getattr(auth.current_user, 'full_name', '')
        user_role_string = auth.current_user.get('role') if isinstance(auth.current_user, dict) else getattr(auth.current_user, 'role', '')

        user_info_layout = QVBoxLayout()
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(2)

        user_name = QLabel(ar(user_name_string or 'اسم المستخدم'))
        user_role = QLabel(ar(user_role_string or 'دور المستخدم'))
        user_role.setStyleSheet('font-size: 12px; color: #cbd5e1;')

        user_info_layout.addWidget(user_name)
        user_info_layout.addWidget(user_role)

        user_layout.addWidget(user_icon)
        user_layout.addLayout(user_info_layout)
        user_layout.addStretch()

        logout_btn = QPushButton("🚪")
        logout_btn.setToolTip(ar("تسجيل الخروج"))
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout_clicked)

        user_layout.addWidget(logout_btn)

        layout.addWidget(user_widget)

        self.apply_style()
        self.set_active_item('dashboard')

    def item_clicked(self, menu_id):
        self.set_active_item(menu_id)
        self.menu_item_clicked.emit(menu_id)

    def set_active_item(self, menu_id):
        self.active_item = menu_id

        for btn in self.findChildren(QPushButton, "SidebarButton"):
            if btn.property('menu_id') == menu_id:
                btn.setProperty('active', True)
            else:
                btn.setProperty('active', False)

            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def logout_clicked(self):
        confirm = QMessageBox.question(
            self,
            ar("تسجيل الخروج"),
            ar("هل أنت متأكد من تسجيل الخروج؟"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.logout_requested.emit()

    def apply_style(self):
        self.setStyleSheet(f"""
            #Sidebar {{
                background-color: {theme_manager.get_color("sidebar")};
                border: none;
            }}

            #SidebarTitle {{
                color: white;
                font-size: 18px;
                font-weight: 700;
                padding: 10px;
            }}

            #SidebarButton {{
                border: none;
                text-align: right;
                padding: 12px 16px;
                color: #cbd5e1;
                font-size: 13px;
                border-radius: 0px;
                min-height: 45px;
                background-color: transparent;
                font-weight: 500;
            }}

            #SidebarButton:hover {{
                background-color: {theme_manager.get_color("sidebar_hover")};
                color: white;
            }}

            #SidebarButton:pressed {{
                background-color: {theme_manager.get_color("sidebar_active")};
            }}

            #SidebarButton[active="true"] {{
                background-color: {theme_manager.get_color("sidebar_active")};
                color: white;
                font-weight: 700;
                border-right: 4px solid white;
            }}

            QFrame {{
                color: #475569;
            }}

            QLabel {{
                color: white;
            }}
        """)