#!/bin/bash

# Mumu WhatsApp Assistant - Startup Script

echo "🤖 Mumu WhatsApp Assistant başlatılıyor..."
echo ""

# Sanal ortam kontrol et
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı aktifleştir
echo "🔧 Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Bağımlılıkları yükle
echo "📚 Bağımlılıklar yükleniyor..."
pip install -r requirements.txt

# .env kontrol et
if [ ! -f ".env" ]; then
    echo "⚠️  .env dosyası bulunamadı!"
    echo "📋 .env.example'dan .env oluşturuluyor..."
    cp .env.example .env
    echo "✏️  .env dosyasını düzenleyip gerekli bilgileri gir!"
    echo ""
    exit 1
fi

# Uygulamayı çalıştır
echo ""
echo "✅ Tüm hazırlıklar tamam!"
echo "🚀 Uygulama başlatılıyor..."
echo ""
python app.py
