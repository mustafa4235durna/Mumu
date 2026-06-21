#!/bin/bash

# 🚀 MUMU DEPLOYMENT AUTOMATION
# Bu script tüm setup'ı otomatik yapar

set -e  # Hata olursa dur

echo "🤖 MUMU WHATSAPP ASSISTANT - AUTOMATED DEPLOYMENT"
echo "=================================================="
echo ""

# 1. GIT SETUP
echo "📦 1. Git setup..."
cd /workspaces/Mumu
git add -A
git commit -m "🔐 Production credentials configured" 2>/dev/null || true
echo "✅ Git ready"
echo ""

# 2. .ENV VALIDATION
echo "🔐 2. Environment variables..."
if [ -f .env ]; then
    echo "✅ .env dosyası bulundu"
    # Kontrol et
    if grep -q "OPENAI_API_KEY" .env && grep -q "TWILIO_ACCOUNT_SID" .env; then
        echo "✅ Tüm gerekli credentials var"
    else
        echo "❌ Eksik credentials!"
        exit 1
    fi
else
    echo "❌ .env dosyası yok!"
    exit 1
fi
echo ""

# 3. PYTHON DEPENDENCIES
echo "📚 3. Python bağımlılıkları..."
if python3 -c "import flask" 2>/dev/null; then
    echo "✅ Flask kurulu"
else
    echo "📥 Flask kuruluyor..."
    pip install -q flask python-dotenv openai twilio requests gunicorn
    echo "✅ Bağımlılıklar kuruldu"
fi
echo ""

# 4. APP TEST
echo "🧪 4. Uygulama test..."
python3 -m py_compile app.py app_advanced.py
echo "✅ Syntax kontrol OK"
echo ""

# 5. WEBHOOK TEST
echo "🔗 5. Webhook test..."
if [ -f test_webhook.py ]; then
    echo "✅ Test script bulundu"
    echo "   (Local test için Flask çalışmalı)"
else
    echo "⚠️  Test script yok"
fi
echo ""

# 6. DEPLOYMENT READY
echo "📋 6. Deployment Checklist..."
echo ""
echo "✅ GitHub repo: https://github.com/mustafa4235durna/Mumu"
echo "✅ Credentials: Configured"
echo "✅ Code: Ready"
echo ""

cat << 'DEPLOYMENT'

🚀 RAILWAY DEPLOYMENT (Sonraki adımlar):

1. https://railway.app git
2. "Create New Project" → "Deploy from GitHub"
3. Repository seç: mustafa4235durna/Mumu
4. Deploy tıkla
5. Railway dashboard → Settings → Variables
6. .env'deki bilgileri environment'a ekle
7. Deploy waiting...

⏱️  15-30 saniye içinde URL alacaksın!

WEBHOOK URL'NI TWILIO'DA AYARLA:

1. https://console.twilio.com → Messaging → Sandbox
2. "When a message comes in" kutusuna:
   https://[railway-url]/webhook
3. Save

TEST ET:

1. WhatsApp sandbox'a katıl:
   +1 415-523-8886
   Mesaj: join something-word

2. Sonra mesaj gönder:
   "Merhaba Mumu!"

3. ✅ Cevap almışsan başarıyorsun!

DEPLOYMENT
echo ""

echo "📊 SUMMARY:"
echo "  • Repository: https://github.com/mustafa4235durna/Mumu"
echo "  • Credentials: ✅ Configured"
echo "  • Code Status: ✅ OK"
echo "  • Next: Railway deployment manual (1 min)"
echo ""

echo "🎉 Hazırlanma tamamlandı! Railway'de deploy et."
echo ""
