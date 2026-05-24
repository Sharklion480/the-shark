# views/entity_dialogs.py
"""نوافذ إضافة وتعديل السجلات"""

from datetime import date, timedelta

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate

from config.constants import (
    PROPERTY_TYPES, PROPERTY_STATUS, CLIENT_TYPES, EGYPTIAN_CITIES,
    CONTRACT_TYPES, CONTRACT_STATUS,
)
from utils.formatters import ar
from utils.validators import Validator
from controllers.data_controller import data


class _FormDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(ar(title))
        self.setMinimumWidth(480)
        self.setLayoutDirection(Qt.RightToLeft)
        self._form = QFormLayout()
        self._form.setLabelAlignment(Qt.AlignRight)
        self._form.setFormAlignment(Qt.AlignRight)
        root = QVBoxLayout(self)
        root.addLayout(self._form)
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

    def _validate_and_accept(self):
        ok, msg = self.validate()
        if ok:
            self.accept()
        else:
            QMessageBox.warning(self, ar("تنبيه"), ar(msg))

    def validate(self):
        return True, ""

    def _add_field(self, label, widget):
        self._form.addRow(ar(label), widget)
        return widget

    def _fill_combo(self, combo, items, allow_empty=False, empty_label="—"):
        combo.clear()
        if allow_empty:
            combo.addItem(ar(empty_label), None)
        for item_id, label in items:
            combo.addItem(ar(str(label)), item_id)

    def _set_combo_value(self, combo, value):
        if value is None:
            if combo.count() and combo.itemData(0) is None:
                combo.setCurrentIndex(0)
            return
        idx = combo.findData(value)
        if idx >= 0:
            combo.setCurrentIndex(idx)

    def _date_edit(self, initial=None):
        w = QDateEdit()
        w.setCalendarPopup(True)
        w.setDisplayFormat("dd/MM/yyyy")
        d = initial or date.today()
        if isinstance(d, date):
            w.setDate(QDate(d.year, d.month, d.day))
        return w

    def _date_value(self, widget):
        qd = widget.date()
        return date(qd.year(), qd.month(), qd.day())


class PropertyDialog(_FormDialog):

    def __init__(self, record_id=None, parent=None):
        title = "تعديل عقار" if record_id else "إضافة عقار"
        super().__init__(title, parent)
        self.record_id = record_id

        self.title_input = self._add_field("العنوان *", QLineEdit())
        self.type_combo = self._add_field("النوع *", QComboBox())
        for key, label in PROPERTY_TYPES.items():
            self.type_combo.addItem(ar(label), key)

        self.status_combo = self._add_field("الحالة *", QComboBox())
        for key, label in PROPERTY_STATUS.items():
            self.status_combo.addItem(ar(label), key)

        self.price_input = self._add_field("السعر *", QLineEdit())
        self.area_input = self._add_field("المساحة (م²) *", QLineEdit())
        self.city_combo = self._add_field("المدينة", QComboBox())
        self.city_combo.setEditable(True)
        for city in EGYPTIAN_CITIES[:15]:
            self.city_combo.addItem(ar(city), city)
        self.address_input = self._add_field("العنوان", QLineEdit())
        self.description_input = self._add_field("الوصف", QTextEdit())
        self.description_input.setMaximumHeight(80)

        if record_id:
            self._load(record_id)

    def _load(self, record_id):
        rec = data.get_property(record_id)
        if not rec:
            return
        self.title_input.setText(rec.get("title", ""))
        idx = self.type_combo.findData(rec.get("property_type"))
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)
        idx = self.status_combo.findData(rec.get("status"))
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)
        self.price_input.setText(str(rec.get("price", 0)))
        self.area_input.setText(str(rec.get("area", 0)))
        self.city_combo.setEditText(rec.get("city", ""))
        self.address_input.setText(rec.get("address", ""))
        self.description_input.setPlainText(rec.get("description", ""))

    def validate(self):
        if not Validator.is_required(self.title_input.text()):
            return False, "الرجاء إدخال عنوان العقار"
        if not Validator.is_number(self.price_input.text(), min=0):
            return False, "السعر غير صحيح"
        if not Validator.is_number(self.area_input.text(), min=0):
            return False, "المساحة غير صحيحة"
        return True, ""

    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "property_type": self.type_combo.currentData(),
            "status": self.status_combo.currentData(),
            "price": float(self.price_input.text().strip()),
            "area": float(self.area_input.text().strip()),
            "city": self.city_combo.currentText().strip(),
            "address": self.address_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
        }

    def save(self):
        ok, msg = data.save_property(self.get_data(), self.record_id)
        return ok, msg


