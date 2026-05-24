# utils/validators.py
"""
التحقق من صحة البيانات
"""

import re
from datetime import date, datetime

class Validator:

    @staticmethod
    def is_required(value):
        if value is None:
            return False
        if isinstance(value, str) and value.strip() == '':
            return False
        return True

    @staticmethod
    def is_phone(phone):
        if not phone:
            return False
        phone = re.sub(r'\D', '', phone)
        return len(phone) == 11 and phone.startswith('01')

    @staticmethod
    def is_national_id(nid):
        """التحقق من صحة الرقم القومي المصري"""
        if not nid:
            return False
        
        nid = re.sub(r'\D', '', nid)
        
        if len(nid) != 14:
            return False
        
        if not nid.startswith(('2', '3')):
            return False
        
        return True

    @staticmethod
    def is_email(email):
        if not email:
            return True # البريد اختياري
        
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_number(value, min=None, max=None):
        try:
            number = float(value)
            if min is not None and number < min:
                return False
            if max is not None and number > max:
                return False
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_date(value):
        if not value:
            return False
        try:
            if isinstance(value, date):
                return True
            datetime.strptime(str(value), '%Y-%m-%d')
            return True
        except:
            return False

    @staticmethod
    def is_future_date(value):
        if not Validator.is_date(value):
            return False
        
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        
        return value >= date.today()

    @staticmethod
    def is_past_date(value):
        if not Validator.is_date(value):
            return False
        
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        
        return value <= date.today()

    @staticmethod
    def get_error_message(rule, *args):
        messages = {
            'required': 'هذا الحقل مطلوب',
            'phone': 'رقم الهاتف غير صحيح',
            'national_id': 'الرقم القومي غير صحيح',
            'email': 'البريد الالكتروني غير صحيح',
            'number': 'الرجاء ادخال رقم صحيح',
            'min': f'القيمة يجب ان تكون اكبر من او تساوي {args[0]}',
            'max': f'القيمة يجب ان تكون اصغر من او تساوي {args[0]}',
            'date': 'التاريخ غير صحيح',
            'future_date': 'التاريخ يجب ان يكون في المستقبل',
            'past_date': 'التاريخ يجب ان يكون في الماضي',
        }
        return messages.get(rule, 'قيمة غير صحيحة')