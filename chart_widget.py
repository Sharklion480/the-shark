# widgets/chart_widget.py
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from utils.formatters import ar, format_currency
from config.themes import theme_manager


class ChartWidget(QChartView):

    def __init__(self, chart_type="line", parent=None):
        super().__init__(parent)

        self.chart_type = chart_type
        self.chart = QChart()

        self.setup_chart()
        self.apply_theme()

    def setup_chart(self):
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

    def apply_theme(self):
        """تطبيق الثيم الحالي على الرسم البياني"""
        if theme_manager.is_dark():
            self.chart.setTheme(QChart.ChartThemeDark)
        else:
            self.chart.setTheme(QChart.ChartThemeLight)

        self.chart.setBackgroundBrush(QBrush(QColor(theme_manager.get_color("surface"))))
        self.chart.setTitleBrush(QBrush(QColor(theme_manager.get_color("text_primary"))))

    def set_bar_chart(self, title, labels, values):
        """انشاء رسم بياني اعمودي"""
        self.chart.removeAllSeries()
        self.chart.setTitle(ar(title))

        set = QBarSet("")
        set.append(values)
        set.setColor(QColor(theme_manager.get_color("primary")))

        series = QBarSeries()
        series.append(set)
        series.setLabelsVisible(True)

        self.chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append([ar(l) for l in labels])
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        self.chart.createDefaultAxes()

    def set_pie_chart(self, title, data):
        """انشاء رسم بياني دائري"""
        self.chart.removeAllSeries()
        self.chart.setTitle(ar(title))

        series = QPieSeries()
        series.setHoleSize(0.45)

        colors = theme_manager.get_chart_colors()

        for i, (label, value) in enumerate(data.items()):
            slice = series.append(ar(label), value)
            slice.setColor(QColor(colors[i % len(colors)]))
            slice.setLabelVisible(True)

        self.chart.addSeries(series)

    def clear(self):
        self.chart.removeAllSeries()

    def refresh_theme(self):
        self.apply_theme()