# database/db_manager.py
"""
مدير الاتصال بقاعدة البيانات
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import logging

from config.settings import Settings


class DatabaseManager:
    """مدير قاعدة البيانات الرئيسي"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Session = None
        self._initialize()
    
    def _initialize(self):
        """تهيئة محرك قاعدة البيانات"""
        try:
            # إنشاء محرك قاعدة البيانات
            self.engine = create_engine(
                Settings.DATABASE_URL,
                echo=False,  # True لعرض استعلامات SQL
                connect_args={
                    "check_same_thread": False,
                    "timeout": 30
                },
                poolclass=StaticPool,
            )
            
            # تفعيل المفاتيح الخارجية في SQLite
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.close()
            
            # إنشاء الجلسات
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
                bind=self.engine
            )
            
            self.Session = scoped_session(self.SessionLocal)
            
            logging.info("✅ تم الاتصال بقاعدة البيانات بنجاح")
            
        except Exception as e:
            logging.error(f"❌ فشل الاتصال بقاعدة البيانات: {e}")
            raise
    
    def create_tables(self):
        """إنشاء جميع الجداول"""
        from database.models import Base
        try:
            Base.metadata.create_all(bind=self.engine)
            logging.info("✅ تم إنشاء الجداول بنجاح")
            return True
        except Exception as e:
            logging.error(f"❌ خطأ في إنشاء الجداول: {e}")
            return False
    
    def drop_tables(self):
        """حذف جميع الجداول (للاختبار فقط)"""
        from database.models import Base
        try:
            Base.metadata.drop_all(bind=self.engine)
            logging.info("⚠️ تم حذف جميع الجداول")
            return True
        except Exception as e:
            logging.error(f"❌ خطأ في حذف الجداول: {e}")
            return False
    
    def get_session(self):
        """الحصول على جلسة جديدة"""
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self):
        """مدير سياق للجلسات (يقوم بالـ commit و rollback تلقائياً)"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"خطأ في الجلسة: {e}")
            raise
        finally:
            session.close()
    
    def close(self):
        """إغلاق الاتصال"""
        if self.Session:
            self.Session.remove()
        if self.engine:
            self.engine.dispose()
        logging.info("تم إغلاق الاتصال بقاعدة البيانات")
    
    def test_connection(self):
        """اختبار الاتصال"""
        try:
            with self.session_scope() as session:
                from sqlalchemy import text
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logging.error(f"فشل اختبار الاتصال: {e}")
            return False
    
    def execute_raw(self, query, params=None):
        """تنفيذ استعلام SQL مباشر"""
        try:
            with self.session_scope() as session:
                from sqlalchemy import text
                result = session.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logging.error(f"خطأ في تنفيذ الاستعلام: {e}")
            return None
    
    def get_database_size(self):
        """الحصول على حجم قاعدة البيانات بالميجابايت"""
        try:
            size_bytes = Settings.DATABASE_PATH.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            return round(size_mb, 2)
        except Exception:
            return 0
    
    def vacuum(self):
        """تنظيف قاعدة البيانات وضغطها"""
        try:
            with self.engine.connect() as conn:
                from sqlalchemy import text
                conn.execute(text("VACUUM"))
                conn.commit()
            logging.info("✅ تم تنظيف قاعدة البيانات")
            return True
        except Exception as e:
            logging.error(f"خطأ في تنظيف قاعدة البيانات: {e}")
            return False


# إنشاء مدير قاعدة البيانات العام (Singleton)
db_manager = DatabaseManager()