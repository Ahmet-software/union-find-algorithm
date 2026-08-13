"""TubitakAdapter — ikinci sürümde özel adaptör (doküman bölüm 34).
MVP'de iskelet olarak yer alır; GenericAdapter mantığıyla genişletilebilir."""
from __future__ import annotations

from typing import List

from sources.base_adapter import BaseSourceAdapter
from models import FundingCall


class TubitakAdapter(BaseSourceAdapter):
    source_name = "TÜBİTAK"
    base_url = ""

    def fetch_calls(self) -> List[FundingCall]:
        # TODO (v2): TÜBİTAK resmi sayfası/portalı için özel parser.
        return []
