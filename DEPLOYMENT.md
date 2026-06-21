## 🚀 Mumu WhatsApp Assistant - Deployment Rehberi

Bu dosya, Mumu'yu çeşitli ortamlarda deploy etmek için detaylı talimatlar içerir.

---

## 📋 İçindekiler

1. [Yerel Geliştirme](#yerel-geliştirme)
2. [Heroku Deploy](#heroku-deploy)
3. [Docker Deploy](#docker-deploy)
4. [AWS Lambda Deploy](#aws-lambda-deploy)
5. [VPS/Dedicated Server](#vpsdedicated-server)
6. [Sorun Giderme](#sorun-giderme)

---

## 🖥️ Yerel Geliştirme

### Hızlı Başlangıç

```bash
# 1. Repository'yi klonla
git clone <repo-url>
cd Mumu

# 2. Dev server'ı başlat
bash dev_server.sh

# 3. Ngrok ile expose et (başka terminal)
ngrok http 5000

# 4. Webhook URL'sini Twilio'da ayarla
# https://<ngrok-url>.ngrok.io/webhook
```

### Detaylı Adımlar

```bash
# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyasını ayarla
cp .env.example .env
# Düzenle: OPENAI_API_KEY, TWILIO_* değerlerini gir

# Flask'ı geliştirme modunda çalıştır
export FLASK_ENV=development
export DEBUG=True
python app.py
```

---

## ☁️ Heroku Deploy

### 1. Kurulum

```bash
# Heroku CLI'yi yükle
# https://devcenter.heroku.com/articles/heroku-cli

# Heroku'ya giriş yap
heroku login

# Yeni uygulama oluştur
heroku create mumu-assistant
```

### 2. Ortam Değişkenlerini Ayarla

```bash
heroku config:set OPENAI_API_KEY=sk-... -a mumu-assistant
heroku config:set TWILIO_ACCOUNT_SID=... -a mumu-assistant
heroku config:set TWILIO_AUTH_TOKEN=... -a mumu-assistant
heroku config:set TWILIO_WHATSAPP_NUMBER=whatsapp:+... -a mumu-assistant
heroku config:set DEBUG=False -a mumu-assistant
```

### 3. Deploy Et

```bash
# Repository'ye ekle
git add .
git commit -m "Deploy Mumu to Heroku"

# Heroku'ya push et
git push heroku main
```

### 4. Webhook URL'sini Güncelleştir

Twilio Console'da webhook URL'sini şu şekilde ayarla:
```
https://mumu-assistant.herokuapp.com/webhook
```

### 5. Logs Kontrol Et

```bash
heroku logs -f -a mumu-assistant
```

### Heroku Sorunları

```bash
# Dyno'yu restart et
heroku restart -a mumu-assistant

# Buildpack kontrol et
heroku buildpacks -a mumu-assistant

# Sağlık durumunu kontrol et
curl https://mumu-assistant.herokuapp.com/health
```

---

## 🐳 Docker Deploy

### 1. Yerel Docker Build

```bash
# Docker image'ı build et
docker build -t mumu-assistant:latest .

# Image'ı çalıştır
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=sk-... \
  -e TWILIO_ACCOUNT_SID=... \
  -e TWILIO_AUTH_TOKEN=... \
  mumu-assistant:latest
```

### 2. Docker Compose ile

```bash
# .env dosyasını ayarla
cp .env.example .env

# Docker Compose'u başlat
docker-compose up -d

# Logs kontrol et
docker-compose logs -f mumu

# Durdur
docker-compose down
```

### 3. Docker Hub'a Push Et

```bash
# Docker Hub'da giriş yap
docker login

# Tag'i ayarla
docker tag mumu-assistant:latest username/mumu-assistant:latest

# Push et
docker push username/mumu-assistant:latest
```

### 4. Docker Tarafından Çalıştır

```bash
docker run -d \
  --name mumu \
  -p 5000:5000 \
  -e OPENAI_API_KEY=sk-... \
  -e TWILIO_ACCOUNT_SID=... \
  -e TWILIO_AUTH_TOKEN=... \
  username/mumu-assistant:latest
```

---

## 🚀 AWS Lambda Deploy

### 1. Zappa Kurulumu

```bash
# Zappa'yı yükle
pip install zappa

# Zappa'yı başlat
zappa init

# Sorulara cevap ver:
# - environment: dev, prod
# - S3 bucket: create new or existing
```

### 2. Zappa Config Ayarla

`zappa_settings.json` düzenle:

```json
{
    "dev": {
        "app_function": "app.app",
        "aws_region": "us-east-1",
        "profile_name": "default",
        "project_name": "mumu",
        "runtime": "python3.11",
        "s3_bucket": "mumu-lambda-bucket",
        "environment_variables": {
            "OPENAI_API_KEY": "sk-...",
            "TWILIO_ACCOUNT_SID": "...",
            "TWILIO_AUTH_TOKEN": "...",
            "DEBUG": "False"
        }
    }
}
```

### 3. Deploy Et

```bash
# Staging ortamını deploy et
zappa deploy dev

# Güncelleştirmeleri push et
zappa update dev

# Logs kontrol et
zappa tail dev
```

### 4. Lambda URL'sini Twilio'da Ayarla

Webhook URL:
```
https://<lambda-url>.lambda-url.us-east-1.on.aws/webhook
```

---

## 🖥️ VPS/Dedicated Server

### 1. Sunucu Hazırlığı (Ubuntu 20.04+)

```bash
# Sistem güncelle
sudo apt update && sudo apt upgrade -y

# Python ve gerekli paketleri yükle
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx
```

### 2. Uygulamayı Klonla

```bash
# /var/www dizinine klonla
sudo mkdir -p /var/www/mumu
cd /var/www/mumu
sudo git clone <repo-url> .

# Sahiplik ayarla
sudo chown -R www-data:www-data /var/www/mumu
```

### 3. Python Ortamı

```bash
# Sanal ortam oluştur
python3.11 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyasını ayarla
sudo cp .env.example .env
sudo nano .env  # Değerleri gir
```

### 4. Gunicorn Servisi Oluştur

`/etc/systemd/system/mumu.service` oluştur:

```ini
[Unit]
Description=Mumu WhatsApp Assistant
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/mumu
Environment="PATH=/var/www/mumu/venv/bin"
EnvironmentFile=/var/www/mumu/.env
ExecStart=/var/www/mumu/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Servisi başlat:
```bash
sudo systemctl start mumu
sudo systemctl enable mumu
sudo systemctl status mumu
```

### 5. Nginx Yapılandırması

`/etc/nginx/sites-available/mumu` oluştur:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Etkinleştir:
```bash
sudo ln -s /etc/nginx/sites-available/mumu /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL Sertifikası (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 7. Logs ve Monitoring

```bash
# Logs kontrol et
sudo journalctl -u mumu -f

# Sağlık durumunu kontrol et
curl https://your-domain.com/health
```

---

## 🐛 Sorun Giderme

### Problem: "OpenAI API key not found"

```bash
# .env dosyasını kontrol et
cat .env | grep OPENAI_API_KEY

# Ortam değişkeni ayarlandı mı?
echo $OPENAI_API_KEY

# Ortam değişkenlerini yükle
export OPENAI_API_KEY="sk-..."
```

### Problem: "Twilio authentication failed"

```bash
# Twilio credentials'ı kontrol et
heroku config -a mumu-assistant

# Test et
curl -X POST https://your-app.com/health
```

### Problem: "Module not found"

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Bağımlılıkları doğrula
pip list | grep -E "flask|openai|twilio"
```

### Problem: "Connection timeout"

```bash
# Firewall kontrol et
sudo ufw status

# Port açılmış mı?
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5000/tcp
```

### Problem: "Rate limit exceeded"

OpenAI rate limiting sorunları:
1. API quota'nı kontrol et (https://platform.openai.com/account/billing/overview)
2. Rate limit handling kodunu kontrol et
3. Cache'i kontrol et

```python
# app_advanced.py'daki cache mekanizmasını kontrol et
GET /stats  # Cached messages sayısını gör
```

---

## 📊 Monitoring ve Logging

### Application Monitoring

```bash
# Health check
curl https://your-domain.com/health

# Statistics
curl https://your-domain.com/stats

# Logs view
tail -f logs/mumu_*.log
```

### Performance Tuning

```bash
# Gunicorn worker sayısını artır
gunicorn -w 8 -b 0.0.0.0:5000 app:app

# Timeout ayarla
gunicorn -w 4 -t 120 -b 0.0.0.0:5000 app:app

# Keep-alive bağlantıları
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

---

## 🔐 Güvenlik En İyi Uygulamaları

### 1. Ortam Değişkenleri

```bash
# Asla repository'ye .env eklemez
echo ".env" >> .gitignore

# Production'da güçlü secret kullan
export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
```

### 2. API Key Rotasyonu

```bash
# Düzenli olarak API key'leri döndür
# Twilio: https://www.twilio.com/console/settings/general
# OpenAI: https://platform.openai.com/account/api-keys
```

### 3. Rate Limiting

App'da zaten yapılmış:
```python
RATE_LIMIT_REQUESTS = 100  # istek
RATE_LIMIT_PERIOD = 3600   # 1 saat
```

### 4. HTTPS

Always use HTTPS in production:
```bash
# Nginx yapılandırmasında SSL enable et
# Heroku otomatik olarak HTTPS sağlar
# AWS Lambda: API Gateway ile HTTPS
```

---

## 📝 Checklist - Production'a Hazırlanma

- [ ] `.env` dosyasında tüm credentials ayarlandı mı?
- [ ] API key'ler hard-coded değil mi?
- [ ] HTTPS/SSL etkinleştirildi mi?
- [ ] Rate limiting ayarlandı mı?
- [ ] Logging yapılandırıldı mı?
- [ ] Health check endpoint'i test edildi mi?
- [ ] Webhook URL'si Twilio'da ayarlandı mı?
- [ ] Backup/Disaster recovery planı var mı?
- [ ] Monitoring setup yapıldı mı?
- [ ] Team'in deployment prosesi biliyor mu?

---

## 📚 Yararlı Kaynaklar

- [Heroku Deployment Best Practices](https://devcenter.heroku.com/articles/best-practices-for-app-configuration)
- [Twilio WebHook Documentation](https://www.twilio.com/docs/sms/webhooks)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Last Updated:** 2024-06-21  
**Version:** 2.0.0
