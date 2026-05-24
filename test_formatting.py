#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار عرض النصوص العربية والتنسيق
"""

import sys
import io

# تعيين UTF-8 لـ stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from utils.formatters import ar, format_currency, format_number, format_date, arabic_number
from datetime import datetime, date

print("=" * 60)
print("  اختبار العربية والتنسيق")
print("=" * 60)

# اختبار 1: اختبار دالة ar()
print("\n🔤 اختبار 1: دالة ar() لعرض النصوص العربية...")
try:
    test_texts = [
        "لوحة التحكم",
        "العقارات",
        "العملاء",
        "تسجيل الدخول",
    ]
    
    for text in test_texts:
        result = ar(text)
        if result and isinstance(result, str):
            print(f"✅ ar('{text}') -> '{result}'")
        else:
            print(f"⚠️ ar('{text}') -> {type(result)}")
except Exception as e:
    print(f"❌ خطأ في ar(): {e}")
    sys.exit(1)

# اختبار 2: اختبار تحويل الأرقام العربية
print("\n🔢 اختبار 2: تحويل الأرقام إلى عربية...")
try:
    test_numbers = [0, 1, 10, 100, 1234, 999999]
    
    for num in test_numbers:
        result = arabic_number(num)
        if result:
            print(f"✅ arabic_number({num}) -> {result}")
        else:
            print(f"❌ arabic_number({num}) فشل")
            sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في arabic_number(): {e}")
    sys.exit(1)

# اختبار 3: اختبار تنسيق العملات
print("\n💰 اختبار 3: تنسيق العملات...")
try:
    test_amounts = [0, 100, 1000, 10000, 1234567.89]
    
    for amount in test_amounts:
        result = format_currency(amount)
        if result:
            print(f"✅ format_currency({amount}) -> {result}")
        else:
            print(f"❌ format_currency({amount}) فشل")
            sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في format_currency(): {e}")
    sys.exit(1)

# اختبار 4: اختبار تنسيق الأرقام
print("\n#️⃣ اختبار 4: تنسيق الأرقام...")
try:
    test_cases = [
        (1000, 0),
        (1234567, 2),
        (99.99, 1),
    ]
    
    for num, decimals in test_cases:
        result = format_number(num, decimals)
        if result:
            print(f"✅ format_number({num}, {decimals}) -> {result}")
        else:
            print(f"❌ format_number({num}, {decimals}) فشل")
            sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في format_number(): {e}")
    sys.exit(1)

# اختبار 5: اختبار تنسيق التواريخ
print("\n📅 اختبار 5: تنسيق التواريخ...")
try:
    today = date.today()
    result = format_date(today)
    if result:
        print(f"✅ format_date({today}) -> {result}")
    else:
        print(f"❌ format_date() فشل")
        sys.exit(1)
    
    # اختبار مع datetime
    now = datetime.now()
    result = format_date(now)
    if result:
        print(f"✅ format_date(datetime) -> {result}")
    else:
        print(f"❌ format_date(datetime) فشل")
        sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في format_date(): {e}")
    sys.exit(1)

# اختبار 6: اختبار ar() مع None والقيم الفارغة
print("\n🔒 اختبار 6: معالجة القيم الفارغة...")
try:
    result_none = ar(None)
    if result_none == "":
        print(f"✅ ar(None) -> ''")
    else:
        print(f"⚠️ ar(None) -> {repr(result_none)}")
    
    result_empty = ar("")
    if result_empty == "":
        print(f"✅ ar('') -> ''")
    else:
        print(f"⚠️ ar('') -> {repr(result_empty)}")
except Exception as e:
    print(f"❌ خطأ في معالجة القيم الفارغة: {e}")
    sys.exit(1)

# اختبار 7: منتقي التاريخ الهجري
print("\n📆 اختبار 7: منتقي التاريخ الهجري...")
try:
    from PyQt5.QtWidgets import QApplication
    from widgets.date_picker_hijri import DatePickerHijri
    from datetime import date

    app = QApplication.instance() or QApplication(sys.argv)
    picker = DatePickerHijri()
    if not picker.date_label.text():
        print("❌ DatePickerHijri لم يعرض تاريخاً")
        sys.exit(1)
    print(f"✅ عرض التاريخ: {picker.date_label.text()}")

    picker.set_date(date(2024, 1, 15))
    if picker.get_date() != date(2024, 1, 15):
        print("❌ set_date/get_date لا يعملان بشكل صحيح")
        sys.exit(1)
    print("✅ set_date/get_date يعملان")
except Exception as e:
    print(f"❌ خطأ في DatePickerHijri: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ جميع اختبارات التنسيق والعربية نجحت!")
print("=" * 60)
sys.exit(0)
