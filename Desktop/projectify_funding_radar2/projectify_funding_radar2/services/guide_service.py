"""
guide_service.py
Kullanıcının yüklediği PDF rehber / site linki / manuel program girişini
analiz eder, FundingCall'a çevirir, profil ile eşleştirip sonucu saklar.
(Doküman bölüm 20 & 27.)
"""
from __future__ import annotations

import os
import tempfile
from typing import List, Optional, Tuple

import requests

from config import FUNDING_GUIDES_DIR, HTTP_TIMEOUT, USER_AGENT
from extractors import (
    discover_pdf_links,
    extract_funding_call_from_text,
    extract_text_from_pdf,
    extract_text_from_url,
)
from models import FundingCall, MatchResult
from services.matching_service import match_single_call
from services.scan_service import store_calls


def analyze_uploaded_guide(file_path: str, source_name: str = "Yüklenen PDF Rehber") -> FundingCall:
    text = extract_text_from_pdf(file_path)
    call = extract_funding_call_from_text(
        text, source_name=source_name, source_url=f"file://{os.path.basename(file_path)}"
    )
    return call


def _download_pdf(url: str) -> Optional[str]:
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        fd, path = tempfile.mkstemp(suffix=".pdf", dir=str(FUNDING_GUIDES_DIR))
        with os.fdopen(fd, "wb") as f:
            f.write(resp.content)
        return path
    except Exception:  # noqa: BLE001
        return None


def analyze_guide_url(url: str, dynamic: bool = False) -> FundingCall:
    """
    Site linkini analiz eder; sayfadaki PDF rehberleri de bulup okur.
    PDF metni + sayfa metni birleştirilerek tek bir çağrı üretilir.
    """
    page_text = extract_text_from_url(url, dynamic=dynamic)
    combined = page_text or ""

    for pdf_url in discover_pdf_links(url)[:3]:
        path = _download_pdf(pdf_url)
        if path:
            combined += "\n" + extract_text_from_pdf(path)

    return extract_funding_call_from_text(
        combined, source_name="Eklenen Web Linki", source_url=url
    )


def analyze_and_match(call: FundingCall) -> Tuple[FundingCall, Optional[MatchResult]]:
    """Üretilen çağrıyı kaydeder ve aktif profil ile eşleştirir."""
    store_calls([call])
    result = match_single_call(call)
    return call, result
