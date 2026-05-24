# config/constants.py
"""
الثوابت المستخدمة في البرنامج
"""

# ============ أنواع العقارات ============
PROPERTY_TYPES = {
    "apartment": "شقة سكنية",
    "villa": "فيلا",
    "shop": "محل تجاري",
    "land": "أرض",
    "office": "مكتب إداري",
    "warehouse": "مخزن",
}

PROPERTY_TYPES_EN = {
    "apartment": "Apartment",
    "villa": "Villa",
    "shop": "Shop",
    "land": "Land",
    "office": "Office",
    "warehouse": "Warehouse",
}

# ============ حالات العقار ============
PROPERTY_STATUS = {
    "for_sale": "للبيع",
    "for_rent": "للإيجار",
    "sold": "مباع",
    "rented": "مؤجر",
    "reserved": "محجوز",
    "unavailable": "غير متاح",
}

PROPERTY_STATUS_EN = {
    "for_sale": "For Sale",
    "for_rent": "For Rent",
    "sold": "Sold",
    "rented": "Rented",
    "reserved": "Reserved",
    "unavailable": "Unavailable",
}

# ============ ألوان حالات العقار ============
PROPERTY_STATUS_COLORS = {
    "for_sale": "#2ecc71",      # أخضر
    "for_rent": "#3498db",      # أزرق
    "sold": "#95a5a6",          # رمادي
    "rented": "#9b59b6",        # بنفسجي
    "reserved": "#f39c12",      # برتقالي
    "unavailable": "#e74c3c",   # أحمر
}

# ============ أدوار المستخدمين ============
USER_ROLES = {
    "admin": "مدير النظام",
    "sales": "موظف مبيعات",
    "rental": "موظف تأجير",
    "accountant": "محاسب",
    "viewer": "مشاهد فقط",
}

USER_ROLES_EN = {
    "admin": "Administrator",
    "sales": "Sales Employee",
    "rental": "Rental Employee",
    "accountant": "Accountant",
    "viewer": "Viewer",
}

# ============ الصلاحيات ============
PERMISSIONS = {
    # العقارات
    "properties_view": "عرض العقارات",
    "properties_add": "إضافة عقارات",
    "properties_edit": "تعديل العقارات",
    "properties_delete": "حذف العقارات",
    
    # العملاء
    "clients_view": "عرض العملاء",
    "clients_add": "إضافة عملاء",
    "clients_edit": "تعديل العملاء",
    "clients_delete": "حذف العملاء",
    
    # المبيعات
    "sales_view": "عرض المبيعات",
    "sales_add": "إضافة مبيعات",
    "sales_edit": "تعديل المبيعات",
    "sales_delete": "حذف المبيعات",
    
    # الإيجارات
    "rentals_view": "عرض الإيجارات",
    "rentals_add": "إضافة إيجارات",
    "rentals_edit": "تعديل الإيجارات",
    "rentals_delete": "حذف الإيجارات",
    
    # العقود
    "contracts_view": "عرض العقود",
    "contracts_add": "إنشاء عقود",
    "contracts_edit": "تعديل العقود",
    "contracts_delete": "حذف العقود",
    
    # التقارير
    "reports_view": "عرض التقارير",
    "reports_export": "تصدير التقارير",
    
    # المستخدمون
    "users_manage": "إدارة المستخدمين",
    
    # الإعدادات
    "settings_manage": "إدارة الإعدادات",
    "backup_manage": "إدارة النسخ الاحتياطية",
}

# الصلاحيات الافتراضية لكل دور
DEFAULT_ROLE_PERMISSIONS = {
    "admin": list(PERMISSIONS.keys()),  # كل الصلاحيات
    
    "sales": [
        "properties_view", "properties_add", "properties_edit",
        "clients_view", "clients_add", "clients_edit",
        "sales_view", "sales_add", "sales_edit",
        "contracts_view", "contracts_add",
        "reports_view",
    ],
    
    "rental": [
        "properties_view", "properties_edit",
        "clients_view", "clients_add", "clients_edit",
        "rentals_view", "rentals_add", "rentals_edit",
        "contracts_view", "contracts_add",
        "reports_view",
    ],
    
    "accountant": [
        "properties_view",
        "clients_view",
        "sales_view", "rentals_view",
        "contracts_view",
        "reports_view", "reports_export",
    ],
    
    "viewer": [
        "properties_view", "clients_view",
        "sales_view", "rentals_view",
        "contracts_view", "reports_view",
    ],
}

# ============ أنواع العقود ============
CONTRACT_TYPES = {
    "sale": "عقد بيع",
    "purchase": "عقد شراء",
    "rental": "عقد إيجار",
}

CONTRACT_STATUS = {
    "draft": "مسودة",
    "active": "ساري",
    "expired": "منتهي",
    "cancelled": "ملغي",
    "completed": "مكتمل",
}

# ============ طرق الدفع ============
PAYMENT_METHODS = {
    "cash": "نقدي",
    "bank_transfer": "تحويل بنكي",
    "check": "شيك",
    "installments": "أقساط",
    "credit_card": "بطاقة ائتمان",
}

