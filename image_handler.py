# utils/image_handler.py
"""
معالجة وضغط الصور
"""

from PIL import Image, ImageOps
from pathlib import Path
import uuid
from config.settings import Settings
from utils.logger import logger


class ImageHandler:

    MAX_SIZE = 1920
    THUMBNAIL_SIZE = 300
    QUALITY = 85

    @staticmethod
    def save_property_image(source_path):
        """حفظ صورة عقار جديدة"""

        # انشاء اسم ملف فريد
        filename = f"{uuid.uuid4()}.webp"
        full_path = Settings.PROPERTIES_IMAGES_DIR / filename
        thumbnail_path = Settings.PROPERTIES_IMAGES_DIR / f"thumb_{filename}"

        try:
            # فتح الصورة واصلاح التدوير
            with Image.open(source_path) as img:
                img = ImageOps.exif_transpose(img)

                # ضغط الصورة الاصلية
                img.thumbnail((ImageHandler.MAX_SIZE, ImageHandler.MAX_SIZE))
                img.save(full_path, 'WEBP', quality=ImageHandler.QUALITY)

                # انشاء الصورة المصغرة
                img.thumbnail((ImageHandler.THUMBNAIL_SIZE, ImageHandler.THUMBNAIL_SIZE))
                img.save(thumbnail_path, 'WEBP', quality=80)

            return str(filename)

        except Exception as e:
            logger.error(f"خطأ في حفظ الصورة: {e}")
            return None

    @staticmethod
    def delete_image(filename):
        """حذف صورة"""
        try:
            full_path = Settings.PROPERTIES_IMAGES_DIR / filename
            thumb_path = Settings.PROPERTIES_IMAGES_DIR / f"thumb_{filename}"

            if full_path.exists():
                full_path.unlink()
            
            if thumb_path.exists():
                thumb_path.unlink()
            
            return True
        except Exception as e:
            logger.error(f"خطأ في حذف الصورة: {e}")
            return False