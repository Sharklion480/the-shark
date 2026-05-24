#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار عمليات قاعدة البيانات
"""

import sys
import io

# تعيين UTF-8 لـ stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from database.db_manager import db_manager
from database.models import User, Property, Client
from datetime import datetime

print("=" * 60)
print("  اختبار عمليات قاعدة البيانات")
print("=" * 60)

# اختبار 1: الاتصال بقاعدة البيانات
print("\n🔗 اختبار 1: الاتصال بقاعدة البيانات...")
try:
    if db_manager.test_connection():
        print("✅ الاتصال بقاعدة البيانات يعمل")
    else:
        print("❌ فشل الاتصال بقاعدة البيانات")
        sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في الاتصال: {e}")
    sys.exit(1)

# اختبار 2: البحث عن المستخدمين
print("\n👥 اختبار 2: البحث عن المستخدمين...")
try:
    with db_manager.session_scope() as session:
        users = session.query(User).all()
        print(f"✅ عدد المستخدمين: {len(users)}")
        for user in users[:3]:
            print(f"   • {user.full_name} ({user.username})")
except Exception as e:
    print(f"❌ خطأ في البحث عن المستخدمين: {e}")
    sys.exit(1)

# اختبار 3: البحث عن العقارات
print("\n🏠 اختبار 3: البحث عن العقارات...")
try:
    with db_manager.session_scope() as session:
        properties = session.query(Property).all()
        print(f"✅ عدد العقارات: {len(properties)}")
        for prop in properties[:3]:
            print(f"   • {prop.title if hasattr(prop, 'title') else 'عقار'}")
except Exception as e:
    print(f"❌ خطأ في البحث عن العقارات: {e}")
    sys.exit(1)

# اختبار 4: البحث عن العملاء
print("\n👨 اختبار 4: البحث عن العملاء...")
try:
    with db_manager.session_scope() as session:
        clients = session.query(Client).all()
        print(f"✅ عدد العملاء: {len(clients)}")
        for client in clients[:3]:
            print(f"   • {client.full_name if hasattr(client, 'full_name') else 'عميل'}")
except Exception as e:
    print(f"❌ خطأ في البحث عن العملاء: {e}")
    sys.exit(1)

# اختبار 5: التحقق من حجم قاعدة البيانات
print("\n💾 اختبار 5: حجم قاعدة البيانات...")
try:
    size = db_manager.get_database_size()
    print(f"✅ حجم قاعدة البيانات: {size} MB")
except Exception as e:
    print(f"❌ خطأ في حساب الحجم: {e}")
    sys.exit(1)

# اختبار 6: التحقق من الفهارس والعلاقات
print("\n🔑 اختبار 6: التحقق من البيانات الخام...")
try:
    result = db_manager.execute_raw("SELECT COUNT(*) as count FROM users")
    if result:
        count = result[0][0]
        print(f"✅ عدد المستخدمين من استعلام SQL: {count}")
    else:
        print("⚠️ لم يتم الحصول على نتائج")
except Exception as e:
    print(f"❌ خطأ في الاستعلام: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ جميع اختبارات قاعدة البيانات نجحت!")
print("=" * 60)
sys.exit(0)
