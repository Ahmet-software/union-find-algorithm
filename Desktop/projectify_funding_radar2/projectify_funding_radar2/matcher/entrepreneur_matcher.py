"""Girişimci uygunluk skorlama — doküman bölüm 17."""
from __future__ import annotations

from config import ENTREPRENEUR_FRIENDLY_KEYWORDS, ENTREPRENEUR_WEIGHTS
from matcher import rule_based_score as R
from models import EntrepreneurProfile, FundingCall, MatchResult, ProjectSummary

_STAGE_TRL = {
    "fikir": 2, "fikir aşaması": 2, "ön doğrulama": 4, "on dogrulama": 4,
    "prototip": 5, "mvp": 6, "pilot": 7, "pilot uygulama": 7,
}


def _stage_trl(profile: EntrepreneurProfile) -> int | None:
    s = (profile.project_stage or "").strip().lower()
    for k, v in _STAGE_TRL.items():
        if k in s:
            return v
    return None


def calculate_entrepreneur_match_score(
    ent: EntrepreneurProfile, project: ProjectSummary, call: FundingCall
) -> MatchResult:
    ptext = project.combined_text()
    country_ok = True
    sub = {}

    sub["applicant_eligibility"] = R.scale(
        R.applicant_eligibility("entrepreneur", call), ENTREPRENEUR_WEIGHTS["applicant_eligibility"]
    )

    # Program tipi uyumu: girişimci-dostu program anahtar kelimeleri
    prog_text = f"{call.call_title} {call.summary or ''} {call.source_name}"
    prog_match = 1.0 if R.any_keyword_in(prog_text, ENTREPRENEUR_FRIENDLY_KEYWORDS) else 0.4
    sub["program_type_match"] = R.scale(prog_match, ENTREPRENEUR_WEIGHTS["program_type_match"])

    sub["sector_match"] = R.scale(R.sector_match(ptext, "", call), ENTREPRENEUR_WEIGHTS["sector_match"])
    sub["technology_match"] = R.scale(R.technology_match(ptext, call), ENTREPRENEUR_WEIGHTS["technology_match"])

    stage_trl = _stage_trl(ent)
    sub["stage_match"] = R.scale(R.trl_match(ptext, stage_trl, call), ENTREPRENEUR_WEIGHTS["stage_match"])

    proto = 0.3
    pstat = (ent.prototype_status or "").lower()
    if any(k in pstat for k in ("var", "evet", "yes", "tamam", "mvp", "prototip")):
        proto = 0.9
    sub["prototype_mvp"] = R.scale(proto, ENTREPRENEUR_WEIGHTS["prototype_mvp"])

    comm = R.commercialization_score(project)
    if (ent.customer_validation_status or "").lower() in ("var", "evet", "yes", "yapildi", "yapıldı"):
        comm = min(1.0, comm + 0.2)
    sub["commercialization_validation"] = R.scale(comm, ENTREPRENEUR_WEIGHTS["commercialization_validation"])

    patent = 0.3
    if (ent.patent_or_brand_status or "").lower() not in ("", "yok", "hayir", "hayır", "no"):
        patent = 0.8
    sub["patent_brand"] = R.scale(patent, ENTREPRENEUR_WEIGHTS["patent_brand"])

    team = 0.4 + (0.3 if ent.has_technical_team else 0) + (0.3 if ent.has_business_team else 0)
    sub["team_fit"] = R.scale(min(1.0, team), ENTREPRENEUR_WEIGHTS["team_fit"])

    total = max(0, min(100, int(round(sum(sub.values())))))
    status = R.classify_score(total)

    strengths, weaknesses, risks, missing, checks, revisions = [], [], [], [], [], []

    if prog_match >= 1.0:
        strengths.append("Çağrı, girişimci-dostu (BiGG/girişimcilik/startup) bir program.")
    if ent.has_technical_team:
        strengths.append("Teknik ekip mevcut.")
    if proto >= 0.9:
        strengths.append("Prototip/MVP mevcut — teknoloji olgunluğu olumlu.")

    # Risk örnekleri (doküman 17)
    if call.eligible_applicants and "entrepreneur" not in call.eligible_applicants and "company" in call.eligible_applicants:
        risks.append("Şirket kuruluşu gerekebilir; başvuru öncesi şirketleşme planlanmalı.")
        checks.append("Şirketleşme gerekliliği doğrulanmalı")
    if not (ent.has_technical_team or ent.has_business_team):
        risks.append("Takım eksikliği değerlendirme puanını düşürebilir.")
        weaknesses.append("Takım yapısı güçlendirilmeli.")
    if proto < 0.5:
        risks.append("Prototip yoksa teknoloji olgunluğu düşük görünebilir.")
    if (ent.customer_validation_status or "").lower() in ("", "yok", "hayir", "hayır", "no"):
        risks.append("Müşteri doğrulaması yapılmamışsa pazar riski oluşur.")
        revisions.append("Müşteri/pazar doğrulaması ekleyip pazar bölümü güçlendirilmeli.")

    if sub["patent_brand"] < ENTREPRENEUR_WEIGHTS["patent_brand"] * 0.6:
        revisions.append("Patentlenebilirlik açıklaması netleştirilmeli.")

    action = (
        "Proje özeti BiGG/iş planı formatına dönüştürülmeli; teknik yenilik ve pazar doğrulama detaylandırılmalı."
        if status in ("Çok Uygun", "Uygun")
        else "Takım, prototip ve müşteri doğrulama eksikleri giderilip yeniden değerlendirilmeli."
        if status == "Revizyonla Uygun"
        else "Bu çağrı için uygunluk düşük; ön kuluçka/hızlandırıcı programları daha uygun olabilir."
    )

    return MatchResult(
        call_title=call.call_title, source_name=call.source_name, institution=call.institution,
        matched_user_type="entrepreneur", total_score=total, status=status,
        strengths=strengths, weaknesses=weaknesses, risks=risks,
        missing_documents=missing, required_checks=checks,
        recommended_action=action, project_revision_suggestions=revisions,
        deadline=str(call.deadline) if call.deadline else None, source_url=call.source_url,
        funding_amount=call.funding_amount, funding_rate=call.funding_rate,
        application_url=call.application_url, guide_url=call.guide_url, subscores=sub,
    )