class ClientDialog(_FormDialog):

    def __init__(self, record_id=None, parent=None):
        title = "تعديل عميل" if record_id else "إضافة عميل"
        super().__init__(title, parent)
        self.record_id = record_id

        self.name_input = self._add_field("الاسم الكامل *", QLineEdit())
        self.phone_input = self._add_field("الهاتف *", QLineEdit())
        self.email_input = self._add_field("البريد", QLineEdit())
        self.type_combo = self._add_field("نوع العميل", QComboBox())
        for key, label in CLIENT_TYPES.items():
            self.type_combo.addItem(ar(label), key)
        self.city_input = self._add_field("المدينة", QLineEdit())
        self.address_input = self._add_field("العنوان", QLineEdit())
        self.national_id_input = self._add_field("الرقم القومي", QLineEdit())

        if record_id:
            self._load(record_id)

    def _load(self, record_id):
        rec = data.get_client(record_id)
        if not rec:
            return
        self.name_input.setText(rec.get("full_name", ""))
        self.phone_input.setText(rec.get("phone", ""))
        self.email_input.setText(rec.get("email", ""))
        idx = self.type_combo.findData(rec.get("client_type"))
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)
        self.city_input.setText(rec.get("city", ""))
        self.address_input.setText(rec.get("address", ""))
        self.national_id_input.setText(rec.get("national_id", ""))

    def validate(self):
        if not Validator.is_required(self.name_input.text()):
            return False, "الرجاء إدخال اسم العميل"
        if not Validator.is_phone(self.phone_input.text()):
            return False, "رقم الهاتف غير صحيح (11 رقم يبدأ بـ 01)"
        email = self.email_input.text().strip()
        if email and not Validator.is_email(email):
            return False, "البريد الإلكتروني غير صحيح"
        nid = self.national_id_input.text().strip()
        if nid and not Validator.is_national_id(nid):
            return False, "الرقم القومي غير صحيح"
        return True, ""

    def get_data(self):
        return {
            "full_name": self.name_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "email": self.email_input.text().strip(),
            "client_type": self.type_combo.currentData(),
            "city": self.city_input.text().strip(),
            "address": self.address_input.text().strip(),
            "national_id": self.national_id_input.text().strip() or None,
        }

    def save(self):
        ok, msg = data.save_client(self.get_data(), self.record_id)
        return ok, msg


class SaleDialog(_FormDialog):

    SALE_TYPES = {"sale": "بيع", "purchase": "شراء"}
    SALE_STATUS = {"pending": "قيد الانتظار", "completed": "مكتمل", "cancelled": "ملغي"}

    def __init__(self, record_id=None, parent=None):
        title = "تعديل عملية بيع" if record_id else "إضافة عملية بيع"
        super().__init__(title, parent)
        self.setMinimumWidth(520)
        self.record_id = record_id

        self.type_combo = self._add_field("نوع العملية *", QComboBox())
        for key, label in self.SALE_TYPES.items():
            self.type_combo.addItem(ar(label), key)

        self.property_combo = self._add_field("العقار *", QComboBox())
        self._fill_combo(self.property_combo, data.list_properties_for_combo())

        self.seller_combo = self._add_field("البائع", QComboBox())
        self._fill_combo(self.seller_combo, data.list_clients_for_combo(), allow_empty=True)

        self.buyer_combo = self._add_field("المشتري", QComboBox())
        self._fill_combo(self.buyer_combo, data.list_clients_for_combo(), allow_empty=True)

        self.price_input = self._add_field("سعر البيع *", QLineEdit())
        self.purchase_input = self._add_field("سعر الشراء", QLineEdit())
        self.commission_input = self._add_field("العمولة", QLineEdit())
        self.status_combo = self._add_field("الحالة", QComboBox())
        for key, label in self.SALE_STATUS.items():
            self.status_combo.addItem(ar(label), key)
        self.date_input = self._add_field("تاريخ العملية *", self._date_edit())
        self.notes_input = self._add_field("ملاحظات", QTextEdit())
        self.notes_input.setMaximumHeight(70)

        if record_id:
            self._load(record_id)

    def _load(self, record_id):
        rec = data.get_sale(record_id)
        if not rec:
            return
        self._set_combo_value(self.type_combo, rec.get("sale_type"))
        self._set_combo_value(self.property_combo, rec.get("property_id"))
        self._set_combo_value(self.seller_combo, rec.get("seller_id"))
        self._set_combo_value(self.buyer_combo, rec.get("buyer_id"))
        self.price_input.setText(str(rec.get("sale_price", 0)))
        self.purchase_input.setText(str(rec.get("purchase_price", 0)))
        self.commission_input.setText(str(rec.get("commission", 0)))
        self._set_combo_value(self.status_combo, rec.get("status"))
        if rec.get("sale_date"):
            self.date_input.setDate(QDate(
                rec["sale_date"].year, rec["sale_date"].month, rec["sale_date"].day
            ))
        self.notes_input.setPlainText(rec.get("notes", ""))

    def validate(self):
        if not self.property_combo.currentData():
            return False, "اختر العقار"
        if not Validator.is_number(self.price_input.text(), min=0):
            return False, "سعر البيع غير صحيح"
        return True, ""

    def get_data(self):
        return {
            "sale_type": self.type_combo.currentData(),
            "property_id": self.property_combo.currentData(),
            "seller_id": self.seller_combo.currentData(),
            "buyer_id": self.buyer_combo.currentData(),
            "sale_price": float(self.price_input.text().strip()),
            "purchase_price": float(self.purchase_input.text().strip() or 0),
            "commission": float(self.commission_input.text().strip() or 0),
            "status": self.status_combo.currentData(),
            "sale_date": self._date_value(self.date_input),
            "notes": self.notes_input.toPlainText().strip(),
        }

    def save(self):
        return data.save_sale(self.get_data(), self.record_id)


