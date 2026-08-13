import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from extractors.guide_analyzer import extract_funding_call_from_text


def test_extract_from_text():
    text = ("KOBİ ve startup başvurabilir. Destek miktarı EUR 60.000. "
            "Destek oranı %100. TRL 4-7. Son başvuru tarihi 30.09.2025. "
            "Yapay zeka ve yazılım alanında.")
    call = extract_funding_call_from_text(text, source_name="Test", source_url="x://y")
    assert call.funding_amount and "60.000" in call.funding_amount
    assert call.funding_rate == "%100"
    assert call.trl_min == 4 and call.trl_max == 7
    assert str(call.deadline) == "2025-09-30"
    assert "company" in call.eligible_applicants
