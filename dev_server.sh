#!/bin/bash

# Mumu WhatsApp Assistant - Development Server Script

echo "🤖 Mumu WhatsApp Assistant - Geliştirme Sunucusu"
echo "================================================"
echo ""

# .env kontrol et
if [ ! -f ".env" ]; then
    echo "⚠️  .env dosyası bulunamadı!"
    echo "📋 .env.example'dan .env oluşturuluyor..."
    cp .env.example .env
    echo ""
    echo "✏️  Lütfen .env dosyasını düzenleyip gerekli bilgileri gir:"
    echo "   - OPENAI_API_KEY"
    echo "   - TWILIO_ACCOUNT_SID"
    echo "   - TWILIO_AUTH_TOKEN"
    echo "   - TWILIO_WHATSAPP_NUMBER"
    echo ""
    echo "💡 Daha sonra bu script'i tekrar çalıştır."
    exit 1
fi

# Sanal ortamı kontrol et
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python3 -m venv venv
    echo "✅ Sanal ortam oluşturuldu"
    echo ""
fi

# Sanal ortamı aktifleştir
echo "🔧 Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Bağımlılıkları yükle
echo "📚 Bağımlılıklar kontrol ediliyor..."
pip install -q -r requirements.txt
echo "✅ Bağımlılıklar yüklendi"
echo ""

# Flask'ı geliştirme modunda çalıştır
echo "✅ Tüm hazırlıklar tamam!"
echo ""
echo "🚀 Geliştirme sunucusu başlatılıyor..."
echo "📍 http://localhost:5000"
echo "🔗 Webhook: http://localhost:5000/webhook"
echo ""
echo "💡 Ngrok ile test etmek için başka terminal penceresinde şu komutu çalıştır:"
echo "   ngrok http 5000"
echo ""
echo "⚙️  Kayıt dosyası: logs/"
echo ""

export FLASK_APP=app
export FLASK_ENV=development
export DEBUG=True

python -m flask run --host=0.0.0.0 --port=5000
