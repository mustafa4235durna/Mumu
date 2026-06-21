# 🤖 Mumu - WhatsApp Asistanı

Mumu, OpenAI GPT-4o-mini ve Twilio WebHook'u kullanarak gerçek zamanlı WhatsApp desteği sağlayan akıllı bir asistandır.

## ✨ Özellikler

- 🤖 **OpenAI GPT-4o-mini**: Güçlü ve ucuz AI modeli
- 💬 **Gerçek Zamanlı**: WhatsApp mesajlarına anında cevap
- 🌍 **Multimedya Desteği**: Twilio aracılığıyla mesaj gönder/al
- 🔒 **Güvenli**: Ortam değişkenleri ile API anahtarı yönetimi
- 📊 **Logging**: Tüm işlemlerin kaydı
- 🚀 **Üretim Hazır**: Gunicorn ile deploy edilmeye hazır
- ⚡ **Hızlı**: Minimal latency ile cevap verme

## 📋 Gereksinimler

- Python 3.8+
- OpenAI API Anahtarı
- Twilio Hesabı (WhatsApp entegrasyonu için)
- pip paket yöneticisi

## 🚀 Kurulum

### 1. Projeyi Klonla
```bash
cd Mumu
```

### 2. Sanal Ortamı Oluştur
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları Kur
```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarla
```bash
cp .env.example .env
```

`.env` dosyasını açıp aşağıdaki bilgileri doldur:

```env
OPENAI_API_KEY=sk-your-api-key-here
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
DEBUG=True
```

### 5. Uygulamayı Çalıştır

**Geliştirme Ortamı:**
```bash
python app.py
```

**Üretim Ortamı:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Uygulama şu adreste çalışacak: `http://localhost:5000`

## 🔧 Twilio Yapılandırması

### Webhook URL Ayarla

1. [Twilio Console](https://console.twilio.com)'a git
2. Messaging → WhatsApp → Sandbox Settings
3. **When a message comes in** alanına şunu ekle:
   ```
   https://your-domain.com/webhook
   ```
4. **Save** butonuna tıkla

### Ngrok ile Yerel Test (Geliştirme)

```bash
# Başka bir terminal penceresinde:
ngrok http 5000
```

Ngrok URL'sini Twilio webhook ayarlarında kullan.

## 📚 API Endpoints

### POST `/webhook`
WhatsApp mesajlarını işler.

**Request:**
```
Body: Kullanıcının mesajı
From: Kullanıcının WhatsApp numarası
```

**Response:**
TwiML format yanıt (Twilio tarafından otomatik olarak gönderilir)

### GET `/health`
Sağlık durumunu kontrol et.

**Response:**
```json
{
    "status": "healthy",
    "service": "Mumu WhatsApp Assistant"
}
```

### GET `/`
Temel bilgi.

**Response:**
```json
{
    "name": "Mumu - WhatsApp Assistant",
    "version": "1.0.0",
    "status": "running",
    "webhook": "/webhook"
}
```

## 🎯 Kullanım Örneği

1. WhatsApp'ta Twilio Sandbox numarasına mesaj gönder
2. Mumu otomatik olarak cevap verir
3. Doğal dil sorularına destekle

**Örnek Sorular:**
- "Merhaba! Bugün nasılsın?"
- "Python hakkında ne düşünüyorsun?"
- "Kahvaltıda ne yesem iyi olur?"
- "Bir şarkı öner"

## 🔐 Güvenlik En İyi Uygulamaları

✅ **Yapılan:**
- API anahtarları `.env` dosyasında tutulur
- `.env` dosyası `.gitignore`'da listelenir
- Rate limit hatası yönetimi
- Authentication hatası yönetimi
- Hata logging'i

⚠️ **Dikkat edilecekler:**
- `.env` dosyasını asla repository'ye eklemez
- API anahtarlarını paylaşma
- Düzenli olarak API kullanımını kontrol et
- Üretim ortamında `DEBUG=False` kullan

## 📊 Dosya Yapısı

```
Mumu/
├── app.py                 # Ana uygulama
├── config.py              # Yapılandırma dosyası
├── requirements.txt       # Python bağımlılıkları
├── .env.example           # Ortam değişkenleri örneği
├── .env                   # Ortam değişkenleri (gitignore'da)
├── .gitignore             # Git ignoring
├── README.md              # Bu dosya
└── venv/                  # Sanal ortam (gitignore'da)
```

## 🐛 Sorun Giderme

### "OpenAI API key not set"
- `.env` dosyasında `OPENAI_API_KEY` ayarlandı mı?
- `load_dotenv()` çalıştırıldı mı?

### "Twilio authentication failed"
- `TWILIO_ACCOUNT_SID` ve `TWILIO_AUTH_TOKEN` doğru mu?
- Twilio hesabınız aktif mi?

### "No module named 'openai'"
```bash
pip install -r requirements.txt
```

### Webhook çalışmıyor
- Webhook URL'si doğru mu?
- Server çalışıyor mu?
- Firewall/NAT bloklaması var mı?
- Geliştirme için Ngrok kullan

## 🚢 Deployment

### Heroku Deploy

1. Heroku hesabı oluştur
2. `Procfile` oluştur:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

3. Deploy et:
```bash
heroku create mumu-assistant
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set TWILIO_ACCOUNT_SID=...
heroku config:set TWILIO_AUTH_TOKEN=...
git push heroku main
```

### Docker Deploy

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📝 Lisans

MIT License - Özgürce kullanabilirsin

## 👨‍💻 Katkılar

Pull request'ler kabul edilir. Büyük değişiklikler için önce issue aç.

## 💬 İletişim

Sorularınız veya önerileriniz için GitHub issue'su açabilirsin.

---

**Mumu** tarafından ❤️ oluşturuldu
