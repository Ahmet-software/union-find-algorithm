"""Bir URL'den (statik veya dinamik) metin çıkarmaya çalışan üst seviye fonksiyon."""
from __future__ import annotations

from extractors.dynamic_page_extractor import extract_text_from_dynamic_page
from extractors.html_extractor import extract_text_from_html


def extract_text_from_url(url: str, dynamic: bool = False) -> str:
    """
    Önce statik istek dener; içerik çok kısaysa (JS ile yüklenen sayfa olabilir)
    veya dynamic=True ise Playwright ile yeniden dener.
    """
    text = ""
    if not dynamic:
        try:
            text = extract_text_from_html(url)
        except Exception:  # noqa: BLE001
            text = ""
    if dynamic or len(text) < 400:
        dyn = extract_text_from_dynamic_page(url)
        if len(dyn) > len(text):
            text = dyn
    return text
