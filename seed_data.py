# database/seed_data.py
"""
إضافة بيانات تجريبية للاختبار
"""

import logging
import bcrypt
import json
from datetime import datetime, date, timedelta
from database.db_manager import db_manager
from database.models import (
    User, Property, PropertyImage, Client, 
    Sale, Rental, RentalPayment, Contract,
    Expense, Revenue, Notification
)
from config.constants import DEFAULT_ROLE_PERMISSIONS


class SeedData:
    """فئة إضافة البيانات التجريبية"""
    
    @staticmethod
    def hash_password(password):
        """تشفير كلمة المرور"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @classmethod
    def create_default_admin(cls):
        """إنشاء حساب المدير الافتراضي"""
        try:
            with db_manager.session_scope() as session:
                # التحقق من وجود المدير
                existing_admin = session.query(User).filter_by(username='admin').first()
                if existing_admin:
                    logging.info("ℹ️ حساب المدير موجود بالفعل")
                    return False
                
                admin = User(
                    username='admin',
                    password_hash=cls.hash_password('admin123'),
                    full_name='المدير العام',
                    email='admin@realestate.com',
                    phone='01000000000',
                    role='admin',
                    permissions=json.dumps(DEFAULT_ROLE_PERMISSIONS['admin']),
                    is_active=True
                )
                session.add(admin)
                logging.info("✅ تم إنشاء حساب المدير الافتراضي")
                logging.info("👤 اسم المستخدم: admin")
                logging.info("🔑 كلمة المرور: admin123")
                return True
                
        except Exception as e:
            logging.error(f"❌ خطأ في إنشاء المدير: {e}")
            return False
    
    @classmethod
    def create_sample_users(cls):
        """إنشاء مستخدمين تجريبيين"""
        try:
            with db_manager.session_scope() as session:
                users_data = [
                    {
                        'username': 'sales1',
                        'password': 'sales123',
                        'full_name': 'أحمد محمد',
                        'email': 'ahmed@realestate.com',
                        'phone': '01111111111',
                        'role': 'sales',
                    },
                    {
                        'username': 'rental1',
                        'password': 'rental123',
                        'full_name': 'محمود علي',
                        'email': 'mahmoud@realestate.com',
                        'phone': '01222222222',
                        'role': 'rental',
                    },
                    {
                        'username': 'accountant1',
                        'password': 'acc123',
                        'full_name': 'فاطمة حسن',
                        'email': 'fatma@realestate.com',
                        'phone': '01333333333',
                        'role': 'accountant',
                    },
                ]
                
                for user_data in users_data:
                    existing = session.query(User).filter_by(username=user_data['username']).first()
                    if not existing:
                        user = User(
                            username=user_data['username'],
                            password_hash=cls.hash_password(user_data['password']),
                            full_name=user_data['full_name'],
                            email=user_data['email'],
                            phone=user_data['phone'],
                            role=user_data['role'],
                            permissions=json.dumps(DEFAULT_ROLE_PERMISSIONS[user_data['role']]),
                            is_active=True
                        )
                        session.add(user)
                
                logging.info("✅ تم إنشاء المستخدمين التجريبيين")
                return True
                
        except Exception as e:
            logging.error(f"❌ خطأ في إنشاء المستخدمين: {e}")
            return False
    
    @classmethod
    def create_sample_clients(cls):
        """إنشاء عملاء تجريبيين"""
        try:
            with db_manager.session_scope() as session:
                clients_data = [
                    {
                        'client_code': 'C-01001',
                        'full_name': 'محمد أحمد السيد',
                        'phone': '01012345678',
                        'email': 'mohamed@example.com',
                        'national_id': '29001011234567',
                        'address': '123 شارع التحرير، القاهرة',
                        'city': 'القاهرة',
                        'client_type': 'buyer',
                        'occupation': 'مهندس',
                    },
                    {
                        'client_code': 'C-01002',
                        'full_name': 'سارة محمود حسن',
                        'phone': '01098765432',
                        'email': 'sara@example.com',
                        'national_id': '29105051234567',
                        'address': '45 شارع النيل، الجيزة',
                        'city': 'الجيزة',
                        'client_type': 'tenant',
                        'occupation': 'طبيبة',
                    },
                    {
                        'client_code': 'C-01003',
                        'full_name': 'علي حسين عبدالله',
                        'phone': '01155556666',
                        'email': 'ali@example.com',
                        'national_id': '28805051234567',
                        'address': '78 شارع الجامعة، الإسكندرية',
                        'city': 'الإسكندرية',
                        'client_type': 'seller',
                        'occupation': 'رجل أعمال',
                    },
                    {
                        'client_code': 'C-01004',
                        'full_name': 'منى السيد إبراهيم',
                        'phone': '01277778888',
                        'email': 'mona@example.com',
                        'national_id': '29307071234567',
                        'address': '12 شارع المعادي، القاهرة',
                        'city': 'القاهرة',
                        'client_type': 'owner',
                        'occupation': 'محامية',
                    },
                ]
                
                for client_data in clients_data:
                    existing = session.query(Client).filter_by(client_code=client_data['client_code']).first()
                    if not existing:
                        client = Client(**client_data, is_active=True)
                        session.add(client)
                
                logging.info("✅ تم إنشاء العملاء التجريبيين")
                return True
                
        except Exception as e:
            logging.error(f"❌ خطأ في إنشاء العملاء: {e}")
            return False
    
    @classmethod
    def create_sample_properties(cls):
        """إنشاء عقارات تجريبية"""
        try:
            with db_manager.session_scope() as session:
                # الحصول على المالكين
                admin = session.query(User).filter_by(username='admin').first()
                owner = session.query(Client).filter_by(client_code='C-01004').first()
                
                properties_data = [
                    {
                        'property_number': 'P-01001',
                        'title': 'شقة فاخرة بالمعادي',
                        'property_type': 'apartment',
                        'status': 'for_sale',
                        'price': 2500000,
                        'area': 180,
                        'address': 'شارع 9، المعادي، القاهرة',
                        'city': 'القاهرة',
                        'district': 'المعادي',
                        'bedrooms': 3,
                        'bathrooms': 2,
                        'floor': 5,
                        'total_floors': 10,
                        'age': 2,
                        'finishing': 'سوبر لوكس',
                        'description': 'شقة فاخرة بإطلالة رائعة، تشطيب سوبر لوكس، مدخل خاص',
                        'purchase_price': 2000000,
                    },
                    {
                        'property_number': 'P-01002',
                        'title': 'فيلا في القاهرة الجديدة',
                        'property_type': 'villa',
                        'status': 'for_sale',
                        'price': 8500000,
                        'area': 500,
                        'address': 'الحي الأول، التجمع الخامس',
                        'city': 'القاهرة',
                        'district': 'القاهرة الجديدة',
                        'bedrooms': 5,
                        'bathrooms': 4,
                        'floor': 0,
                        'total_floors': 2,
                        'age': 1,
                        'finishing': 'سوبر لوكس',
                        'description': 'فيلا فاخرة بحديقة كبيرة وحمام سباحة',
                        'purchase_price': 7000000,
                    },
                    {
                        'property_number': 'P-01003',
                        'title': 'محل تجاري بوسط البلد',
                        'property_type': 'shop',
                        'status': 'for_rent',
                        'price': 15000,
                        'area': 80,
                        'address': 'شارع طلعت حرب، وسط البلد',
                        'city': 'القاهرة',
                        'district': 'وسط البلد',
                        'description': 'محل تجاري بموقع مميز، واجهة زجاجية كبيرة',
                    },
                    {
                        'property_number': 'P-01004',
                        'title': 'أرض للبيع بالشيخ زايد',
                        'property_type': 'land',
                        'status': 'for_sale',
                        'price': 4000000,
                        'area': 600,
                        'address': 'الحي الثامن، الشيخ زايد',
                        'city': 'الجيزة',
                        'district': 'الشيخ زايد',
                        'description': 'قطعة أرض على ناصية بموقع مميز',
                    },
                    {
                        'property_number': 'P-01005',
                        'title': 'مكتب إداري بالمهندسين',
                        'property_type': 'office',
                        'status': 'for_rent',
                        'price': 25000,
                        'area': 150,
                        'address': 'شارع جامعة الدول، المهندسين',
                        'city': 'الجيزة',
                        'district': 'المهندسين',
                        'floor': 8,
                        'total_floors': 15,
                        'finishing': 'لوكس',
                        'description': 'مكتب إداري بإطلالة على النيل',
                    },
                ]
                
                for prop_data in properties_data:
                    existing = session.query(Property).filter_by(property_number=prop_data['property_number']).first()
                    if not existing:
                        prop_data['price_per_meter'] = prop_data['price'] / prop_data['area'] if prop_data['area'] > 0 else 0
                        if owner:
                            prop_data['owner_id'] = owner.id
                        if admin:
                            prop_data['created_by'] = admin.id
                        
                        property_obj = Property(**prop_data)
                        session.add(property_obj)
                
                logging.info("✅ تم إنشاء العقارات التجريبية")
                return True
                
        except Exception as e:
            logging.error(f"❌ خطأ في إنشاء العقارات: {e}")
            return False
    
    @classmethod
    def create_sample_notifications(cls):
        """إنشاء إشعارات تجريبية"""
        try:
            with db_manager.session_scope() as session:
                admin = session.query(User).filter_by(username='admin').first()
                if not admin:
                    return False
                
                notifications_data = [
                    {
                        'title': 'مرحباً بك في النظام',
                        'message': 'نرحب بك في نظام إدارة الاستثمار العقاري',
                        'notification_type': 'info',
                        'priority': 'normal',
                    },
                    {
                        'title': 'تذكير: مراجعة العقود',
                        'message': 'يوجد 3 عقود قاربت على الانتهاء، يرجى المراجعة',
                        'notification_type': 'contract_expiry',
                        'priority': 'high',
                    },
                    {
                        'title': 'نسخة احتياطية مطلوبة',
                        'message': 'يُنصح بعمل نسخة احتياطية للبيانات',
                        'notification_type': 'system',
                        'priority': 'normal',
                    },
                ]
                
                for notif_data in notifications_data:
                    notification = Notification(
                        user_id=admin.id,
                        **notif_data,
                        is_read=False
                    )
                    session.add(notification)
                
                logging.info("✅ تم إنشاء الإشعارات التجريبية")
                return True
                
        except Exception as e:
            logging.error(f"❌ خطأ في إنشاء الإشعارات: {e}")
            return False
    
    @classmethod
    def seed_all(cls, with_samples=True):
        """تشغيل كل البيانات التجريبية"""
        logging.info("=" * 50)
        logging.info("🌱 بدء إضافة البيانات التجريبية...")
        logging.info("=" * 50)
        
        # إنشاء حساب المدير دائماً
        cls.create_default_admin()
        
        # البيانات التجريبية (اختياري)
        if with_samples:
            cls.create_sample_users()
            cls.create_sample_clients()
            cls.create_sample_properties()
            cls.create_sample_notifications()
        
        logging.info("=" * 50)
        logging.info("✅ اكتملت عملية إضافة البيانات")
        logging.info("=" * 50)


# دالة سريعة للاستخدام
def seed_database(with_samples=True):
    """تهيئة قاعدة البيانات بالبيانات التجريبية"""
    SeedData.seed_all(with_samples=with_samples)