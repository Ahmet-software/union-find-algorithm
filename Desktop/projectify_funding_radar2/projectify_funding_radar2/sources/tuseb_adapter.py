"""TusebAdapter — ikinci sürümde özel adaptör (doküman bölüm 34).
MVP'de iskelet olarak yer alır; GenericAdapter mantığıyla genişletilebilir."""
from __future__ import annotations

from typing import List

from sources.base_adapter import BaseSourceAdapter
from models import FundingCall


class TusebAdapter(BaseSourceAdapter):
    source_name = "TÜSEB"
    base_url = ""

    def fetch_calls(self) -> List[FundingCall]:
        # TODO (v2): TÜSEB resmi sayfası/portalı için özel parser.
        return []