class RentalDialog(_FormDialog):

    RENTAL_STATUS = {
        "active": "نشط",
        "expired": "منتهي",
        "cancelled": "ملغي",
        "completed": "مكتمل",
    }

    def __init__(self, record_id=None, parent=None):
        title = "تعديل عقد إيجار" if record_id else "إضافة عقد إيجار"
        super().__init__(title, parent)
        self.setMinimumWidth(520)
        self.record_id = record_id

        self.property_combo = self._add_field("العقار *", QComboBox())
        self._fill_combo(self.property_combo, data.list_properties_for_combo())

        self.tenant_combo = self._add_field("المستأجر *", QComboBox())
        self._fill_combo(self.tenant_combo, data.list_clients_for_combo())

        self.owner_combo = self._add_field("المالك", QComboBox())
        self._fill_combo(self.owner_combo, data.list_clients_for_combo(), allow_empty=True)

        self.rent_input = self._add_field("الإيجار الشهري *", QLineEdit())
        self.deposit_input = self._add_field("التأمين", QLineEdit())
        self.start_input = self._add_field("تاريخ البداية *", self._date_edit())
        self.end_input = self._add_field(
            "تاريخ النهاية *",
            self._date_edit(date.today() + timedelta(days=365)),
        )
        self.status_combo = self._add_field("الحالة", QComboBox())
        for key, label in self.RENTAL_STATUS.items():
            self.status_combo.addItem(ar(label), key)
        self.notes_input = self._add_field("ملاحظات", QTextEdit())
        self.notes_input.setMaximumHeight(70)

        if record_id:
            self._load(record_id)

    def _load(self, record_id):
        rec = data.get_rental(record_id)
        if not rec:
            return
        self._set_combo_value(self.property_combo, rec.get("property_id"))
        self._set_combo_value(self.tenant_combo, rec.get("tenant_id"))
        self._set_combo_value(self.owner_combo, rec.get("owner_id"))
        self.rent_input.setText(str(rec.get("monthly_rent", 0)))
        self.deposit_input.setText(str(rec.get("deposit", 0)))
        self._set_combo_value(self.status_combo, rec.get("status"))
        for field, widget in (("start_date", self.start_input), ("end_date", self.end_input)):
            d = rec.get(field)
            if d:
                widget.setDate(QDate(d.year, d.month, d.day))
        self.notes_input.setPlainText(rec.get("notes", ""))

    def validate(self):
        if not self.property_combo.currentData():
            return False, "اختر العقار"
        if not self.tenant_combo.currentData():
            return False, "اختر المستأجر"
        if not Validator.is_number(self.rent_input.text(), min=0):
            return False, "الإيجار الشهري غير صحيح"
        if self._date_value(self.end_input) <= self._date_value(self.start_input):
            return False, "تاريخ النهاية يجب أن يكون بعد تاريخ البداية"
        return True, ""

    def get_data(self):
        return {
            "property_id": self.property_combo.currentData(),
            "tenant_id": self.tenant_combo.currentData(),
            "owner_id": self.owner_combo.currentData(),
            "monthly_rent": float(self.rent_input.text().strip()),
            "deposit": float(self.deposit_input.text().strip() or 0),
            "start_date": self._date_value(self.start_input),
            "end_date": self._date_value(self.end_input),
            "status": self.status_combo.currentData(),
            "notes": self.notes_input.toPlainText().strip(),
        }

    def save(self):
        return data.save_rental(self.get_data(), self.record_id)


