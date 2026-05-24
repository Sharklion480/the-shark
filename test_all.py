"""
🧪 اختبار شامل لجميع مراحل البرنامج
يفحص: الملفات - المكتبات - قاعدة البيانات - الكود - الواجهة
"""

import os
import sys
import sqlite3
import ast
from datetime import datetime

# ألوان للطباعة
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

total = 0
passed = 0
failed = 0
warnings_list = []

def test(name, condition, warning_msg=None):
    global total, passed, failed
    total += 1
    if condition:
        passed += 1
        print(f"  {Colors.GREEN}✅ {name}{Colors.END}")
    else:
        failed += 1
        print(f"  {Colors.RED}❌ {name}{Colors.END}")
        if warning_msg:
            warnings_list.append(warning_msg)
            print(f"     {Colors.YELLOW}💡 {warning_msg}{Colors.END}")

def section(title):
    print()
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*55}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}  {title}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*55}{Colors.END}")


# ================================================
# المرحلة 1: فحص Python
# ================================================
section("🐍 المرحلة 1: فحص Python")

# إصدار Python
python_version = sys.version
test(f"Python مثبت (الإصدار: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})", True)
test("Python 3.8 أو أحدث", sys.version_info >= (3, 8), 
     "يُفضل Python 3.11 للتوافق الأفضل")

if sys.version_info >= (3, 13):
    print(f"  {Colors.YELLOW}⚠️ تحذير: Python {sys.version_info.major}.{sys.version_info.minor} جديد جداً - قد تظهر تحذيرات{Colors.END}")


# ================================================
# المرحلة 2: فحص المكتبات
# ================================================
section("📦 المرحلة 2: فحص المكتبات")

libraries = {
    "PyQt5": {"import": "PyQt5", "required": True},
    "PyQt5.QtWidgets": {"import": "PyQt5.QtWidgets", "required": True},
    "PyQt5.QtCore": {"import": "PyQt5.QtCore", "required": True},
    "PyQt5.QtGui": {"import": "PyQt5.QtGui", "required": True},
    "sqlite3": {"import": "sqlite3", "required": True},
    "reportlab": {"import": "reportlab", "required": False},
    "openpyxl": {"import": "openpyxl", "required": False},
    "Pillow": {"import": "PIL", "required": False},
    "matplotlib": {"import": "matplotlib", "required": False},
}

for name, info in libraries.items():
    try:
        module = __import__(info["import"])
        version = getattr(module, '__version__', 'OK')
        test(f"{name} → {version}", True)
    except ImportError:
        if info["required"]:
            test(f"{name} (مطلوب!)", False, f"pip install {name}")
        else:
            test(f"{name} (اختياري)", False, f"pip install {name}")


# ================================================
# المرحلة 3: فحص الملفات
# ================================================
section("📁 المرحلة 3: فحص الملفات والمجلدات")

# الملف الرئيسي
test("ملف main.py موجود", os.path.exists("main.py"),
     "أنشئ ملف main.py في المجلد الحالي")

# حجم الملف
if os.path.exists("main.py"):
    size = os.path.getsize("main.py")
    test(f"main.py ليس فارغاً ({size:,} bytes)", size > 100,
         "الملف فارغ! انسخ الكود فيه")

# ملفات إضافية
optional_files = [
    ("app.py", "ملف الويب"),
    ("test_app.py", "ملف الاختبار"),
    ("check.py", "ملف الفحص"),
    ("database.py", "قاعدة البيانات المنفصلة"),
]

for filename, desc in optional_files:
    if os.path.exists(filename):
        print(f"  📄 {filename} → موجود ({desc})")

# مجلدات
optional_dirs = ["static", "static/css", "static/js", "templates", "ui", "utils"]
for dirname in optional_dirs:
    if os.path.exists(dirname):
        print(f"  📁 {dirname}/ → موجود")


