# database/models.py
"""
نماذج جداول قاعدة البيانات
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Date,
    Text, ForeignKey, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


# ============================================================
# 1️⃣ جدول المستخدمين
# ============================================================
class User(Base):
    """المستخدمون والموظفون"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    role = Column(String(20), nullable=False, default='viewer')
    permissions = Column(Text)  # JSON string
    avatar = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # العلاقات
    created_properties = relationship("Property", back_populates="creator", foreign_keys="[Property.created_by]")
    created_sales = relationship("Sale", back_populates="creator")
    created_rentals = relationship("Rental", back_populates="creator")
    created_contracts = relationship("Contract", back_populates="creator")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("ActivityLog", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


# ============================================================
# 2️⃣ جدول العقارات
# ============================================================
class Property(Base):
    """العقارات"""
    __tablename__ = 'properties'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_number = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    property_type = Column(String(30), nullable=False, index=True)
    status = Column(String(20), nullable=False, default='for_sale', index=True)
    
    # السعر والمساحة
    price = Column(Float, nullable=False, default=0)
    area = Column(Float, nullable=False, default=0)
    price_per_meter = Column(Float, default=0)
    
    # الموقع
    address = Column(String(500))
    city = Column(String(50), index=True)
    district = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # تفاصيل العقار
    bedrooms = Column(Integer, default=0)
    bathrooms = Column(Integer, default=0)
    floor = Column(Integer)
    total_floors = Column(Integer)
    age = Column(Integer)  # عمر العقار بالسنوات
    finishing = Column(String(50))  # نوع التشطيب
    
    # وصف
    description = Column(Text)
    features = Column(Text)  # JSON string للمميزات
    
    # بيانات الشراء
    purchase_price = Column(Float, default=0)
    purchase_date = Column(Date)
    
    # العلاقات
    owner_id = Column(Integer, ForeignKey('clients.id'))
    created_by = Column(Integer, ForeignKey('users.id'))
    
    # التواريخ
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # العلاقات
    owner = relationship("Client", back_populates="owned_properties", foreign_keys=[owner_id])
    creator = relationship("User", back_populates="created_properties", foreign_keys=[created_by])
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")
    sales = relationship("Sale", back_populates="property", cascade="all, delete-orphan")
    rentals = relationship("Rental", back_populates="property", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="property")
    expenses = relationship("Expense", back_populates="property", cascade="all, delete-orphan")
    revenues = relationship("Revenue", back_populates="property", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_property_search', 'property_type', 'status', 'city'),
    )
    
    def __repr__(self):
        return f"<Property(id={self.id}, number={self.property_number}, title={self.title})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'property_number': self.property_number,
            'title': self.title,
            'property_type': self.property_type,
            'status': self.status,
            'price': self.price,
            'area': self.area,
            'address': self.address,
            'city': self.city,
            'district': self.district,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


# ============================================================
# 3️⃣ جدول صور العقارات
# ============================================================
class PropertyImage(Base):
    """صور العقارات"""
    __tablename__ = 'property_images'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('properties.id', ondelete='CASCADE'), nullable=False)
    image_path = Column(String(500), nullable=False)
    thumbnail_path = Column(String(500))
    is_primary = Column(Boolean, default=False)
    description = Column(String(200))
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    
    # العلاقات
    property = relationship("Property", back_populates="images")
    
    def __repr__(self):
        return f"<PropertyImage(id={self.id}, property_id={self.property_id})>"


