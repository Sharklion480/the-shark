#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار تدفق المصادقة والواجهات
"""

import sys
import io

# تعيين UTF-8 لـ stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from database.db_manager import db_manager
from database.models import User
from controllers.auth_controller import auth
from utils.encryption import Encryption

print("=" * 60)
print("  اختبار المصادقة وتدفق المستخدم")
print("=" * 60)

# اختبار 1: التحقق من وجود مستخدم في قاعدة البيانات
print("\n🔍 اختبار 1: البحث عن مستخدم في قاعدة البيانات...")
try:
    with db_manager.session_scope() as session:
        user = session.query(User).filter_by(username='admin').first()
        if user:
            print(f"✅ تم العثور على المستخدم: {user.full_name}")
        else:
            print("❌ لم يتم العثور على المستخدم admin")
            sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في البحث عن المستخدم: {e}")
    sys.exit(1)

# اختبار 2: اختبار تسجيل الدخول
print("\n🔐 اختبار 2: محاولة تسجيل الدخول...")
try:
    success, message = auth.login("admin", "admin123")
    if success:
        print(f"✅ تسجيل الدخول نجح: {message}")
        print(f"   المستخدم: {auth.current_user}")
    else:
        print(f"❌ تسجيل الدخول فشل: {message}")
        sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في تسجيل الدخول: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# اختبار 3: التحقق من بيانات المستخدم المحفوظة
print("\n👤 اختبار 3: التحقق من بيانات المستخدم...")
try:
    if auth.current_user:
        if isinstance(auth.current_user, dict):
            print(f"✅ بيانات المستخدم محفوظة بشكل صحيح:")
            print(f"   الاسم: {auth.current_user.get('full_name')}")
            print(f"   الدور: {auth.current_user.get('role')}")
            print(f"   معرف: {auth.current_user.get('id')}")
        else:
            print(f"❌ بيانات المستخدم ليست dict: {type(auth.current_user)}")
            sys.exit(1)
    else:
        print("❌ لم يتم حفظ بيانات المستخدم")
        sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في التحقق من البيانات: {e}")
    sys.exit(1)

# اختبار 4: اختبار الصلاحيات
print("\n🔒 اختبار 4: التحقق من الصلاحيات...")
try:
    has_perm = auth.has_permission('properties_view')
    if auth.current_user.get('role') == 'admin':
        if has_perm:
            print(f"✅ المسؤول لديه صلاحيات")
        else:
            print(f"⚠️ تحذير: المسؤول لا يملك الصلاحيات المتوقعة")
    else:
        print(f"✅ التحقق من الصلاحيات يعمل")
except Exception as e:
    print(f"❌ خطأ في التحقق من الصلاحيات: {e}")
    sys.exit(1)

# اختبار 5: اختبار تسجيل الخروج
print("\n🚪 اختبار 5: اختبار تسجيل الخروج...")
try:
    auth.logout()
    if auth.current_user is None:
        print("✅ تسجيل الخروج نجح")
    else:
        print("❌ لم يتم تسجيل الخروج بشكل صحيح")
        sys.exit(1)
except Exception as e:
    print(f"❌ خطأ في تسجيل الخروج: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ جميع اختبارات المصادقة نجحت!")
print("=" * 60)
sys.exit(0)
