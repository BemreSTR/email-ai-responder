
# 🤖 Email AI Responder

Gmail entegrasyonu ile çalışan otomatik AI e-posta yanıt sistemi. Google Gemini 2.0 Flash kullanarak akıllı yanıtlar oluşturur.

## ✨ Özellikler

- 📧 Gmail API ile otomatik e-posta okuma
- 🤖 Google Gemini 2.0 Flash ile akıllı yanıt üretimi
- 🔒 OAuth 2.0 güvenli kimlik doğrulama
- 📊 E-posta duygu analizi
- 🎨 Renkli terminal arayüzü
- ⚙️ Kullanıcı onayı ile yanıt gönderimi

## 🚀 Kurulum

### 1. Repository'yi klonlayın
```bash
git clone https://github.com/BemreSTR/email-ai-responder.git
cd email-ai-responder
```

### 2. Virtual environment oluşturun
```bash
python3 -m venv venv
source venv/bin/activate  # MacOS/Linux
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. Google Cloud Console Ayarları

#### Gmail API Etkinleştirme:
1. [Google Cloud Console](https://console.cloud.google.com/) açın
2. Yeni proje oluşturun veya mevcut projeyi seçin
3. **APIs & Services > Library** bölümüne gidin
4. "Gmail API" arayın ve etkinleştirin

#### OAuth 2.0 Credentials:
1. **APIs & Services > Credentials** bölümüne gidin
2. **+ CREATE CREDENTIALS > OAuth 2.0 Client IDs** seçin
3. Application type: **Desktop application**
4. Name: **Email AI Responder**
5. **CREATE** butonuna tıklayın
6. JSON dosyasını indirin

### 5. Credentials dosyasını yerleştirin
```bash
mkdir -p credentials
# İndirdiğiniz JSON dosyasını credentials/credentials.json olarak kaydedin
```

### 6. Environment değişkenlerini ayarlayın
`.env` dosyası zaten oluşturuldu, gerekirse düzenleyin:
```bash
nano .env
```

## 📖 Kullanım

### Sistemi başlatın:
```bash
python main.py
```

### İlk çalıştırma:
- Tarayıcıda Google OAuth onay sayfası açılacak
- Gmail hesabınızla giriş yapın
- İzinleri onaylayın
- Sistem otomatik olarak çalışmaya başlayacak

### Sistem özellikleri:
- ✅ Okunmamış e-postaları otomatik tarar
- 🤖 Her e-posta için AI yanıtı üretir
- 👀 Yanıtı önizleme imkanı
- ✏️ Yanıtı düzenleme seçeneği
- 📤 Onayınızla yanıt gönderimi

## 🎮 Komutlar

Sistem çalışırken:
- `y` - Yanıtı gönder
- `n` - Yanıtı gönderme, e-postayı okundu olarak işaretle
- `e` - Yanıtı düzenle
- `s` - E-postayı atla
- `Ctrl+C` - Sistemi durdur

## ⚙️ Yapılandırma

`.env` dosyasındaki ayarlar:

```env
GMAIL_ADDRESS=example@gmail.com
GEMINI_API_KEY=your_gemini__api_key
CHECK_INTERVAL=60           # Kontrol aralığı (saniye)
MAX_EMAILS_PER_CHECK=10     # Maksimum e-posta sayısı
LOG_LEVEL=INFO              # Log seviyesi
```

## 📁 Proje Yapısı

```
email-ai-responder/
├── main.py              # Ana uygulama
├── gmail_client.py      # Gmail API istemcisi
├── ai_responder.py      # AI yanıt üreticisi
├── config.py           # Konfigürasyon yönetimi
├── requirements.txt    # Python bağımlılıkları
├── .env               # Çevre değişkenleri
├── .env.example       # Örnek çevre değişkenleri
├── .gitignore         # Git ignore dosyası
├── credentials/       # Google OAuth credentials
├── token.json         # OAuth token (otomatik oluşturulur)
└── email_ai.log       # Log dosyası
```

## 🔧 Sorun Giderme

### Credential hatası:
```bash
# credentials.json dosyasının doğru yerde olduğundan emin olun
ls credentials/credentials.json
```

### API hatası:
```bash
# Gmail API'nin etkin olduğundan emin olun
# Google Cloud Console'da kontrol edin
```

### Python import hatası:
```bash
# Virtual environment'ın aktif olduğundan emin olun
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 Log Dosyası

Sistem aktivitelerini takip etmek için:
```bash
tail -f email_ai.log
```

## 🛡️ Güvenlik

- ✅ OAuth 2.0 güvenli kimlik doğrulama
- ✅ Hassas bilgiler .gitignore ile korunuyor
- ✅ API anahtarları environment değişkenlerinde
- ✅ Otomatik e-posta filtreleme

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. Log dosyasını kontrol edin: `email_ai.log`
2. GitHub Issues bölümünde yeni issue açın
3. Hatanın detaylarını paylaşın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

**⚡ Yapay Zeka ile E-posta Yönetimini Kolaylaştırın!**
