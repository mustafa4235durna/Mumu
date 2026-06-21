"""
Webhook Test Script - Mumu WhatsApp Assistant
"""

import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Test URL
WEBHOOK_URL = "http://localhost:5000/webhook"

# Test mesajları
test_messages = [
    "Merhaba! Bugün nasılsın?",
    "Python nedir?",
    "Bana bir şarkı öner",
    "Kahvaltıda ne yesem?",
]

def test_webhook():
    """Webhook'u test et"""
    
    for message in test_messages:
        print(f"\n{'='*50}")
        print(f"📤 Mesaj: {message}")
        print('='*50)
        
        # Test payload
        data = {
            "Body": message,
            "From": "whatsapp:+1234567890",
            "AccountSid": os.environ.get("TWILIO_ACCOUNT_SID", "test"),
        }
        
        try:
            response = requests.post(WEBHOOK_URL, data=data, timeout=10)
            print(f"✅ Status: {response.status_code}")
            print(f"📥 Response:\n{response.text[:500]}")
        except requests.exceptions.ConnectionError:
            print("❌ Hata: Sunucuya bağlanılamadı")
            print("💡 Tip: Flask uygulaması çalışıyor mu? (python app.py)")
        except Exception as e:
            print(f"❌ Hata: {str(e)}")

def test_health():
    """Health endpoint'i test et"""
    print(f"\n{'='*50}")
    print("🏥 Health Check")
    print('='*50)
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Response: {response.json()}")
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

if __name__ == "__main__":
    print("🤖 Mumu WhatsApp Assistant - Webhook Test\n")
    
    # Health kontrolü
    test_health()
    
    # Webhook testi
    test_webhook()
    
    print(f"\n{'='*50}")
    print("✅ Test tamamlandı!")
    print('='*50)
