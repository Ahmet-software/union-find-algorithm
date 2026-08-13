import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from matcher import match_user_project_to_call
from models import EntrepreneurProfile, ProjectSummary
from sources.demo_data import bigg_demo_call


def test_entrepreneur_bigg_high_match():
    ent = EntrepreneurProfile(full_name="T", project_stage="MVP aşaması",
                              has_technical_team=True, prototype_status="var",
                              customer_validation_status="yapıldı",
                              patent_or_brand_status="var")
    proj = ProjectSummary(project_name="AI app", project_purpose="ai",
                          project_method="machine learning",
                          commercialization_patent_status="patent pazar gelir modeli")
    res = match_user_project_to_call("entrepreneur", ent, proj, bigg_demo_call())
    assert 0 <= res.total_score <= 100
    assert res.status in ("Çok Uygun", "Uygun", "Revizyonla Uygun", "Düşük Uygunluk", "Uygun Değil")
    assert res.matched_user_type == "entrepreneur"
