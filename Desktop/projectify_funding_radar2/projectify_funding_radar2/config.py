"""
config.py
Projectify Funding Radar — merkezi yapılandırma.
Tüm yollar, sabitler ve skorlama ağırlıkları burada tutulur.
"""
from __future__ import annotations

import os
from pathlib import Path

# --------------------------------------------------------------------------
# Yol yapılandırması
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"

COMPANY_DOCS_DIR = UPLOAD_DIR / "company_docs"
ACADEMIC_DOCS_DIR = UPLOAD_DIR / "academic_docs"
ENTREPRENEUR_DOCS_DIR = UPLOAD_DIR / "entrepreneur_docs"
PROJECT_SUMMARIES_DIR = UPLOAD_DIR / "project_summaries"
FUNDING_GUIDES_DIR = UPLOAD_DIR / "funding_guides"

for _d in (
    DATA_DIR,
    UPLOAD_DIR,
    COMPANY_DOCS_DIR,
    ACADEMIC_DOCS_DIR,
    ENTREPRENEUR_DOCS_DIR,
    PROJECT_SUMMARIES_DIR,
    FUNDING_GUIDES_DIR,
):
    _d.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "funding_radar.db"
DATABASE_URL = os.getenv("FUNDING_RADAR_DB_URL", f"sqlite:///{DB_PATH}")

# --------------------------------------------------------------------------
# Genel sabitler
# --------------------------------------------------------------------------
APP_NAME = "Projectify Funding Radar"
APP_VERSION = "0.1.0 (MVP)"
LOGO_PATH = BASE_DIR / "ui" / "assets" / "logo.png"
PROJECT_SUMMARY_MAX_LEN = 500
HTTP_TIMEOUT = 20
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 ProjectifyFundingRadar/0.1"
)

USER_TYPES = ["company", "academic", "entrepreneur"]
USER_TYPE_LABELS = {
    "company": "Şirket",
    "academic": "Akademisyen",
    "entrepreneur": "Girişimci",
}

# --------------------------------------------------------------------------
# Skor sınıflandırma eşikleri (doküman bölüm 14)
# --------------------------------------------------------------------------
SCORE_THRESHOLDS = [
    (85, "Çok Uygun"),
    (70, "Uygun"),
    (55, "Revizyonla Uygun"),
    (40, "Düşük Uygunluk"),
    (0, "Uygun Değil"),
]

# --------------------------------------------------------------------------
# Skorlama ağırlıkları (doküman bölüm 15-16-17). Toplam = 100.
# --------------------------------------------------------------------------
COMPANY_WEIGHTS = {
    "applicant_eligibility": 15,
    "sector_match": 15,
    "technology_match": 15,
    "trl_match": 10,
    "financial_fit": 10,
    "tax_sgk_risk": 10,
    "rationale_match": 10,
    "commercialization": 10,
    "consortium_country": 5,
}

ACADEMIC_WEIGHTS = {
    "applicant_eligibility": 15,
    "academic_field_match": 15,
    "topic_match": 15,
    "scientific_method": 10,
    "technology_trl": 10,
    "track_record": 10,
    "institution_fit": 10,
    "commercialization": 10,
    "consortium_country": 5,
}

ENTREPRENEUR_WEIGHTS = {
    "applicant_eligibility": 15,
    "program_type_match": 15,
    "sector_match": 10,
    "technology_match": 15,
    "stage_match": 10,
    "prototype_mvp": 10,
    "commercialization_validation": 10,
    "patent_brand": 10,
    "team_fit": 5,
}

# Girişimci için yüksek uyumlu sayılan program anahtar kelimeleri (doküman 17)
ENTREPRENEUR_FRIENDLY_KEYWORDS = [
    "bigg",
    "1812",
    "girişimcilik",
    "entrepreneur",
    "startup",
    "start-up",
    "eit",
    "eic accelerator",
    "cascade",
    "kuluçka",
    "incubator",
    "hızlandırıcı",
    "accelerator",
    "üniversite girişimcilik",
]


# --------------------------------------------------------------------------
# Alt skor (subscore) Türkçe etiketleri — dashboard grafiği için
# --------------------------------------------------------------------------
SUBSCORE_LABELS = {
    "applicant_eligibility": "Başvuru Sahibi Uygunluğu",
    "sector_match": "Sektör Uyumu",
    "technology_match": "Teknoloji Uyumu",
    "trl_match": "TRL Uyumu",
    "financial_fit": "Finansal Uygunluk",
    "tax_sgk_risk": "Vergi / SGK Risk",
    "rationale_match": "Proje Gerekçesi Uyumu",
    "commercialization": "Ticarileşme / Patent",
    "consortium_country": "Konsorsiyum / Ülke",
    "academic_field_match": "Akademik Alan Uyumu",
    "topic_match": "Proje Konusu Uyumu",
    "scientific_method": "Bilimsel Yöntem",
    "technology_trl": "Teknoloji / TRL",
    "track_record": "Yayın / Patent / Proje Geçmişi",
    "institution_fit": "Kurum Uygunluğu",
    "program_type_match": "Program Tipi Uyumu",
    "stage_match": "Proje Aşaması Uyumu",
    "prototype_mvp": "Prototip / MVP",
    "commercialization_validation": "Ticarileşme / Müşteri Doğrulama",
    "patent_brand": "Patent / Marka",
    "team_fit": "Takım Uygunluğu",
}


