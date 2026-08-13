"""Şirket uygunluk skorlama — doküman bölüm 15."""
from __future__ import annotations

from config import COMPANY_WEIGHTS
from matcher import rule_based_score as R
from models import CompanyProfile, FundingCall, MatchResult, ProjectSummary


def calculate_company_match_score(
    company: CompanyProfile, project: ProjectSummary, call: FundingCall
) -> MatchResult:
    ptext = project.combined_text()
    sector_ctx = " ".join(filter(None, [company.activity_area, company.nace_code]))
    country_ok = True  # Türkiye varsayımı; çağrı ülke kısıtı consortium_country_fit'te

    sub = {}
    sub["applicant_eligibility"] = R.scale(
        R.applicant_eligibility("company", call), COMPANY_WEIGHTS["applicant_eligibility"]
    )
    sub["sector_match"] = R.scale(
        R.sector_match(ptext, sector_ctx, call), COMPANY_WEIGHTS["sector_match"]
    )
    sub["technology_match"] = R.scale(
        R.technology_match(ptext, call), COMPANY_WEIGHTS["technology_match"]
    )
    sub["trl_match"] = R.scale(R.trl_match(ptext, None, call), COMPANY_WEIGHTS["trl_match"])

    # Finansal uygunluk: bilanço/satış bilgisi varsa daha güçlü
    fin_ratio = 0.5
    if company.net_sales or company.total_assets or company.balance_sheet_summary:
        fin_ratio = 0.85
    sub["financial_fit"] = R.scale(fin_ratio, COMPANY_WEIGHTS["financial_fit"])

    # Vergi / SGK risk kontrolü
    risk_ratio = 1.0
    risks, missing, checks = [], [], []
    if (company.tax_debt_status or "").strip().lower() in ("var", "evet", "yes", "true"):
        risk_ratio -= 0.5
        risks.append("Vergi borcu beyan edildi — bazı programlarda başvuru riski oluşturur.")
    if (company.sgk_debt_status or "").strip().lower() in ("var", "evet", "yes", "true"):
        risk_ratio -= 0.5
        risks.append("SGK borcu beyan edildi — sözleşme/ödeme aşamasında sorun çıkabilir.")
    sub["tax_sgk_risk"] = R.scale(max(0.0, risk_ratio), COMPANY_WEIGHTS["tax_sgk_risk"])

    sub["rationale_match"] = R.scale(R.rationale_match(project, call), COMPANY_WEIGHTS["rationale_match"])
    sub["commercialization"] = R.scale(R.commercialization_score(project), COMPANY_WEIGHTS["commercialization"])
    sub["consortium_country"] = R.scale(
        R.consortium_country_fit(country_ok, call), COMPANY_WEIGHTS["consortium_country"]
    )

    total = int(round(sum(sub.values())))
    total = max(0, min(100, total))
    status = R.classify_score(total)

    # Güçlü / zayıf yönler
    strengths, weaknesses = [], []
    if R.applicant_eligibility("company", call) >= 1.0:
        strengths.append("Şirket, çağrının uygun başvuru sahibi tanımına giriyor.")
    if sub["technology_match"] >= COMPANY_WEIGHTS["technology_match"] * 0.7:
        strengths.append("Proje teknolojisi çağrı teknoloji alanlarıyla örtüşüyor.")
    if sub["sector_match"] < COMPANY_WEIGHTS["sector_match"] * 0.5:
        weaknesses.append("Sektör uyumu zayıf görünüyor; faaliyet alanı/NACE netleştirilmeli.")
    if not company.r_and_d_history:
        weaknesses.append("Ar-Ge proje geçmişi belirtilmemiş.")

    # Eksik belgeler
    if not company.balance_sheet_summary:
        missing.append("Bilanço / finansal tablo özeti")
    if not company.patent_brand_info:
        checks.append("Patent / marka / faydalı model bilgisi doğrulanmalı")
    if call.consortium_required:
        checks.append("Konsorsiyum ortağı gerekli — uygun ortak teyit edilmeli")

    revisions = []
    if sub["commercialization"] < COMPANY_WEIGHTS["commercialization"] * 0.6:
        revisions.append("Ticarileşme ve patentlenebilirlik bölümü güçlendirilmeli.")
    if sub["rationale_match"] < COMPANY_WEIGHTS["rationale_match"] * 0.6:
        revisions.append("Proje gerekçesi, çağrının öncelikleriyle daha açık ilişkilendirilmeli.")

    action = _recommend_action(status, call)

    return MatchResult(
        call_title=call.call_title,
        source_name=call.source_name,
        institution=call.institution,
        matched_user_type="company",
        total_score=total,
        status=status,
        strengths=strengths,
        weaknesses=weaknesses,
        risks=risks,
        missing_documents=missing,
        required_checks=checks,
        recommended_action=action,
        project_revision_suggestions=revisions,
        deadline=str(call.deadline) if call.deadline else None,
        source_url=call.source_url,
        funding_amount=call.funding_amount,
        funding_rate=call.funding_rate,
        application_url=call.application_url,
        guide_url=call.guide_url,
        subscores=sub,
    )


def _recommend_action(status: str, call: FundingCall) -> str:
    if status in ("Çok Uygun", "Uygun"):
        return "Başvuru dosyası hazırlanmalı; eksik belgeler tamamlanıp son tarihe göre planlanmalı."
    if status == "Revizyonla Uygun":
        return "Proje özeti revize edilip eksik/riskli alanlar giderildikten sonra başvuru düşünülebilir."
    return "Bu çağrı için uygunluk düşük; profil veya proje farklı bir programa yönlendirilmeli."
