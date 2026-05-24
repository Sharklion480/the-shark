# utils/export_helper.py
"""تصدير البيانات إلى ملفات"""

import csv
from datetime import datetime

from config.settings import Settings


def export_rows_to_csv(filename_prefix, columns, rows):
    """
    تصدير صفوف إلى CSV
    columns: list of dicts with 'key' and 'title'
    rows: list of dicts
    """
    Settings.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Settings.EXPORTS_DIR / f"{filename_prefix}_{timestamp}.csv"

    headers = [col["title"] for col in columns]
    keys = [col["key"] for col in columns]

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(k, "") for k in keys])

    return str(path)
