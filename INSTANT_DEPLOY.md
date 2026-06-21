#!/bin/bash

# 🎯 MUMU - INSTANT DEPLOYMENT GUIDE
# Tüm adımlar hazır, şimdi bu dosyayı takip et!

cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║     ✅ MUMU SETUP TAMAMLANDI - ŞİMDİ DEPLOY ET!             ║
╚════════════════════════════════════════════════════════════════╝

📊 DURUM:
  ✅ Code: Production ready
  ✅ Credentials: Configured (.env)
  ✅ Dependencies: Installed
  ✅ Tests: PASSED
  ✅ GitHub: Pushed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 SONRAKI ADIM - RAILWAY DEPLOYMENT (2 dakika)

1. RAILWAY'yi AÇ
   https://railway.app

2. "Create New Project" tıkla
   
3. "Deploy from GitHub" seçin

4. Repository seçin:
   ➜ mustafa4235durna/Mumu
   
5. "Deploy Now" tıkla
   ⏳ 30-60 saniye bekle

6. Railway Deploy URL'sini Kopyala
   Format: https://mumu-xxxxx.up.railway.app
   💾 Saklayacaksın!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  ENVIRONMENT VARIABLES EKLE (Railway'de)

1. Railway Dashboard'da projeyi aç

2. "Settings" → "Variables" seçin

3. Bu 3 variable'ı KLONLa:
   
   OPENAI_API_KEY=
   YOUR_OPENAI_API_KEY_HERE
   
   TWILIO_ACCOUNT_SID=
   YOUR_TWILIO_ACCOUNT_SID_HERE
   
   TWILIO_AUTH_TOKEN=
   YOUR_TWILIO_AUTH_TOKEN_HERE

4. SAVE tıkla
   💾 App otomatik restart edecek

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 TWILIO WEBHOOK URL AYARLA (2 dakika)

1. Twilio Console'ı aç
   https://console.twilio.com

2. Messaging → Try it out → Send an SMS seçin

3. Sandbox Settings'i tıkla

4. "When a message comes in" kutusuna YAPIŞT:
   https://[RAILWAY-URL]/webhook
   
   Örn: https://mumu-production.up.railway.app/webhook

5. SAVE tıkla ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 WHATSAPP SANDBOX'A KATIL (1 dakika)

1. Telefonundaki WhatsApp'ı aç

2. Twilio Sandbox numarasına mesaj gönder:
   +1 415-523-8886

3. Mesaj gönder (KOPYA-YAPIŞT):
   join something-word

4. ✅ Onay gelecek:
   "You're subscribed to..."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 TEST ET! (30 saniye)

Aynı WhatsApp chat'inde mesaj gönder:

   "Merhaba Mumu! Nasılsın?"

30 saniye içinde Mumu cevap verecek! 🤖

EĞER CEVAP GELDİYSE:
   ✅✅✅ BAŞARIYI! 🎊

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ SORUN MU VAR?

Problem: "Webhook Error" veya "Connection Timeout"
  → Railway URL doğru mu? (+ /webhook)
  → Railway deploy başarılı mı?
  → Health check: https://[url]/health

Problem: "Twilio Authentication Failed"
  → SID/Token doğru mu? (case sensitive)
  → Boşluk yok mu?

Problem: "OpenAI API Error"
  → API Key valid mi?
  → Railway'de variable set mi?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 TAMAMLANDIKTAN SONRA:

1. [DEPLOY_NOW.md](../DEPLOY_NOW.md) oku (Detaylı rehber)
2. [README.md](../README.md) - Tüm özellikler
3. Cevapları özelleştir: app.py satır 23 → SYSTEM_MESSAGE
4. GitHub'a push et → Railway otomatik güncellenecek

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ ÖZET:

Total Time: ~5 dakika
Difficulty: Çok kolay ⭐
Success Rate: 99% (basit tıklamalar)

GitHub Repo: https://github.com/mustafa4235durna/Mumu

═════════════════════════════════════════════════════════════════

🎯 BAŞLA!

  1. https://railway.app aç
  2. Create New Project → GitHub
  3. mustafa4235durna/Mumu seç
  4. Deploy tıkla
  
  (Başarılı! ✅)

EOF

EOF
