"""Metinden uygunluk bilgilerini (başvuru sahibi türü, ülke, sektör, teknoloji) çıkarır."""
from __future__ import annotations

import re
from typing import List

from extractors.text_cleaner import normalize_for_match

_APPLICANT_KEYWORDS = {
    "company": ["şirket", "sirket", "kobi", "sme", "firma", "tüzel", "tuzel", "company", "enterprise"],
    "academic": ["üniversite", "universite", "akademi", "araştırmacı", "arastirmaci",
                 "academic", "researcher", "university", "research organisation",
                 "research organization"],
    "entrepreneur": ["girişimci", "girisimci", "startup", "start-up", "entrepreneur",
                     "girişim", "girisim", "natural person", "gerçek kişi", "gercek kisi"],
}

_SECTOR_KEYWORDS = [
    "sağlık", "saglik", "health", "enerji", "energy", "tarım", "tarim", "agriculture",
    "yazılım", "yazilim", "software", "bilişim", "bilisim", "ict", "imalat",
    "manufacturing", "savunma", "defence", "defense", "biyoteknoloji", "biotech",
    "fintech", "finans", "finance", "otomotiv", "automotive", "uzay", "space",
    "iklim", "climate", "çevre", "cevre", "environment", "gıda", "gida", "food",
    "lojistik", "logistics", "turizm", "tourism", "eğitim", "egitim", "education",
]

_TECH_KEYWORDS = [
    "yapay zeka", "artificial intelligence", "ai", "machine learning", "makine öğrenmesi",
    "makine ogrenmesi", "blockchain", "iot", "nesnelerin interneti", "robotik", "robotics",
    "siber güvenlik", "siber guvenlik", "cybersecurity", "kuantum", "quantum",
    "nanoteknoloji", "nanotechnology", "5g", "6g", "yenilenebilir", "renewable",
    "hidrojen", "hydrogen", "veri analitiği", "data analytics", "bulut", "cloud",
    "biyomedikal", "biomedical", "genom", "genomics", "ilaç", "ilac", "pharma",
]

_COUNTRY_KEYWORDS = [
    "türkiye", "turkiye", "turkey", "avrupa birliği", "avrupa birligi", "european union",
    "eu", "horizon europe", "ab üyesi", "ab uyesi", "associated countries",
]


def _find_keywords(text: str, keywords: List[str]) -> List[str]:
    norm = normalize_for_match(text)
    found = []
    for kw in keywords:
        if normalize_for_match(kw) in norm:
            found.append(kw)
    # tekrarları sırayı koruyarak temizle
    seen, out = set(), []
    for f in found:
        if f.lower() not in seen:
            seen.add(f.lower())
            out.append(f)
    return out


def extract_eligible_applicants(text: str) -> List[str]:
    norm = normalize_for_match(text)
    result = []
    for utype, kws in _APPLICANT_KEYWORDS.items():
        if any(normalize_for_match(k) in norm for k in kws):
            result.append(utype)
    return result


def extract_sectors(text: str) -> List[str]:
    return _find_keywords(text, _SECTOR_KEYWORDS)


def extract_technologies(text: str) -> List[str]:
    return _find_keywords(text, _TECH_KEYWORDS)


def extract_countries(text: str) -> List[str]:
    return _find_keywords(text, _COUNTRY_KEYWORDS)


def detect_consortium(text: str):
    norm = normalize_for_match(text)
    pos = ["konsorsiyum", "consortium", "ortak gerekli", "partner required",
           "en az 3 ortak", "minimum 3 partners", "ortaklık zorunlu"]
    neg = ["konsorsiyum gerekmez", "no consortium", "tek başvuru", "single applicant"]
    if any(normalize_for_match(n) in norm for n in neg):
        return False
    if any(normalize_for_match(p) in norm for p in pos):
        return True
    return None
