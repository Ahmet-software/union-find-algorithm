import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import database
from services import (clear_scan_results, count_calls, count_results,
                      load_profile, save_profile, store_calls)
from models import EntrepreneurProfile
from sources.demo_data import cascade_demo_calls


def test_clear_preserves_profile():
    database.init_db()
    save_profile("entrepreneur", EntrepreneurProfile(full_name="X"))
    store_calls(cascade_demo_calls())
    assert count_calls() > 0
    clear_scan_results()
    assert count_calls() == 0 and count_results() == 0
    ut, profile = load_profile()
    assert ut == "entrepreneur" and profile is not None
