"""
WhatsApp Assistant - Mumu
Powered by OpenAI GPT-4o-mini and Twilio
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv
import logging

# Ortam değişkenlerini yükle
load_dotenv()

# Logging ayarla
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask uygulamasını oluştur
app = Flask(__name__)

# OpenAI API anahtarını ayarla
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Sistem mesajı - Mumuun kişiliği
SYSTEM_MESSAGE = """Sen Mumu'sun. Samimi, yardımcı ve kısa cevap veren bir WhatsApp asistanısın.
Özelliklerin:
- Kullanıcının adını öğrenmek ve hatırlamak
- Metin analizi ve özet çıkarma yapabilmek
- Tavsiye ve bilgi sağlayabilmek
- Türkçe cevap vermek (elbette kullanıcı başka dil kullanmadıkça)
- Emojiyi uygun kullanmak (abartma)
- Kısa ve öz cevaplar vermek (WhatsApp mesajları için uygun)

Mesajlara cevap verirken samimi ve yardımcı ol."""


@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    """
    Twilio WebHook - WhatsApp mesajlarını işle
    """
    try:
        # Gelen veriler
        gelen_mesaj = request.form.get("Body", "").strip()
        numara = request.form.get("From", "")
        
        if not gelen_mesaj:
            logger.warning("Boş mesaj alındı")
            return "OK", 400
        
        logger.info(f"Mesaj alındı: {numara} -> {gelen_mesaj}")
        
        # OpenAI API'ye istek gönder
        cevap = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": gelen_mesaj}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Yanıtı al
        yanit = cevap.choices[0].message.content
        
        logger.info(f"Yanıt gönderildi: {yanit[:50]}...")
        
        # Twilio TwiML yanıtı oluştur
        resp = MessagingResponse()
        resp.message(yanit)
        
        return str(resp), 200
        
    except openai.error.RateLimitError:
        logger.error("OpenAI rate limit hatası")
        resp = MessagingResponse()
        resp.message("Çok fazla istek alıyorum, lütfen biraz sonra tekrar dene 🔄")
        return str(resp), 429
        
    except openai.error.AuthenticationError:
        logger.error("OpenAI kimlik doğrulama hatası")
        resp = MessagingResponse()
        resp.message("Üzgünüm, sistem hatasından dolayı şu anda çalışamıyorum ❌")
        return str(resp), 500
        
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {str(e)}")
        resp = MessagingResponse()
        resp.message("Bir hata oluştu, lütfen daha sonra tekrar dene 😔")
        return str(resp), 500


@app.route("/health", methods=["GET"])
def health():
    """
    Sağlık kontrol endpointi
    """
    return {"status": "healthy", "service": "Mumu WhatsApp Assistant"}, 200


@app.route("/", methods=["GET"])
def home():
    """
    Ana sayfa
    """
    return {
        "name": "Mumu - WhatsApp Assistant",
        "version": "1.0.0",
        "status": "running",
        "webhook": "/webhook"
    }, 200


if __name__ == "__main__":
    # Üretim ortamı için Gunicorn kullan: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    # Geliştirme ortamı:
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
