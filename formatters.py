# utils/formatters.py
"""
ادوات تنسيق البيانات للعربية
"""

from datetime import datetime, date
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from config.settings import Settings

ARABIC_DIGITS = '٠١٢٣٤٥٦٧٨٩'

def arabic_number(number):
    """تحويل الرقم الى ارقام عربية"""
    if number is None:
        return ""
    s = str(number)
    return ''.join(ARABIC_DIGITS[int(c)] if c.isdigit() else c for c in s)

def format_currency(amount, use_arabic=True):
    """تنسيق المبلغ كعملة"""
    if amount is None:
        return "0"
    
    amount = float(amount)
    
    # اضافة الفواصل الالفية
    formatted = f"{amount:,.2f}"
    
    # ازالة الاصفار الزائدة بعد الفاصلة
    if formatted.endswith('.00'):
        formatted = formatted[:-3]
    
    if use_arabic:
        formatted = arabic_number(formatted)
    
    currency = Settings.get('currency', 'ج.م')
    
    return f"{formatted} {currency}"

def format_number(number, decimals=0):
    """تنسيق الرقم مع الفواصل"""
    if number is None:
        return "0"
    
    if decimals == 0:
        formatted = f"{int(number):,}"
    else:
        formatted = f"{number:,.{decimals}f}"
    
    return arabic_number(formatted)

def format_date(dt, format="%d/%m/%Y"):
    """تنسيق التاريخ"""
    if dt is None:
        return ""

    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return dt

    if hasattr(dt, "toPyDate"):
        dt = dt.toPyDate()
    elif isinstance(dt, datetime):
        dt = dt.date()

    return arabic_number(dt.strftime(format))

def format_phone(phone):
    """تنسيق رقم الهاتف"""
    if not phone:
        return ""
    
    phone = ''.join(c for c in phone if c.isdigit())
    
    if len(phone) == 11 and phone.startswith('01'):
        return f"{phone[:3]} {phone[3:6]} {phone[6:]}"
    
    return phone

def format_file_size(size_bytes):
    """تنسيق حجم الملف"""
    if size_bytes == 0:
        return "0 بايت"
    
    size_names = ["بايت", "كيلوبايت", "ميجابايت", "جيجابايت"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names)-1:
        size_bytes /= 1024
        i += 1
    
    return f"{round(size_bytes, 1)} {size_names[i]}"

def days_ago(target_date):
    """ارجاع نص كم يوم مضى او باقي"""
    if not target_date:
        return ""
    
    if isinstance(target_date, datetime):
        target_date = target_date.date()
    
    delta = target_date - date.today()
    days = delta.days
    
    if days == 0:
        return "اليوم"
    elif days == 1:
        return "غدا"
    elif days > 1:
        return f"متبقي {arabic_number(days)} يوم"
    elif days == -1:
        return "امس"
    else:
        return f"منذ {arabic_number(abs(days))} ايام"

def ar(text):
    """اصلاح عرض النص العربي في PyQt"""
    if not text:
        return ""
    return get_display(reshape(str(text)))