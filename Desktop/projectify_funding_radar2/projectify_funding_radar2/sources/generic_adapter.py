"""
GenericAdapter — bilinmeyen herhangi bir web sayfası veya PDF için genel scraper.
Kaynak türünü tespit eder, metni çıkarır ve FundingCall'a dönüştürür.
"""
from __future__ import annotations

from typing import List, Optional

from sources.base_adapter import BaseSourceAdapter
from models import FundingCall


class GenericAdapter(BaseSourceAdapter):
    source_name = "Genel Kaynak"

    def __init__(self, url: Optional[str] = None, dynamic: bool = False):
        self.url = url
        self.dynamic = dynamic
        self.base_url = url or ""

    def detect_source_type(self, url: str) -> str:
        u = (url or "").lower().split("?")[0]
        if u.endswith(".pdf"):
            return "pdf"
        if u.endswith(".xml") or "/rss" in u or "/feed" in u:
            return "rss"
        if "/api/" in u or u.endswith(".json"):
            return "api"
        return "html"

    def fetch_from_url(self, url: str) -> List[FundingCall]:
        from extractors.guide_analyzer import extract_funding_call_from_text
        from extractors.url_extractor import extract_text_from_url

        stype = self.detect_source_type(url)
        text = ""
        if stype == "pdf":
            # PDF linki indirilip okunmalı; burada metni url_extractor üzerinden
            # alamayız, indirme guide_service tarafında yapılır.
            text = ""
        elif stype == "rss":
            try:
                import feedparser
                feed = feedparser.parse(url)
                text = "\n".join(
                    f"{e.get('title','')}\n{e.get('summary','')}" for e in feed.entries[:20]
                )
            except Exception:  # noqa: BLE001
                text = ""
        else:
            text = extract_text_from_url(url, dynamic=self.dynamic)

        if not text:
            return []
        call = extract_funding_call_from_text(
            text, source_name=self.source_name, source_url=url
        )
        return [call]

    def fetch_calls(self) -> List[FundingCall]:
        if not self.url:
            return []
        return self.fetch_from_url(self.url)
