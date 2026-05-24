# test_db.py
import logging
logging.basicConfig(level=logging.INFO)

from database.migrations import migration_manager
from database.seed_data import seed_database

# تهيئة قاعدة البيانات
print("🔄 جاري تهيئة قاعدة البيانات...")
migration_manager.initialize_database()

# إضافة البيانات التجريبية
print("🌱 جاري إضافة البيانات التجريبية...")
seed_database(with_samples=True)

print("\n✅ تم! تحقق من ملف:")
print("   data/db/real_estate.db")
print("\n👤 حساب الدخول:")
print("   Username: admin")
print("   Password: admin123")