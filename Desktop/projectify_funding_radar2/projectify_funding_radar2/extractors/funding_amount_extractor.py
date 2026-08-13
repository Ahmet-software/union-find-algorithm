"""Metinden destek miktarı ve destek oranını çıkarır."""
from __future__ import annotations

import re
from typing import Optional, Tuple

_CURRENCY = r"(₺|TL|EUR|€|USD|\$|GBP|£)"
_NUM = r"\d[\d.,]*"


def extract_funding_amount(text: str) -> Optional[str]:
    if not text:
        return None
    lowered = text.lower()
    hints = ["destek miktar", "bütçe", "butce", "funding", "grant", "hibe tutar",
             "support amount", "azami", "üst limit", "up to", "maximum"]
    zones = []
    for h in hints:
        i = lowered.find(h)
        if i != -1:
            zones.append(text[i: i + 160])
    zones.append(text)
    for zone in zones:
        m = re.search(rf"({_CURRENCY}\s*{_NUM}|{_NUM}\s*{_CURRENCY})", zone)
        if m:
            return re.sub(r"\s+", " ", m.group(0)).strip()
    return None


def extract_funding_rate(text: str) -> Optional[str]:
    if not text:
        return None
    lowered = text.lower()
    hints = ["destek oran", "support rate", "funding rate", "co-financing", "eş finansman", "es finansman"]
    zones = []
    for h in hints:
        i = lowered.find(h)
        if i != -1:
            zones.append(text[i: i + 80])
    zones.append(text)
    for zone in zones:
        m = re.search(r"%\s*\d{1,3}|\d{1,3}\s*%", zone)
        if m:
            return m.group(0).replace(" ", "")
    return None


def extract_trl(text: str) -> Tuple[Optional[int], Optional[int]]:
    """TRL aralığını bulur (örn 'TRL 4-7')."""
    if not text:
        return None, None
    m = re.search(r"trl\s*:?[\s]*([1-9])\s*[-–to]+\s*([1-9])", text, re.IGNORECASE)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"trl\s*:?[\s]*([1-9])", text, re.IGNORECASE)
    if m:
        return int(m.group(1)), int(m.group(1))
    return None, None


def extract_duration(text: str) -> Optional[str]:
    if not text:
        return None
    m = re.search(r"(\d{1,2})\s*(ay|month|months|yıl|yil|year|years)", text, re.IGNORECASE)
    if m:
        return f"{m.group(1)} {m.group(2)}"
    return None
