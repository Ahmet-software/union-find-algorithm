"""Statik HTML sayfasından metin ve link çıkarma (requests + BeautifulSoup)."""
from __future__ import annotations

from typing import List, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import HTTP_TIMEOUT, USER_AGENT
from extractors.text_cleaner import clean_text


def fetch_html(url: str) -> str:
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "tr,en;q=0.8"}
    resp = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.text


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return clean_text(soup.get_text(separator="\n"))


def extract_text_from_html(url: str) -> str:
    return html_to_text(fetch_html(url))


def extract_links(html: str, base_url: str) -> List[Tuple[str, str]]:
    """(metin, mutlak_url) çiftlerini döndürür."""
    soup = BeautifulSoup(html, "lxml")
    out = []
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        out.append((a.get_text(strip=True), href))
    return out


def discover_pdf_links(url: str) -> List[str]:
    """Sayfadaki PDF rehber linklerini bulur."""
    try:
        html = fetch_html(url)
    except Exception:  # noqa: BLE001
        return []
    pdfs = []
    for _text, href in extract_links(html, url):
        if href.lower().split("?")[0].endswith(".pdf"):
            pdfs.append(href)
    return list(dict.fromkeys(pdfs))
