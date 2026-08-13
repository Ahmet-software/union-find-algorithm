"""
Demo / yedek çağrı verisi.
Canlı scraping başarısız olursa (ağ engeli, site değişikliği) bu veriler kullanılır;
böylece uygulama her koşulda çalışır.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import List

from models import FundingCall


def _now() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def cascade_demo_calls() -> List[FundingCall]:
    return [
        FundingCall(
            source_name="Cascade Funding (Demo)",
            institution="EU Cascade Funding / FSTP",
            call_title="AI4EU Cascade Open Call for SMEs and Startups",
            summary=("AI tabanlı çözüm geliştiren KOBİ ve startup'lara yönelik "
                     "Financial Support to Third Parties (FSTP) açık çağrısı."),
            deadline=date(2026, 10, 31),
            funding_amount="EUR 60.000",
            funding_rate="%100",
            project_duration="9 ay",
            eligible_applicants=["company", "entrepreneur"],
            eligible_countries=["EU", "Associated Countries", "Türkiye"],
            technology_areas=["artificial intelligence", "machine learning", "data analytics"],
            sectors=["software", "ICT", "health"],
            trl_min=4, trl_max=7,
            consortium_required=False,
            application_url="https://cascadefunding.eu/open-calls/",
            guide_url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/competitive-calls",
            source_url="https://cascadefunding.eu/open-calls/",
            raw_text="AI cascade funding open call FSTP SME startup TRL 4-7 deadline 30.09.2025",
            extracted_at=_now(),
            verification_status="doğrulandı",
        ),
        FundingCall(
            source_name="Cascade Funding (Demo)",
            institution="EU Green Deal Cascade",
            call_title="GreenTech Cascade Call — Climate & Energy Startups",
            summary=("İklim ve enerji alanında çalışan girişimlere yönelik cascade "
                     "hibe programı. Prototip ve pilot uygulama destekleniyor."),
            deadline=date(2026, 12, 15),
            funding_amount="EUR 100.000",
            funding_rate="%90",
            project_duration="12 ay",
            eligible_applicants=["company", "entrepreneur", "academic"],
            eligible_countries=["EU", "Türkiye"],
            technology_areas=["renewable", "hydrogen", "iot"],
            sectors=["energy", "environment", "climate"],
            trl_min=5, trl_max=8,
            consortium_required=True,
            application_url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/competitive-calls",
            guide_url=None,
            source_url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/competitive-calls",
            raw_text="green deal cascade climate energy hydrogen consortium TRL 5-8 deadline 15.11.2025",
            extracted_at=_now(),
            verification_status="doğrulandı",
        ),
        FundingCall(
            source_name="Cascade Funding (Demo)",
            institution="DIH Cascade / Digital Europe",
            call_title="Digital Health Cascade Open Call",
            summary="Dijital sağlık ve biyomedikal çözümler için açık çağrı.",
            deadline=date(2026, 9, 30),
            funding_amount="EUR 50.000",
            funding_rate="%70",
            project_duration="6 ay",
            eligible_applicants=["company", "academic"],
            eligible_countries=["EU", "Türkiye"],
            technology_areas=["biomedical", "artificial intelligence"],
            sectors=["health"],
            trl_min=6, trl_max=9,
            consortium_required=False,
            application_url="https://cascadefunding.eu/open-calls/",
            guide_url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/competitive-calls",
            source_url="https://cascadefunding.eu/open-calls/",
            raw_text="digital health cascade biomedical AI TRL 6-9 deadline 20.08.2025",
            extracted_at=_now(),
            verification_status="doğrulandı",
        ),
    ]


def bigg_demo_call() -> FundingCall:
    """Girişimci senaryosunu test etmek için BiGG benzeri demo çağrı."""
    return FundingCall(
        source_name="TÜBİTAK (Demo)",
        institution="TÜBİTAK",
        call_title="TÜBİTAK 1812 BiGG Bireysel Genç Girişim",
        summary=("Teknoloji ve yenilik odaklı iş fikirlerini olgunlaştırmak isteyen "
                 "genç girişimcilere sermaye desteği. Şirketleşme öncesi/sonrası."),
        deadline=date(2026, 11, 1),
        funding_amount="₺ 900.000",
        funding_rate="%100",
        project_duration="12 ay",
        eligible_applicants=["entrepreneur"],
        eligible_countries=["Türkiye"],
        technology_areas=["artificial intelligence", "software"],
        sectors=["software", "ICT"],
        trl_min=3, trl_max=6,
        consortium_required=False,
        application_url="https://www.tubitak.gov.tr/tr/destekler/girisimcilik",
        guide_url="https://www.tubitak.gov.tr/tr/destekler/girisimcilik",
        source_url="https://www.tubitak.gov.tr/tr/destekler/girisimcilik",
        raw_text="bigg 1812 girişimcilik startup TRL 3-6 deadline 01.10.2025",
        extracted_at=_now(),
        verification_status="doğrulandı",
    )
