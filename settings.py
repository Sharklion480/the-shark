# config/settings.py
"""
إعدادات البرنامج العامة
"""

import os
import json
from pathlib import Path


class Settings:
    """فئة إدارة إعدادات البرنامج"""
    
    # ============ المسارات الأساسية ============
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    DB_DIR = DATA_DIR / "db"
    BACKUP_DIR = DATA_DIR / "backups"
    EXPORTS_DIR = DATA_DIR / "exports"
    UPLOADS_DIR = DATA_DIR / "uploads"
    PROPERTIES_IMAGES_DIR = UPLOADS_DIR / "properties"
    LOGS_DIR = DATA_DIR / "logs"
    
    # مسارات الموارد
    RESOURCES_DIR = BASE_DIR / "resources"
    ICONS_DIR = RESOURCES_DIR / "icons"
    IMAGES_DIR = RESOURCES_DIR / "images"
    FONTS_DIR = RESOURCES_DIR / "fonts"
    STYLES_DIR = RESOURCES_DIR / "styles"
    TEMPLATES_DIR = RESOURCES_DIR / "templates"
    TRANSLATIONS_DIR = BASE_DIR / "translations"
    
    # ============ قاعدة البيانات ============
    DATABASE_NAME = "real_estate.db"
    DATABASE_PATH = DB_DIR / DATABASE_NAME
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    
    # ============ معلومات التطبيق ============
    APP_NAME = "نظام إدارة الاستثمار العقاري"
    APP_NAME_EN = "Real Estate Investment Manager"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Your Company"
    APP_ICON = "app_icon.ico"
    
    # ============ الإعدادات الافتراضية ============
    DEFAULT_LANGUAGE = "ar"  # ar | en
    DEFAULT_THEME = "light"  # light | dark
    DEFAULT_CURRENCY = "ج.م"  # العملة الافتراضية
    DEFAULT_FONT = "Cairo"
    DEFAULT_FONT_SIZE = 10
    
    # ============ إعدادات الأمان ============
    PASSWORD_MIN_LENGTH = 6
    SESSION_TIMEOUT = 3600  # ساعة واحدة بالثواني
    MAX_LOGIN_ATTEMPTS = 5
    ENCRYPTION_KEY_FILE = DATA_DIR / ".key"
    
    # ============ النسخ الاحتياطي ============
    AUTO_BACKUP_ENABLED = True
    AUTO_BACKUP_INTERVAL_DAYS = 7
    MAX_BACKUP_FILES = 10
    
    # ============ الإشعارات ============
    CONTRACT_EXPIRY_WARNING_DAYS = 30  # تنبيه قبل انتهاء العقد
    PAYMENT_REMINDER_DAYS = 3  # تذكير قبل موعد السداد
    
    # ============ الصور ============
    MAX_IMAGE_SIZE_MB = 5
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']
    THUMBNAIL_SIZE = (200, 200)
    
    # ============ التقارير ============
    DEFAULT_REPORT_FORMAT = "pdf"  # pdf | excel | word | csv
    REPORTS_PER_PAGE = 25
    
    # ============ ملف الإعدادات المستخدم ============
    USER_SETTINGS_FILE = DATA_DIR / "user_settings.json"
    
    # إعدادات قابلة للتعديل من قبل المستخدم
    _user_settings = {
        "language": DEFAULT_LANGUAGE,
        "theme": DEFAULT_THEME,
        "currency": DEFAULT_CURRENCY,
        "font": DEFAULT_FONT,
        "font_size": DEFAULT_FONT_SIZE,
        "auto_backup": AUTO_BACKUP_ENABLED,
        "company_name": "",
        "company_logo": "",
        "company_phone": "",
        "company_email": "",
        "company_address": "",
    }
    
    @classmethod
    def create_directories(cls):
        """إنشاء جميع المجلدات المطلوبة"""
        directories = [
            cls.DATA_DIR,
            cls.DB_DIR,
            cls.BACKUP_DIR,
            cls.EXPORTS_DIR,
            cls.UPLOADS_DIR,
            cls.PROPERTIES_IMAGES_DIR,
            cls.LOGS_DIR,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def load_user_settings(cls):
        """تحميل إعدادات المستخدم من الملف"""
        if cls.USER_SETTINGS_FILE.exists():
            try:
                with open(cls.USER_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    cls._user_settings.update(saved_settings)
            except Exception as e:
                print(f"خطأ في تحميل الإعدادات: {e}")
        return cls._user_settings
    
    @classmethod
    def save_user_settings(cls):
        """حفظ إعدادات المستخدم في الملف"""
        try:
            cls.USER_SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(cls.USER_SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(cls._user_settings, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"خطأ في حفظ الإعدادات: {e}")
            return False
    
    @classmethod
    def get(cls, key, default=None):
        """الحصول على قيمة إعداد"""
        return cls._user_settings.get(key, default)
    
    @classmethod
    def set(cls, key, value):
        """تعيين قيمة إعداد"""
        cls._user_settings[key] = value
        cls.save_user_settings()
    
    @classmethod
    def get_icon_path(cls, icon_name):
        """الحصول على مسار أيقونة"""
        return str(cls.ICONS_DIR / icon_name)
    
    @classmethod
    def get_font_path(cls, font_name):
        """الحصول على مسار خط"""
        return str(cls.FONTS_DIR / font_name)
    
    @classmethod
    def get_style_path(cls, style_name):
        """الحصول على مسار ملف تنسيق"""
        return str(cls.STYLES_DIR / style_name)


# تهيئة الإعدادات عند الاستيراد
Settings.create_directories()
Settings.load_user_settings()