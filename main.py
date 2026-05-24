import sys
import sqlite3
import warnings
import shutil
from datetime import datetime

warnings.filterwarnings("ignore")

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit,
    QGroupBox, QTabWidget, QDialog, QFormLayout, QMessageBox, QFrame,
    QListWidget, QScrollArea, QCheckBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QColor


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("real_estate.db")
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_type TEXT, name TEXT, area REAL,
            location TEXT, floors INTEGER, units_count INTEGER,
            rental_value REAL, sale_value REAL,
            status TEXT DEFAULT 'متاح', description TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER, unit_number TEXT,
            floor_number INTEGER, area REAL, rooms INTEGER,
            bathrooms INTEGER, rental_value REAL,
            sale_value REAL, status TEXT DEFAULT 'شاغر',
            features TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS rental_contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_number TEXT UNIQUE, unit_id INTEGER,
            tenant_name TEXT, tenant_id TEXT,
            tenant_phone TEXT, tenant_email TEXT,
            start_date DATE, end_date DATE,
            monthly_rent REAL, deposit REAL,
            payment_day INTEGER, contract_status TEXT DEFAULT 'نشط',
            notes TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER, contract_type TEXT,
            payment_date DATE, due_date DATE,
            amount REAL, payment_method TEXT,
            status TEXT DEFAULT 'معلق', receipt_number TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER, expense_type TEXT,
            description TEXT, amount REAL,
            expense_date DATE, category TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS lands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            land_number TEXT, area REAL, location TEXT,
            land_type TEXT, purchase_price REAL,
            current_value REAL, status TEXT DEFAULT 'متاح',
            deed_number TEXT, notes TEXT)''')

        self.conn.commit()


class StatCard(QFrame):
    def __init__(self, title, value, color):
        super().__init__()
        self.setFixedHeight(120)
        self.setStyleSheet(f"QFrame{{background:white;border-radius:10px;border-left:5px solid {color};}}")
        layout = QVBoxLayout()
        t = QLabel(title)
        t.setStyleSheet(f"color:{color};font-size:13px;font-weight:bold;")
        t.setAlignment(Qt.AlignCenter)
        self.v = QLabel(str(value))
        self.v.setStyleSheet(f"color:{color};font-size:26px;font-weight:bold;")
        self.v.setAlignment(Qt.AlignCenter)
        layout.addWidget(t)
        layout.addWidget(self.v)
        self.setLayout(layout)

    def set_value(self, val):
        self.v.setText(str(val))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("نظام إدارة العقارات والاستثمار العقاري")
        self.setGeometry(50, 50, 1300, 800)
        self.setStyleSheet("""
            QMainWindow{background:#f1f5f9}
            QTabWidget::pane{background:white;border:1px solid #cbd5e1;border-radius:5px}
            QTabBar::tab{background:#e2e8f0;color:#334155;padding:12px 25px;font-size:13px;font-weight:bold;margin-right:2px;border-top-left-radius:5px;border-top-right-radius:5px}
            QTabBar::tab:selected{background:#3b82f6;color:white}
            QTabBar::tab:hover{background:#60a5fa;color:white}
            QTableWidget{background:white;gridline-color:#e2e8f0;font-size:12px}
            QHeaderView::section{background:#1e3a8a;color:white;padding:8px;font-weight:bold}
            QPushButton{padding:10px 20px;border-radius:5px;font-weight:bold;font-size:13px}
            QLineEdit,QComboBox,QSpinBox,QDoubleSpinBox,QDateEdit{padding:8px;border:2px solid #cbd5e1;border-radius:5px;font-size:13px}
            QGroupBox{font-weight:bold;font-size:14px;border:2px solid #cbd5e1;border-radius:5px;margin-top:10px;padding-top:10px}
        """)
        self.build_ui()
        self.refresh_all()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_lay = QVBoxLayout()
        central.setLayout(main_lay)

        header = QFrame()
        header.setStyleSheet("QFrame{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #1e3a8a,stop:1 #3b82f6);border-radius:10px;padding:15px}")
        hl = QHBoxLayout()
        title = QLabel("🏢 نظام إدارة العقارات والاستثمار العقاري")
        title.setStyleSheet("color:white;font-size:22px;font-weight:bold")
        self.clock = QLabel()
        self.clock.setStyleSheet("color:white;font-size:13px")
        hl.addWidget(title)
        hl.addStretch()
        hl.addWidget(self.clock)
        header.setLayout(hl)
        main_lay.addWidget(header)

        timer = QTimer(self)
        timer.timeout.connect(lambda: self.clock.setText(datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")))
        timer.start(1000)
        self.clock.setText(datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))

        self.tabs = QTabWidget()
        self.tabs.addTab(self.make_dashboard(), "📊 لوحة المعلومات")
        self.tabs.addTab(self.make_properties(), "🏢 العقارات")
        self.tabs.addTab(self.make_contracts(), "📄 العقود")
        self.tabs.addTab(self.make_payments(), "💰 المدفوعات")
        self.tabs.addTab(self.make_expenses(), "💸 المصروفات")
        self.tabs.addTab(self.make_reports(), "📈 التقارير")
        self.tabs.addTab(self.make_settings(), "⚙️ الإعدادات")
        main_lay.addWidget(self.tabs)

        self.statusBar().showMessage("✅ جاهز")
        self.statusBar().setStyleSheet("background:#1e293b;color:white;padding:5px")

    def make_dashboard(self):
        w = QWidget()
        lay = QVBoxLayout()
        cards = QHBoxLayout()
        self.c1 = StatCard("🏢 العقارات", "0", "#3b82f6")
        self.c2 = StatCard("✅ شاغرة", "0", "#10b981")
        self.c3 = StatCard("🔑 مؤجرة", "0", "#f59e0b")
        self.c4 = StatCard("💰 الإيرادات", "0", "#8b5cf6")
        cards.addWidget(self.c1)
        cards.addWidget(self.c2)
        cards.addWidget(self.c3)
        cards.addWidget(self.c4)
        lay.addLayout(cards)

        tables = QHBoxLayout()
        g1 = QGroupBox("🏠 الوحدات الشاغرة")
        l1 = QVBoxLayout()
        self.vacant_tbl = QTableWidget(0, 4)
        self.vacant_tbl.setHorizontalHeaderLabels(["العقار", "الوحدة", "المساحة", "الإيجار"])
        self.vacant_tbl.horizontalHeader().setStretchLastSection(True)
        l1.addWidget(self.vacant_tbl)
        g1.setLayout(l1)

        g2 = QGroupBox("⚠️ المتأخرات")
        l2 = QVBoxLayout()
        self.overdue_tbl = QTableWidget(0, 4)
        self.overdue_tbl.setHorizontalHeaderLabels(["المستأجر", "المبلغ", "الاستحقاق", "التأخير"])
        self.overdue_tbl.horizontalHeader().setStretchLastSection(True)
        l2.addWidget(self.overdue_tbl)
        g2.setLayout(l2)

        tables.addWidget(g1)
        tables.addWidget(g2)
        lay.addLayout(tables)
        w.setLayout(lay)
        return w

    def make_properties(self):
        w = QWidget()
        lay = QVBoxLayout()
        btns = QHBoxLayout()
        b1 = QPushButton("➕ إضافة عقار")
        b1.setStyleSheet("background:#3b82f6;color:white")
        b1.clicked.connect(self.add_property)
        b2 = QPushButton("🏠 إضافة وحدة")
        b2.setStyleSheet("background:#10b981;color:white")
        b2.clicked.connect(self.add_unit)
        b3 = QPushButton("🗑️ حذف عقار")
        b3.setStyleSheet("background:#ef4444;color:white")
        b3.clicked.connect(self.delete_property)
        btns.addWidget(b1)
        btns.addWidget(b2)
        btns.addWidget(b3)
        btns.addStretch()
        search = QLineEdit()
        search.setPlaceholderText("🔍 بحث...")
        search.textChanged.connect(self.search_props)
        btns.addWidget(search)
        lay.addLayout(btns)

        self.prop_tbl = QTableWidget(0, 8)
        self.prop_tbl.setHorizontalHeaderLabels(["الرقم", "النوع", "الاسم", "الموقع", "المساحة", "الوحدات", "الإيجار", "الحالة"])
        self.prop_tbl.horizontalHeader().setStretchLastSection(True)
        self.prop_tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self.prop_tbl.setAlternatingRowColors(True)
        lay.addWidget(self.prop_tbl)

        g = QGroupBox("📋 الوحدات")
        gl = QVBoxLayout()
        self.unit_tbl = QTableWidget(0, 8)
        self.unit_tbl.setHorizontalHeaderLabels(["العقار", "الوحدة", "الطابق", "المساحة", "الغرف", "الحمامات", "الإيجار", "الحالة"])
        self.unit_tbl.horizontalHeader().setStretchLastSection(True)
        self.unit_tbl.setAlternatingRowColors(True)
        gl.addWidget(self.unit_tbl)
        g.setLayout(gl)
        lay.addWidget(g)
        w.setLayout(lay)
        return w

    def make_contracts(self):
        w = QWidget()
        lay = QVBoxLayout()
        btns = QHBoxLayout()
        b = QPushButton("➕ عقد إيجار جديد")
        b.setStyleSheet("background:#3b82f6;color:white")
        b.clicked.connect(self.add_contract)
        btns.addWidget(b)
        btns.addStretch()
        lay.addLayout(btns)
        self.cont_tbl = QTableWidget(0, 8)
        self.cont_tbl.setHorizontalHeaderLabels(["رقم العقد", "المستأجر", "الوحدة", "البداية", "النهاية", "الإيجار", "المتبقي", "الحالة"])
        self.cont_tbl.horizontalHeader().setStretchLastSection(True)
        self.cont_tbl.setAlternatingRowColors(True)
        lay.addWidget(self.cont_tbl)
        w.setLayout(lay)
        return w

    def make_payments(self):
        w = QWidget()
        lay = QVBoxLayout()
        btns = QHBoxLayout()
        b = QPushButton("➕ تسجيل دفعة")
        b.setStyleSheet("background:#10b981;color:white")
        b.clicked.connect(self.add_payment)
        btns.addWidget(b)
        btns.addStretch()
        f = QComboBox()
        f.addItems(["الكل", "مدفوع", "معلق"])
        f.currentTextChanged.connect(self.filter_pay)
        btns.addWidget(QLabel("الحالة:"))
        btns.addWidget(f)
        lay.addLayout(btns)
        self.pay_tbl = QTableWidget(0, 6)
        self.pay_tbl.setHorizontalHeaderLabels(["المستأجر", "المبلغ", "الاستحقاق", "تاريخ الدفع", "الطريقة", "الحالة"])
        self.pay_tbl.horizontalHeader().setStretchLastSection(True)
        self.pay_tbl.setAlternatingRowColors(True)
        lay.addWidget(self.pay_tbl)
        w.setLayout(lay)
        return w

    def make_expenses(self):
        w = QWidget()
        lay = QVBoxLayout()
        btns = QHBoxLayout()
        b = QPushButton("➕ إضافة مصروف")
        b.setStyleSheet("background:#ef4444;color:white")
        b.clicked.connect(self.add_expense)
        btns.addWidget(b)
        btns.addStretch()
        lay.addLayout(btns)
        self.exp_tbl = QTableWidget(0, 5)
        self.exp_tbl.setHorizontalHeaderLabels(["التاريخ", "النوع", "الوصف", "المبلغ", "العقار"])
        self.exp_tbl.horizontalHeader().setStretchLastSection(True)
        self.exp_tbl.setAlternatingRowColors(True)
        lay.addWidget(self.exp_tbl)
        w.setLayout(lay)
        return w

    def make_reports(self):
        w = QWidget()
        lay = QVBoxLayout()
        cards = QHBoxLayout()
        self.r1 = StatCard("💰 الإيرادات", "0 ر.س", "#10b981")
        self.r2 = StatCard("💸 المصروفات", "0 ر.س", "#ef4444")
        self.r3 = StatCard("📈 صافي الربح", "0 ر.س", "#3b82f6")
        cards.addWidget(self.r1)
        cards.addWidget(self.r2)
        cards.addWidget(self.r3)
        lay.addLayout(cards)
        period = QHBoxLayout()
        period.addWidget(QLabel("من:"))
        self.d1 = QDateEdit()
        self.d1.setCalendarPopup(True)
        self.d1.setDate(QDate.currentDate().addMonths(-1))
        period.addWidget(self.d1)
        period.addWidget(QLabel("إلى:"))
        self.d2 = QDateEdit()
        self.d2.setCalendarPopup(True)
        self.d2.setDate(QDate.currentDate())
        period.addWidget(self.d2)
        rb = QPushButton("🔄 تحديث")
        rb.clicked.connect(self.refresh_reports)
        period.addWidget(rb)
        period.addStretch()
        lay.addLayout(period)
        self.rep_tbl = QTableWidget(0, 4)
        self.rep_tbl.setHorizontalHeaderLabels(["التاريخ", "النوع", "البيان", "المبلغ"])
        self.rep_tbl.horizontalHeader().setStretchLastSection(True)
        self.rep_tbl.setAlternatingRowColors(True)
        lay.addWidget(self.rep_tbl)
        w.setLayout(lay)
        return w

    def make_settings(self):
        w = QWidget()
        main_lay = QVBoxLayout()
        title = QLabel("⚙️ الإعدادات العامة")
        title.setStyleSheet("font-size:20px;font-weight:bold;color:#1e3a8a;padding:10px")
        main_lay.addWidget(title)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        sw = QWidget()
        lay = QVBoxLayout()

        g1 = QGroupBox("🖥️ إعدادات النظام")
        l1 = QFormLayout()
        self.currency = QComboBox()
        self.currency.addItems(["ر.س (ريال سعودي)", "د.إ (درهم)", "ج.م (جنيه)", "$ (دولار)"])
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("اسم الشركة")
        l1.addRow("العملة:", self.currency)
        l1.addRow("اسم الشركة:", self.company_name)
        sb1 = QPushButton("💾 حفظ")
        sb1.setStyleSheet("background:#3b82f6;color:white")
        sb1.clicked.connect(lambda: QMessageBox.information(self, "✅", "تم الحفظ!"))
        l1.addRow(sb1)
        g1.setLayout(l1)
        lay.addWidget(g1)

        g2 = QGroupBox("📄 أنواع العقود")
        l2 = QVBoxLayout()
        self.contract_types = QListWidget()
        self.contract_types.addItems(["عقد إيجار سكني", "عقد إيجار تجاري", "عقد بيع عقار", "عقد شراء عقار", "عقد بيع أرض", "عقد شراء أرض", "عقد استثمار"])
        self.contract_types.setMaximumHeight(200)
        l2.addWidget(self.contract_types)
        al = QHBoxLayout()
        self.new_type = QLineEdit()
        self.new_type.setPlaceholderText("نوع عقد جديد...")
        ab = QPushButton("➕ إضافة")
        ab.setStyleSheet("background:#10b981;color:white")
        ab.clicked.connect(self.add_contract_type)
        db = QPushButton("🗑️ حذف")
        db.setStyleSheet("background:#ef4444;color:white")
        db.clicked.connect(self.del_contract_type)
        al.addWidget(self.new_type)
        al.addWidget(ab)
        al.addWidget(db)
        l2.addLayout(al)
        g2.setLayout(l2)
        lay.addWidget(g2)

        g3 = QGroupBox("📋 إدارة العقود الحالية")
        l3 = QVBoxLayout()
        bl = QHBoxLayout()
        eb = QPushButton("✏️ تعديل عقد")
        eb.setStyleSheet("background:#f59e0b;color:white")
        eb.clicked.connect(self.edit_contract)
        rb2 = QPushButton("🔄 تجديد عقد")
        rb2.setStyleSheet("background:#3b82f6;color:white")
        rb2.clicked.connect(self.renew_contract)
        tb = QPushButton("⛔ إنهاء عقد")
        tb.setStyleSheet("background:#ef4444;color:white")
        tb.clicked.connect(self.terminate_contract)
        bl.addWidget(eb)
        bl.addWidget(rb2)
        bl.addWidget(tb)
        l3.addLayout(bl)
        self.sett_tbl = QTableWidget(0, 7)
        self.sett_tbl.setHorizontalHeaderLabels(["الرقم", "رقم العقد", "المستأجر", "الوحدة", "الإيجار", "النهاية", "الحالة"])
        self.sett_tbl.horizontalHeader().setStretchLastSection(True)
        self.sett_tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self.sett_tbl.setAlternatingRowColors(True)
        l3.addWidget(self.sett_tbl)
        g3.setLayout(l3)
        lay.addWidget(g3)

        g5 = QGroupBox("💾 النسخ الاحتياطي")
        l5 = QHBoxLayout()
        bk = QPushButton("📥 نسخ احتياطي")
        bk.setStyleSheet("background:#3b82f6;color:white")
        bk.clicked.connect(self.backup)
        rs = QPushButton("🔄 إعادة تعيين")
        rs.setStyleSheet("background:#ef4444;color:white")
        rs.clicked.connect(self.reset_data)
        l5.addWidget(bk)
        l5.addWidget(rs)
        g5.setLayout(l5)
        lay.addWidget(g5)

        lay.addStretch()
        sw.setLayout(lay)
        scroll.setWidget(sw)
        main_lay.addWidget(scroll)
        w.setLayout(main_lay)
        self.load_sett_contracts()
        return w

    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_properties()
        self.refresh_units()
        self.refresh_contracts()
        self.refresh_payments()
        self.refresh_expenses()
        self.refresh_reports()
        try:
            self.load_sett_contracts()
        except:
            pass

    def fill_table(self, table, rows, money_cols=None, color_col=None, color_map=None):
        if money_cols is None: money_cols = []
        table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                if c in money_cols: item = QTableWidgetItem(f"{val or 0:,.0f} ر.س")
                else: item = QTableWidgetItem(str(val or ""))
                item.setTextAlignment(Qt.AlignCenter)
                if color_col is not None and c == color_col and color_map:
                    item.setBackground(QColor(color_map.get(val, "#ffffff")))
                table.setItem(r, c, item)

    def refresh_dashboard(self):
        c = self.db.conn.cursor()
        c.execute("SELECT COUNT(*) FROM properties"); self.c1.set_value(c.fetchone()[0])
        c.execute("SELECT COUNT(*) FROM units WHERE status='شاغر'"); self.c2.set_value(c.fetchone()[0])
        c.execute("SELECT COUNT(*) FROM units WHERE status='مؤجر'"); self.c3.set_value(c.fetchone()[0])
        c.execute("SELECT COALESCE(SUM(monthly_rent),0) FROM rental_contracts WHERE contract_status='نشط'"); self.c4.set_value(f"{c.fetchone()[0]:,.0f} ر.س")
        c.execute("SELECT p.name,u.unit_number,u.area,u.rental_value FROM units u JOIN properties p ON u.property_id=p.id WHERE u.status='شاغر'")
        self.fill_table(self.vacant_tbl, c.fetchall(), [3])
        c.execute("SELECT rc.tenant_name,p.amount,p.due_date,CAST(julianday('now')-julianday(p.due_date) AS INT) FROM payments p JOIN rental_contracts rc ON p.contract_id=rc.id WHERE p.status='معلق' AND p.due_date<date('now') ORDER BY 4 DESC")
        rows = c.fetchall()
        self.overdue_tbl.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for col, val in enumerate(row):
                if col == 1: item = QTableWidgetItem(f"{val:,.0f} ر.س")
                elif col == 3:
                    item = QTableWidgetItem(f"{val} يوم")
                    if val > 30: item.setBackground(QColor("#fecaca"))
                    elif val > 15: item.setBackground(QColor("#fef3c7"))
                else: item = QTableWidgetItem(str(val or ""))
                item.setTextAlignment(Qt.AlignCenter)
                self.overdue_tbl.setItem(r, col, item)

    def refresh_properties(self):
        c = self.db.conn.cursor()
        c.execute("SELECT id,property_type,name,location,area,units_count,rental_value,status FROM properties ORDER BY id DESC")
        self.fill_table(self.prop_tbl, c.fetchall(), [6])

    def refresh_units(self):
        c = self.db.conn.cursor()
        c.execute("SELECT p.name,u.unit_number,u.floor_number,u.area,u.rooms,u.bathrooms,u.rental_value,u.status FROM units u JOIN properties p ON u.property_id=p.id ORDER BY p.name,u.unit_number")
        self.fill_table(self.unit_tbl, c.fetchall(), [6], 7, {"شاغر":"#d1fae5","مؤجر":"#dbeafe","مباع":"#fef3c7"})

    def refresh_contracts(self):
        c = self.db.conn.cursor()
        c.execute("SELECT rc.contract_number,rc.tenant_name,u.unit_number,rc.start_date,rc.end_date,rc.monthly_rent,CAST(julianday(rc.end_date)-julianday('now') AS INT),rc.contract_status FROM rental_contracts rc LEFT JOIN units u ON rc.unit_id=u.id ORDER BY rc.id DESC")
        rows = c.fetchall()
        self.cont_tbl.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for col, val in enumerate(row):
                if col == 5: item = QTableWidgetItem(f"{val:,.0f} ر.س")
                elif col == 6:
                    d = val or 0; item = QTableWidgetItem(f"{d} يوم")
                    if d < 0: item.setBackground(QColor("#fecaca"))
                    elif d < 30: item.setBackground(QColor("#fef3c7"))
                else: item = QTableWidgetItem(str(val or ""))
                item.setTextAlignment(Qt.AlignCenter)
                self.cont_tbl.setItem(r, col, item)

    def refresh_payments(self):
        c = self.db.conn.cursor()
        c.execute("SELECT rc.tenant_name,p.amount,p.due_date,p.payment_date,p.payment_method,p.status FROM payments p JOIN rental_contracts rc ON p.contract_id=rc.id ORDER BY p.due_date DESC")
        self.fill_table(self.pay_tbl, c.fetchall(), [1], 5, {"مدفوع":"#d1fae5","معلق":"#fef3c7"})

    def refresh_expenses(self):
        c = self.db.conn.cursor()
        c.execute("SELECT e.expense_date,e.expense_type,e.description,e.amount,COALESCE(p.name,'عام') FROM expenses e LEFT JOIN properties p ON e.property_id=p.id ORDER BY e.expense_date DESC")
        self.fill_table(self.exp_tbl, c.fetchall(), [3])

    def refresh_reports(self):
        c = self.db.conn.cursor()
        f = self.d1.date().toString("yyyy-MM-dd"); t = self.d2.date().toString("yyyy-MM-dd")
        c.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='مدفوع' AND payment_date BETWEEN ? AND ?", (f, t)); inc = c.fetchone()[0]
        c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE expense_date BETWEEN ? AND ?", (f, t)); exp = c.fetchone()[0]
        self.r1.set_value(f"{inc:,.0f} ر.س"); self.r2.set_value(f"{exp:,.0f} ر.س"); self.r3.set_value(f"{inc-exp:,.0f} ر.س")
        c.execute("SELECT payment_date,'إيراد',rc.tenant_name,amount FROM payments p LEFT JOIN rental_contracts rc ON p.contract_id=rc.id WHERE p.status='مدفوع' AND p.payment_date BETWEEN ? AND ? UNION ALL SELECT expense_date,'مصروف',expense_type||' - '||description,amount FROM expenses WHERE expense_date BETWEEN ? AND ? ORDER BY 1 DESC", (f, t, f, t))
        self.fill_table(self.rep_tbl, c.fetchall(), [3], 1, {"إيراد":"#d1fae5","مصروف":"#fee2e2"})

    def load_sett_contracts(self):
        c = self.db.conn.cursor()
        c.execute("SELECT rc.id,rc.contract_number,rc.tenant_name,u.unit_number,rc.monthly_rent,rc.end_date,rc.contract_status FROM rental_contracts rc LEFT JOIN units u ON rc.unit_id=u.id ORDER BY rc.id DESC")
        rows = c.fetchall()
        self.sett_tbl.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for col, val in enumerate(row):
                if col == 4: item = QTableWidgetItem(f"{val:,.0f} ر.س")
                else: item = QTableWidgetItem(str(val or ""))
                item.setTextAlignment(Qt.AlignCenter)
                if col == 6:
                    if val == "نشط": item.setBackground(QColor("#d1fae5"))
                    elif val == "منتهي": item.setBackground(QColor("#fee2e2"))
                self.sett_tbl.setItem(r, col, item)

    def add_property(self):
        d = QDialog(self); d.setWindowTitle("➕ إضافة عقار"); d.setMinimumWidth(500)
        lay = QFormLayout()
        typ = QComboBox(); typ.addItems(["عمارة", "فيلا", "شقة", "محل تجاري", "مستودع", "مكتب"])
        name = QLineEdit(); name.setPlaceholderText("اسم العقار")
        loc = QLineEdit(); loc.setPlaceholderText("الموقع")
        area = QDoubleSpinBox(); area.setMaximum(999999); area.setSuffix(" م²")
        floors = QSpinBox(); floors.setMaximum(100)
        units = QSpinBox(); units.setMaximum(1000)
        rent = QDoubleSpinBox(); rent.setMaximum(9999999); rent.setSuffix(" ر.س")
        sale = QDoubleSpinBox(); sale.setMaximum(99999999); sale.setSuffix(" ر.س")
        status = QComboBox(); status.addItems(["متاح", "مؤجر", "مباع", "تحت الصيانة"])
        desc = QTextEdit(); desc.setMaximumHeight(60)
        lay.addRow("النوع:", typ); lay.addRow("الاسم:", name); lay.addRow("الموقع:", loc)
        lay.addRow("المساحة:", area); lay.addRow("الأدوار:", floors); lay.addRow("الوحدات:", units)
        lay.addRow("الإيجار:", rent); lay.addRow("البيع:", sale); lay.addRow("الحالة:", status); lay.addRow("الوصف:", desc)
        btn = QPushButton("💾 حفظ"); btn.setStyleSheet("background:#10b981;color:white")
        def save():
            if not name.text(): QMessageBox.warning(d, "!", "أدخل اسم العقار"); return
            self.db.conn.cursor().execute("INSERT INTO properties(property_type,name,area,location,floors,units_count,rental_value,sale_value,status,description) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (typ.currentText(),name.text(),area.value(),loc.text(),floors.value(),units.value(),rent.value(),sale.value(),status.currentText(),desc.toPlainText()))
            self.db.conn.commit(); QMessageBox.information(d, "✅", "تم!"); d.accept(); self.refresh_all()
        btn.clicked.connect(save); lay.addRow(btn); d.setLayout(lay); d.exec_()

    def add_unit(self):
        d = QDialog(self); d.setWindowTitle("🏠 إضافة وحدة"); d.setMinimumWidth(500)
        lay = QFormLayout()
        prop = QComboBox()
        for p in self.db.conn.cursor().execute("SELECT id,name FROM properties").fetchall(): prop.addItem(p[1], p[0])
        num = QLineEdit(); num.setPlaceholderText("رقم الوحدة")
        floor = QSpinBox(); floor.setMaximum(100)
        area = QDoubleSpinBox(); area.setMaximum(99999); area.setSuffix(" م²")
        rooms = QSpinBox(); rooms.setMaximum(20)
        baths = QSpinBox(); baths.setMaximum(10)
        rent = QDoubleSpinBox(); rent.setMaximum(9999999); rent.setSuffix(" ر.س")
        status = QComboBox(); status.addItems(["شاغر", "مؤجر", "مباع"])
        lay.addRow("العقار:", prop); lay.addRow("الوحدة:", num); lay.addRow("الطابق:", floor)
        lay.addRow("المساحة:", area); lay.addRow("الغرف:", rooms); lay.addRow("الحمامات:", baths)
        lay.addRow("الإيجار:", rent); lay.addRow("الحالة:", status)
        btn = QPushButton("💾 حفظ"); btn.setStyleSheet("background:#10b981;color:white")
        def save():
            if not num.text(): QMessageBox.warning(d, "!", "أدخل رقم الوحدة"); return
            self.db.conn.cursor().execute("INSERT INTO units(property_id,unit_number,floor_number,area,rooms,bathrooms,rental_value,status) VALUES(?,?,?,?,?,?,?,?)",
                (prop.currentData(),num.text(),floor.value(),area.value(),rooms.value(),baths.value(),rent.value(),status.currentText()))
            self.db.conn.commit(); QMessageBox.information(d, "✅", "تم!"); d.accept(); self.refresh_all()
        btn.clicked.connect(save); lay.addRow(btn); d.setLayout(lay); d.exec_()

    def add_contract(self):
        d = QDialog(self); d.setWindowTitle("📄 عقد إيجار جديد"); d.setMinimumWidth(600)
        lay = QFormLayout()
        c = self.db.conn.cursor()
        c.execute("SELECT COUNT(*) FROM rental_contracts"); cnt = c.fetchone()[0]
        cn = QLineEdit(); cn.setText(f"RC-{datetime.now().year}-{cnt+1:04d}"); cn.setReadOnly(True)
        unit = QComboBox()
        for u in c.execute("SELECT u.id,p.name||' - '||u.unit_number FROM units u JOIN properties p ON u.property_id=p.id WHERE u.status='شاغر'").fetchall(): unit.addItem(u[1], u[0])
        tname = QLineEdit(); tname.setPlaceholderText("اسم المستأجر")
        tid = QLineEdit(); tid.setPlaceholderText("رقم الهوية")
        tphone = QLineEdit(); tphone.setPlaceholderText("الجوال")
        sd = QDateEdit(); sd.setCalendarPopup(True); sd.setDate(QDate.currentDate())
        dur = QSpinBox(); dur.setMinimum(1); dur.setMaximum(60); dur.setValue(12); dur.setSuffix(" شهر")
        ed = QDateEdit(); ed.setCalendarPopup(True); ed.setDate(QDate.currentDate().addMonths(12))
        dur.valueChanged.connect(lambda: ed.setDate(sd.date().addMonths(dur.value())))
        rent = QDoubleSpinBox(); rent.setMaximum(9999999); rent.setSuffix(" ر.س")
        dep = QDoubleSpinBox(); dep.setMaximum(9999999); dep.setSuffix(" ر.س")
        lay.addRow("رقم العقد:", cn); lay.addRow("الوحدة:", unit); lay.addRow("المستأجر:", tname)
        lay.addRow("الهوية:", tid); lay.addRow("الجوال:", tphone); lay.addRow("البداية:", sd)
        lay.addRow("المدة:", dur); lay.addRow("النهاية:", ed); lay.addRow("الإيجار:", rent); lay.addRow("التأمين:", dep)
        btn = QPushButton("💾 حفظ"); btn.setStyleSheet("background:#10b981;color:white")
        def save():
            if not tname.text(): QMessageBox.warning(d, "!", "أدخل اسم المستأجر"); return
            if unit.count() == 0: QMessageBox.warning(d, "!", "لا توجد وحدات شاغرة!"); return
            cur = self.db.conn.cursor()
            cur.execute("INSERT INTO rental_contracts(contract_number,unit_id,tenant_name,tenant_id,tenant_phone,start_date,end_date,monthly_rent,deposit,contract_status) VALUES(?,?,?,?,?,?,?,?,?,'نشط')",
                (cn.text(),unit.currentData(),tname.text(),tid.text(),tphone.text(),sd.date().toString("yyyy-MM-dd"),ed.date().toString("yyyy-MM-dd"),rent.value(),dep.value()))
            cid = cur.lastrowid
            cur.execute("UPDATE units SET status='مؤجر' WHERE id=?", (unit.currentData(),))
            start = sd.date()
            for i in range(dur.value()):
                cur.execute("INSERT INTO payments(contract_id,contract_type,due_date,amount,status) VALUES(?,'إيجار',?,?,'معلق')", (cid, start.addMonths(i).toString("yyyy-MM-dd"), rent.value()))
            self.db.conn.commit(); QMessageBox.information(d, "✅", "تم حفظ العقد!"); d.accept(); self.refresh_all()
        btn.clicked.connect(save); lay.addRow(btn); d.setLayout(lay); d.exec_()

    def add_payment(self):
        d = QDialog(self); d.setWindowTitle("💰 تسجيل دفعة"); d.setMinimumWidth(400)
        lay = QFormLayout()
        cont = QComboBox()
        for r in self.db.conn.cursor().execute("SELECT id,contract_number||' - '||tenant_name FROM rental_contracts WHERE contract_status='نشط'").fetchall(): cont.addItem(r[1], r[0])
        amount = QDoubleSpinBox(); amount.setMaximum(9999999); amount.setSuffix(" ر.س")
        pdate = QDateEdit(); pdate.setCalendarPopup(True); pdate.setDate(QDate.currentDate())
        method = QComboBox(); method.addItems(["نقداً", "تحويل بنكي", "شيك", "بطاقة"])
        lay.addRow("العقد:", cont); lay.addRow("المبلغ:", amount); lay.addRow("التاريخ:", pdate); lay.addRow("الطريقة:", method)
        btn = QPushButton("💾 حفظ"); btn.setStyleSheet("background:#10b981;color:white")
        def save():
            self.db.conn.cursor().execute("UPDATE payments SET payment_date=?,payment_method=?,status='مدفوع',receipt_number=? WHERE id=(SELECT id FROM payments WHERE contract_id=? AND status='معلق' ORDER BY due_date LIMIT 1)",
                (pdate.date().toString("yyyy-MM-dd"),method.currentText(),f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}",cont.currentData()))
            self.db.conn.commit(); QMessageBox.information(d, "✅", "تم!"); d.accept(); self.refresh_all()
        btn.clicked.connect(save); lay.addRow(btn); d.setLayout(lay); d.exec_()

    def add_expense(self):
        d = QDialog(self); d.setWindowTitle("💸 إضافة مصروف"); d.setMinimumWidth(400)
        lay = QFormLayout()
        typ = QComboBox(); typ.addItems(["صيانة", "كهرباء", "ماء", "نظافة", "رسوم", "أخرى"])
        prop = QComboBox(); prop.addItem("عام", None)
        for p in self.db.conn.cursor().execute("SELECT id,name FROM properties").fetchall(): prop.addItem(p[1], p[0])
        desc = QLineEdit(); desc.setPlaceholderText("الوصف")
        amount = QDoubleSpinBox(); amount.setMaximum(9999999); amount.setSuffix(" ر.س")
        edate = QDateEdit(); edate.setCalendarPopup(True); edate.setDate(QDate.currentDate())
        lay.addRow("النوع:", typ); lay.addRow("العقار:", prop); lay.addRow("الوصف:", desc); lay.addRow("المبلغ:", amount); lay.addRow("التاريخ:", edate)
        btn = QPushButton("💾 حفظ"); btn.setStyleSheet("background:#10b981;color:white")
        def save():
            self.db.conn.cursor().execute("INSERT INTO expenses(property_id,expense_type,description,amount,expense_date,category) VALUES(?,?,?,?,?,?)",
                (prop.currentData(),typ.currentText(),desc.text(),amount.value(),edate.date().toString("yyyy-MM-dd"),typ.currentText()))
            self.db.conn.commit(); QMessageBox.information(d, "✅", "تم!"); d.accept(); self.refresh_all()
        btn.clicked.connect(save); lay.addRow(btn); d.setLayout(lay); d.exec_()

    def delete_property(self):
        row = self.prop_tbl.currentRow()
        if row < 0: QMessageBox.warning(self, "!", "اختر عقار"); return
        pid = self.prop_tbl.item(row, 0).text()
        if QMessageBox.question(self, "تأكيد", "حذف هذا العقار؟") == QMessageBox.Yes:
            c = self.db.conn.cursor(); c.execute("DELETE FROM units WHERE property_id=?", (pid,)); c.execute("DELETE FROM properties WHERE id=?", (pid,))
            self.db.conn.commit(); self.refresh_all()

    def search_props(self, text):
        for r in range(self.prop_tbl.rowCount()):
            match = any(self.prop_tbl.item(r, c) and text.lower() in self.prop_tbl.item(r, c).text().lower() for c in range(self.prop_tbl.columnCount()))
            self.prop_tbl.setRowHidden(r, not match)

    def filter_pay(self, status):
        for r in range(self.pay_tbl.rowCount()):
            if status == "الكل": self.pay_tbl.setRowHidden(r, False)
            else:
                item = self.pay_tbl.item(r, 5)
                self.pay_tbl.setRowHidden(r, not item or item.text() != status)

    def add_contract_type(self):
        t = self.new_type.text().strip()
        if t: self.contract_types.addItem(t); self.new_type.clear()
        else: QMessageBox.warning(self, "!", "أدخل نوع العقد")

    def del_contract_type(self):
        r = self.contract_types.currentRow()
        if r >= 0: self.contract_types.takeItem(r)

    def edit_contract(self):
        row = self.sett_tbl.currentRow()
        if row < 0: QMessageBox.warning(self, "!", "اختر عقد"); return
        cid = self.sett_tbl.item(row, 0).text()
        data = self.db.conn.cursor().execute("SELECT * FROM rental_contracts WHERE id=?", (cid,)).fetchone()
        if not data: return
        d = QDialog(self); d.setWindowTitle("✏️ تعديل العقد"); d.setMinimumWidth(500)
        lay = QFormLayout()
        tname = QLineEdit(data[3] or ""); tid = QLineEdit(data[4] or ""); tphone = QLineEdit(data[5] or "")
        rent = QDoubleSpinBox(); rent.setMaximum(9999999); rent.setSuffix(" ر.س"); rent.setValue(data[9] or 0)
        dep = QDoubleSpinBox(); dep.setMaximum(9999999); dep.setSuffix(" ر.س"); dep.setValue(data[10] or 0)
        status = QComboBox(); status.addItems(["نشط", "منتهي", "ملغي"]); status.setCurrentText(data[12] or "نشط")
        lay.addRow("المستأجر:", tname); lay.addRow("الهوية:", tid); lay.addRow("الجوال:", tphone)
        lay.addRow("الإيجار:", rent); lay.addRow("التأمين:", dep); lay.addRow("الحالة:", status)
        btn = QPushButton("💾 حفظ"); btn.setStyleSheet("background:#10b981;color:white")
        def save():
            self.db.conn.cursor().execute("UPDATE rental_contracts SET tenant_name=?,tenant_id=?,tenant_phone=?,monthly_rent=?,deposit=?,contract_status=? WHERE id=?",
                (tname.text(),tid.text(),tphone.text(),rent.value(),dep.value(),status.currentText(),cid))
            self.db.conn.commit(); QMessageBox.information(d, "✅", "تم!"); d.accept(); self.refresh_all()
        btn.clicked.connect(save); lay.addRow(btn); d.setLayout(lay); d.exec_()

    def renew_contract(self):
        row = self.sett_tbl.currentRow()
        if row < 0: QMessageBox.warning(self, "!", "اختر عقد"); return
        cid = self.sett_tbl.item(row, 0).text()
        data = self.db.conn.cursor().execute("SELECT monthly_rent FROM rental_contracts WHERE id=?", (cid,)).fetchone()
        d = QDialog(self); d.setWindowTitle("🔄 تجديد العقد"); d.setMinimumWidth(400)
        lay = QFormLayout()
        sd = QDateEdit(); sd.setCalendarPopup(True); sd.setDate(QDate.currentDate())
        dur = QSpinBox(); dur.setMinimum(1); dur.setMaximum(60); dur.setValue(12); dur.setSuffix(" شهر")
        rent = QDoubleSpinBox(); rent.setMaximum(9999999); rent.setSuffix(" ر.س"); rent.setValue(data[0] if data else 0)
        lay.addRow("البداية:", sd); lay.addRow("المدة:", dur); lay.addRow("الإيجار:", rent)
        btn = QPushButton("🔄 تجديد"); btn.setStyleSheet("background:#3b82f6;color:white")
        def save():
            cur = self.db.conn.cursor()
            cur.execute("UPDATE rental_contracts SET contract_status='منتهي' WHERE id=?", (cid,))
            cur.execute("INSERT INTO rental_contracts(contract_number,unit_id,tenant_name,tenant_id,tenant_phone,tenant_email,start_date,end_date,monthly_rent,deposit,contract_status) SELECT contract_number||'-R',unit_id,tenant_name,tenant_id,tenant_phone,tenant_email,?,?,?,deposit,'نشط' FROM rental_contracts WHERE id=?",
                (sd.date().toString("yyyy-MM-dd"),sd.date().addMonths(dur.value()).toString("yyyy-MM-dd"),rent.value(),cid))
            ncid = cur.lastrowid; start = sd.date()
            for i in range(dur.value()):
                cur.execute("INSERT INTO payments(contract_id,contract_type,due_date,amount,status) VALUES(?,'إيجار',?,?,'معلق')", (ncid, start.addMonths(i).toString("yyyy-MM-dd"), rent.value()))
            self.db.conn.commit(); QMessageBox.information(d, "✅", "تم التجديد!"); d.accept(); self.refresh_all()
        btn.clicked.connect(save); lay.addRow(btn); d.setLayout(lay); d.exec_()

    def terminate_contract(self):
        row = self.sett_tbl.currentRow()
        if row < 0: QMessageBox.warning(self, "!", "اختر عقد"); return
        cid = self.sett_tbl.item(row, 0).text()
        if QMessageBox.question(self, "⚠️", "إنهاء هذا العقد؟") == QMessageBox.Yes:
            cur = self.db.conn.cursor()
            cur.execute("UPDATE rental_contracts SET contract_status='منتهي' WHERE id=?", (cid,))
            cur.execute("UPDATE units SET status='شاغر' WHERE id=(SELECT unit_id FROM rental_contracts WHERE id=?)", (cid,))
            cur.execute("UPDATE payments SET status='ملغي' WHERE contract_id=? AND status='معلق'", (cid,))
            self.db.conn.commit(); QMessageBox.information(self, "✅", "تم!"); self.refresh_all()

    def backup(self):
        try:
            name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy("real_estate.db", name)
            QMessageBox.information(self, "✅", f"تم النسخ: {name}")
        except Exception as e: QMessageBox.critical(self, "خطأ", str(e))

    def reset_data(self):
        if QMessageBox.question(self, "⚠️", "حذف جميع البيانات؟") == QMessageBox.Yes:
            if QMessageBox.question(self, "⚠️⚠️", "متأكد 100%؟") == QMessageBox.Yes:
                c = self.db.conn.cursor()
                for t in ["payments","expenses","rental_contracts","units","properties","lands"]: c.execute(f"DELETE FROM {t}")
                self.db.conn.commit(); QMessageBox.information(self, "✅", "تم!"); self.refresh_all()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())