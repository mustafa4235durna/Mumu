"""
Mumu WhatsApp Assistant - Yapılandırma
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Temel yapılandırma"""
    
    # OpenAI
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    
    # Twilio
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")
    
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DEBUG = os.environ.get("DEBUG", False)
    
    # Asistan
    ASSISTANT_NAME = os.environ.get("ASSISTANT_NAME", "Mumu")
    ASSISTANT_PERSONALITY = os.environ.get("ASSISTANT_PERSONALITY", "friendly")
    MAX_RESPONSE_LENGTH = int(os.environ.get("MAX_RESPONSE_LENGTH", 1000))


class DevelopmentConfig(Config):
    """Geliştirme yapılandırması"""
    DEBUG = True


class ProductionConfig(Config):
    """Üretim yapılandırması"""
    DEBUG = False


class TestingConfig(Config):
    """Test yapılandırması"""
    TESTING = True
    DEBUG = True


# Ortama göre yapılandırma seç
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
