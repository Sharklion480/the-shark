# run_all.py
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

# تعيين UTF-8 لـ stdout على ويندوز
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

tests = [
    "test_imports.py",
    "test_auth_flow.py",
    "test_formatting.py",
    "test_database.py",
    "test_ui.py",
]

env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"

failed = []
for t in tests:
    print(f"\n{'=' * 50}")
    print(f"  تشغيل {t}")
    print(f"{'=' * 50}")
    result = subprocess.run(
        [sys.executable, t],
        cwd=ROOT,
        env=env,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        failed.append(t)

if failed:
    print(f"\n❌ فشلت الاختبارات: {', '.join(failed)}")
    sys.exit(1)

print("\n✅ انتهت جميع الاختبارات")
