"""Tüm kaynak adaptörlerinin temel sınıfı — doküman bölüm 19."""
from __future__ import annotations

from typing import List

from models import FundingCall


class BaseSourceAdapter:
    source_name: str = "Base"
    base_url: str = ""

    def get_call_links(self) -> List[str]:
        """Çağrı detay sayfası linklerini döndürür."""
        raise NotImplementedError

    def parse_call_detail(self, url: str) -> dict:
        """Tek bir çağrının ham verisini döndürür."""
        raise NotImplementedError

    def normalize(self, raw_data: dict) -> FundingCall:
        """Ham veriyi standart FundingCall modeline dönüştürür."""
        raise NotImplementedError

    def fetch_calls(self) -> List[FundingCall]:
        """Adaptörün uçtan uca tarama akışı. Alt sınıf override edebilir."""
        calls: List[FundingCall] = []
        for url in self.get_call_links():
            try:
                raw = self.parse_call_detail(url)
                calls.append(self.normalize(raw))
            except Exception:  # noqa: BLE001
                continue
        return calls
