"""
source_registry.py
Hazır kaynakların kaydı ve tarama orkestrasyonu.
"""
from __future__ import annotations

from typing import Dict, List

from sources.cascade_adapter import CascadeFundingAdapter
from sources.eu_adapter import EUFundingAdapter
from sources.kalkinma_adapter import KalkinmaAjansiAdapter
from sources.kosgeb_adapter import KosgebAdapter
from sources.tubitak_adapter import TubitakAdapter
from sources.tuseb_adapter import TusebAdapter
from models import FundingCall

# Hazır kaynaklar: MVP'de yalnızca Cascade aktif; diğerleri v2 stub.
READY_SOURCES = {
    "cascade": "Cascade Funding",
    "tubitak": "TÜBİTAK",
    "kosgeb": "KOSGEB",
    "tuseb": "TÜSEB",
    "kalkinma": "Kalkınma Ajansları",
    "eu": "AB Programları",
}


def build_adapter(key: str, use_live: bool = True):
    if key == "cascade":
        return CascadeFundingAdapter(use_live=use_live)
    if key == "tubitak":
        return TubitakAdapter()
    if key == "kosgeb":
        return KosgebAdapter()
    if key == "tuseb":
        return TusebAdapter()
    if key == "kalkinma":
        return KalkinmaAjansiAdapter()
    if key == "eu":
        return EUFundingAdapter()
    raise ValueError(f"Bilinmeyen kaynak: {key}")


def scan_sources(keys: List[str], use_live: bool = True) -> Dict[str, List[FundingCall]]:
    """Verilen kaynakları tarar; {kaynak_key: [FundingCall, ...]} döndürür."""
    results: Dict[str, List[FundingCall]] = {}
    for key in keys:
        try:
            adapter = build_adapter(key, use_live=use_live)
            results[key] = adapter.fetch_calls()
        except Exception:  # noqa: BLE001
            results[key] = []
    return results
