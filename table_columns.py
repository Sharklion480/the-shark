# views/table_columns.py
"""تعريف أعمدة جداول العرض"""

PROPERTY_COLUMNS = [
    {"key": "property_number", "title": "الرقم", "width": 90},
    {"key": "title", "title": "العنوان", "width": 200},
    {"key": "property_type", "title": "النوع", "width": 100},
    {"key": "status", "title": "الحالة", "width": 90, "color": "status_color"},
    {"key": "price", "title": "السعر", "width": 120},
    {"key": "city", "title": "المدينة", "width": 100},
    {"key": "area", "title": "المساحة", "width": 80},
]

CLIENT_COLUMNS = [
    {"key": "client_code", "title": "الكود", "width": 80},
    {"key": "full_name", "title": "الاسم", "width": 180},
    {"key": "phone", "title": "الهاتف", "width": 120},
    {"key": "client_type", "title": "النوع", "width": 90},
    {"key": "city", "title": "المدينة", "width": 100},
    {"key": "is_active", "title": "الحالة", "width": 80},
]

SALE_COLUMNS = [
    {"key": "sale_number", "title": "رقم العملية", "width": 100},
    {"key": "property", "title": "العقار", "width": 180},
    {"key": "sale_price", "title": "السعر", "width": 120},
    {"key": "sale_date", "title": "التاريخ", "width": 100},
    {"key": "status", "title": "الحالة", "width": 90},
]

RENTAL_COLUMNS = [
    {"key": "rental_number", "title": "رقم العقد", "width": 100},
    {"key": "property", "title": "العقار", "width": 160},
    {"key": "tenant", "title": "المستأجر", "width": 140},
    {"key": "monthly_rent", "title": "الإيجار الشهري", "width": 120},
    {"key": "end_date", "title": "تاريخ الانتهاء", "width": 110},
    {"key": "status", "title": "الحالة", "width": 80},
]

CONTRACT_COLUMNS = [
    {"key": "contract_number", "title": "رقم العقد", "width": 110},
    {"key": "contract_type", "title": "النوع", "width": 100},
    {"key": "title", "title": "العنوان", "width": 160},
    {"key": "amount", "title": "المبلغ", "width": 120},
    {"key": "contract_date", "title": "التاريخ", "width": 100},
    {"key": "status", "title": "الحالة", "width": 90},
]

NOTIFICATION_COLUMNS = [
    {"key": "title", "title": "العنوان", "width": 180},
    {"key": "message", "title": "الرسالة", "width": 220},
    {"key": "notification_type", "title": "النوع", "width": 100},
    {"key": "priority", "title": "الأولوية", "width": 80},
    {"key": "is_read", "title": "الحالة", "width": 80},
    {"key": "created_at", "title": "التاريخ", "width": 100},
]
