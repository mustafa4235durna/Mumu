FROM python:3.11-slim

WORKDIR /app

# Sistem paketlerini güncelle
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python paketlerini kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Port açımla
EXPOSE 5000

# Uygulamayı çalıştır
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
