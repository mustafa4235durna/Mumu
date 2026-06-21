"""
Logging Konfigürasyonu
"""

import logging
import logging.handlers
import os
from datetime import datetime

# Log dizinini oluştur
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log dosyası adı
LOG_FILE = os.path.join(LOG_DIR, f"mumu_{datetime.now().strftime('%Y-%m-%d')}.log")


def setup_logging():
    """Logging'i ayarla"""
    
    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10485760,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Handler'ları logger'a ekle
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


if __name__ == "__main__":
    logger = setup_logging()
    logger.info("Logging sistemi ayarlandı")
    logger.debug("Bu bir debug mesajı")
    logger.warning("Bu bir uyarı mesajı")
    logger.error("Bu bir hata mesajı")