# ================================================
# المرحلة 4: فحص الكود
# ================================================
section("🔍 المرحلة 4: فحص كود main.py")

if os.path.exists("main.py"):
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        # فحص بناء الكود
        try:
            ast.parse(code)
            test("بناء الكود (Syntax) سليم", True)
        except SyntaxError as e:
            test(f"بناء الكود - خطأ في سطر {e.lineno}", False,
                 f"الخطأ: {e.msg} في سطر {e.lineno}")
            
            # عرض السطر الذي فيه الخطأ
            lines = code.split('\n')
            if e.lineno and e.lineno <= len(lines):
                print(f"\n  {Colors.YELLOW}السطر {e.lineno}:{Colors.END}")
                
                # عرض 3 أسطر قبل وبعد
                start = max(0, e.lineno - 3)
                end = min(len(lines), e.lineno + 2)
                
                for i in range(start, end):
                    marker = ">>>" if i == e.lineno - 1 else "   "
                    color = Colors.RED if i == e.lineno - 1 else ""
                    end_color = Colors.END if i == e.lineno - 1 else ""
                    print(f"  {marker} {i+1:4d} | {color}{lines[i]}{end_color}")
                print()

        # فحص وجود الـ Classes المطلوبة
        required_classes = [
            "MainWindow",
            "Database", 
            "StatCard",
        ]
        
        for cls in required_classes:
            test(f"Class '{cls}' موجود", f"class {cls}" in code,
                 f"أضف class {cls} في الكود")

        # فحص وجود الدوال المطلوبة
        required_functions = [
            ("build_ui", "بناء الواجهة"),
            ("make_dashboard", "لوحة المعلومات"),
            ("make_properties", "العقارات"),
            ("make_contracts", "العقود"),
            ("make_payments", "المدفوعات"),
            ("make_expenses", "المصروفات"),
            ("make_reports", "التقارير"),
            ("make_settings", "الإعدادات"),
            ("refresh_all", "تحديث البيانات"),
            ("add_property", "إضافة عقار"),
            ("add_unit", "إضافة وحدة"),
            ("add_contract", "إضافة عقد"),
            ("add_payment", "إضافة دفعة"),
            ("add_expense", "إضافة مصروف"),
        ]

        for func, desc in required_functions:
            test(f"دالة {func}() → {desc}", 
                 f"def {func}" in code,
                 f"أضف دالة {func}() للـ {desc}")

        # فحص الـ imports
        required_imports = [
            "from PyQt5.QtWidgets import",
            "from PyQt5.QtCore import",
            "from PyQt5.QtGui import",
            "import sqlite3",
        ]

        for imp in required_imports:
            test(f"Import: {imp.split('import')[0].strip()}", 
                 imp in code)

        # فحص نقطة التشغيل
        test("نقطة التشغيل (if __name__) موجودة",
             'if __name__ == "__main__"' in code or
             "if __name__ == '__main__'" in code,
             "أضف if __name__ == '__main__' في نهاية الملف")

        # فحص المسافات (Indentation)
        lines = code.split('\n')
        indent_errors = []
        for i, line in enumerate(lines, 1):
            if line and not line.strip().startswith('#'):
                # فحص خلط tabs مع spaces
                if '\t' in line and '    ' in line:
                    indent_errors.append(i)
        
        test("لا يوجد خلط بين Tabs و Spaces", 
             len(indent_errors) == 0,
             f"أسطر فيها خلط: {indent_errors[:5]}")

        # عدد الأسطر
        line_count = len(lines)
        print(f"\n  📊 إحصائيات الكود:")
        print(f"     عدد الأسطر: {line_count:,}")
        print(f"     حجم الملف: {len(code):,} حرف")
        
        # عدد الـ Classes
        class_count = code.count("class ")
        print(f"     عدد الـ Classes: {class_count}")
        
        # عدد الدوال
        def_count = code.count("def ")
        print(f"     عدد الدوال: {def_count}")

    except Exception as e:
        test(f"قراءة الملف", False, str(e))
