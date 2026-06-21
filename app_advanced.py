"""
Mumu WhatsApp Assistant - Gelişmiş Sürüm
Yüksek performanslı, hata toleranslı, üretim-hazır
"""

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv
import logging
import json
from datetime import datetime
from functools import wraps
import time

# Ortam değişkenlerini yükle
load_dotenv()

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask uygulamasını oluştur
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# OpenAI API anahtarını ayarla
openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    logger.warning("⚠️ OPENAI_API_KEY belirlenmemiş!")

# Sistem mesajı - Mumu'nun kişiliği
SYSTEM_MESSAGE = """Sen Mumu'sun. Samimi, yardımcı ve kısa cevap veren bir WhatsApp asistanısın.
Özelliklerin:
- Kullanıcının adını öğrenmek ve hatırlamak
- Metin analizi ve özet çıkarma yapabilmek
- Tavsiye ve bilgi sağlayabilmek
- Türkçe cevap vermek (elbette kullanıcı başka dil kullanmadıkça)
- Emojiyi uygun kullanmak (abartma)
- Kısa ve öz cevaplar vermek (WhatsApp mesajları için uygun)
- Merak edilen konularda derinlemesine cevap verebilmek
- Bazen espri yapmak ve sohbeti keyifli tutmak

Mesajlara cevap verirken samimi, yardımcı ve profesyonel ol."""

# Cache için basit bir dict (production'da Redis kullanılmalı)
message_cache = {}
CACHE_TTL = 3600  # 1 saat

# Rate limiting
rate_limit = {}
RATE_LIMIT_REQUESTS = 100  # İstek sayısı
RATE_LIMIT_PERIOD = 3600  # 1 saat


def rate_limiter(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        phone_number = request.form.get('From', 'unknown')
        now = time.time()
        
        if phone_number not in rate_limit:
            rate_limit[phone_number] = []
        
        # Eski istekleri temizle
        rate_limit[phone_number] = [
            req_time for req_time in rate_limit[phone_number]
            if now - req_time < RATE_LIMIT_PERIOD
        ]
        
        # Rate limit kontrolü
        if len(rate_limit[phone_number]) >= RATE_LIMIT_REQUESTS:
            logger.warning(f"Rate limit exceeded for {phone_number}")
            resp = MessagingResponse()
            resp.message("⏱️ Çok fazla istek gönderdin. Lütfen biraz sonra tekrar dene!")
            return str(resp), 429
        
        rate_limit[phone_number].append(now)
        return f(*args, **kwargs)
    
    return decorated_function


def get_cache_key(message: str, phone: str) -> str:
    """Cache anahtarı oluştur"""
    return f"{phone}:{hash(message.lower())}"


def get_cached_response(message: str, phone: str) -> str | None:
    """Önbellekten yanıt al"""
    key = get_cache_key(message, phone)
    if key in message_cache:
        cached = message_cache[key]
        if time.time() - cached['timestamp'] < CACHE_TTL:
            logger.info(f"Cache hit: {key}")
            return cached['response']
        else:
            del message_cache[key]
    return None


def set_cached_response(message: str, phone: str, response: str):
    """Yanıtı önbelleğe al"""
    key = get_cache_key(message, phone)
    message_cache[key] = {
        'response': response,
        'timestamp': time.time()
    }


@app.before_request
def log_request():
    """Gelen istekleri kaydet"""
    if request.method == 'POST':
        logger.info(f"📨 POST {request.path} from {request.remote_addr}")


@app.after_request
def log_response(response):
    """Giden yanıtları kaydet"""
    if request.method == 'POST':
        logger.info(f"📤 Response {response.status_code} for {request.path}")
    return response


@app.route("/webhook", methods=["POST"])
@rate_limiter
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
        
        logger.info(f"📬 Mesaj alındı: {numara} -> '{gelen_mesaj[:50]}'")
        
        # Önbellekten kontrol et
        cached = get_cached_response(gelen_mesaj, numara)
        if cached:
            logger.info("✅ Önbellekten yanıt kullanıldı")
            resp = MessagingResponse()
            resp.message(cached)
            return str(resp), 200
        
        # OpenAI API'ye istek gönder
        logger.info("🔄 OpenAI API'ye istek gönderiliyor...")
        cevap = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": gelen_mesaj}
            ],
            temperature=0.7,
            max_tokens=500,
            presence_penalty=0.1,
            frequency_penalty=0.1
        )
        
        # Yanıtı al
        yanit = cevap.choices[0].message.content
        
        # Yanıtı önbelleğe al
        set_cached_response(gelen_mesaj, numara, yanit)
        
        logger.info(f"✅ Yanıt hazır: {yanit[:50]}...")
        
        # Twilio TwiML yanıtı oluştur
        resp = MessagingResponse()
        resp.message(yanit)
        
        return str(resp), 200
        
    except openai.error.RateLimitError:
        logger.error("❌ OpenAI rate limit hatası")
        resp = MessagingResponse()
        resp.message("🔄 Sistem şu anda yoğun, lütfen biraz sonra tekrar dene!")
        return str(resp), 429
        
    except openai.error.AuthenticationError:
        logger.error("❌ OpenAI kimlik doğrulama hatası - API anahtarı kontrol et")
        resp = MessagingResponse()
        resp.message("🔑 Sistemde kimlik doğrulama sorunu var. Lütfen yöneticiye bildir.")
        return str(resp), 500
        
    except openai.error.APIError as e:
        logger.error(f"❌ OpenAI API hatası: {str(e)}")
        resp = MessagingResponse()
        resp.message("⚠️ Üzgünüm, bir hata oluştu. Lütfen daha sonra tekrar dene.")
        return str(resp), 500
        
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        resp.message("😔 Bir hata oluştu, lütfen daha sonra tekrar dene!")
        return str(resp), 500


@app.route("/health", methods=["GET"])
def health():
    """
    Sağlık kontrol endpointi
    """
    health_status = {
        "status": "healthy",
        "service": "Mumu WhatsApp Assistant",
        "timestamp": datetime.now().isoformat(),
        "openai_configured": bool(openai.api_key)
    }
    return jsonify(health_status), 200


@app.route("/stats", methods=["GET"])
def stats():
    """
    İstatistikler endpointi
    """
    stats_data = {
        "cached_messages": len(message_cache),
        "active_users": len(rate_limit),
        "timestamp": datetime.now().isoformat()
    }
    return jsonify(stats_data), 200


@app.route("/", methods=["GET"])
def home():
    """
    Ana sayfa
    """
    return jsonify({
        "name": "Mumu - WhatsApp Assistant",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "webhook": "POST /webhook",
            "health": "GET /health",
            "stats": "GET /stats"
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """404 hatası"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """500 hatası"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("DEBUG", "False") == "True"
    
    logger.info("=" * 50)
    logger.info("🤖 Mumu WhatsApp Assistant başlatılıyor...")
    logger.info(f"📍 http://0.0.0.0:{port}")
    logger.info(f"🔧 Debug Mode: {debug_mode}")
    logger.info("=" * 50)
    
    app.run(host="0.0.0.0", port=port, debug=debug_mode, use_reloader=False)
