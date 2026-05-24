# controllers/data_controller.py
"""وصول البيانات للواجهات"""

from datetime import date, datetime, timedelta

from sqlalchemy import func

from database.db_manager import db_manager
from database.models import (
    Property, Client, Sale, Rental, Contract, Notification, User,
)
from config.constants import (
    PROPERTY_TYPES, PROPERTY_STATUS, PROPERTY_STATUS_COLORS,
    CLIENT_TYPES, CONTRACT_TYPES, CONTRACT_STATUS,
    USER_ROLES, NOTIFICATION_TYPES,
)
from database.migrations import migration_manager
from controllers.auth_controller import auth
from utils.formatters import format_currency, format_date
from utils.logger import logger


def _label(mapping, key, default=""):
    return mapping.get(key, default or str(key or ""))


class DataController:

    @staticmethod
    def get_dashboard_stats():
        with db_manager.session_scope() as session:
            return {
                "properties": session.query(func.count(Property.id)).scalar() or 0,
                "clients": session.query(func.count(Client.id)).scalar() or 0,
                "sales": session.query(func.count(Sale.id)).scalar() or 0,
                "rentals": session.query(func.count(Rental.id)).filter(
                    Rental.status == "active"
                ).scalar() or 0,
                "contracts": session.query(func.count(Contract.id)).scalar() or 0,
                "notifications": session.query(func.count(Notification.id)).filter(
                    Notification.is_read == False
                ).scalar() or 0,
                "sales_total": session.query(func.coalesce(func.sum(Sale.sale_price), 0)).scalar() or 0,
            }

    @staticmethod
    def get_property_status_chart():
        with db_manager.session_scope() as session:
            rows = (
                session.query(Property.status, func.count(Property.id))
                .group_by(Property.status)
                .all()
            )
            return {
                _label(PROPERTY_STATUS, status): count
                for status, count in rows
            }

    @staticmethod
    def get_properties(search=""):
        with db_manager.session_scope() as session:
            q = session.query(Property).order_by(Property.created_at.desc())
            rows = q.all()
            data = []
            for p in rows:
                row = {
                    "id": p.id,
                    "property_number": p.property_number,
                    "title": p.title,
                    "property_type": _label(PROPERTY_TYPES, p.property_type),
                    "status": _label(PROPERTY_STATUS, p.status),
                    "status_key": p.status,
                    "status_color": PROPERTY_STATUS_COLORS.get(p.status, "#64748b"),
                    "price": format_currency(p.price),
                    "city": p.city or "",
                    "area": p.area,
                }
                if search:
                    hay = " ".join(str(v) for v in row.values()).lower()
                    if search.lower() not in hay:
                        continue
                data.append(row)
            return data

    @staticmethod
    def get_clients(search=""):
        with db_manager.session_scope() as session:
            rows = session.query(Client).order_by(Client.full_name).all()
            data = []
            for c in rows:
                row = {
                    "id": c.id,
                    "client_code": c.client_code or "",
                    "full_name": c.full_name,
                    "phone": c.phone,
                    "email": c.email or "",
                    "client_type": _label(CLIENT_TYPES, c.client_type),
                    "city": c.city or "",
                    "is_active": "نشط" if c.is_active else "غير نشط",
                }
                if search:
                    hay = " ".join(str(v) for v in row.values()).lower()
                    if search.lower() not in hay:
                        continue
                data.append(row)
            return data

    @staticmethod
    def get_sales(search=""):
        with db_manager.session_scope() as session:
            rows = session.query(Sale).order_by(Sale.sale_date.desc()).all()
            data = []
            for s in rows:
                prop = session.query(Property).filter_by(id=s.property_id).first()
                row = {
                    "id": s.id,
                    "sale_number": s.sale_number or "",
                    "property": prop.title if prop else "",
                    "sale_price": format_currency(s.sale_price),
                    "sale_date": format_date(s.sale_date) if s.sale_date else "",
                    "status": s.status or "",
                    "sale_type": s.sale_type or "",
                }
                if search:
                    hay = " ".join(str(v) for v in row.values()).lower()
                    if search.lower() not in hay:
                        continue
                data.append(row)
            return data

    @staticmethod
    def get_rentals(search=""):
        with db_manager.session_scope() as session:
            rows = session.query(Rental).order_by(Rental.start_date.desc()).all()
            data = []
            for r in rows:
                prop = session.query(Property).filter_by(id=r.property_id).first()
                tenant = session.query(Client).filter_by(id=r.tenant_id).first()
                row = {
                    "id": r.id,
                    "rental_number": r.rental_number or "",
                    "property": prop.title if prop else "",
                    "tenant": tenant.full_name if tenant else "",
                    "monthly_rent": format_currency(r.monthly_rent),
                    "start_date": format_date(r.start_date) if r.start_date else "",
                    "end_date": format_date(r.end_date) if r.end_date else "",
                    "status": r.status or "",
                }
                if search:
                    hay = " ".join(str(v) for v in row.values()).lower()
                    if search.lower() not in hay:
                        continue
                data.append(row)
            return data

    @staticmethod
    def get_contracts(search=""):
        with db_manager.session_scope() as session:
            rows = session.query(Contract).order_by(Contract.contract_date.desc()).all()
            data = []
            for c in rows:
                row = {
                    "id": c.id,
                    "contract_number": c.contract_number,
                    "contract_type": _label(CONTRACT_TYPES, c.contract_type),
                    "title": c.title or "",
                    "amount": format_currency(c.amount),
                    "contract_date": format_date(c.contract_date) if c.contract_date else "",
                    "status": _label(CONTRACT_STATUS, c.status),
                }
                if search:
                    hay = " ".join(str(v) for v in row.values()).lower()
                    if search.lower() not in hay:
                        continue
                data.append(row)
            return data

    @staticmethod
    def get_notifications(search=""):
        with db_manager.session_scope() as session:
            rows = (
                session.query(Notification)
                .order_by(Notification.created_at.desc())
                .limit(200)
                .all()
            )
            data = []
            for n in rows:
                row = {
                    "id": n.id,
                    "title": n.title,
                    "message": (n.message or "")[:80],
                    "notification_type": _label(NOTIFICATION_TYPES, n.notification_type),
                    "priority": n.priority or "",
                    "is_read": "مقروء" if n.is_read else "جديد",
                    "created_at": format_date(n.created_at) if n.created_at else "",
                }
                if search:
                    hay = " ".join(str(v) for v in row.values()).lower()
                    if search.lower() not in hay:
                        continue
                data.append(row)
            return data

    @staticmethod
    def get_users():
        with db_manager.session_scope() as session:
            rows = session.query(User).order_by(User.full_name).all()
            return [
                {
                    "id": u.id,
                    "username": u.username,
                    "full_name": u.full_name,
                    "role": _label(USER_ROLES, u.role),
                    "email": u.email or "",
                    "is_active": "نشط" if u.is_active else "معطل",
                }
                for u in rows
            ]

    @staticmethod
    def get_system_settings():
        from database.models import Setting
        with db_manager.session_scope() as session:
            rows = (
                session.query(Setting)
                .filter(Setting.is_editable == True)
                .order_by(Setting.category, Setting.key)
                .all()
            )
            return [
                {
                    "id": s.id,
                    "key": s.key,
                    "value": s.value or "",
                    "category": s.category or "",
                    "description": s.description or "",
                }
                for s in rows
            ]

    @staticmethod
    def get_property(record_id):
        with db_manager.session_scope() as session:
            p = session.query(Property).filter_by(id=record_id).first()
            if not p:
                return None
            return {
                "id": p.id,
                "title": p.title,
                "property_type": p.property_type,
                "status": p.status,
                "price": p.price,
                "area": p.area,
                "city": p.city or "",
                "address": p.address or "",
                "description": p.description or "",
            }

    @staticmethod
    def save_property(payload, record_id=None):
        try:
            with db_manager.session_scope() as session:
                user_id = (auth.current_user or {}).get("id")
                if record_id:
                    prop = session.query(Property).filter_by(id=record_id).first()
                    if not prop:
                        return False, "العقار غير موجود"
                else:
                    prop = Property(
                        property_number=migration_manager.get_next_number(
                            "property_number_prefix", "property_number_counter"
                        ),
                        created_by=user_id,
                    )
                    session.add(prop)

                prop.title = payload["title"]
                prop.property_type = payload["property_type"]
                prop.status = payload["status"]
                prop.price = payload["price"]
                prop.area = payload["area"]
                prop.city = payload.get("city") or ""
                prop.address = payload.get("address") or ""
                prop.description = payload.get("description") or ""
                if prop.area and prop.price:
                    prop.price_per_meter = round(prop.price / prop.area, 2)

            return True, "تم حفظ العقار بنجاح"
        except Exception as e:
            logger.error("خطأ في حفظ العقار", e)
            return False, "حدث خطأ أثناء الحفظ"

    @staticmethod
    def delete_property(record_id):
        try:
            with db_manager.session_scope() as session:
                prop = session.query(Property).filter_by(id=record_id).first()
                if not prop:
                    return False, "العقار غير موجود"
                session.delete(prop)
            return True, "تم حذف العقار"
        except Exception as e:
            logger.error("خطأ في حذف العقار", e)
            return False, "لا يمكن الحذف: العقار مرتبط بسجلات أخرى"

    @staticmethod
    def get_client(record_id):
        with db_manager.session_scope() as session:
            c = session.query(Client).filter_by(id=record_id).first()
            if not c:
                return None
            return {
                "id": c.id,
                "full_name": c.full_name,
                "phone": c.phone,
                "email": c.email or "",
                "client_type": c.client_type,
                "city": c.city or "",
                "address": c.address or "",
                "national_id": c.national_id or "",
            }

    @staticmethod
    def save_client(payload, record_id=None):
        try:
            with db_manager.session_scope() as session:
                if record_id:
                    client = session.query(Client).filter_by(id=record_id).first()
                    if not client:
                        return False, "العميل غير موجود"
                else:
                    client = Client(
                        client_code=migration_manager.get_next_number(
                            "client_code_prefix", "client_code_counter"
                        ),
                    )
                    session.add(client)

                client.full_name = payload["full_name"]
                client.phone = payload["phone"]
                client.email = payload.get("email") or None
                client.client_type = payload.get("client_type") or "buyer"
                client.city = payload.get("city") or ""
                client.address = payload.get("address") or ""
                client.national_id = payload.get("national_id")

            return True, "تم حفظ العميل بنجاح"
        except Exception as e:
            logger.error("خطأ في حفظ العميل", e)
            return False, "حدث خطأ أثناء الحفظ"

    @staticmethod
    def delete_client(record_id):
        try:
            with db_manager.session_scope() as session:
                client = session.query(Client).filter_by(id=record_id).first()
                if not client:
                    return False, "العميل غير موجود"
                session.delete(client)
            return True, "تم حذف العميل"
        except Exception as e:
            logger.error("خطأ في حذف العميل", e)
            return False, "لا يمكن الحذف: العميل مرتبط بسجلات أخرى"

    @staticmethod
    def list_properties_for_combo():
        with db_manager.session_scope() as session:
            rows = session.query(Property).order_by(Property.title).all()
            return [(p.id, f"{p.property_number} - {p.title}") for p in rows]

    @staticmethod
    def list_clients_for_combo():
        with db_manager.session_scope() as session:
            rows = session.query(Client).filter_by(is_active=True).order_by(Client.full_name).all()
            return [(c.id, c.full_name) for c in rows]

    @staticmethod
    def get_sale(record_id):
        with db_manager.session_scope() as session:
            s = session.query(Sale).filter_by(id=record_id).first()
            if not s:
                return None
            return {
                "id": s.id,
                "sale_type": s.sale_type,
                "property_id": s.property_id,
                "seller_id": s.seller_id,
                "buyer_id": s.buyer_id,
                "sale_price": s.sale_price,
                "purchase_price": s.purchase_price or 0,
                "commission": s.commission or 0,
                "status": s.status or "completed",
                "sale_date": s.sale_date,
                "notes": s.notes or "",
            }

    @staticmethod
    def save_sale(payload, record_id=None):
        try:
            with db_manager.session_scope() as session:
                user_id = (auth.current_user or {}).get("id")
                if record_id:
                    sale = session.query(Sale).filter_by(id=record_id).first()
                    if not sale:
                        return False, "عملية البيع غير موجودة"
                else:
                    sale = Sale(
                        sale_number=migration_manager.get_next_number(
                            "sale_number_prefix", "sale_number_counter"
                        ),
                        created_by=user_id,
                    )
                    session.add(sale)

                sale.sale_type = payload["sale_type"]
                sale.property_id = payload["property_id"]
                sale.seller_id = payload.get("seller_id")
                sale.buyer_id = payload.get("buyer_id")
                sale.sale_price = payload["sale_price"]
                sale.purchase_price = payload.get("purchase_price") or 0
                sale.commission = payload.get("commission") or 0
                sale.taxes = sale.taxes or 0
                sale.other_fees = sale.other_fees or 0
                sale.status = payload.get("status") or "completed"
                sale.sale_date = payload["sale_date"]
                sale.notes = payload.get("notes") or ""
                sale.calculate_profit()

            return True, "تم حفظ عملية البيع بنجاح"
        except Exception as e:
            logger.error("خطأ في حفظ البيع", e)
            return False, "حدث خطأ أثناء الحفظ"

    @staticmethod
    def delete_sale(record_id):
        try:
            with db_manager.session_scope() as session:
                sale = session.query(Sale).filter_by(id=record_id).first()
                if not sale:
                    return False, "العملية غير موجودة"
                session.delete(sale)
            return True, "تم حذف عملية البيع"
        except Exception as e:
            logger.error("خطأ في حذف البيع", e)
            return False, "حدث خطأ أثناء الحذف"

    @staticmethod
    def get_rental(record_id):
        with db_manager.session_scope() as session:
            r = session.query(Rental).filter_by(id=record_id).first()
            if not r:
                return None
            return {
                "id": r.id,
                "property_id": r.property_id,
                "tenant_id": r.tenant_id,
                "owner_id": r.owner_id,
                "monthly_rent": r.monthly_rent,
                "deposit": r.deposit or 0,
                "start_date": r.start_date,
                "end_date": r.end_date,
                "status": r.status or "active",
                "notes": r.notes or "",
            }

    @staticmethod
    def save_rental(payload, record_id=None):
        try:
            with db_manager.session_scope() as session:
                user_id = (auth.current_user or {}).get("id")
                if record_id:
                    rental = session.query(Rental).filter_by(id=record_id).first()
                    if not rental:
                        return False, "عقد الإيجار غير موجود"
                else:
                    rental = Rental(
                        rental_number=migration_manager.get_next_number(
                            "rental_number_prefix", "rental_number_counter"
                        ),
                        created_by=user_id,
                    )
                    session.add(rental)

                rental.property_id = payload["property_id"]
                rental.tenant_id = payload["tenant_id"]
                rental.owner_id = payload.get("owner_id")
                rental.monthly_rent = payload["monthly_rent"]
                rental.deposit = payload.get("deposit") or 0
                rental.start_date = payload["start_date"]
                rental.end_date = payload["end_date"]
                rental.status = payload.get("status") or "active"
                rental.notes = payload.get("notes") or ""
                if rental.start_date and rental.end_date:
                    months = (rental.end_date.year - rental.start_date.year) * 12
                    months += rental.end_date.month - rental.start_date.month
                    rental.duration_months = max(months, 1)

            return True, "تم حفظ عقد الإيجار بنجاح"
        except Exception as e:
            logger.error("خطأ في حفظ الإيجار", e)
            return False, "حدث خطأ أثناء الحفظ"

    @staticmethod
    def delete_rental(record_id):
        try:
            with db_manager.session_scope() as session:
                rental = session.query(Rental).filter_by(id=record_id).first()
                if not rental:
                    return False, "العقد غير موجود"
                session.delete(rental)
            return True, "تم حذف عقد الإيجار"
        except Exception as e:
            logger.error("خطأ في حذف الإيجار", e)
            return False, "حدث خطأ أثناء الحذف"

    @staticmethod
    def get_contract(record_id):
        with db_manager.session_scope() as session:
            c = session.query(Contract).filter_by(id=record_id).first()
            if not c:
                return None
            return {
                "id": c.id,
                "contract_type": c.contract_type,
                "property_id": c.property_id,
                "party1_id": c.party1_id,
                "party2_id": c.party2_id,
                "title": c.title or "",
                "amount": c.amount or 0,
                "contract_date": c.contract_date,
                "start_date": c.start_date,
                "end_date": c.end_date,
                "status": c.status or "draft",
                "content": c.content or "",
            }

    @staticmethod
    def save_contract(payload, record_id=None):
        try:
            with db_manager.session_scope() as session:
                user_id = (auth.current_user or {}).get("id")
                if record_id:
                    contract = session.query(Contract).filter_by(id=record_id).first()
                    if not contract:
                        return False, "العقد غير موجود"
                else:
                    contract = Contract(
                        contract_number=migration_manager.get_next_number(
                            "contract_number_prefix", "contract_number_counter"
                        ),
                        created_by=user_id,
                    )
                    session.add(contract)

                contract.contract_type = payload["contract_type"]
                contract.property_id = payload.get("property_id")
                contract.party1_id = payload.get("party1_id")
                contract.party2_id = payload.get("party2_id")
                contract.title = payload.get("title") or ""
                contract.amount = payload.get("amount") or 0
                contract.contract_date = payload.get("contract_date") or date.today()
                contract.start_date = payload.get("start_date")
                contract.end_date = payload.get("end_date")
                contract.status = payload.get("status") or "draft"
                contract.content = payload.get("content") or ""

            return True, "تم حفظ العقد بنجاح"
        except Exception as e:
            logger.error("خطأ في حفظ العقد", e)
            return False, "حدث خطأ أثناء الحفظ"

    @staticmethod
    def delete_contract(record_id):
        try:
            with db_manager.session_scope() as session:
                contract = session.query(Contract).filter_by(id=record_id).first()
                if not contract:
                    return False, "العقد غير موجود"
                session.delete(contract)
            return True, "تم حذف العقد"
        except Exception as e:
            logger.error("خطأ في حذف العقد", e)
            return False, "حدث خطأ أثناء الحذف"

    @staticmethod
    def mark_notification_read(record_id):
        try:
            with db_manager.session_scope() as session:
                n = session.query(Notification).filter_by(id=record_id).first()
                if n:
                    n.is_read = True
                    n.read_at = datetime.now()
            return True, "تم تحديد الإشعار كمقروء"
        except Exception as e:
            logger.error("خطأ في تحديث الإشعار", e)
            return False, "حدث خطأ"


data = DataController()
