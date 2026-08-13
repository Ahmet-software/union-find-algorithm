"""Proje Özeti veri modeli — doküman bölüm 9. Her alan en fazla 500 karakter."""
from __future__ import annotations

from pydantic import BaseModel, Field

from config import PROJECT_SUMMARY_MAX_LEN


class ProjectSummary(BaseModel):
    project_name: str = Field("", max_length=PROJECT_SUMMARY_MAX_LEN)
    project_purpose: str = Field("", max_length=PROJECT_SUMMARY_MAX_LEN)
    project_rationale: str = Field("", max_length=PROJECT_SUMMARY_MAX_LEN)
    project_method: str = Field("", max_length=PROJECT_SUMMARY_MAX_LEN)
    commercialization_patent_status: str = Field("", max_length=PROJECT_SUMMARY_MAX_LEN)
    competitors: str = Field("", max_length=PROJECT_SUMMARY_MAX_LEN)
    competitive_advantage: str = Field("", max_length=PROJECT_SUMMARY_MAX_LEN)

    def combined_text(self) -> str:
        """Eşleştirme için tüm metni birleştirir."""
        return " ".join(
            [
                self.project_name,
                self.project_purpose,
                self.project_rationale,
                self.project_method,
                self.commercialization_patent_status,
                self.competitors,
                self.competitive_advantage,
            ]
        ).strip()
