"""
CascadeFundingAdapter — gerçek canlı scraping denemesi + güvenli demo yedeği.

Cascade fonları tek bir kanonik sitede toplanmadığından, bilinen bir cascade
çağrı listesi sayfasını taramayı dener. Sayfa yapısı değişebileceği veya ağ
erişimi engellenebileceği için her hata durumunda demo veriye düşer.

CASCADE_LIST_URL ortam değişkeni ile gerçek bir liste sayfası verilebilir.
"""
from __future__ import annotations

import os
from datetime import datetime
from typing import List

from sources.base_adapter import BaseSourceAdapter
from sources.demo_data import cascade_demo_calls
from models import FundingCall


class CascadeFundingAdapter(BaseSourceAdapter):
    source_name = "Cascade Funding"
    base_url = os.getenv("CASCADE_LIST_URL", "https://cascadefunding.eu/open-calls/")

    def __init__(self, use_live: bool = True, max_calls: int = 10):
        self.use_live = use_live
        self.max_calls = max_calls
        self.last_error: str | None = None

    # ---- canlı tarama denemesi --------------------------------------
    def get_call_links(self) -> List[str]:
        from extractors.html_extractor import extract_links, fetch_html

        html = fetch_html(self.base_url)
        links = extract_links(html, self.base_url)
        out = []
        for text, href in links:
            t = (text or "").lower()
            if any(k in t for k in ("call", "çağrı", "cagri", "open call", "cascade", "funding")):
                out.append(href)
        return list(dict.fromkeys(out))[: self.max_calls]

    def parse_call_detail(self, url: str) -> dict:
        from extractors.url_extractor import extract_text_from_url

        text = extract_text_from_url(url)
        return {"url": url, "text": text}

    def normalize(self, raw_data: dict) -> FundingCall:
        from extractors.guide_analyzer import extract_funding_call_from_text

        call = extract_funding_call_from_text(
            raw_data.get("text", ""),
            source_name=self.source_name,
            source_url=raw_data.get("url", self.base_url),
        )
        return call

    # ---- uçtan uca, demo yedekli ------------------------------------
    def fetch_calls(self) -> List[FundingCall]:
        if not self.use_live:
            return cascade_demo_calls()
        try:
            links = self.get_call_links()
            calls: List[FundingCall] = []
            for url in links:
                try:
                    raw = self.parse_call_detail(url)
                    if raw.get("text"):
                        calls.append(self.normalize(raw))
                except Exception:  # noqa: BLE001
                    continue
            if calls:
                return calls
            self.last_error = "Canlı tarama sonuç döndürmedi; demo veri kullanıldı."
            return cascade_demo_calls()
        except Exception as exc:  # noqa: BLE001
            self.last_error = f"Canlı tarama başarısız ({exc}); demo veri kullanıldı."
            return cascade_demo_calls()
