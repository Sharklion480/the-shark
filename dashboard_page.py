# views/dashboard_page.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from views.base_page import BasePage
from controllers.data_controller import data
from controllers.auth_controller import auth
from widgets.stat_card import StatCard
from widgets.chart_widget import ChartWidget
from utils.formatters import ar, format_currency


class DashboardPage(BasePage):

    def __init__(self, parent=None):
        user = auth.current_user or {}
        name = user.get("full_name", "") if isinstance(user, dict) else ""
        subtitle = f"مرحباً بك، {name}" if name else "مرحباً بك"
        super().__init__("لوحة التحكم", subtitle, parent)
        self._stat_cards = []
        self._build_content()

    def _build_content(self):
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)

        self.cards_layout = stats_row
        self._layout.addLayout(stats_row)

        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        self.chart = ChartWidget("pie")
        self.chart.setMinimumHeight(320)
        charts_row.addWidget(self.chart, 1)

        summary = QFrame()
        summary.setStyleSheet(
            "QFrame { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; }"
        )
        summary_layout = QVBoxLayout(summary)
        summary_layout.setContentsMargins(20, 20, 20, 20)
        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.summary_label.setStyleSheet("font-size: 14px; color: #334155; line-height: 1.6;")
        summary_layout.addWidget(self.summary_label)
        charts_row.addWidget(summary, 1)

        self._layout.addLayout(charts_row, 1)
        self.refresh()

    def refresh(self):
        stats = data.get_dashboard_stats()
        chart_data = data.get_property_status_chart()

        specs = [
            ("العقارات", stats["properties"], "🏠", "#1976D2", False),
            ("العملاء", stats["clients"], "👥", "#2ecc71", False),
            ("المبيعات", stats["sales"], "💰", "#f39c12", False),
            ("إيجارات نشطة", stats["rentals"], "📅", "#9b59b6", False),
            ("عقود", stats["contracts"], "📋", "#e67e22", False),
            ("إشعارات جديدة", stats["notifications"], "🔔", "#e74c3c", False),
        ]

        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._stat_cards = []
        for title, value, icon, color, is_currency in specs:
            card = StatCard(title, value, icon, color, is_currency)
            card.clicked.connect(self.refresh)
            self.cards_layout.addWidget(card)
            self._stat_cards.append(card)

        if chart_data:
            self.chart.set_pie_chart("توزيع العقارات حسب الحالة", chart_data)
        else:
            self.chart.clear()

        self.summary_label.setText(
            ar(
                f"إجمالي قيمة المبيعات: {format_currency(stats['sales_total'])}\n"
                f"إشعارات غير مقروءة: {stats['notifications']}\n"
                f"آخر تحديث: الآن"
            )
        )
