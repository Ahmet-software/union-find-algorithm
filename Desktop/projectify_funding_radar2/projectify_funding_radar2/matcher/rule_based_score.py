"""
rule_based_score.py
Matcher'ların paylaştığı kural-tabanlı yardımcı fonksiyonlar.
"""
from __future__ import annotations

from typing import List, Optional

from config import SCORE_THRESHOLDS
from extractors.text_cleaner import normalize_for_match
from models import FundingCall, ProjectSummary
import re
NEGATION_PATTERN=re.compile(
    """Olumsuz sozcuklerle olusabilecek karmasiktan eklenmistir."""
    r"\b(" 
    r"degil\w*|deil\w*|" 
    r"yok|w*|"
    r"\w+mama\w*|\w+meme\w*|"
    r"\w+madi\w*|\w+medi\w*|"
    r"\w+muyo\w*|"
    r"\w+mami\w*|\w+memi\w*|"
    r"sahip\s+degil\w*"
    r")\b"
)
def _safe_str(value:Optional[str])->str:
    """bos gecebilecek veya none atabilecek string verilerini normalize edilmis bir string ifadeye cevirir."""
    if not value:
        return ""
    return normalize_for_match(str(value))


def classify_score(score: int) -> str:
    """Doküman bölüm 14 — skoru uygunluk seviyesine çevirir."""
    for threshold, label in SCORE_THRESHOLDS:
        if score >= threshold:
            return label
    return "Uygun Değil"


def score_treshold_check(score:int,threshold:int)->int:
    """skorun esik deger cikma ihtimalinde yardimci olabilecek fonksiyon"""
    return threshold if score>=threshold else 999


def keyword_overlap_ratio(text_a: str, keywords: List[str]) -> float:
    """text_a içinde keywords'ten kaçının geçtiğinin oranı (0..1)."""
    if not keywords:
        return 0.0
    norm = normalize_for_match(text_a or "")
    hits = sum(1 for kw in keywords if normalize_for_match(kw) in norm)
    return hits / len(keywords)


def any_keyword_in(text: str, keywords: List[str]) -> bool:
    norm = normalize_for_match(text or "")
    return any(normalize_for_match(kw) in norm for kw in keywords)


def applicant_eligibility(user_type: str, call: FundingCall) -> float:
    """
    Başvuru sahibi uygunluğu (0..1).
    Çağrıda uygun başvuru tipi belirtilmemişse nötr (0.6) kabul edilir.
    """
    if not call.eligible_applicants:
        return 0.6  # bilgi yok → orta
    return 1.0 if user_type in call.eligible_applicants else 0.0


def sector_match(project_text: str, profile_sectors_text: str, call: FundingCall) -> float:
    if not call.sectors:
        return 0.6
    combined = f"{project_text} {profile_sectors_text}"
    ratio = keyword_overlap_ratio(combined, call.sectors)
    return min(1.0, 0.4 + ratio) if ratio > 0 else 0.2


def technology_match(project_text: str, call: FundingCall) -> float:
    if not call.technology_areas:
        return 0.6
    ratio = keyword_overlap_ratio(project_text, call.technology_areas)
    return min(1.0, 0.4 + ratio) if ratio > 0 else 0.2


def trl_match(project_text: str, profile_stage_trl: Optional[int], call: FundingCall) -> float:
    """
    Proje TRL'i çağrı aralığına giriyor mu?
    profile_stage_trl bilinmiyorsa metinden tahmin denenir; yoksa nötr.
    """
    if call.trl_min is None and call.trl_max is None:
        return 0.6
    trl = profile_stage_trl
    if trl is None:
        trl = _guess_trl_from_text(project_text)
    if trl is None:
        return 0.5  # çağrı TRL istiyor ama bizde yok → doğrulanmalı
    lo = call.trl_min or 1
    hi = call.trl_max or 9
    if lo <= trl <= hi:
        return 1.0
    # aralığa yakınlık
    distance = min(abs(trl - lo), abs(trl - hi))
    return max(0.0, 1.0 - 0.25 * distance)

def _is_negated(text:str,match_index=int, window:int=30)->bool:
    """Anahtar kelimelerden once veya sonra negatif kelime gecip gecmemesini kontrol eder"""
    snippet=text[match_index:match_index+window]
    return bool(NEGATION_PATTERN.search(snippet))


def _guess_trl_from_text(text: str) -> Optional[int]:
    
    """
    metin icerisinden TRL analizi yaparak puanlama sistemi yapar(anahtar kelimeler),ayni zamanda olumsuz ifadelerin kontrolu saglanir.
    """
    norm=_safe_str(text)
    if not norm:
        return None

    trl_rules=[
        (7,["pilot","ticari","satis","musteri dogrula","seri uretim"]),
        (6,["mvp"]),
        (5,["prototip","prototype"]),
        (4,["on dogrulama","validation"]),
        (2,["fikir","idea","concept"]),
    ]
    
    for trl_level,keywords in trl_rules:
        for kw in keywords:
            """Tüm anaht.kelimelerin yerini bulur"""
            for match in re.finditer(r"\b" +re.escape(kw)+r"\b",norm):
                pos = match.start()
                """ Eğer kullanımlardan !!!EN az biri olumsuz değilse TRL'i ver. """
                if not _is_negated(norm,pos):
                    return trl_level
    return None

        
    
        
   


def rationale_match(project: ProjectSummary, call: FundingCall) -> float:
    """Proje gerekçesi / problem tanımının çağrı ile örtüşmesi."""
    text = f"{project.project_rationale} {project.project_purpose}"
    if not text.strip():
        return 0.3
    base = 0.6
    if call.technology_areas and keyword_overlap_ratio(text, call.technology_areas) > 0:
        base += 0.2
    if call.sectors and keyword_overlap_ratio(text, call.sectors) > 0:
        base += 0.2
    return min(1.0, base)


def commercialization_score(project: ProjectSummary) -> float:
    """Ticarileşme / patentlenebilirlik beyanının gücü."""
    text = normalize_for_match(project.commercialization_patent_status)
    if not text.strip():
        return 0.2
    strong = ["patent", "lisans", "license", "ticarilesme", "pazar", "market",
              "musteri", "gelir modeli", "is modeli", "spin-off", "spinoff"]
    hits = sum(1 for k in strong if k in text)
    return min(1.0, 0.4 + 0.15 * hits)


def consortium_country_fit(user_country_ok: bool, call: FundingCall) -> float:
    score = 1.0
    if call.consortium_required:
        score -= 0.5  # konsorsiyum gerekiyorsa risk; ortak yoksa düşer
    if call.eligible_countries and not user_country_ok:
        score -= 0.5
    return max(0.0, score)


def scale(subscore_ratio: float, weight: int) -> float:
    """0..1 oranını ağırlıkla puana çevirir."""
    return round(max(0.0, min(1.0, subscore_ratio)) * weight, 2)
