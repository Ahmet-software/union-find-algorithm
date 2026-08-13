"""Akademisyen uygunluk skorlama — doküman bölüm 16."""
from __future__ import annotations

from config import ACADEMIC_WEIGHTS
from matcher import rule_based_score as R
from matcher.semantic_matcher import semantic_similarity
from models import AcademicProfile, FundingCall, MatchResult, ProjectSummary


def calculate_academic_match_score(
    academic: AcademicProfile, project: ProjectSummary, call: FundingCall
) -> MatchResult:
    ptext = project.combined_text()
    expertise_text = " ".join(academic.expertise_fields or [])
    country_ok = True

    sub = {}
    sub["applicant_eligibility"] = R.scale(
        R.applicant_eligibility("academic", call), ACADEMIC_WEIGHTS["applicant_eligibility"]
    )
    # Akademik alan uyumu: uzmanlık ↔ proje/çağrı
    field_ratio = max(
        semantic_similarity(expertise_text, ptext),
        R.keyword_overlap_ratio(expertise_text, call.technology_areas + call.sectors),
    )
    sub["academic_field_match"] = R.scale(min(1.0, 0.4 + field_ratio), ACADEMIC_WEIGHTS["academic_field_match"])
    sub["topic_match"] = R.scale(R.rationale_match(project, call), ACADEMIC_WEIGHTS["topic_match"])
    sub["scientific_method"] = R.scale(
        0.8 if project.project_method.strip() else 0.3, ACADEMIC_WEIGHTS["scientific_method"]
    )
    sub["technology_trl"] = R.scale(R.technology_match(ptext, call), ACADEMIC_WEIGHTS["technology_trl"])

    track = 0.4
    if academic.publications:
        track += 0.2
    if academic.previous_projects:
        track += 0.2
    if academic.patents:
        track += 0.2
    sub["track_record"] = R.scale(min(1.0, track), ACADEMIC_WEIGHTS["track_record"])

    inst = 0.6 + (0.2 if academic.tto_info else 0) + (0.2 if academic.laboratory_infrastructure else 0)
    sub["institution_fit"] = R.scale(min(1.0, inst), ACADEMIC_WEIGHTS["institution_fit"])
    sub["commercialization"] = R.scale(R.commercialization_score(project), ACADEMIC_WEIGHTS["commercialization"])
    sub["consortium_country"] = R.scale(
        R.consortium_country_fit(country_ok, call), ACADEMIC_WEIGHTS["consortium_country"]
    )

    total = max(0, min(100, int(round(sum(sub.values())))))
    status = R.classify_score(total)

    strengths, weaknesses, risks, missing, checks, revisions = [], [], [], [], [], []

    if academic.publications:
        strengths.append("Yayın geçmişi başvuruyu güçlendiriyor.")
    if academic.laboratory_infrastructure:
        strengths.append("Laboratuvar / araştırma altyapısı mevcut.")
    if not academic.industry_collaboration_history:
        weaknesses.append("Sanayi iş birliği geçmişi belirtilmemiş.")

    # Risk örnekleri (doküman 16)
    if call.eligible_applicants and "academic" not in call.eligible_applicants and "company" in call.eligible_applicants:
        risks.append("Program yalnızca şirketlere açık olabilir; akademisyen doğrudan başvuramayabilir.")
        checks.append("Akademisyenin doğrudan başvuru hakkı doğrulanmalı")
    if call.consortium_required:
        risks.append("Sanayi/ortak gerektiriyor olabilir; uygun ortak bulunmalı.")
    if "klinik" in (ptext.lower()) and not academic.ethics_committee_access:
        risks.append("Klinik çalışma için etik kurul ihtiyacı doğabilir.")
        missing.append("Etik kurul / klinik araştırma onayı")
    if not academic.laboratory_infrastructure:
        weaknesses.append("Laboratuvar altyapısı yetersizse uygulama riski oluşabilir.")

    if sub["commercialization"] < ACADEMIC_WEIGHTS["commercialization"] * 0.6:
        revisions.append("Ticarileşme / patent potansiyeli bölümü detaylandırılmalı.")

    action = (
        "Başvuru için TTO ile iletişime geçilmeli ve gerekli ortaklıklar planlanmalı."
        if status in ("Çok Uygun", "Uygun")
        else "Proje konusu ve ortaklık yapısı çağrıya göre revize edilmeli."
        if status == "Revizyonla Uygun"
        else "Uygunluk düşük; farklı bir akademik destek programı değerlendirilmeli."
    )

    return MatchResult(
        call_title=call.call_title, source_name=call.source_name, institution=call.institution,
        matched_user_type="academic", total_score=total, status=status,
        strengths=strengths, weaknesses=weaknesses, risks=risks,
        missing_documents=missing, required_checks=checks,
        recommended_action=action, project_revision_suggestions=revisions,
        deadline=str(call.deadline) if call.deadline else None, source_url=call.source_url,
        funding_amount=call.funding_amount, funding_rate=call.funding_rate,
        application_url=call.application_url, guide_url=call.guide_url, subscores=sub,
    )
