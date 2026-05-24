# utils/logger.py
"""
نظام تسجيل الاحداث والاخطاء
"""

import logging
from pathlib import Path
from datetime import datetime
from config.settings import Settings


class Logger:
    def __init__(self):
        self.log_file = Settings.LOGS_DIR / f"app_{datetime.now().strftime('%Y_%m_%d')}.log"
        
        # تهيئة نظام اللوج
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
        # ازالة الرسائل المكررة
        self.logger.propagate = False

    def info(self, message):
        self.logger.info(message)
    
    def success(self, message):
        self.logger.info(f"✅ {message}")
    
    def warning(self, message):
        self.logger.warning(f"⚠️ {message}")
    
    def error(self, message, exception=None):
        if exception:
            self.logger.error(f"❌ {message}: {exception}", exc_info=True)
        else:
            self.logger.error(f"❌ {message}")
    
    def debug(self, message):
        self.logger.debug(f"🔍 {message}")
    
    def critical(self, message):
        self.logger.critical(f"🔥 {message}")


# انشاء نسخة عامة
logger = Logger()