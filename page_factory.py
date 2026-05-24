# views/page_factory.py
"""إنشاء صفحات التطبيق"""

from views.dashboard_page import DashboardPage
from views.base_page import EntityListPage, BasePage
from views.settings_page import SettingsPage
from views.reports_page import ReportsPage
from views.table_columns import (
    PROPERTY_COLUMNS,
    CLIENT_COLUMNS,
    SALE_COLUMNS,
    RENTAL_COLUMNS,
    CONTRACT_COLUMNS,
    NOTIFICATION_COLUMNS,
)
from controllers.data_controller import data


def create_app_page(page_id):
    pages = {
        "dashboard": lambda: DashboardPage(),
        "properties": lambda: EntityListPage(
            "العقارات",
            "إدارة وعرض جميع العقارات المسجلة",
            PROPERTY_COLUMNS,
            data.get_properties,
            "properties_view",
            entity_key="properties",
            add_permission="properties_add",
            edit_permission="properties_edit",
            delete_permission="properties_delete",
        ),
        "clients": lambda: EntityListPage(
            "العملاء",
            "قائمة العملاء والمالكين والمستأجرين",
            CLIENT_COLUMNS,
            data.get_clients,
            "clients_view",
            entity_key="clients",
            add_permission="clients_add",
            edit_permission="clients_edit",
            delete_permission="clients_delete",
        ),
        "sales": lambda: EntityListPage(
            "المبيعات",
            "عمليات البيع والشراء",
            SALE_COLUMNS,
            data.get_sales,
            "sales_view",
            entity_key="sales",
            add_permission="sales_add",
            edit_permission="sales_edit",
            delete_permission="sales_delete",
        ),
        "rentals": lambda: EntityListPage(
            "الإيجارات",
            "عقود الإيجار النشطة والمنتهية",
            RENTAL_COLUMNS,
            data.get_rentals,
            "rentals_view",
            entity_key="rentals",
            add_permission="rentals_add",
            edit_permission="rentals_edit",
            delete_permission="rentals_delete",
        ),
        "contracts": lambda: EntityListPage(
            "العقود",
            "عقود البيع والشراء والإيجار",
            CONTRACT_COLUMNS,
            data.get_contracts,
            "contracts_view",
            entity_key="contracts",
            add_permission="contracts_add",
            edit_permission="contracts_edit",
            delete_permission="contracts_delete",
        ),
        "notifications": lambda: EntityListPage(
            "الإشعارات",
            "تنبيهات النظام والمهام",
            NOTIFICATION_COLUMNS,
            data.get_notifications,
            entity_key="notifications",
        ),
        "reports": lambda: ReportsPage(),
        "settings": lambda: SettingsPage(),
    }
    factory = pages.get(page_id)
    if factory:
        return factory()
    return BasePage(page_id, "الصفحة غير معرّفة")
