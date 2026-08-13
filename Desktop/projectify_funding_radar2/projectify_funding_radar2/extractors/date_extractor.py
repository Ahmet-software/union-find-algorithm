"""Metinden son başvuru tarihini çıkarır (TR + EN biçimleri)."""
from __future__ import annotations

import re
from datetime import date, datetime
from typing import Optional

_MONTHS_TR = {
    "ocak": 1, "şubat": 2, "subat": 2, "mart": 3, "nisan": 4, "mayıs": 5,
    "mayis": 5, "haziran": 6, "temmuz": 7, "ağustos": 8, "agustos": 8,
    "eylül": 9, "eylul": 9, "ekim": 10, "kasım": 11, "kasim": 11, "aralık": 12,
    "aralik": 12,
}
_MONTHS_EN = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12, "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7,
    "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}

_DEADLINE_HINTS = [
    "son başvuru", "son basvuru", "deadline", "kapanış", "kapanis",
    "başvuru bitiş", "basvuru bitis", "closing date", "submission deadline",
    "son tarih",
]


def _try_numeric(s: str) -> Optional[date]:
    for fmt in ("%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def extract_deadline(text: str) -> Optional[date]:
    """Metinden en olası son başvuru tarihini döndürür."""
    if not text:
        return None
    lowered = text.lower()

    # Önce 'deadline' ipucu içeren satırlara öncelik ver
    candidate_zones = []
    for hint in _DEADLINE_HINTS:
        idx = lowered.find(hint)
        if idx != -1:
            candidate_zones.append(text[idx: idx + 120])
    candidate_zones.append(text)  # son çare: tüm metin

    for zone in candidate_zones:
        # 12.05.2025 / 12/05/2025 / 2025-05-12
        m = re.search(r"\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}-\d{2}-\d{2})\b", zone)
        if m:
            d = _try_numeric(m.group(1))
            if d:
                return d
        # 12 Mayıs 2025 / 12 May 2025
        m = re.search(r"\b(\d{1,2})\s+([A-Za-zçğıöşüÇĞİÖŞÜ]+)\s+(\d{4})\b", zone)
        if m:
            day, month_name, year = m.group(1), m.group(2).lower(), m.group(3)
            month = _MONTHS_TR.get(month_name) or _MONTHS_EN.get(month_name)
            if month:
                try:
                    return date(int(year), month, int(day))
                except ValueError:
                    pass
    return None