else:
    print(f"  {Colors.RED}❌ main.py غير موجود - لا يمكن فحص الكود{Colors.END}")


# ================================================
# المرحلة 5: فحص قاعدة البيانات
# ================================================
section("💾 المرحلة 5: فحص قاعدة البيانات")

try:
    # إنشاء قاعدة بيانات تجريبية
    test_db = "test_check.db"
    conn = sqlite3.connect(test_db)
    c = conn.cursor()
    test("إنشاء اتصال بقاعدة البيانات", True)

    # إنشاء جدول تجريبي
    c.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)")
    test("إنشاء جدول تجريبي", True)

    # إدراج بيانات
    c.execute("INSERT INTO test_table (name) VALUES ('test')")
    conn.commit()
    test("إدراج بيانات", True)

    # قراءة بيانات
    c.execute("SELECT * FROM test_table")
    result = c.fetchone()
    test("قراءة بيانات", result is not None)

    # حذف بيانات
    c.execute("DELETE FROM test_table WHERE name='test'")
    conn.commit()
    test("حذف بيانات", True)

    conn.close()
    os.remove(test_db)
    test("تنظيف قاعدة البيانات التجريبية", True)

except Exception as e:
    test(f"قاعدة البيانات", False, str(e))

# فحص قاعدة البيانات الحقيقية
if os.path.exists("real_estate.db"):
    try:
        conn = sqlite3.connect("real_estate.db")
        c = conn.cursor()
        
        # فحص الجداول
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in c.fetchall()]
        
        required_tables = ["properties", "units", "rental_contracts", "payments", "expenses"]
        
        for table in required_tables:
            test(f"جدول '{table}' موجود", table in tables)
        
        # عدد السجلات
        print(f"\n  📊 بيانات قاعدة البيانات:")
        for table in tables:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            print(f"     {table}: {count} سجل")
        
        conn.close()
    except Exception as e:
        test("قراءة قاعدة البيانات الحقيقية", False, str(e))
else:
    print(f"  ℹ️ قاعدة البيانات real_estate.db غير موجودة (ستُنشأ عند التشغيل)")


# ================================================
# المرحلة 6: فحص الواجهة
# ================================================
section("🖥️ المرحلة 6: فحص الواجهة")

try:
    import warnings
    warnings.filterwarnings("ignore")
    
    from PyQt5.QtWidgets import QApplication
    
    # التحقق من وجود QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    test("إنشاء QApplication", True)

    # فحص العناصر المطلوبة
    from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
        QHBoxLayout, QPushButton, QLabel, QTableWidget,
        QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox,
        QDateEdit, QTextEdit, QGroupBox, QTabWidget,
        QDialog, QFormLayout, QMessageBox, QFrame,
        QScrollArea, QListWidget, QCheckBox, QFileDialog,
        QTableWidgetItem)
    test("جميع عناصر الواجهة متاحة", True)

    from PyQt5.QtCore import Qt, QTimer, QDate
    test("عناصر Qt Core متاحة", True)

    from PyQt5.QtGui import QColor
    test("عناصر Qt GUI متاحة", True)

    # محاولة إنشاء نافذة تجريبية
    try:
        w = QMainWindow()
        w.setWindowTitle("Test")
        w.setGeometry(0, 0, 100, 100)
        test("إنشاء نافذة تجريبية", True)
        w.close()
        w.deleteLater()
    except Exception as e:
        test("إنشاء نافذة تجريبية", False, str(e))

except ImportError as e:
    test(f"استيراد PyQt5", False, f"pip install PyQt5\nالخطأ: {e}")


# ================================================
# المرحلة 7: محاولة تشغيل البرنامج
# ================================================
section("🚀 المرحلة 7: محاولة تحميل البرنامج")

