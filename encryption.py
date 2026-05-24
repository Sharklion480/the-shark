# utils/encryption.py
"""
التشفير وكلمات المرور
"""

import bcrypt
from cryptography.fernet import Fernet
from pathlib import Path
from config.settings import Settings


class Encryption:

    @staticmethod
    def generate_key():
        """انشاء مفتاح تشفير جديد"""
        key = Fernet.generate_key()
        with open(Settings.ENCRYPTION_KEY_FILE, 'wb') as f:
            f.write(key)
        return key

    @staticmethod
    def get_key():
        """الحصول على مفتاح التشفير"""
        if not Settings.ENCRYPTION_KEY_FILE.exists():
            return Encryption.generate_key()
        
        with open(Settings.ENCRYPTION_KEY_FILE, 'rb') as f:
            return f.read()

    @staticmethod
    def encrypt(data):
        """تشفير بيانات"""
        if not data:
            return None
        
        fernet = Fernet(Encryption.get_key())
        return fernet.encrypt(str(data).encode('utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(encrypted_data):
        """فك تشفير البيانات"""
        if not encrypted_data:
            return None
        
        try:
            fernet = Fernet(Encryption.get_key())
            return fernet.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
        except:
            return None

    @staticmethod
    def hash_password(password):
        """تشفير كلمة المرور"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, password_hash):
        """التحقق من كلمة المرور"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except:
            return False