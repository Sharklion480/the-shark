# controllers/auth_controller.py
from datetime import datetime
from database.db_manager import db_manager
from database.models import User
from utils.encryption import Encryption
from utils.logger import logger


class AuthController:

    current_user = None
    login_time = None

    @classmethod
    def login(cls, username, password):
        """محاولة تسجيل الدخول"""

        try:
            with db_manager.session_scope() as session:
                user = session.query(User).filter_by(username=username, is_active=True).first()

                if not user:
                    logger.warning(f"محاولة دخول فاشلة باسم مستخدم غير موجود: {username}")
                    return False, "اسم المستخدم او كلمة المرور غير صحيحة"

                if not Encryption.verify_password(password, user.password_hash):
                    logger.warning(f"محاولة دخول فاشلة للمستخدم {username}")
                    return False, "اسم المستخدم او كلمة المرور غير صحيحة"

                # تحديث اخر دخول
                user.last_login = datetime.now()

                cls.current_user = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': user.role,
                    'permissions': user.permissions,
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'is_active': user.is_active,
                }
                cls.login_time = datetime.now()

                logger.success(f"تم تسجيل الدخول بنجاح: {user.full_name}")

                return True, "تم تسجيل الدخول بنجاح"

        except Exception as e:
            logger.error("خطأ في تسجيل الدخول", e)
            return False, "خطأ داخلي في النظام"

    @classmethod
    def logout(cls):
        """تسجيل الخروج"""
        if cls.current_user:
            user_name = cls.current_user.get('full_name') if isinstance(cls.current_user, dict) else getattr(cls.current_user, 'full_name', '')
            logger.info(f"تم تسجيل الخروج: {user_name}")
        cls.current_user = None
        cls.login_time = None
        return True

    @classmethod
    def is_logged_in(cls):
        """التحقق من وجود مستخدم مسجل دخول"""
        return cls.current_user is not None

    @classmethod
    def has_permission(cls, permission):
        """التحقق من ان المستخدم لديه صلاحية معينة"""

        if not cls.is_logged_in():
            return False

        # المدير لديه كل الصلاحيات
        current_role = cls.current_user.get('role') if isinstance(cls.current_user, dict) else getattr(cls.current_user, 'role', None)
        if current_role == 'admin':
            return True

        import json
        try:
            permissions_value = cls.current_user.get('permissions') if isinstance(cls.current_user, dict) else getattr(cls.current_user, 'permissions', None)
            permissions = json.loads(permissions_value or '[]')
            return permission in permissions
        except (json.JSONDecodeError, TypeError):
            return False

    @classmethod
    def get_current_user(cls):
        return cls.current_user

# انشاء نسخة عامة
auth = AuthController()