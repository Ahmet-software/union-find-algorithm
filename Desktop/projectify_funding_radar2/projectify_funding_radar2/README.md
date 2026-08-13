# 📡 Projectify Funding Radar (MVP)

Şirket, akademisyen ve girişimci kullanıcıların **profil + proje özeti** bilgilerini
alarak fon/hibe çağrılarını tarayan, her çağrıyı standart bir veri modeline
dönüştüren ve proje ile çağrı arasındaki uygunluğu **0–100 arası** skorlayan
Python tabanlı analiz platformu.

> Bu sürüm **MVP**'dir. Arayüz **Streamlit** ile çalışır: komutla başlatılır,
> tarayıcıda yerel olarak (`localhost`) açılır. Veriler yerel **SQLite**'ta tutulur.

---

## Kurulum ve Çalıştırma

### Windows
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install
streamlit run main.py
```

### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
streamlit run main.py
```

> `playwright install` yalnızca **dinamik (JavaScript)** sayfaları taramak için
> gereklidir. Kurulmazsa uygulama yine çalışır; dinamik sayfalarda otomatik olarak
> statik isteğe (requests + BeautifulSoup) geri düşer.

Uygulama açıldıktan sonra tarayıcıda `http://localhost:8501` adresine gidin.

---

## Kullanım Akışı

1. **Kullanıcı Profili** → tipinizi seçin (Şirket / Akademisyen / Girişimci) ve formu doldurun.
2. **Proje Özeti** → 7 alanı doldurun. Her alan **en fazla 500 karakter**; canlı sayaç ve
   sınır kontrolü vardır. Sınır aşılırsa form kaydedilmez ve hangi alanın aştığı gösterilir.
3. **Fon Kaynakları** → hazır kaynaklardan seçin (MVP'de **Cascade** canlı taranır) veya
   kendi **PDF rehberinizi / web linkinizi / manuel program bilginizi** ekleyin.
4. **Tarama ve Analiz** → taramayı başlatın, ardından *Eşleştir ve Skorla*'ya basın.
   Burada **Clear / Taramaları Sil** butonu da bulunur.
5. **Uygunluk Sonuçları** → skor tablosu + her çağrı için detaylı analiz
   (güçlü/zayıf yönler, riskler, eksik belgeler, doğrulanacaklar, revizyon önerileri, aksiyon).
6. **Raporlar** → sonuçları **Excel (.xlsx)** veya **PDF/metin** olarak indirin.

---

## Canlı Scraping & Demo Yedeği

Cascade fonları tek bir kanonik sitede toplanmadığından, `CascadeFundingAdapter`
gerçek bir liste sayfasını taramayı **dener**; site yapısı değişir, içerik bulunamaz
veya ağ erişimi engellenirse otomatik olarak **demo veriye düşer**. Böylece uygulama
her koşulda çalışır.

Gerçek bir liste sayfası vermek için `.env` (veya ortam değişkeni) kullanın:
```
CASCADE_LIST_URL=https://gercek-cascade-liste-sayfasi.example/calls
```
`.env.example` dosyasını kopyalayıp düzenleyebilirsiniz.

---

## Proje Yapısı

```
projectify_funding_radar/
├── main.py              # Giriş noktası (streamlit run main.py)
├── config.py            # Yollar, sabitler, skor ağırlıkları
├── database.py          # SQLite + SQLAlchemy
├── models/              # Pydantic veri modelleri (bölüm 8-13)
├── sources/             # Kaynak adaptörleri (Cascade canlı + Generic + v2 stub'lar) + demo veri
├── extractors/          # PDF / HTML / dinamik sayfa okuma + tarih/bütçe/uygunluk çıkarımı
├── matcher/             # Şirket / Akademisyen / Girişimci skorlama + açıklayıcı
├── services/            # Profil, proje, tarama, eşleştirme, rehber, temizleme servisleri
├── reports/             # Excel / PDF / özet rapor
├── ui/                  # Streamlit sayfaları
├── uploads/             # Yüklenen belgeler
├── data/                # SQLite veritabanı
└── tests/               # Birim testleri
```

---

## Skorlama (Özet)

Toplam skor **100** puan üzerinden hesaplanır ve şu seviyelere ayrılır:

| Skor | Seviye |
|------|--------|
| 85–100 | Çok Uygun |
| 70–84  | Uygun |
| 55–69  | Revizyonla Uygun |
| 40–54  | Düşük Uygunluk |
| 0–39   | Uygun Değil |

Ağırlıklar kullanıcı tipine göre değişir (doküman bölüm 15–17) ve `config.py`
içinde `COMPANY_WEIGHTS`, `ACADEMIC_WEIGHTS`, `ENTREPRENEUR_WEIGHTS` olarak
ayarlanabilir.

---

## Testler
```bash
pytest tests/ -q
```

---

## İkinci Sürüm Yol Haritası (v2)

TÜBİTAK / KOSGEB / TÜSEB / Kalkınma Ajansı / AB özel adaptörleri, **LLM destekli**
rehber analizi, **semantik** eşleştirme (sentence-transformers), otomatik haftalık
tarama (APScheduler), e-posta/Telegram bildirimi, çoklu proje portföyü, başvuru
takvimi ve SaaS kullanıcı yönetimi. İlgili adaptör iskeletleri `sources/` altında
hazırdır.

---

## Notlar

- Bu yazılım bir **karar destek** aracıdır; ürettiği uygunluk skorları ve riskler
  bilgilendirme amaçlıdır, resmi başvuru kararı yerine geçmez. Program koşulları
  daima ilgili kurumun güncel resmi rehberinden teyit edilmelidir.
- `verification_status = "doğrulanmalı"` olan alanlar, otomatik çıkarımdan emin
  olunamadığını gösterir ve kullanıcı tarafından kontrol edilmelidir.


---

## Sürüm Notu (güncellemeler)

- Geçmiş son-başvuru tarihli çağrılar otomatik elenir (config: `EXCLUDE_PAST_DEADLINES`).
- Uygunluk sonuçlarında her kaynak farklı renkle gösterilir (TÜBİTAK, TÜSEB, KOSGEB, Cascade...).
- Alt skorlar yatay çubuk grafikle gösterilir.
- PDF/Excel raporlar başvuran bilgilerini, proje özetini, logoyu ve **Pi Sağlık Teknolojileri / pixr.store** künyesini içerir.
