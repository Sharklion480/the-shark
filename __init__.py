# widgets/__init__.py
"""
عناصر واجهة مستخدم مخصصة
"""

from widgets.stat_card import StatCard
from widgets.search_bar import SearchBar
from widgets.data_table import DataTable
from widgets.image_gallery import ImageGallery
from widgets.chart_widget import ChartWidget
from widgets.signature_pad import SignaturePad
from widgets.date_picker_hijri import DatePickerHijri

__all__ = [
    'StatCard',
    'SearchBar',
    'DataTable',
    'ImageGallery',
    'ChartWidget',
    'SignaturePad',
    'DatePickerHijri'
]