# ============================================================
# 4️⃣ جدول العملاء
# ============================================================
class Client(Base):
    """العملاء"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(20), unique=True, index=True)
    full_name = Column(String(100), nullable=False, index=True)
    phone = Column(String(20), nullable=False, index=True)
    phone2 = Column(String(20))
    email = Column(String(100), index=True)
    national_id = Column(String(20), unique=True, index=True)
    
    # العنوان
    address = Column(String(500))
    city = Column(String(50))
    
    # تفاصيل إضافية
    client_type = Column(String(20), default='buyer')  # buyer, seller, tenant, owner, both
    occupation = Column(String(100))
    company = Column(String(100))
    notes = Column(Text)
    
    # حالة العميل
    is_active = Column(Boolean, default=True)
    is_blacklisted = Column(Boolean, default=False)
    blacklist_reason = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # العلاقات
    owned_properties = relationship("Property", back_populates="owner", foreign_keys="[Property.owner_id]")
    purchases = relationship("Sale", back_populates="buyer", foreign_keys="[Sale.buyer_id]")
    sales_made = relationship("Sale", back_populates="seller", foreign_keys="[Sale.seller_id]")
    rentals_as_tenant = relationship("Rental", back_populates="tenant", foreign_keys="[Rental.tenant_id]")
    rentals_as_owner = relationship("Rental", back_populates="owner", foreign_keys="[Rental.owner_id]")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name={self.full_name}, phone={self.phone})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_code': self.client_code,
            'full_name': self.full_name,
            'phone': self.phone,
            'phone2': self.phone2,
            'email': self.email,
            'national_id': self.national_id,
            'address': self.address,
            'city': self.city,
            'client_type': self.client_type,
            'is_active': self.is_active,
        }


# ============================================================
# 5️⃣ جدول عمليات البيع والشراء
# ============================================================
class Sale(Base):
    """عمليات البيع والشراء"""
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_number = Column(String(20), unique=True, index=True)
    sale_type = Column(String(20), nullable=False)  # sale, purchase
    
    # العلاقات
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('clients.id'))
    buyer_id = Column(Integer, ForeignKey('clients.id'))
    
    # الأسعار
    sale_price = Column(Float, nullable=False, default=0)
    purchase_price = Column(Float, default=0)
    profit = Column(Float, default=0)
    commission = Column(Float, default=0)
    commission_percentage = Column(Float, default=0)
    taxes = Column(Float, default=0)
    other_fees = Column(Float, default=0)
    net_profit = Column(Float, default=0)
    
    # طريقة الدفع
    payment_method = Column(String(30))
    is_installment = Column(Boolean, default=False)
    down_payment = Column(Float, default=0)
    installment_count = Column(Integer, default=0)
    installment_amount = Column(Float, default=0)
    
    # التواريخ
    sale_date = Column(Date, nullable=False, default=datetime.now)
    
    # ملاحظات
    notes = Column(Text)
    status = Column(String(20), default='completed')  # pending, completed, cancelled
    
    # المنشئ
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # العلاقات
    property = relationship("Property", back_populates="sales")
    buyer = relationship("Client", back_populates="purchases", foreign_keys=[buyer_id])
    seller = relationship("Client", back_populates="sales_made", foreign_keys=[seller_id])
    creator = relationship("User", back_populates="created_sales")
    
    def __repr__(self):
        return f"<Sale(id={self.id}, type={self.sale_type}, price={self.sale_price})>"
    
    def calculate_profit(self):
        """حساب الربح تلقائياً"""
        self.profit = (self.sale_price or 0) - (self.purchase_price or 0)
        self.net_profit = (
            self.profit
            - (self.commission or 0)
            - (self.taxes or 0)
            - (self.other_fees or 0)
        )
        return self.net_profit


# ============================================================
# 6️⃣ جدول الإيجارات
# ============================================================
class Rental(Base):
    """عقود الإيجار"""
    __tablename__ = 'rentals'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    rental_number = Column(String(20), unique=True, index=True)
    
    # العلاقات
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    tenant_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('clients.id'))
    
    # الإيجار
    monthly_rent = Column(Float, nullable=False)
    deposit = Column(Float, default=0)
    commission = Column(Float, default=0)
    
    # المدة
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    duration_months = Column(Integer, default=12)
    
    # الدفع
    payment_day = Column(Integer, default=1)  # يوم الدفع من الشهر
    payment_method = Column(String(30))
    
    # الحالة
    status = Column(String(20), default='active')  # active, expired, cancelled, completed
    
    # ملاحظات
    notes = Column(Text)
    terms = Column(Text)
    
    # المنشئ
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # العلاقات
    property = relationship("Property", back_populates="rentals")
    tenant = relationship("Client", back_populates="rentals_as_tenant", foreign_keys=[tenant_id])
    owner = relationship("Client", back_populates="rentals_as_owner", foreign_keys=[owner_id])
    creator = relationship("User", back_populates="created_rentals")
    payments = relationship("RentalPayment", back_populates="rental", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Rental(id={self.id}, property_id={self.property_id}, rent={self.monthly_rent})>"
    
    def days_until_expiry(self):
        """حساب الأيام المتبقية لانتهاء العقد"""
        from datetime import date
        if self.end_date:
            delta = self.end_date - date.today()
            return delta.days
        return None


# ============================================================
# 7️⃣ جدول دفعات الإيجار
# ============================================================
class RentalPayment(Base):
    """دفعات الإيجار الشهرية"""
    __tablename__ = 'rental_payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    rental_id = Column(Integer, ForeignKey('rentals.id', ondelete='CASCADE'), nullable=False)
    
    # المبلغ
    amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0)
    
    # التواريخ
    due_date = Column(Date, nullable=False, index=True)
    paid_date = Column(Date)
    
    # الحالة
    status = Column(String(20), default='pending', index=True)  # pending, paid, overdue, partial, cancelled
    
    # طريقة الدفع
    payment_method = Column(String(30))
    receipt_number = Column(String(50))
    
    # ملاحظات
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # العلاقات
    rental = relationship("Rental", back_populates="payments")
    
    def __repr__(self):
        return f"<RentalPayment(id={self.id}, amount={self.amount}, status={self.status})>"


# ============================================================
# 8️⃣ جدول العقود
# ============================================================
class Contract(Base):
    """العقود (بيع - شراء - إيجار)"""
    __tablename__ = 'contracts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_number = Column(String(30), unique=True, nullable=False, index=True)
    contract_type = Column(String(20), nullable=False, index=True)  # sale, purchase, rental
    
    # الأطراف
    property_id = Column(Integer, ForeignKey('properties.id'))
    party1_id = Column(Integer, ForeignKey('clients.id'))  # البائع/المؤجر
    party2_id = Column(Integer, ForeignKey('clients.id'))  # المشتري/المستأجر
    
    # التواريخ والمبالغ
    contract_date = Column(Date, default=datetime.now)
    start_date = Column(Date)
    end_date = Column(Date)
    amount = Column(Float, default=0)
    
    # المحتوى
    title = Column(String(200))
    content = Column(Text)  # محتوى العقد الكامل
    terms = Column(Text)  # الشروط والبنود
    
    # التوقيعات
    party1_signature = Column(Text)  # توقيع رقمي (base64)
    party2_signature = Column(Text)
    witness_signature = Column(Text)
    
    # الملفات
    pdf_file = Column(String(500))
    template_used = Column(String(100))
    
    # الحالة
    status = Column(String(20), default='draft', index=True)  # draft, active, expired, cancelled, completed
    is_archived = Column(Boolean, default=False)
    
    # المنشئ
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # العلاقات
    property = relationship("Property", back_populates="contracts")
    party1 = relationship("Client", foreign_keys=[party1_id])
    party2 = relationship("Client", foreign_keys=[party2_id])
    creator = relationship("User", back_populates="created_contracts")
    
    def __repr__(self):
        return f"<Contract(id={self.id}, number={self.contract_number}, type={self.contract_type})>"


# ============================================================
# 9️⃣ جدول المصروفات
# ============================================================
class Expense(Base):
    """المصروفات"""
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    
    category = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    expense_date = Column(Date, nullable=False, default=datetime.now, index=True)
    
    # المستفيد
    payee = Column(String(100))
    payment_method = Column(String(30))
    receipt_number = Column(String(50))
    receipt_image = Column(String(500))
    
    # المنشئ
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    
    # العلاقات
    property = relationship("Property", back_populates="expenses")
    
    def __repr__(self):
        return f"<Expense(id={self.id}, category={self.category}, amount={self.amount})>"


# ============================================================
# 🔟 جدول الإيرادات
# ============================================================
class Revenue(Base):
    """الإيرادات"""
    __tablename__ = 'revenues'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    
    source = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    revenue_date = Column(Date, nullable=False, default=datetime.now, index=True)
    
    # المصدر
    payer = Column(String(100))
    payment_method = Column(String(30))
    receipt_number = Column(String(50))
    
    # المنشئ
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    
    # العلاقات
    property = relationship("Property", back_populates="revenues")
    
    def __repr__(self):
        return f"<Revenue(id={self.id}, source={self.source}, amount={self.amount})>"


# ============================================================
# 1️⃣1️⃣ جدول الإشعارات
# ============================================================
class Notification(Base):
    """الإشعارات"""
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(30), nullable=False, index=True)
    
    # المرجع
    related_table = Column(String(50))
    related_id = Column(Integer)
    
    # الحالة
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime)
    
    # الأولوية
    priority = Column(String(20), default='normal')  # low, normal, high, urgent
    
    created_at = Column(DateTime, default=datetime.now, index=True)
    
    # العلاقات
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, title={self.title}, is_read={self.is_read})>"


# ============================================================
# 1️⃣2️⃣ جدول سجل النشاطات
# ============================================================
class ActivityLog(Base):
    """سجل نشاطات المستخدمين"""
    __tablename__ = 'activity_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    action = Column(String(50), nullable=False, index=True)  # create, update, delete, login, logout
    table_name = Column(String(50), index=True)
    record_id = Column(Integer)
    
    # التفاصيل
    description = Column(Text)
    old_values = Column(Text)  # JSON
    new_values = Column(Text)  # JSON
    
    # معلومات إضافية
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.now, index=True)
    
    # العلاقات
    user = relationship("User", back_populates="activities")
    
    def __repr__(self):
        return f"<ActivityLog(id={self.id}, action={self.action}, user_id={self.user_id})>"


# ============================================================
# 1️⃣3️⃣ جدول الإعدادات
# ============================================================
class Setting(Base):
    """إعدادات النظام"""
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text)
    category = Column(String(50), default='general', index=True)
    description = Column(String(255))
    data_type = Column(String(20), default='string')  # string, integer, float, boolean, json
    is_editable = Column(Boolean, default=True)
    
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Setting(key={self.key}, value={self.value})>"