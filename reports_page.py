# views/reports_page.py
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from views.base_page import BasePage
from controllers.auth_controller import auth
from controllers.data_controller import data
from widgets.chart_widget import ChartWidget
from utils.formatters import ar, format_currency
from utils.export_helper import export_rows_to_csv
from views.table_columns import (
    PROPERTY_COLUMNS, CLIENT_COLUMNS, SALE_COLUMNS,
    RENTAL_COLUMNS, CONTRACT_COLUMNS,
)


class ReportsPage(BasePage):

    def __init__(self, parent=None):
        super().__init__("التقارير", "ملخصات وإحصائيات سريعة", parent)

        if not auth.has_permission("reports_view"):
            lbl = QLabel(ar("ليس لديك صلاحية لعرض التقارير"))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 16px; color: #e74c3c; padding: 40px;")
            self._layout.addWidget(lbl)
            return

        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignRight)
        self.stats_label.setWordWrap(True)
        self.stats_label.setStyleSheet(
            "font-size: 14px; color: #334155; padding: 12px; "
            "background: #f8fafc; border-radius: 8px;"
        )
        self._layout.addWidget(self.stats_label)

        self.bar_chart = ChartWidget("bar")
        self.bar_chart.setMinimumHeight(280)
        self._layout.addWidget(self.bar_chart, 1)

        export_grid = QGridLayout()
        exports = [
            ("properties", ar("العقارات")),
            ("clients", ar("العملاء")),
            ("sales", ar("المبيعات")),
            ("rentals", ar("الإيجارات")),
            ("contracts", ar("العقود")),
        ]
        for i, (key, label) in enumerate(exports):
            btn = QPushButton(ar(f"تصدير {label} CSV"))
            btn.clicked.connect(lambda _, k=key: self._export_table(k))
            export_grid.addWidget(btn, i // 3, i % 3)
        self._layout.addLayout(export_grid)

        self.refresh()

    def refresh(self):
        stats = data.get_dashboard_stats()
        self.stats_label.setText(
            ar(
                f"العقارات: {stats['properties']} | العملاء: {stats['clients']} | "
                f"المبيعات: {stats['sales']} | الإيجارات النشطة: {stats['rentals']}\n"
                f"إجمالي المبيعات: {format_currency(stats['sales_total'])}"
            )
        )
        chart = data.get_property_status_chart()
        if chart:
            labels = list(chart.keys())
            values = list(chart.values())
            self.bar_chart.set_bar_chart("العقارات حسب الحالة", labels, values)
        else:
            self.bar_chart.clear()

    def _export_table(self, table_type):
        if not auth.has_permission("reports_export"):
            QMessageBox.warning(self, ar("تنبيه"), ar("ليس لديك صلاحية التصدير"))
            return
        export_map = {
            "properties": (PROPERTY_COLUMNS, data.get_properties, "properties"),
            "clients": (CLIENT_COLUMNS, data.get_clients, "clients"),
            "sales": (SALE_COLUMNS, data.get_sales, "sales"),
            "rentals": (RENTAL_COLUMNS, data.get_rentals, "rentals"),
            "contracts": (CONTRACT_COLUMNS, data.get_contracts, "contracts"),
        }
        if table_type not in export_map:
            return
        columns, fetch, prefix = export_map[table_type]
        rows = fetch()

        if not rows:
            QMessageBox.information(self, ar("تصدير"), ar("لا توجد بيانات للتصدير"))
            return

        path = export_rows_to_csv(prefix, columns, rows)
        QMessageBox.information(
            self,
            ar("تم التصدير"),
            ar(f"تم حفظ الملف:\n{path}"),
        )
        if os.name == "nt":
            os.startfile(os.path.dirname(path))
