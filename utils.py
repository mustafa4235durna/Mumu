"""
Mumu Assistant Utils - Yardımcı fonksiyonlar
"""

import logging
from functools import wraps
from datetime import datetime

logger = logging.getLogger(__name__)


def log_message(func):
    """Mesaj işleme için logging decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start_time = datetime.now()
            result = func(*args, **kwargs)
            elapsed_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ {func.__name__} tamamlandı ({elapsed_time:.2f}s)")
            return result
        except Exception as e:
            logger.error(f"❌ {func.__name__} başarısız: {str(e)}")
            raise
    return wrapper


def truncate_message(message: str, max_length: int = 1000) -> str:
    """Mesajı belirtilen uzunlukta kes"""
    if len(message) > max_length:
        return message[:max_length - 3] + "..."
    return message


def is_greeting(message: str) -> bool:
    """Selam mesajı kontrolü"""
    greetings = ["merhaba", "selam", "hey", "alo", "hi", "hello"]
    return any(greeting in message.lower() for greeting in greetings)


def is_help_request(message: str) -> bool:
    """Yardım talebi kontrolü"""
    help_keywords = ["yardım", "help", "ne yapabilirsin", "neler yapabilirsin", "özellikleri"]
    return any(keyword in message.lower() for keyword in help_keywords)


def get_help_message() -> str:
    """Yardım mesajı"""
    return """🤖 **Mumu Yardım**

Ben Mumu'yum! Şunları yapabilirim:
• 💬 Sohbet etme ve sorularına cevap verme
• 📝 Metin analizi ve özet çıkarma
• 💡 Tavsiye ve bilgi sağlama
• 🎯 Görev ve hedef belirleme
• 🎓 Öğrenme konularında destek

Sadece sorunu sor veya sohbet etmek için yazı gönder! 😊"""


def validate_message(message: str) -> tuple[bool, str]:
    """Mesajı doğrula"""
    if not message:
        return False, "Boş mesaj alındı"
    
    if len(message) > 10000:
        return False, "Mesaj çok uzun (maksimum 10000 karakter)"
    
    return True, "OK"


def format_response(response: str, username: str = None) -> str:
    """Yanıtı formatla"""
    if username:
        return f"Merhaba {username}! 👋\n\n{response}"
    return response
