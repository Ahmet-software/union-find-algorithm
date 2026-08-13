"""Metin temizleme yardımcıları."""
from __future__ import annotations

import re


def clean_text(text: str) -> str:
    """Fazla boşlukları ve kontrol karakterlerini temizler."""
    if not text:
        return ""
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_for_match(text: str) -> str:
    """Eşleştirme için küçük harfe çevirip Türkçe karakterleri sadeleştirir."""
    if not text:
        return ""
    text = text.lower()
    replace = {
        "ı": "i", "İ": "i", "ş": "s", "ğ": "g",
        "ü": "u", "ö": "o", "ç": "c",
    }
    for a, b in replace.items():
        text = text.replace(a, b)
    return text


def first_nonempty_line(text: str) -> str:
    for line in (text or "").splitlines():
        line = line.strip()
        if line:
            return line
    return ""
