import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from datetime import date

import database
from config import is_active_call, source_color
from models import FundingCall
from services import store_calls, count_calls, clear_scan_results


def test_is_active_call():
    assert is_active_call(None) is True
    assert is_active_call(date(2000, 1, 1)) is False
    assert is_active_call(date(2099, 1, 1)) is True


def test_store_filters_past():
    database.init_db()
    clear_scan_results()
    calls = [
        FundingCall(source_name="X", call_title="Gelecek", deadline=date(2099, 1, 1),
                    source_url="http://x"),
        FundingCall(source_name="X", call_title="Geçmiş", deadline=date(2000, 1, 1),
                    source_url="http://x"),
        FundingCall(source_name="X", call_title="Belirsiz", deadline=None, source_url="http://x"),
    ]
    added = store_calls(calls)
    assert added == 2  # geçmiş elenir, gelecek + belirsiz kalır
    clear_scan_results()


def test_source_color_turkish():
    assert source_color("TÜBİTAK (Demo)") == "#1565C0"
    assert source_color("TÜSEB") == "#6A1B9A"
    assert source_color("Cascade Funding") == "#00838F"
