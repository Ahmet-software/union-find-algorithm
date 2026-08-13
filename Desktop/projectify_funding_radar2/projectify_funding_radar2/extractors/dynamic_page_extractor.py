"""Dinamik (JavaScript) sayfalardan metin çıkarma (Playwright).

Playwright kurulu değilse veya tarayıcı indirilmemişse, html_extractor'a
(statik istek) güvenli biçimde geri düşer.
"""
from __future__ import annotations

from config import HTTP_TIMEOUT
from extractors.html_extractor import extract_text_from_html, html_to_text


def extract_text_from_dynamic_page(url: str) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        # Playwright yok → statik istek ile dene
        return extract_text_from_html(url)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=HTTP_TIMEOUT * 1000, wait_until="networkidle")
            html = page.content()
            browser.close()
            return html_to_text(html)
    except Exception:  # noqa: BLE001
        # Tarayıcı indirilmemiş / sayfa hatası → statik geri dönüş
        try:
            return extract_text_from_html(url)
        except Exception:  # noqa: BLE001
            return ""
