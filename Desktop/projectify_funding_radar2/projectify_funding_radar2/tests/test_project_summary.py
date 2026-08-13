import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import PROJECT_SUMMARY_MAX_LEN
from services.project_service import validate_project_summary


def test_within_limit():
    data = {k: "ok" for k in [
        "project_name", "project_purpose", "project_rationale", "project_method",
        "commercialization_patent_status", "competitors", "competitive_advantage"]}
    ok, errors = validate_project_summary(data)
    assert ok and errors == []


def test_over_limit():
    data = {k: "" for k in [
        "project_name", "project_purpose", "project_rationale", "project_method",
        "commercialization_patent_status", "competitors", "competitive_advantage"]}
    data["project_purpose"] = "x" * (PROJECT_SUMMARY_MAX_LEN + 5)
    ok, errors = validate_project_summary(data)
    assert not ok and len(errors) == 1
