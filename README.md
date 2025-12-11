# AI Interview Simulator 🎯

Yapay Zeka destekli mülakat simülasyon sistemi. Kullanıcılar CV'lerini yükleyerek gerçekçi iş görüşmesi deneyimi yaşayabilirler.

## 🌟 Özellikler

- ✅ Kullanıcı kayıt ve giriş sistemi
- 📄 CV yükleme ve analiz (PDF)
- 🤖 AI destekli soru oluşturma
- ⚙️ Soru sayısı ve zorluk seviyesi seçimi
- 💯 Otomatik değerlendirme ve puanlama
- 📊 Mülakat geçmişi görüntüleme

## 🛠️ Teknolojiler

- **Python 3.8+**
- **Streamlit** - Web arayüzü
- **OpenAI API** - GPT-3.5-turbo
- **SQLite** - Veritabanı
- **PyPDF2** - PDF işleme

## 📦 Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/benmevic/ai-interview-simulator.git
cd ai-interview-simulator
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. Environment variables ayarlayın:
```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin ve OpenAI API key'inizi ekleyin:
```
OPENAI_API_KEY=your_openai_api_key_here
```

5. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

## 🚀 Kullanım

1. **Kayıt Ol**: İlk kez kullanıyorsanız bir hesap oluşturun
2. **Giriş Yap**: Mevcut hesabınızla giriş yapın
3. **CV Yükle**: PDF formatında CV'nizi yükleyin
4. **Ayarlar**: Soru sayısı (3/5/7) ve zorluk (Kolay/Orta/Zor) seçin
5. **Mülakat**: Soruları cevaplayın
6. **Sonuç**: Puanınızı ve değerlendirmenizi görün
7. **Geçmiş**: Önceki mülakatlarınızı inceleyin

## 📝 Proje Yapısı

```
ai-interview-simulator/
├── app.py                 # Ana uygulama
├── config.py             # Konfigürasyon
├── requirements.txt      # Bağımlılıklar
├── database/
│   ├── db_manager.py    # Veritabanı yönetimi
│   └── schema.sql       # Veritabanı şeması
├── services/
│   ├── auth_service.py  # Kimlik doğrulama
│   ├── cv_analyzer.py   # CV analizi
│   └── openai_service.py # AI entegrasyonu
└── uploads/             # Yüklenen dosyalar
```

## 🔐 Güvenlik

- Şifreler bcrypt ile hashlenir
- Dosya yüklemeleri doğrulanır
- SQL injection koruması
- API key'ler environment variables'da saklanır

## 📊 Veritabanı Şeması

- **users**: Kullanıcı bilgileri
- **interviews**: Mülakat kayıtları
- **questions**: Soru ve cevaplar
- **evaluations**: Değerlendirmeler

## 👨‍💻 Geliştirici

**Benmevic**
- Zonguldak Bülent Ecevit Üniversitesi
- Bilgisayar Mühendisliği 4. Sınıf

## ⚠️ Notlar

- OpenAI API kullanımı için hesap ve API key gereklidir
- API kullanımı ücretlidir (ücretsiz kredi ile başlayabilirsiniz)
- İlk çalıştırmada veritabanı otomatik oluşturulur

## 📧 İletişim

Sorularınız için issue açabilir veya pull request gönderebilirsiniz.
