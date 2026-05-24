# views/login_view.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from controllers.auth_controller import auth
from utils.formatters import ar
from config.settings import Settings
from config.themes import theme_manager


class LoginView(QDialog):

    login_success = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.apply_style()

    def setup_ui(self):
        self.setWindowTitle(ar(Settings.APP_NAME))
        self.setFixedSize(450, 550)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # الشعار والعنوان
        logo_label = QLabel("🏢")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 64px;")

        title_label = QLabel(ar(Settings.APP_NAME))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("LoginTitle")

        version_label = QLabel(ar(f"الاصدار {Settings.APP_VERSION}"))
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setObjectName("VersionLabel")

        # حقول الادخال
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(ar("اسم المستخدم"))
        self.username_input.setText("admin")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(ar("كلمة المرور"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText("admin123")

        # رسالة الخطأ
        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setVisible(False)

        # زر الدخول
        self.login_button = QPushButton(ar("تسجيل الدخول"))
        self.login_button.setObjectName("LoginButton")
        self.login_button.clicked.connect(self.do_login)
        self.login_button.setCursor(Qt.PointingHandCursor)

        # اضافة كل شيء للواجهة
        layout.addStretch()
        layout.addWidget(logo_label)
        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addSpacing(30)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.error_label)
        layout.addSpacing(20)
        layout.addWidget(self.login_button)
        layout.addStretch()

        # اختصار انتر
        self.password_input.returnPressed.connect(self.do_login)

    def do_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self.show_error("الرجاء ادخال اسم المستخدم وكلمة المرور")
            return

        self.login_button.setEnabled(False)
        self.login_button.setText(ar("جاري تسجيل الدخول..."))

        QApplication.processEvents()

        success, message = auth.login(username, password)

        if success:
            self.accept()
            self.login_success.emit()
        else:
            self.show_error(message)
            self.login_button.setEnabled(True)
            self.login_button.setText(ar("تسجيل الدخول"))

    def show_error(self, message):
        self.error_label.setText(ar(message))
        self.error_label.setVisible(True)
        QTimer.singleShot(4000, lambda: self.error_label.setVisible(False))

    def apply_style(self):
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme_manager.get_color("surface")};
            }}

            #LoginTitle {{
                font-size: 22px;
                font-weight: 700;
                color: {theme_manager.get_color("text_primary")};
            }}

            #VersionLabel {{
                font-size: 12px;
                color: {theme_manager.get_color("text_secondary")};
            }}

            QLineEdit {{
                padding: 12px 16px;
                border-radius: 8px;
                border: 1px solid {theme_manager.get_color("border")};
                font-size: 14px;
                background-color: {theme_manager.get_color("background")};
            }}

            QLineEdit:focus {{
                border: 1px solid {theme_manager.get_color("primary")};
            }}

            #LoginButton {{
                padding: 14px;
                border-radius: 8px;
                border: none;
                background-color: {theme_manager.get_color("primary")};
                color: white;
                font-size: 15px;
                font-weight: 600;
            }}

            #LoginButton:hover {{
                background-color: {theme_manager.get_color("primary_dark")};
            }}

            #LoginButton:disabled {{
                opacity: 0.7;
            }}

            #ErrorLabel {{
                color: {theme_manager.get_color("danger")};
                font-size: 13px;
            }}
        """)