# 🔍 Domain Tracker

Telegram bot entegrasyonlu domain izleme uygulaması. Belirlediğiniz domainlerin kayıt durumunu kontrol eder ve müsait hale geldiklerinde Telegram üzerinden bildirim gönderir.

## 🚀 Kurulum

### 1. Proje İndirme

```bash
git clone https://github.com/omer-faruk-ozmen/domain-tracker.git
cd domain-tracker
```

### 2. Bağımlılıkları Yükleme

```bash
python3 -m venv venv
source venv/bin/activate  # Linux
# veya
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Konfigürasyon

`.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:

```bash
cp .env.example .env
nano .env
```

```properties
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_AVAILABLE_CHAT_ID=YOUR_CHAT_ID_HERE
TELEGRAM_UNAVAILABLE_CHAT_ID=YOUR_CHAT_ID_HERE
```

### 4. Çalıştırma

```bash
python main.py
```

## 🎮 Bot Komutları

- `/add <domain>` - Domain izlemeye ekle
- `/remove <domain>` - Domain izlemeden çıkar
- `/reset <domain>` - Müsait domain'i tekrar izlemeye al
- `/list` - İzlenen domainleri listele
- `/status` - İstatistikleri göster
- `/logs` - Son logları göster
- `/help` - Yardım

## 🖥️ Linux Sunucuda Servis Olarak Çalıştırma

1. **Servis dosyasını oluşturun:**

```bash
sudo nano /etc/systemd/system/domain-tracker.service
```

2. **İçeriği kopyalayın:** (Proje dizinindeki `domain-tracker.service` dosyasından)

3. **Servisi başlatın:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable domain-tracker
sudo systemctl start domain-tracker
```

4. **Durumu kontrol edin:**

```bash
sudo systemctl status domain-tracker
journalctl -u domain-tracker -f
```

## 📁 Proje Yapısı

```text
domain-tracker/
├── main.py                 # Ana uygulama
├── domain_monitor.py       # Domain izleme
├── telegram_bot.py         # Bot işlemleri
├── config.py              # Konfigürasyon
├── .env                   # Hassas bilgiler
└── logs/                  # Log dosyaları
```

## 🔧 Telegram Bot Kurulumu

1. [@BotFather](https://t.me/BotFather)'a `/newbot` gönderin
2. Bot adını belirleyin
3. Token'ı alın ve `.env` dosyasına ekleyin
4. Chat ID'nizi [@userinfobot](https://t.me/userinfobot)'tan öğrenin

---

⭐ Faydalı bulduysanız yıldız vermeyi unutmayın!