# ============ حالات الدفع ============
PAYMENT_STATUS = {
    "pending": "قيد الانتظار",
    "paid": "مدفوع",
    "overdue": "متأخر",
    "cancelled": "ملغي",
    "partial": "جزئي",
}

PAYMENT_STATUS_COLORS = {
    "pending": "#f39c12",
    "paid": "#2ecc71",
    "overdue": "#e74c3c",
    "cancelled": "#95a5a6",
    "partial": "#3498db",
}

# ============ أنواع العملاء ============
CLIENT_TYPES = {
    "buyer": "مشتري",
    "seller": "بائع",
    "tenant": "مستأجر",
    "owner": "مالك",
    "both": "متعدد",
}

# ============ أنواع الإشعارات ============
NOTIFICATION_TYPES = {
    "contract_expiry": "انتهاء عقد",
    "payment_due": "موعد سداد",
    "payment_overdue": "سداد متأخر",
    "new_property": "عقار جديد",
    "new_client": "عميل جديد",
    "system": "نظام",
    "info": "معلومات",
    "warning": "تحذير",
    "error": "خطأ",
}

# ============ أيقونات الإشعارات ============
NOTIFICATION_ICONS = {
    "contract_expiry": "📋",
    "payment_due": "💰",
    "payment_overdue": "⚠️",
    "new_property": "🏠",
    "new_client": "👤",
    "system": "⚙️",
    "info": "ℹ️",
    "warning": "⚠️",
    "error": "❌",
}

# ============ فئات المصروفات ============
EXPENSE_CATEGORIES = {
    "maintenance": "صيانة",
    "utilities": "مرافق",
    "taxes": "ضرائب",
    "insurance": "تأمين",
    "commissions": "عمولات",
    "marketing": "تسويق",
    "legal": "قانوني",
    "other": "أخرى",
}

# ============ مصادر الإيرادات ============
REVENUE_SOURCES = {
    "sale": "بيع",
    "rent": "إيجار",
    "commission": "عمولة",
    "deposit": "تأمين",
    "other": "أخرى",
}

# ============ صيغ التصدير ============
EXPORT_FORMATS = {
    "pdf": "PDF",
    "excel": "Excel",
    "word": "Word",
    "csv": "CSV",
}

# ============ رسائل النظام ============
MESSAGES = {
    "save_success": "تم الحفظ بنجاح",
    "update_success": "تم التحديث بنجاح",
    "delete_success": "تم الحذف بنجاح",
    "delete_confirm": "هل أنت متأكد من الحذف؟",
    "save_error": "حدث خطأ أثناء الحفظ",
    "update_error": "حدث خطأ أثناء التحديث",
    "delete_error": "حدث خطأ أثناء الحذف",
    "required_fields": "الرجاء ملء جميع الحقول المطلوبة",
    "invalid_data": "البيانات المدخلة غير صحيحة",
    "login_success": "تم تسجيل الدخول بنجاح",
    "login_failed": "اسم المستخدم أو كلمة المرور غير صحيحة",
    "logout_confirm": "هل تريد تسجيل الخروج؟",
    "no_permission": "ليس لديك صلاحية للقيام بهذه العملية",
    "connection_error": "خطأ في الاتصال بقاعدة البيانات",
    "backup_success": "تم إنشاء النسخة الاحتياطية بنجاح",
    "backup_error": "حدث خطأ أثناء إنشاء النسخة الاحتياطية",
    "restore_success": "تم استعادة النسخة بنجاح",
    "restore_confirm": "سيتم استبدال البيانات الحالية. هل تريد المتابعة؟",
}

# ============ أحجام النوافذ ============
WINDOW_SIZES = {
    "login": (450, 600),
    "main": (1400, 900),
    "main_min": (1200, 700),
    "dialog_small": (400, 300),
    "dialog_medium": (600, 500),
    "dialog_large": (900, 700),
    "form": (700, 600),
}

# ============ المدن المصرية (مثال) ============
EGYPTIAN_CITIES = [
    "القاهرة", "الإسكندرية", "الجيزة", "شرم الشيخ", "الغردقة",
    "الأقصر", "أسوان", "المنصورة", "طنطا", "الإسماعيلية",
    "السويس", "بورسعيد", "دمياط", "المنيا", "أسيوط",
    "سوهاج", "قنا", "بني سويف", "الفيوم", "كفر الشيخ",
    "البحيرة", "الدقهلية", "الشرقية", "الغربية", "المنوفية",
    "القليوبية", "العاشر من رمضان", "مدينة نصر", "6 أكتوبر", "الشيخ زايد",
]

# ============ الحد الأقصى لعدد الصور لكل عقار ============
MAX_PROPERTY_IMAGES = 20

# ============ إعدادات الصفحات ============
ITEMS_PER_PAGE = 25
PAGINATION_OPTIONS = [10, 25, 50, 100]