class ContractDialog(_FormDialog):

    def __init__(self, record_id=None, parent=None):
        title = "تعديل عقد" if record_id else "إضافة عقد"
        super().__init__(title, parent)
        self.setMinimumWidth(520)
        self.record_id = record_id

        self.type_combo = self._add_field("نوع العقد *", QComboBox())
        for key, label in CONTRACT_TYPES.items():
            self.type_combo.addItem(ar(label), key)

        self.title_input = self._add_field("عنوان العقد", QLineEdit())
        self.property_combo = self._add_field("العقار", QComboBox())
        self._fill_combo(self.property_combo, data.list_properties_for_combo(), allow_empty=True)

        self.party1_combo = self._add_field("الطرف الأول", QComboBox())
        self._fill_combo(self.party1_combo, data.list_clients_for_combo(), allow_empty=True)

        self.party2_combo = self._add_field("الطرف الثاني", QComboBox())
        self._fill_combo(self.party2_combo, data.list_clients_for_combo(), allow_empty=True)

        self.amount_input = self._add_field("المبلغ", QLineEdit())
        self.contract_date = self._add_field("تاريخ العقد", self._date_edit())
        self.start_date = self._add_field("تاريخ البداية", self._date_edit())
        self.end_date = self._add_field("تاريخ النهاية", self._date_edit())

        self.status_combo = self._add_field("الحالة", QComboBox())
        for key, label in CONTRACT_STATUS.items():
            self.status_combo.addItem(ar(label), key)

        self.content_input = self._add_field("ملاحظات / بنود", QTextEdit())
        self.content_input.setMaximumHeight(90)

        if record_id:
            self._load(record_id)

    def _load(self, record_id):
        rec = data.get_contract(record_id)
        if not rec:
            return
        self._set_combo_value(self.type_combo, rec.get("contract_type"))
        self.title_input.setText(rec.get("title", ""))
        self._set_combo_value(self.property_combo, rec.get("property_id"))
        self._set_combo_value(self.party1_combo, rec.get("party1_id"))
        self._set_combo_value(self.party2_combo, rec.get("party2_id"))
        self.amount_input.setText(str(rec.get("amount", 0)))
        self._set_combo_value(self.status_combo, rec.get("status"))
        for field, widget in (
            ("contract_date", self.contract_date),
            ("start_date", self.start_date),
            ("end_date", self.end_date),
        ):
            d = rec.get(field)
            if d:
                widget.setDate(QDate(d.year, d.month, d.day))
        self.content_input.setPlainText(rec.get("content", ""))

    def validate(self):
        if not self.type_combo.currentData():
            return False, "اختر نوع العقد"
        amount = self.amount_input.text().strip()
        if amount and not Validator.is_number(amount, min=0):
            return False, "المبلغ غير صحيح"
        return True, ""

    def get_data(self):
        amount_text = self.amount_input.text().strip()
        return {
            "contract_type": self.type_combo.currentData(),
            "title": self.title_input.text().strip(),
            "property_id": self.property_combo.currentData(),
            "party1_id": self.party1_combo.currentData(),
            "party2_id": self.party2_combo.currentData(),
            "amount": float(amount_text) if amount_text else 0,
            "contract_date": self._date_value(self.contract_date),
            "start_date": self._date_value(self.start_date),
            "end_date": self._date_value(self.end_date),
            "status": self.status_combo.currentData(),
            "content": self.content_input.toPlainText().strip(),
        }

    def save(self):
        return data.save_contract(self.get_data(), self.record_id)


DIALOG_MAP = {
    "properties": PropertyDialog,
    "clients": ClientDialog,
    "sales": SaleDialog,
    "rentals": RentalDialog,
    "contracts": ContractDialog,
}
