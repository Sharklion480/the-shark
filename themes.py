# config/themes.py
"""
إدارة الثيمات (الألوان والمظهر)
"""

from pathlib import Path
from config.settings import Settings


class ThemeColors:
    """ألوان الثيمات"""
    
    LIGHT = {
        # الألوان الأساسية
        "primary": "#1976D2",           # أزرق رئيسي
        "primary_dark": "#1565C0",      # أزرق غامق
        "primary_light": "#42A5F5",     # أزرق فاتح
        
        "secondary": "#FF6F00",         # برتقالي
        "secondary_dark": "#E65100",
        "secondary_light": "#FFB74D",
        
        # ألوان الحالة
        "success": "#2E7D32",           # أخضر
        "warning": "#F57C00",           # برتقالي تحذيري
        "danger": "#C62828",            # أحمر
        "info": "#0288D1",              # أزرق معلوماتي
        
        # الخلفيات
        "background": "#F5F5F5",        # خلفية رئيسية
        "surface": "#FFFFFF",           # خلفية البطاقات
        "sidebar": "#1E293B",           # القائمة الجانبية
        "sidebar_hover": "#334155",
        "sidebar_active": "#1976D2",
        
        # النصوص
        "text_primary": "#212121",      # نص رئيسي
        "text_secondary": "#757575",    # نص ثانوي
        "text_disabled": "#BDBDBD",
        "text_on_primary": "#FFFFFF",
        "text_on_sidebar": "#FFFFFF",
        
        # الحدود والفواصل
        "border": "#E0E0E0",
        "divider": "#EEEEEE",
        
        # المدخلات
        "input_background": "#FFFFFF",
        "input_border": "#CCCCCC",
        "input_focus": "#1976D2",
        
        # الجداول
        "table_header": "#F5F5F5",
        "table_row_alt": "#FAFAFA",
        "table_hover": "#E3F2FD",
        "table_selected": "#BBDEFB",
    }
    
    DARK = {
        # الألوان الأساسية
        "primary": "#2196F3",
        "primary_dark": "#1976D2",
        "primary_light": "#64B5F6",
        
        "secondary": "#FF9800",
        "secondary_dark": "#F57C00",
        "secondary_light": "#FFB74D",
        
        # ألوان الحالة
        "success": "#4CAF50",
        "warning": "#FF9800",
        "danger": "#F44336",
        "info": "#03A9F4",
        
        # الخلفيات
        "background": "#121212",
        "surface": "#1E1E1E",
        "sidebar": "#0F172A",
        "sidebar_hover": "#1E293B",
        "sidebar_active": "#2196F3",
        
        # النصوص
        "text_primary": "#FFFFFF",
        "text_secondary": "#B0B0B0",
        "text_disabled": "#666666",
        "text_on_primary": "#FFFFFF",
        "text_on_sidebar": "#FFFFFF",
        
        # الحدود والفواصل
        "border": "#333333",
        "divider": "#2A2A2A",
        
        # المدخلات
        "input_background": "#2A2A2A",
        "input_border": "#444444",
        "input_focus": "#2196F3",
        
        # الجداول
        "table_header": "#2A2A2A",
        "table_row_alt": "#252525",
        "table_hover": "#1E3A5F",
        "table_selected": "#1565C0",
    }


class ThemeManager:
    """مدير الثيمات"""
    
    LIGHT_THEME = "light"
    DARK_THEME = "dark"
    
    def __init__(self):
        self.current_theme = Settings.get("theme", "light")
        self.colors = self._load_colors()
    
    def _load_colors(self):
        """تحميل ألوان الثيم الحالي"""
        if self.current_theme == self.DARK_THEME:
            return ThemeColors.DARK
        return ThemeColors.LIGHT
    
    def get_color(self, color_name):
        """الحصول على لون معين"""
        return self.colors.get(color_name, "#000000")
    
    def switch_theme(self, theme_name):
        """تبديل الثيم"""
        if theme_name in [self.LIGHT_THEME, self.DARK_THEME]:
            self.current_theme = theme_name
            self.colors = self._load_colors()
            Settings.set("theme", theme_name)
            return True
        return False
    
    def toggle_theme(self):
        """التبديل بين الفاتح والداكن"""
        new_theme = self.DARK_THEME if self.current_theme == self.LIGHT_THEME else self.LIGHT_THEME
        self.switch_theme(new_theme)
        return new_theme
    
    def is_dark(self):
        """التحقق من الوضع الداكن"""
        return self.current_theme == self.DARK_THEME
    
    def load_stylesheet(self):
        """تحميل ملف التنسيق المناسب"""
        try:
            # تحميل الملف المشترك
            common_path = Settings.get_style_path("common.qss")
            theme_file = "dark_theme.qss" if self.is_dark() else "light_theme.qss"
            theme_path = Settings.get_style_path(theme_file)
            
            stylesheet = ""
            
            # قراءة الملف المشترك
            if Path(common_path).exists():
                with open(common_path, 'r', encoding='utf-8') as f:
                    stylesheet += f.read() + "\n"
            
            # قراءة ملف الثيم
            if Path(theme_path).exists():
                with open(theme_path, 'r', encoding='utf-8') as f:
                    stylesheet += f.read()
            
            # استبدال متغيرات الألوان في الـ stylesheet
            for color_name, color_value in self.colors.items():
                stylesheet = stylesheet.replace(f"@{color_name}", color_value)
            
            return stylesheet
            
        except Exception as e:
            print(f"خطأ في تحميل ملف التنسيق: {e}")
            return ""
    
    def apply_theme(self, app):
        """تطبيق الثيم على التطبيق"""
        stylesheet = self.load_stylesheet()
        if stylesheet:
            app.setStyleSheet(stylesheet)
    
    def get_chart_colors(self):
        """الحصول على ألوان للرسوم البيانية"""
        return [
            self.get_color("primary"),
            self.get_color("secondary"),
            self.get_color("success"),
            self.get_color("warning"),
            self.get_color("danger"),
            self.get_color("info"),
            self.get_color("primary_light"),
            self.get_color("secondary_light"),
        ]


# إنشاء مدير الثيمات العام
theme_manager = ThemeManager()