if os.path.exists("main.py"):
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        # التحقق من أن الكود قابل للتحليل
        ast.parse(code)
        test("الكود قابل للتحليل (parseable)", True)
        
        # التحقق من وجود الـ main block
        has_main = ('if __name__' in code and 
                    'QApplication' in code and 
                    'MainWindow' in code)
        test("نقطة التشغيل صحيحة", has_main)
        
        if has_main:
            test("البرنامج جاهز للتشغيل! 🎉", True)
        
    except SyntaxError as e:
        test(f"الكود فيه خطأ في سطر {e.lineno}", False,
             f"افتح main.py وأصلح سطر {e.lineno}\n"
             f"     الخطأ: {e.msg}")
        
        # إظهار الحل
        print(f"\n  {Colors.YELLOW}🔧 كيف تصلح الخطأ:{Colors.END}")
        print(f"  1. افتح main.py في VS Code")
        print(f"  2. اذهب لسطر {e.lineno} (Ctrl+G ثم اكتب {e.lineno})")
        print(f"  3. تأكد من المسافات (Indentation)")
        print(f"  4. تأكد أن كل الأقواس مغلقة")


# ================================================
# المرحلة 8: فحص المسار
# ================================================
section("📍 المرحلة 8: معلومات المسار")

print(f"  المجلد الحالي: {os.getcwd()}")
print(f"  Python: {sys.executable}")
print(f"  إصدار Python: {sys.version}")

# قائمة الملفات
print(f"\n  📁 محتويات المجلد:")
for item in sorted(os.listdir(".")):
    if os.path.isdir(item):
        print(f"     📂 {item}/")
    else:
        size = os.path.getsize(item)
        print(f"     📄 {item} ({size:,} bytes)")


# ================================================
# النتيجة النهائية
# ================================================
print()
print(f"{Colors.BOLD}{'='*55}{Colors.END}")
print(f"{Colors.BOLD}  📊 النتيجة النهائية{Colors.END}")
print(f"{Colors.BOLD}{'='*55}{Colors.END}")

percentage = (passed / total * 100) if total > 0 else 0

print(f"""
  إجمالي الاختبارات: {total}
  {Colors.GREEN}✅ ناجح: {passed}{Colors.END}
  {Colors.RED}❌ فاشل: {failed}{Colors.END}
  📈 نسبة النجاح: {percentage:.1f}%
""")

# شريط التقدم
bar_length = 40
filled = int(bar_length * passed / total) if total > 0 else 0
bar = "█" * filled + "░" * (bar_length - filled)
color = Colors.GREEN if percentage >= 90 else Colors.YELLOW if percentage >= 70 else Colors.RED
print(f"  {color}[{bar}] {percentage:.0f}%{Colors.END}")
print()

if failed == 0:
    print(f"  {Colors.GREEN}{Colors.BOLD}🎉🎉🎉 جميع الاختبارات ناجحة!{Colors.END}")
    print(f"  {Colors.GREEN}✅ البرنامج جاهز للتشغيل!{Colors.END}")
    print()
    print(f"  لتشغيل البرنامج:")
    print(f"  {Colors.BOLD}python -W ignore main.py{Colors.END}")
elif failed <= 3:
    print(f"  {Colors.YELLOW}⚠️ يوجد {failed} مشكلة بسيطة{Colors.END}")
    print(f"  البرنامج قد يعمل - جرب تشغيله:")
    print(f"  {Colors.BOLD}python -W ignore main.py{Colors.END}")
else:
    print(f"  {Colors.RED}❌ يوجد {failed} مشكلة تحتاج إصلاح{Colors.END}")

# عرض التحذيرات
if warnings_list:
    print(f"\n  {Colors.YELLOW}💡 الحلول المقترحة:{Colors.END}")
    for i, w in enumerate(warnings_list, 1):
        print(f"  {i}. {w}")

print()
print(f"{'='*55}")
input("اضغط Enter للإغلاق...")