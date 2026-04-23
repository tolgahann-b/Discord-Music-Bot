# Python'un hafif bir sürümünü kullanıyoruz
FROM python:3.12-slim

# Sistem güncellemelerini yap ve müzik için gerekli olan FFmpeg'i kur
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini oluştur
WORKDIR /app

# Kütüphane listesini kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm kodları kopyala
COPY . .

# Botu çalıştır
CMD ["python", "main.py"]
