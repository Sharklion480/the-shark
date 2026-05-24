# views/base_page.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from utils.formatters import ar
from widgets.data_table import DataTable
from widgets.search_bar import SearchBar
from controllers.auth_controller import auth
from views.entity_dialogs import DIALOG_MAP


class BasePage(QWidget):
    """صفحة أساسية مع عنوان ومحتوى"""

    def __init__(self, title, subtitle=None, parent=None):
        super().__init__(parent)
        self.page_title = title
        self._subtitle = subtitle
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(20, 20, 20, 20)
        self._layout.setSpacing(12)
        self._build_header()

    def _build_header(self):
        header = QLabel(ar(self.page_title))
        header.setObjectName("PageHeader")
        header.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header.setStyleSheet(
            "font-size: 28px; font-weight: 700; color: #1e293b;"
        )
        self._layout.addWidget(header)

        if self._subtitle:
            sub = QLabel(ar(self._subtitle))
            sub.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            sub.setStyleSheet("font-size: 14px; color: #64748b;")
            self._layout.addWidget(sub)

    def refresh(self):
        pass

    def show_add_dialog(self):
        pass


class EntityListPage(BasePage):
    """صفحة قائمة بيانات مع بحث وجدول وإجراءات"""

    def __init__(
        self,
        title,
        subtitle,
        columns,
        fetch_data,
        permission=None,
        entity_key=None,
        add_permission=None,
        edit_permission=None,
        delete_permission=None,
        parent=None,
    ):
        super().__init__(title, subtitle, parent)
        self.columns = columns
        self.fetch_data = fetch_data
        self.permission = permission
        self.entity_key = entity_key
        self.add_permission = add_permission
        self.edit_permission = edit_permission
        self.delete_permission = delete_permission
        self._dialog_cls = DIALOG_MAP.get(entity_key) if entity_key else None

        if permission and not auth.has_permission(permission):
            self._layout.addWidget(self._no_permission_label())
            return

        self._build_actions()
        self.search_bar = SearchBar("ابحث في السجلات...")
        self.search_bar.textChanged.connect(self._on_search)
        self._layout.addWidget(self.search_bar)

        self.table = DataTable(columns)
        self.table.rowDoubleClicked.connect(self._on_row_double_clicked)
        self._layout.addWidget(self.table, 1)

        self.count_label = QLabel()
        self.count_label.setAlignment(Qt.AlignRight)
        self.count_label.setStyleSheet("font-size: 13px; color: #64748b;")
        self._layout.addWidget(self.count_label)

        self.reload_data()

    def _build_actions(self):
        bar = QHBoxLayout()
        bar.addStretch()

        btn_style = (
            "padding: 8px 14px; border-radius: 6px; font-size: 13px; font-weight: 600;"
        )

        if self._can_add():
            add_btn = QPushButton("➕ " + ar("إضافة"))
            add_btn.clicked.connect(self.show_add_dialog)
            add_btn.setStyleSheet(
                btn_style + " background: #1976D2; color: white; border: none;"
            )
            bar.addWidget(add_btn)

        if self._can_edit():
            edit_btn = QPushButton("✏️ " + ar("تعديل"))
            edit_btn.clicked.connect(self.show_edit_dialog)
            edit_btn.setStyleSheet(
                btn_style + " background: #f8fafc; border: 1px solid #cbd5e1;"
            )
            bar.addWidget(edit_btn)

        if self._can_delete():
            del_btn = QPushButton("🗑️ " + ar("حذف"))
            del_btn.clicked.connect(self.delete_selected)
            del_btn.setStyleSheet(
                btn_style + " background: #fef2f2; color: #dc2626; border: 1px solid #fecaca;"
            )
            bar.addWidget(del_btn)

        if self.entity_key == "notifications":
            read_btn = QPushButton("✓ " + ar("تعيين كمقروء"))
            read_btn.clicked.connect(self._mark_notification_read)
            read_btn.setStyleSheet(
                btn_style + " background: #f0fdf4; border: 1px solid #bbf7d0;"
            )
            bar.addWidget(read_btn)

        wrap = QWidget()
        wrap.setLayout(bar)
        self._layout.addWidget(wrap)

    def _can_add(self):
        return self._dialog_cls and (
            not self.add_permission or auth.has_permission(self.add_permission)
        )

    def _can_edit(self):
        return self._dialog_cls and (
            not self.edit_permission or auth.has_permission(self.edit_permission)
        )

    def _can_delete(self):
        return self.entity_key in (
            "properties", "clients", "sales", "rentals", "contracts",
        ) and (
            not self.delete_permission or auth.has_permission(self.delete_permission)
        )

    def _no_permission_label(self):
        lbl = QLabel(ar("ليس لديك صلاحية لعرض هذه الصفحة"))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 16px; color: #e74c3c; padding: 40px;")
        return lbl

    def reload_data(self, search=""):
        if not hasattr(self, "table"):
            return
        rows = self.fetch_data(search)
        self.table.set_data(rows)
        self.count_label.setText(ar(f"عدد السجلات: {len(rows)}"))

    def filter_text(self, text):
        if hasattr(self, "search_bar"):
            self.search_bar.set_text(text)
        self.reload_data(text)

    def _on_search(self, text):
        self.reload_data(text)

    def _selected_id(self):
        if hasattr(self, "table"):
            return self.table.get_selected_id()
        return None

    def show_add_dialog(self):
        if not self._can_add():
            QMessageBox.warning(self, ar("تنبيه"), ar("ليس لديك صلاحية الإضافة"))
            return
        dialog = self._dialog_cls(parent=self.window())
        if dialog.exec_() == QDialog.Accepted:
            ok, msg = dialog.save()
            if ok:
                self.reload_data(self.search_bar.get_text())
                QMessageBox.information(self, ar("نجاح"), ar(msg))
            else:
                QMessageBox.warning(self, ar("خطأ"), ar(msg))

    def show_edit_dialog(self, record_id=None):
        if not self._can_edit():
            QMessageBox.warning(self, ar("تنبيه"), ar("ليس لديك صلاحية التعديل"))
            return
        record_id = record_id or self._selected_id()
        if not record_id:
            QMessageBox.information(self, ar("تنبيه"), ar("اختر سجلاً من الجدول"))
            return
        dialog = self._dialog_cls(record_id=record_id, parent=self.window())
        if dialog.exec_() == QDialog.Accepted:
            ok, msg = dialog.save()
            if ok:
                self.reload_data(self.search_bar.get_text())
                QMessageBox.information(self, ar("نجاح"), ar(msg))
            else:
                QMessageBox.warning(self, ar("خطأ"), ar(msg))

    def delete_selected(self):
        if not self._can_delete():
            QMessageBox.warning(self, ar("تنبيه"), ar("ليس لديك صلاحية الحذف"))
            return
        record_id = self._selected_id()
        if not record_id:
            QMessageBox.information(self, ar("تنبيه"), ar("اختر سجلاً للحذف"))
            return
        confirm = QMessageBox.question(
            self,
            ar("تأكيد الحذف"),
            ar("هل أنت متأكد من حذف هذا السجل؟"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        from controllers.data_controller import data as dc

        delete_handlers = {
            "properties": dc.delete_property,
            "clients": dc.delete_client,
            "sales": dc.delete_sale,
            "rentals": dc.delete_rental,
            "contracts": dc.delete_contract,
        }
        handler = delete_handlers.get(self.entity_key)
        if not handler:
            return
        ok, msg = handler(record_id)

        if ok:
            self.reload_data(self.search_bar.get_text())
            QMessageBox.information(self, ar("نجاح"), ar(msg))
        else:
            QMessageBox.warning(self, ar("خطأ"), ar(msg))

    def _mark_notification_read(self):
        from controllers.data_controller import data as dc

        record_id = self._selected_id()
        if not record_id:
            QMessageBox.information(self, ar("تنبيه"), ar("اختر إشعاراً"))
            return
        ok, msg = dc.mark_notification_read(record_id)
        if ok:
            self.reload_data(self.search_bar.get_text())
        else:
            QMessageBox.warning(self, ar("خطأ"), ar(msg))

    def _on_row_double_clicked(self, row_id, row_data):
        if self._can_edit():
            self.show_edit_dialog(row_id)
        else:
            QMessageBox.information(
                self,
                ar("تفاصيل"),
                ar(f"معرف السجل: {row_id}"),
            )

    def refresh(self):
        search = self.search_bar.get_text() if hasattr(self, "search_bar") else ""
        self.reload_data(search)
