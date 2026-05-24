# database/migrations.py
"""
إدارة تحديثات قاعدة البيانات
"""

import logging
from sqlalchemy import inspect, text
from database.db_manager import db_manager
from database.models import Base


class MigrationManager:
    """مدير التحديثات (Migrations)"""
    
    CURRENT_VERSION = "1.0.0"
    
    def __init__(self):
        self.engine = db_manager.engine
        self.inspector = inspect(self.engine)
    
    def initialize_database(self):
        """تهيئة قاعدة البيانات لأول مرة"""
        try:
            # إنشاء جميع الجداول
            Base.metadata.create_all(bind=self.engine)
            logging.info("✅ تم إنشاء قاعدة البيانات بنجاح")
            
            # إضافة الإعدادات الأساسية
            self._insert_default_settings()
            
            # حفظ إصدار قاعدة البيانات
            self._save_version()
            
            return True
            
        except Exception as e:
            logging.error(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
            return False
    
    def check_database_exists(self):
        """التحقق من وجود قاعدة البيانات"""
        tables = self.inspector.get_table_names()
        return len(tables) > 0
    
    def check_table_exists(self, table_name):
        """التحقق من وجود جدول معين"""
        return table_name in self.inspector.get_table_names()
    
    def get_database_version(self):
        """الحصول على إصدار قاعدة البيانات الحالي"""
        try:
            with db_manager.session_scope() as session:
                from database.models import Setting
                version_setting = session.query(Setting).filter_by(key='db_version').first()
                if version_setting:
                    return version_setting.value
        except Exception as e:
            logging.error(f"خطأ في قراءة إصدار قاعدة البيانات: {e}")
        return None
    
    def _save_version(self):
        """حفظ إصدار قاعدة البيانات"""
        try:
            with db_manager.session_scope() as session:
                from database.models import Setting
                version_setting = session.query(Setting).filter_by(key='db_version').first()
                if version_setting:
                    version_setting.value = self.CURRENT_VERSION
                else:
                    version_setting = Setting(
                        key='db_version',
                        value=self.CURRENT_VERSION,
                        category='system',
                        description='إصدار قاعدة البيانات',
                        is_editable=False
                    )
                    session.add(version_setting)
        except Exception as e:
            logging.error(f"خطأ في حفظ الإصدار: {e}")
    
    def _insert_default_settings(self):
        """إضافة الإعدادات الافتراضية"""
        default_settings = [
            # ============ إعدادات الشركة ============
            {'key': 'company_name', 'value': 'شركة الاستثمار العقاري', 'category': 'company', 'description': 'اسم الشركة'},
            {'key': 'company_logo', 'value': '', 'category': 'company', 'description': 'شعار الشركة'},
            {'key': 'company_phone', 'value': '', 'category': 'company', 'description': 'هاتف الشركة'},
            {'key': 'company_email', 'value': '', 'category': 'company', 'description': 'بريد الشركة'},
            {'key': 'company_address', 'value': '', 'category': 'company', 'description': 'عنوان الشركة'},
            {'key': 'company_tax_number', 'value': '', 'category': 'company', 'description': 'الرقم الضريبي'},
            
            # ============ إعدادات العامة ============
            {'key': 'currency', 'value': 'ج.م', 'category': 'general', 'description': 'العملة'},
            {'key': 'language', 'value': 'ar', 'category': 'general', 'description': 'اللغة'},
            {'key': 'theme', 'value': 'light', 'category': 'general', 'description': 'الثيم'},
            {'key': 'date_format', 'value': 'DD/MM/YYYY', 'category': 'general', 'description': 'صيغة التاريخ'},
            
            # ============ إعدادات النسخ الاحتياطي ============
            {'key': 'auto_backup_enabled', 'value': 'true', 'category': 'backup', 'description': 'النسخ الاحتياطي التلقائي', 'data_type': 'boolean'},
            {'key': 'auto_backup_interval', 'value': '7', 'category': 'backup', 'description': 'مدة النسخ الاحتياطي (أيام)', 'data_type': 'integer'},
            {'key': 'max_backup_files', 'value': '10', 'category': 'backup', 'description': 'أقصى عدد نسخ احتياطية', 'data_type': 'integer'},
            
            # ============ إعدادات الإشعارات ============
            {'key': 'contract_expiry_days', 'value': '30', 'category': 'notifications', 'description': 'تنبيه قبل انتهاء العقد بالأيام', 'data_type': 'integer'},
            {'key': 'payment_reminder_days', 'value': '3', 'category': 'notifications', 'description': 'تذكير قبل موعد السداد', 'data_type': 'integer'},
            {'key': 'enable_sound', 'value': 'true', 'category': 'notifications', 'description': 'تفعيل صوت الإشعارات', 'data_type': 'boolean'},
            
            # ============ إعدادات العقارات ============
            {'key': 'property_number_prefix', 'value': 'P', 'category': 'properties', 'description': 'بادئة رقم العقار'},
            {'key': 'property_number_counter', 'value': '1000', 'category': 'properties', 'description': 'العداد الحالي', 'data_type': 'integer'},
            
            # ============ إعدادات العملاء ============
            {'key': 'client_code_prefix', 'value': 'C', 'category': 'clients', 'description': 'بادئة كود العميل'},
            {'key': 'client_code_counter', 'value': '1000', 'category': 'clients', 'description': 'العداد الحالي', 'data_type': 'integer'},
            
            # ============ إعدادات العقود ============
            {'key': 'contract_number_prefix', 'value': 'CT', 'category': 'contracts', 'description': 'بادئة رقم العقد'},
            {'key': 'contract_number_counter', 'value': '1000', 'category': 'contracts', 'description': 'العداد الحالي', 'data_type': 'integer'},
            
            # ============ إعدادات المبيعات ============
            {'key': 'sale_number_prefix', 'value': 'S', 'category': 'sales', 'description': 'بادئة رقم البيع'},
            {'key': 'sale_number_counter', 'value': '1000', 'category': 'sales', 'description': 'العداد الحالي', 'data_type': 'integer'},
            
            # ============ إعدادات الإيجارات ============
            {'key': 'rental_number_prefix', 'value': 'R', 'category': 'rentals', 'description': 'بادئة رقم الإيجار'},
            {'key': 'rental_number_counter', 'value': '1000', 'category': 'rentals', 'description': 'العداد الحالي', 'data_type': 'integer'},
            
            # ============ إعدادات الأمان ============
            {'key': 'session_timeout', 'value': '3600', 'category': 'security', 'description': 'مهلة الجلسة بالثواني', 'data_type': 'integer'},
            {'key': 'max_login_attempts', 'value': '5', 'category': 'security', 'description': 'أقصى محاولات دخول فاشلة', 'data_type': 'integer'},
            {'key': 'password_min_length', 'value': '6', 'category': 'security', 'description': 'أقل طول لكلمة المرور', 'data_type': 'integer'},
        ]
        
        try:
            with db_manager.session_scope() as session:
                from database.models import Setting
                
                for setting_data in default_settings:
                    # التحقق من عدم وجود الإعداد
                    existing = session.query(Setting).filter_by(key=setting_data['key']).first()
                    if not existing:
                        setting = Setting(**setting_data)
                        session.add(setting)
                
                logging.info("✅ تم إضافة الإعدادات الافتراضية")
                
        except Exception as e:
            logging.error(f"❌ خطأ في إضافة الإعدادات: {e}")
    
    def get_next_number(self, prefix_key, counter_key):
        """توليد رقم تسلسلي جديد (للعقارات، العملاء، العقود، إلخ)"""
        try:
            with db_manager.session_scope() as session:
                from database.models import Setting
                
                prefix_setting = session.query(Setting).filter_by(key=prefix_key).first()
                counter_setting = session.query(Setting).filter_by(key=counter_key).first()
                
                prefix = prefix_setting.value if prefix_setting else "X"
                counter = int(counter_setting.value) if counter_setting and counter_setting.value else 1000

                new_number = f"{prefix}-{counter:05d}"

                if counter_setting:
                    counter_setting.value = str(counter + 1)
                else:
                    session.add(Setting(
                        key=counter_key,
                        value=str(counter + 1),
                        category="system",
                        description="عداد تسلسلي",
                    ))

                return new_number
                
        except Exception as e:
            logging.error(f"خطأ في توليد الرقم: {e}")
            return None
    
    def backup_before_migration(self):
        """إنشاء نسخة احتياطية قبل التحديث"""
        try:
            import shutil
            from datetime import datetime
            from config.settings import Settings
            
            backup_name = f"pre_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = Settings.BACKUP_DIR / backup_name
            
            shutil.copy2(Settings.DATABASE_PATH, backup_path)
            logging.info(f"✅ تم إنشاء نسخة احتياطية: {backup_name}")
            return True
            
        except Exception as e:
            logging.error(f"❌ خطأ في النسخ الاحتياطي: {e}")
            return False
    
    def add_column_if_not_exists(self, table_name, column_name, column_type):
        """إضافة عمود جديد إذا لم يكن موجوداً"""
        try:
            columns = [col['name'] for col in self.inspector.get_columns(table_name)]
            
            if column_name not in columns:
                with self.engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
                    conn.commit()
                logging.info(f"✅ تم إضافة العمود {column_name} للجدول {table_name}")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"❌ خطأ في إضافة العمود: {e}")
            return False


# إنشاء مدير التحديثات
migration_manager = MigrationManager()