def weights_for(user_type: str) -> dict:
    """Kullanıcı tipine göre alt skor maksimum ağırlıklarını döndürür."""
    return {
        "company": COMPANY_WEIGHTS,
        "academic": ACADEMIC_WEIGHTS,
        "entrepreneur": ENTREPRENEUR_WEIGHTS,
    }.get(user_type, {})


# --------------------------------------------------------------------------
# Geçmiş tarihli çağrılar gizlensin mi? (son başvuru < bugün)
# Tarihi belirsiz (None) olanlar her zaman tutulur.
# --------------------------------------------------------------------------
from datetime import date as _date

EXCLUDE_PAST_DEADLINES = True


def is_active_call(deadline) -> bool:
    """deadline None ise (bilinmiyor) aktif sayılır; geçmişse pasif."""
    if not EXCLUDE_PAST_DEADLINES:
        return True
    if deadline is None:
        return True
    try:
        if isinstance(deadline, str):
            deadline = _date.fromisoformat(deadline)
        return deadline >= _date.today()
    except (ValueError, TypeError):
        return True  # ayrıştırılamıyorsa elemeyelim


# --------------------------------------------------------------------------
# Kaynak renkleri — uygunluk sonuçlarında kaynakları ayırt etmek için
# --------------------------------------------------------------------------
# Anahtarlar ASCII; gelen ad da ASCII'ye normalize edilir (Türkçe küçük harf tuzağı için).
SOURCE_COLOR_RULES = [
    ("tubitak", "#1565C0"),
    ("kosgeb", "#2E7D32"),
    ("tuseb", "#6A1B9A"),
    ("kalkinma", "#EF6C00"), ("ajans", "#EF6C00"),
    ("cascade", "#00838F"), ("horizon", "#00838F"), ("avrupa", "#00838F"), ("eu", "#00838F"),
    ("eklenen web", "#5D4037"), ("link", "#5D4037"),
    ("yuklenen", "#AD1457"), ("pdf", "#AD1457"),
    ("manuel", "#455A64"),
]
SOURCE_COLOR_DEFAULT = "#607D8B"

_TR_ASCII = str.maketrans({
    "ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g",
    "ü": "u", "Ü": "u", "ö": "o", "Ö": "o", "ç": "c", "Ç": "c",
    "\u0307": "",  # birleşik nokta
})


def _ascii_lower(text: str) -> str:
    return (text or "").translate(_TR_ASCII).lower()


def source_color(name: str) -> str:
    n = _ascii_lower(name)
    for key, color in SOURCE_COLOR_RULES:
        if key in n:
            return color
    return SOURCE_COLOR_DEFAULT


# --------------------------------------------------------------------------
# Rapor künyesi (Pi Sağlık Teknolojileri)
# --------------------------------------------------------------------------
DEVELOPER_LINE = "Bu uygulama Pi Sağlık Teknolojileri tarafından geliştirilmiştir."
DEVELOPER_WEBSITE = "pixr.store"


# --------------------------------------------------------------------------
# Profil alan etiketleri (rapor için) — üç model birleşik
# --------------------------------------------------------------------------
PROFILE_FIELD_LABELS = {
    # Şirket
    "company_name": "Şirket Unvanı", "establishment_year": "Kuruluş Yılı",
    "activity_area": "Faaliyet Alanı", "nace_code": "NACE Kodu",
    "employee_count": "Personel Sayısı", "sme_status": "KOBİ Ölçeği",
    "balance_sheet_summary": "Bilanço Özeti", "net_sales": "Net Satış (₺)",
    "total_assets": "Aktif Toplamı (₺)", "tax_debt_status": "Vergi Borcu",
    "sgk_debt_status": "SGK Borcu", "r_and_d_history": "Ar-Ge Geçmişi",
    "patent_brand_info": "Patent / Marka", "export_info": "İhracat",
    "investment_incentive_history": "Yatırım / Teşvik Geçmişi",
    # Akademisyen
    "full_name": "Ad Soyad", "university": "Üniversite", "faculty": "Fakülte",
    "department": "Bölüm", "division": "Ana Bilim Dalı", "academic_title": "Unvan",
    "expertise_fields": "Uzmanlık Alanları", "previous_projects": "Önceki Projeler",
    "publications": "Yayınlar", "patents": "Patentler",
    "laboratory_infrastructure": "Laboratuvar / Altyapı", "tto_info": "TTO Bilgisi",
    "ethics_committee_access": "Etik Kurul Erişimi",
    "industry_collaboration_history": "Sanayi İş Birliği",
    # Girişimci
    "education_level": "Eğitim Durumu", "graduation_status": "Mezuniyet Durumu",
    "startup_idea_name": "Girişim Fikri", "trainings_certificates": "Eğitim / Sertifika",
    "team_members": "Takım Üyeleri", "has_technical_team": "Teknik Ekip",
    "has_business_team": "İş Geliştirme Ekibi", "project_stage": "Proje Aşaması",
    "company_establishment_plan": "Şirketleşme Planı",
    "patent_or_brand_status": "Patent / Marka Durumu", "prototype_status": "Prototip",
    "customer_validation_status": "Müşteri Doğrulama", "sales_or_loi_status": "Satış / LOI",
    "uploaded_documents": "Yüklenen Belgeler",
}
